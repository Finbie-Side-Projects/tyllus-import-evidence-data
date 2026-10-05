#!/usr/bin/env python3
"""Verify real-data pages, links, data integrity and the publication boundary."""
import csv
import hashlib
import json
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from build_site import ROOT, LOCALES, build_page


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
    payload = json.loads((ROOT / 'data/us-import-evidence-change-radar.json').read_text())
    notices = payload['notices']
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
        require('Human-readable source' not in contents, f'Unwanted heading in {relative}')
        page = Page()
        page.feed(contents)
        require(page.lang == locale, f'Wrong document language: {relative}')
        require(set(page.notice_ids) == expected and len(page.notice_ids) == len(notices), f'Missing readable notices in {relative}')
        require(len(page.ids) == len(set(page.ids)), f'Duplicate HTML IDs in {relative}')
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
    for asset in ('app.js', 'theme.js'):
        subprocess.run(['node', '--check', str(ROOT / 'assets' / asset)], check=True)
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
