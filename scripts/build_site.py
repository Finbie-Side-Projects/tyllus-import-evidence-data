#!/usr/bin/env python3
"""Build complete localized HTML from the committed public snapshot."""
import hashlib
import json
import re
from pathlib import Path
from site_render import date_text, options, render_breakdowns, render_notice, text, time_tag, type_label

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = 'https://finbie-side-projects.github.io/tyllus-import-evidence-data/'
LOCALES = ('en', 'tr', 'it', 'es')


def render_featured(notices, strings):
    by_id = {n['id']: n for n in notices}
    cards = []
    for key, content in strings['featured'].items():
        if key not in by_id:
            continue
        notice = by_id[key]
        date_value = notice.get('effectiveOn') or notice.get('commentsCloseOn') or notice['publicationDate']
        label = strings['effective'] if notice.get('effectiveOn') else strings['comments'] if notice.get('commentsCloseOn') else strings['published']
        cards.append(f'<a class="featured-card" data-notice="{key}" href="#notice-{key}"><span class="featured-type">{text(type_label(notice["sourceType"], strings))}</span><h3>{text(content["title"])} <span aria-hidden="true">↗</span></h3><p>{text(content["summary"])}</p><span class="featured-date">{text(label)}: {time_tag(date_value, strings)}</span></a>')
    return ''.join(cards)


def build_page(locale, dataset, root=False):
    strings = json.loads((ROOT / 'locales' / f'{locale}.json').read_text())
    notices = sorted(dataset['notices'], key=lambda n: (n['publicationDate'], n['id']), reverse=True)
    prefix = './' if root else '../'
    agency_names = {n['agencySlug']: n['agency'] for n in notices}
    agency_rows, topic_rows = render_breakdowns(notices, strings)
    snapshot = date_text(dataset['generatedAt'], strings)
    earliest = min(n['publicationDate'] for n in notices)
    latest = max(n['publicationDate'] for n in notices)
    context = {key: text(value) for key, value in strings.items() if isinstance(value, str)}
    context.update({
        'locale': locale, 'prefix': prefix, 'canonical': BASE_URL + locale + '/',
        'rootRedirect': f'<meta http-equiv="refresh" content="0;url={BASE_URL}en/" />' if root else '',
        'snapshotDate': snapshot, 'snapshotIso': dataset['generatedAt'][:10],
        'coverageDates': date_text(earliest, strings) + ' – ' + date_text(latest, strings),
        'noticeCount': len(notices), 'agencyCount': len(agency_names),
        'topicCount': len({d['id'] for n in notices for d in n['evidenceDomains']}),
        'featuredCards': render_featured(notices, strings),
        'quickButtons': ''.join(f'<button class="quick-search" type="button" data-query="{query}">{text(label)}</button>' for query, label in zip(('steel', 'aluminum', 'photovoltaic', 'China', 'India', 'Türkiye', 'Vietnam'), strings['quickLabels'])),
        'noticeCards': '\n'.join(render_notice(n, strings) for n in notices),
        'agencyRows': agency_rows, 'topicRows': topic_rows,
        'agencyOptions': options(sorted(agency_names.items(), key=lambda pair: pair[1])),
        'topicOptions': options(strings['topicLabels'].items()),
        'typeOptions': options((kind, type_label(kind, strings)) for kind in sorted({n['sourceType'] for n in notices})),
        'localeOptions': options(strings['languageLabels'].items()),
        'initialResults': text(strings['results'].replace('{start}', '1').replace('{end}', str(len(notices))).replace('{count}', str(len(notices)))),
        'interfaceJson': json.dumps(strings, ensure_ascii=False).replace('<', '\\u003c'),
        'alternateLinks': '\n'.join(f'<link rel="alternate" hreflang="{code}" href="{BASE_URL}{code}/" />' for code in LOCALES),
    })
    for asset in ('styles.css', 'app.js', 'theme.js'):
        context[asset.replace('.', '_') + 'Version'] = hashlib.sha256((ROOT / 'assets' / asset).read_bytes()).hexdigest()[:12]
    schema = {
        '@context': 'https://schema.org', '@type': 'Dataset',
        'name': 'Tyllus U.S. Import Evidence Change Radar', 'description': strings['description'],
        'url': context['canonical'], 'inLanguage': 'en', 'dateModified': dataset['generatedAt'][:10],
        'temporalCoverage': f'{earliest}/{latest}',
        'isBasedOn': 'https://www.tyllus.com/en/resources/us-import-evidence-change-radar',
        'creator': {'@type': 'Organization', 'name': 'Tyllus', 'url': 'https://www.tyllus.com/'},
        'license': 'https://www.tyllus.com/en/terms-of-use',
        'distribution': [{'@type': 'DataDownload', 'encodingFormat': mime, 'contentUrl': BASE_URL + 'data/' + name} for name, mime in [('us-import-evidence-change-radar.json', 'application/json'), ('us-import-evidence-change-radar.csv', 'text/csv'), ('us-import-evidence-change-radar.dcat.json', 'application/ld+json')]],
    }
    context['schemaJson'] = json.dumps(schema, ensure_ascii=False).replace('<', '\\u003c')
    template = (ROOT / 'site' / 'page.html').read_text()
    return re.sub(r'\{\{(\w+)\}\}', lambda m: str(context[m[1]]), template)


def main():
    dataset = json.loads((ROOT / 'data' / 'us-import-evidence-change-radar.json').read_text())
    for locale in LOCALES:
        directory = ROOT / locale
        directory.mkdir(exist_ok=True)
        (directory / 'index.html').write_text(build_page(locale, dataset))
    (ROOT / 'index.html').write_text(build_page('en', dataset, root=True))
    urls = ''.join(f'<url><loc>{BASE_URL}{locale}/</loc></url>' for locale in LOCALES)
    (ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    print(f'Built {len(dataset["notices"])} readable notices in {len(LOCALES)} locales.')


if __name__ == '__main__':
    main()
