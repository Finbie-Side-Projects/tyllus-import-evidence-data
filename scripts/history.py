"""Preserve references from earlier committed public source selections."""
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from site_render import text, time_tag

RELATIVE = Path('data/previously-included-notices.json')


def record_hash(notice):
    raw = json.dumps(notice, ensure_ascii=False, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(raw.encode()).hexdigest()


def load_history(root):
    path = root / RELATIVE
    if not path.exists():
        return {'schemaVersion': 1, 'entries': []}
    history = json.loads(path.read_text())
    seen = set()
    for entry in history['entries']:
        notice = entry['notice']
        key = notice['id']
        if not re.fullmatch(r'\d{4}-\d{4,6}', key) or key in seen:
            raise ValueError('Invalid or duplicate historical notice ID')
        seen.add(key)
        if entry['noticeSha256'] != record_hash(notice):
            raise ValueError('Historical record checksum differs')
        if not re.fullmatch(r'[a-f0-9]{40}', entry['sourceCommit']):
            raise ValueError('Historical record needs a source commit')
        if not re.fullmatch(r'[a-f0-9]{64}', entry['sourceSnapshotSha256']):
            raise ValueError('Historical record needs a snapshot checksum')
        if notice['radarUrl'] != f'https://www.tyllus.com/en/resources/us-import-evidence-change-radar/{key}':
            raise ValueError('Unexpected historical reader URL')
        official = urlparse(notice['officialUrl'])
        if official.scheme != 'https' or official.hostname != 'www.federalregister.gov':
            raise ValueError('Unexpected historical official URL')
    return history


def retain_previous(root, previous_bytes, current):
    if not previous_bytes:
        return
    previous = json.loads(previous_bytes)
    current_ids = {notice['id'] for notice in current['notices']}
    removed = [notice for notice in previous['notices'] if notice['id'] not in current_ids]
    if not removed:
        return
    committed = subprocess.check_output(['git', 'show', 'HEAD:data/us-import-evidence-change-radar.json'], cwd=root)
    if committed != previous_bytes:
        raise ValueError('Historical references must come from the committed public snapshot')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root).decode().strip()
    history = load_history(root)
    entries = {entry['notice']['id']: entry for entry in history['entries']}
    for notice in removed:
        entries[notice['id']] = {
            'lastIncludedSnapshot': previous['generatedAt'],
            'sourceCommit': commit,
            'sourceSnapshotSha256': hashlib.sha256(previous_bytes).hexdigest(),
            'noticeSha256': record_hash(notice),
            'notice': notice,
        }
    history['entries'] = [entries[key] for key in sorted(entries, reverse=True)]
    (root / RELATIVE).write_text(json.dumps(history, ensure_ascii=False, indent=2) + '\n')


def render_history(root, strings):
    entries = load_history(root)['entries']
    if not entries:
        return ''
    rows = []
    for entry in entries:
        notice = entry['notice']
        source = f'https://github.com/Finbie-Side-Projects/tyllus-import-evidence-data/blob/{entry["sourceCommit"]}/data/us-import-evidence-change-radar.json'
        rows.append(f'''<div class="previous-record" data-previous-id="{text(notice['id'])}">
<h4>{text(notice['id'])} · <span lang="en">{text(notice['title'])}</span></h4>
<p>{text(strings['previousSnapshot'])}: {time_tag(entry['lastIncludedSnapshot'], strings)}</p>
<div class="notice-links"><a data-previous-reader href="{text(notice['radarUrl'])}">{text(strings['readerRecord'])}<span aria-hidden="true"> ↗</span></a><a data-previous-official href="{text(notice['officialUrl'])}">{text(strings['officialNotice'])}<span aria-hidden="true"> ↗</span></a><a href="{source}">{text(strings['previousSource'])}<span aria-hidden="true"> ↗</span></a></div></div>''')
    return f'''<details id="earlier-selections" class="earlier-selections"><summary>{text(strings['previousTitle'])} · {len(entries)}</summary><p>{text(strings['previousScope'])}</p>{''.join(rows)}</details>'''
