"""Escape and render public notice records for the static explorer."""
from collections import Counter
from datetime import date
from html import escape, unescape
import re


def text(value):
    return escape(str(value), quote=True)


def date_text(value, strings):
    if not value:
        return text(strings['notSupplied'])
    d = date.fromisoformat(value[:10])
    return f'{d.day} {strings["months"][d.month - 1]} {d.year}'


def time_tag(value, strings):
    if not value:
        return text(strings['notSupplied'])
    return f'<time datetime="{text(value[:10])}">{date_text(value, strings)}</time>'


def type_label(value, strings):
    return strings[{'Notice': 'notice', 'Rule': 'rule', 'Proposed Rule': 'proposedRule'}.get(value, 'notice')]


def options(items):
    return ''.join(f'<option value="{text(value)}">{text(label)}</option>' for value, label in items)


def readable_title(title):
    """Shorten country names without changing the notice's actual subject."""
    parts = re.split(r': |; ', title, maxsplit=1)
    subject = re.sub(r'^Certain ', '', parts[0])
    for formal, short in [("the People's Republic of China", "China"), ("the Republic of Türkiye", "Türkiye"), ("the Republic of Korea", "South Korea"), ("the Socialist Republic of Vietnam", "Vietnam"), ("the Sultanate of Oman", "Oman"), ("the Lao People's Democratic Republic", "Laos"), ("the Republic of Kazakhstan", "Kazakhstan"), ("the Czech Republic", "Czech Republic")]:
        subject = subject.replace(formal, short)
    return subject, parts[1] if len(parts) > 1 else ''


def render_notice(notice, strings):
    s = {key: text(value) for key, value in strings.items() if isinstance(value, str)}
    abstract = notice.get('abstract') or ''
    for entity, letter in {'uuml': 'ü', 'uacute': 'ú', 'scedil': 'ş', 'Scedil': 'Ş', 'ntilde': 'ñ'}.items():
        abstract = abstract.replace(f'[{entity}]', letter)
    heading, change = readable_title(notice['title'])
    change_html = f'<p class="notice-change" lang="en">{text(change)}</p>' if change else ''
    preview = abstract[:280].rsplit(' ', 1)[0] + '…' if len(abstract) > 280 else abstract
    domains = notice['evidenceDomains']
    badges = ''.join(f'<span class="tag">{text(strings["topicLabels"][d["id"]])}</span>' for d in domains)
    matches = ''.join(f'<li><strong>{text(strings["topicLabels"][d["id"]])}</strong><span lang="en">{text(", ".join(d["matchedTerms"]))}</span></li>' for d in domains)
    docket = ', '.join(notice.get('docketIds', [])) or strings['notSupplied']
    action = f'<div><dt>{s["action"]}</dt><dd lang="en">{text(notice["action"])}</dd></div>' if notice.get('action') else ''
    pdf = f'<a href="{text(notice["pdfUrl"])}" target="_blank" rel="noopener noreferrer">{s["officialPdf"]}<span aria-hidden="true"> ↗</span></a>' if notice.get('pdfUrl') else ''
    search = ' '.join([notice['title'], abstract, notice['id'], notice['agency'], docket] + [term for d in domains for term in d['matchedTerms']])
    return f'''<article class="notice" id="notice-{text(notice['id'])}" data-agency="{text(notice['agencySlug'])}" data-topics="{text(' '.join(d['id'] for d in domains))}" data-type="{text(notice['sourceType'])}" data-date="{text(notice['publicationDate'])}" data-search="{text(search)}">
<div class="notice-meta">{time_tag(notice['publicationDate'], strings)}<span class="type">{text(type_label(notice['sourceType'], strings))}</span><span class="document-id">{text(notice['id'])}</span></div>
<p class="notice-agency" lang="en">{text(notice['agency'])}</p>
<h3 lang="en"><a href="{text(notice['officialUrl'])}" target="_blank" rel="noopener noreferrer">{text(heading)}<span aria-hidden="true"> ↗</span></a></h3>{change_html}
<p class="abstract"{(' lang="en"' if abstract else '')}>{text(preview) if abstract else s['noAbstract']}</p>
<div class="tags">{badges}</div>
<details><summary>{s['details']}<span class="sr-only" lang="en">: {text(notice['id'])}</span></summary>
<div class="notice-details"><h4>{s['originalTitle']}</h4><p lang="en">{text(notice['title'])}</p><h4>{s['fullAbstract']}</h4><p{(' lang="en"' if abstract else '')}>{text(abstract) if abstract else s['noAbstract']}</p>
<dl class="dates"><div><dt>{s['published']}</dt><dd>{time_tag(notice['publicationDate'], strings)}</dd></div><div><dt>{s['effective']}</dt><dd>{time_tag(notice.get('effectiveOn'), strings)}</dd></div><div><dt>{s['comments']}</dt><dd>{time_tag(notice.get('commentsCloseOn'), strings)}</dd></div><div><dt>{s['dockets']}</dt><dd lang="en">{text(docket)}</dd></div>{action}</dl>
<h4>{s['matchedTerms']}</h4><ul class="matches">{matches}</ul></div></details>
<div class="notice-links"><a href="{text(notice['officialUrl'])}" target="_blank" rel="noopener noreferrer">{s['officialNotice']}<span aria-hidden="true"> ↗</span></a>{pdf}</div>
</article>'''


def render_breakdowns(notices, strings):
    agency_counts = Counter(n['agencySlug'] for n in notices)
    agency_names = {n['agencySlug']: n['agency'] for n in notices}
    topic_counts = Counter(d['id'] for n in notices for d in n['evidenceDomains'])
    agencies = ''.join(f'<button type="button" class="breakdown" data-filter="agency" data-value="{text(key)}" aria-pressed="false"><span lang="en">{text(agency_names[key])}</span><strong>{count}</strong><meter min="0" max="{len(notices)}" value="{count}" aria-label="{text(agency_names[key])}"></meter></button>' for key, count in agency_counts.most_common())
    topics = ''.join(f'<button type="button" class="topic-row" data-filter="topic" data-value="{text(key)}" aria-pressed="false"><span>{text(strings["topicLabels"][key])}</span><strong>{count}</strong></button>' for key, count in topic_counts.most_common())
    return agencies, topics
