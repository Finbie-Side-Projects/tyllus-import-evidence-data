"""Recognize the official source URL for the same notice and publication date."""
import re
from urllib.parse import urlparse


def valid_official_source(notice):
    url = urlparse(notice['officialUrl'])
    if url.scheme != 'https' or url.netloc not in ('www.federalregister.gov', 'www.govinfo.gov'):
        return False
    if url.params or url.query or url.fragment:
        return False
    key, date = notice['id'], notice['publicationDate']
    if not re.fullmatch(r'\d{4}-\d{4,6}', key) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', date):
        return False
    if url.netloc == 'www.govinfo.gov':
        return url.path == f'/content/pkg/FR-{date}/html/{key}.htm'
    prefix = f'/documents/{date.replace("-", "/")}/{key}/'
    return url.path.startswith(prefix) and bool(re.fullmatch(r'[a-z0-9-]+', url.path[len(prefix):]))
