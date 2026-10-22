#!/usr/bin/env python3
"""Verify real-data pages, links, data integrity and the publication boundary."""
import csv
import hashlib
import html
import io
import json
import re
import subprocess
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET
from feeds import FEEDS, render_feed, selected_notices
from build_site import ROOT, LOCALES, build_page
from consultation import load_questions, csv_text, RELATIVE, FIELDS


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.notice_ids = []
        self.sources = []
        self.article_depth = False
        self.title = False
        self.headings = []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'article' and 'notice' in attrs.get('class', '').split():
            self.notice_ids.append(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])


def require(condition, message):
    if not condition:
        raise SystemExit(message)


def main():
    questions = load_questions(ROOT)
    workbook = (ROOT / RELATIVE / 'response-worksheet.csv').read_bytes()
    require(workbook == csv_text(questions).encode('utf-8'), 'Response worksheet differs from official questions')
    worksheet_rows = list(csv.DictReader(io.StringIO(workbook.decode('utf-8-sig'))))
    require(len(worksheet_rows) == 64, 'Response worksheet needs all64 questions')
    require(all(not row[field] for row in worksheet_rows for field in FIELDS[5:]), 'Invented answers or company facts in blank worksheet')
    # Verify the native workbook artifact without changing its source or inputs.
    ns = {'m': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
    with zipfile.ZipFile(ROOT / RELATIVE / 'response-workbook.xlsx') as archive:
        names = archive.namelist()
        require(not any('vbaProject' in n or n.startswith('xl/externalLinks/') for n in names), 'Unexpected workbook macro or external connection')
        strings = ET.fromstring(archive.read('xl/sharedStrings.xml'))
        shared = [''.join(node.itertext()) for node in strings]
        def sheet_values(filename):
            tree = ET.fromstring(archive.read(filename))
            values = {}
            for cell in tree.findall('.//m:sheetData/m:row/m:c', ns):
                value = cell.find('m:v', ns)
                text = value.text if value is not None else ''
                values[cell.attrib['r']] = shared[int(text)] if cell.attrib.get('t') == 's' and text else text
            return tree, values
        response_tree, response_values = sheet_values('xl/worksheets/sheet1.xml')
        _, question_values = sheet_values('xl/worksheets/sheet2.xml')
        for index, question in enumerate(questions['questions']):
            source_row, input_row = index + 6, index + 13
            require(question_values.get(f'A{source_row}') == f'Q{index + 1}', 'Workbook question numbering changed')
            require(question_values.get(f'C{source_row}') == question['question'], 'Workbook source question differs')
            require(question_values.get(f'D{source_row}') == question['sourceUrl'], 'Workbook source URL differs')
            require(response_values.get(f'A{input_row}') == f'Q{index + 1}', 'Workbook response identity differs')
            require(all(response_values.get(f'{col}{input_row}', '') == '' for col in 'CDEFGHIJKLM'), 'Invented workbook input')
        formulas = response_tree.findall('.//m:f', ns)
        require(len(formulas) == 68, 'Missing next-step or summary formulas')
        require(len(response_tree.findall('.//m:dataValidation', ns)) == 2, 'Missing workbook dropdowns')
        require(len([n for n in names if re.fullmatch(r'xl/tables/table\d+\.xml', n)]) == 2, 'Missing workbook filter tables')
    payload = json.loads((ROOT / 'data/us-import-evidence-change-radar.json').read_text())
    notices = payload['notices']
    for filename, (_, agency) in FEEDS.items():
        contents = (ROOT / 'feeds' / filename).read_bytes()
        require(contents == render_feed(payload, filename), f'Stale RSS feed: {filename}')
        channel = ET.fromstring(contents).find('channel')
        require(all(channel.findtext(field) for field in ('title', 'link', 'description')), f'Missing RSS channel metadata: {filename}')
        items = channel.findall('item')
        selected = selected_notices(payload, agency)
        require(len(items) == len(selected), f'RSS record count mismatch: {filename}')
        require(len({item.findtext('guid') for item in items}) == len(items), f'Duplicate RSS GUIDs: {filename}')
        for item, notice in zip(items, selected):
            require(item.findtext('link') == notice['officialUrl'] and item.findtext('title') == notice['title'], f'RSS source mismatch: {filename}')
            require(item.find('pubDate') is None, f'Invented publication time: {filename}')
    require(bool(notices), 'Dataset must contain real notices.')
    expected = {f'notice-{n["id"]}' for n in notices}
    require(len(expected) == len(notices), 'Duplicate notice IDs in dataset.')
    english = json.loads((ROOT / 'locales/en.json').read_text())
    for locale in LOCALES:
        strings = json.loads((ROOT / 'locales' / f'{locale}.json').read_text())
        require(set(strings) == set(english), f'Incomplete interface in {locale}.')
    for locale, relative, root in [(locale, f'{locale}/index.html', False) for locale in LOCALES] + [('en', 'index.html', True)]:
        path = ROOT / relative
        contents = path.read_text()
        require(contents == build_page(locale, payload, root), f'Generated page is stale: {relative}')
        embedded = json.loads(re.search(r'<script id="notice-data" type="application/json">(.*?)</script>', contents, re.S).group(1))
        require(embedded == payload, f'Embedded export dataset differs from source: {relative}')
        require('Human-readable source' not in contents, f'Unwanted heading in {relative}')
        page = Page()
        page.feed(contents)
        require(page.lang == locale, f'Wrong document language: {relative}')
        require(set(page.notice_ids) == expected and len(page.notice_ids) == len(notices), f'Missing readable notices in {relative}')
        require(len(page.ids) == len(set(page.ids)), f'Duplicate HTML IDs in {relative}')
        require(all(f'cbp-q{i}' in page.ids for i in range(1, 65)), f'Missing readable official question in {relative}')
        require(all(html.escape(q['question']) in contents for q in questions['questions']), f'Official question text missing in {relative}')
        for notice in notices:
            require(notice['officialUrl'] in contents, f'Missing official source in {relative}')
            require(urlparse(notice['officialUrl']).hostname == 'www.federalregister.gov', 'Unexpected source host.')
        for link in page.links:
            url = urlparse(link)
            if url.scheme or url.netloc:
                require(url.scheme in ('https',), f'Unsafe link scheme in {relative}')
                continue
            if not url.path:
                require(not url.fragment or url.fragment in page.ids, f'Broken anchor in {relative}: {url.fragment}')
                continue
            target = (path.parent / unquote(url.path)).resolve()
            require(target.is_relative_to(ROOT.resolve()), f'Link outside publication in {relative}')
            require(target.exists(), f'Broken internal link in {relative}: {url.path}')
    manifest = json.loads((ROOT / 'data/manifest.json').read_text())
    require(manifest['record_count'] == len(notices), 'Manifest record count differs from snapshot.')
    require(manifest['dataset_generated_at'] == payload['generatedAt'], 'Snapshot dates disagree.')
    for entry in manifest['files']:
        require(hashlib.sha256((ROOT / entry['file']).read_bytes()).hexdigest() == entry['sha256'], f'Checksum mismatch: {entry["file"]}')
    with (ROOT / 'data/us-import-evidence-change-radar.csv').open(newline='') as f:
        rows = list(csv.DictReader(f))
    require(len(rows) == len(notices), 'CSV/JSON record counts differ.')
    for asset in ('app.js', 'theme.js', 'selection.js'):
        subprocess.run(['node', '--check', str(ROOT / 'assets' / asset)], check=True)
    subprocess.run(['node', '--test', str(ROOT / 'scripts/selection.test.cjs')], check=True)
    files = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0')
    secret_patterns = [r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----', r'gh[pousr]_[A-Za-z0-9]{30,}', r'AIza[0-9A-Za-z_-]{35}', r'sk-(?:proj-)?[A-Za-z0-9_-]{30,}', r'Authorization\s*:\s*[\"\x27]?Bearer\s+[A-Za-z0-9._-]{20,}', r'(?:live|test)_[A-Za-z0-9]{32,}']
    for filename in filter(None, files):
        path = ROOT / filename
        require(not path.name.startswith('.env') and not re.search(r'service[-_]?account|credentials|private[-_]?key', path.name, re.I), f'Sensitive filename: {filename}')
        require(path.suffix.lower() not in ('.docx', '.pem', '.key', '.p12'), f'Private/upload file in publication: {filename}')
        if not path.is_file():
            continue
        contents = path.read_text(errors='ignore')
        require(not any(re.search(pattern, contents) for pattern in secret_patterns), f'Potential secret in {filename}; value redacted.')
    require(not any('process.env' in p.read_text() for p in (ROOT / 'assets').glob('*.js')), 'Unexpected client environment access.')
    print(f'PASS: {len(notices)} notices × 4 locales + root fallback; local links, localized UI, snapshot checksums, CSV count, JavaScript syntax and secret scan.')


if __name__ == '__main__':
    main()
