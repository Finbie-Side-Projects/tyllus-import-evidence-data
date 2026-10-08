"""Render RSS feeds from the committed, non-exhaustive public notice selection."""
from datetime import datetime
from email.utils import format_datetime
from html import escape
from xml.etree import ElementTree as ET

BASE_URL = 'https://finbie-side-projects.github.io/tyllus-import-evidence-data/'
FEEDS = {
    'notices.xml': ('Selected U.S. import notices', None),
    'ustr.xml': ('Selected USTR notices', 'trade-representative-office-of-united-states'),
}
LIMIT = 50
ATOM = 'http://www.w3.org/2005/Atom'
ET.register_namespace('atom', ATOM)


def selected_notices(dataset, agency):
    notices = (n for n in dataset['notices'] if agency is None or n['agencySlug'] == agency)
    return sorted(notices, key=lambda n: (n['publicationDate'], n['id']), reverse=True)[:LIMIT]


def render_feed(dataset, filename):
    title, agency = FEEDS[filename]
    rss = ET.Element('rss', {'version': '2.0'})
    channel = ET.SubElement(rss, 'channel')
    for key, value in {
        'title': 'Tyllus Radar — ' + title,
        'link': BASE_URL + 'en/',
        'description': 'Up to 50 latest notices in the current Tyllus selection, with original Federal Register titles and abstracts. Non-exhaustive discovery aid; verify official sources before acting. Dataset terms: https://www.tyllus.com/en/terms-of-use',
        'language': 'en',
        'lastBuildDate': format_datetime(datetime.fromisoformat(dataset['generatedAt'].replace('Z', '+00:00')), usegmt=True),
    }.items():
        ET.SubElement(channel, key).text = value
    ET.SubElement(channel, '{' + ATOM + '}link', {
        'href': BASE_URL + 'feeds/' + filename, 'rel': 'self', 'type': 'application/rss+xml',
    })
    for notice in selected_notices(dataset, agency):
        item = ET.SubElement(channel, 'item')
        ET.SubElement(item, 'title').text = notice['title']
        ET.SubElement(item, 'link').text = notice['officialUrl']
        ET.SubElement(item, 'guid', {'isPermaLink': 'false'}).text = 'urn:federal-register:' + notice['id']
        ET.SubElement(item, 'category').text = notice['agency']
        ET.SubElement(item, 'category').text = notice['sourceType']
        details = [('Document', notice['id']), ('Published', notice['publicationDate'])]
        details += [(label, notice[key]) for key, label in [('effectiveOn', 'Effective date'), ('commentsCloseOn', 'Comments close')] if notice.get(key)]
        body = '<p>' + '; '.join(escape(label + ': ' + value) for label, value in details) + '</p>'
        if notice.get('abstract'):
            body += '<p>' + escape(notice['abstract']) + '</p>'
        body += '<p><a href="' + escape(notice['pdfUrl'], quote=True) + '">Official PDF</a> · <a href="' + escape(notice['radarUrl'], quote=True) + '">Dates and context in Tyllus Radar</a></p>'
        ET.SubElement(item, 'description').text = body
        # The source provides a publication date, not an exact time. Do not invent pubDate.
    ET.indent(rss, space='  ')
    return ET.tostring(rss, encoding='utf-8', xml_declaration=True) + b'\n'


def build_feeds(root, dataset):
    directory = root / 'feeds'
    directory.mkdir(exist_ok=True)
    for filename in FEEDS:
        (directory / filename).write_bytes(render_feed(dataset, filename))
