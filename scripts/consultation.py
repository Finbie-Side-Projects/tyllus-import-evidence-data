"""Build a blank response worksheet from the retained official CBP questions."""
import csv
import hashlib
import html
import io
import json
import re
from pathlib import Path

RELATIVE = 'worksheets/2026-17926'
FIELDS = ('question_number', 'official_section', 'official_question', 'official_pdf',
          'original_comments_close_on', 'response_draft', 'evidence_reference',
          'answer_owner', 'observed_time_minutes', 'observed_cost_amount', 'currency',
          'measurement_period', 'sample_size', 'measured_or_estimated',
          'assumptions_and_limits', 'review_status')


def load_questions(root):
    folder = root / RELATIVE
    data = json.loads((folder / 'questions.json').read_text())
    source = (folder / 'official-source.html').read_bytes()
    assert hashlib.sha256(source).hexdigest() == data['sourceSha256'], 'Question source changed'
    text = html.unescape(re.sub('<[^>]+>', '', source.decode()))
    matches = list(re.finditer(r'^\s{4}Q(\d+)\. ', text, re.M))
    assert [int(m[1]) for m in matches] == list(range(1, 65)), 'Official question numbering changed'
    assert [q['number'] for q in data['questions']] == list(range(1, 65)), 'Missing or duplicate question'
    for i, (match, question) in enumerate(zip(matches, data['questions'])):
        block = text[match.end():matches[i + 1].start() if i < 63 else len(text)]
        block = re.sub(r'\n\s*\[\[Page \d+\]\]\s*\n', '\n', block)
        block = re.split(r'\n\s*\n|\n(?=[1-9A-ZIVX]+\. )', block, maxsplit=1)[0]
        block = re.sub(r'([a-z])-\s*\n([a-z])', r'\1-\2', block)
        assert question['question'] == ' '.join(block.split()), f'Question Q{i + 1} differs from source'
    return data


def csv_text(data):
    stream = io.StringIO(newline='')
    writer = csv.DictWriter(stream, fieldnames=FIELDS, quoting=csv.QUOTE_ALL, lineterminator='\n')
    writer.writeheader()
    for q in data['questions']:
        writer.writerow({'question_number': f'Q{q["number"]}',
                         'official_section': q['section'], 'official_question': q['question'],
                         'official_pdf': q['sourceUrl'],
                         'original_comments_close_on': data['originalCommentsCloseOn']})
    return '\ufeff' + stream.getvalue()


def build_worksheet(root):
    data = load_questions(root)
    (root / RELATIVE / 'response-worksheet.csv').write_bytes(csv_text(data).encode('utf-8'))


def render_questions(root, strings):
    data = load_questions(root)
    groups = {}
    esc = html.escape
    for q in data['questions']:
        groups.setdefault((q['section'], q['sectionTitle']), []).append(q)
    rendered = []
    for (section, title), questions in groups.items():
        items = ''.join(f'<li id="cbp-q{q["number"]}"><p lang="en"><strong>Q{q["number"]}.</strong> {esc(q["question"])}</p><a href="{esc(q["sourceUrl"], quote=True)}">{esc(strings["worksheetSourcePage"])} {q["sourcePage"]} ↗</a></li>' for q in questions)
        rendered.append(f'<details class="consultation-group"><summary lang="en">{esc(section)} · {esc(title)} <span>(Q{questions[0]["number"]}–Q{questions[-1]["number"]})</span></summary><ol class="consultation-questions">{items}</ol></details>')
    return ''.join(rendered)
