"""Render frozen Chinese annotations and aligned English translations as vectors.

Chinese text, source offsets, and annotations remain unchanged in the input JSON.
Only explicit display_omissions hide original advertisement list markers. English
spans are translation alignments linked to Chinese spans, not evaluation labels.
Archived English explanations remain in the JSON but are not displayed.
ReportLab is required. CNSS_CN_FONT/CNSS_EN_FONT/CNSS_EN_BOLD optionally locate
TrueType fonts. The optional layout report supports clipping and alignment checks.
"""
from pathlib import Path
import argparse
import json
import os
import re
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor, white

ROOT = Path(__file__).resolve().parent
FILL = {'L': '#E3DDF6', 'K': '#B9EEF0', 'S': '#FAED99', 'T': '#C6EBCB'}
EDGE = {'L': '#64439A', 'K': '#167E87', 'S': '#987500', 'T': '#278846'}
W, PAD, LABEL_WIDTH = 510.0, 10.0, 26.0
TEXT_X = PAD + LABEL_WIDTH
TEXT_WIDTH = W - TEXT_X - PAD
CNFS, ENFS = 13.3, 10.8
CNLEAD, ENLEAD = 19.0, 17.0
TYPE_FS, TYPE_GAP = 7.8, 11.0

def width(value, font, size):
    return pdfmetrics.stringWidth(value, font, size)

def validate_example(ex):
    assert ex['full_record_text'][ex['excerpt_start']:ex['excerpt_end']] == ex['text']
    previous = 0
    for span in ex['spans']:
        assert previous <= span['start'] < span['end'] <= len(ex['text'])
        assert ex['text'][span['start']:span['end']] == span['text']
        assert ex['full_record_text'][span['source_start']:span['source_end']] == span['text']
        previous = span['end']
    previous = 0
    for omission in ex['display_omissions']:
        assert previous <= omission['start'] < omission['end'] <= len(ex['text'])
        assert ex['text'][omission['start']:omission['end']] == omission['text']
        assert all(omission['end'] <= s['start'] or omission['start'] >= s['end']
                   for s in ex['spans']), 'A display omission intersects an annotation'
        previous = omission['end']
    links, previous = [], 0
    for span in ex['english_spans']:
        assert previous <= span['start'] < span['end'] <= len(ex['english_translation'])
        assert ex['english_translation'][span['start']:span['end']] == span['text']
        assert span['type'] == ex['spans'][span['cn_span_index']]['type']
        links.append(span['cn_span_index'])
        previous = span['end']
    assert sorted(links) == list(range(len(ex['spans']))), 'Each Chinese span needs one English alignment'

def tokens(ex, language):
    if language == 'ZH':
        source, spans = ex['text'], ex['spans']
        omissions = {v['start']: v for v in ex['display_omissions']}
    else:
        source, spans, omissions = ex['english_translation'], ex['english_spans'], {}
    span_starts = {s['start']: (i, s) for i, s in enumerate(spans)}
    result, pos = [], 0
    while pos < len(source):
        if pos in omissions:
            omission = omissions[pos]
            pos = omission['end']
            if omission.get('line_break_after'):
                result.append({'text': '\n', 'type': None, 'span_index': None})
        elif pos in span_starts:
            index, span = span_starts[pos]
            result.append({'text': span['text'], 'type': span['type'],
                           'span_index': index if language == 'ZH' else span['cn_span_index']})
            pos = span['end']
        else:
            stop = min([s for s in list(span_starts) + list(omissions) if s > pos] + [len(source)])
            pattern = r'[A-Za-z]+|[^A-Za-z]' if language == 'ZH' else r'\n|[^\S\n]+|[^\s]+'
            result.extend({'text': t, 'type': None, 'span_index': None}
                          for t in re.findall(pattern, source[pos:stop]))
            pos = stop
    return result

def layout(ex, language):
    font, size = ('CN', CNFS) if language == 'ZH' else ('EN', ENFS)
    items, placed, x, row = tokens(ex, language), [], 0.0, 0
    for index, item in enumerate(items):
        value = item['text']
        if value == '\n':
            if x:
                row += 1
                x = 0.0
            continue
        if not x and value.isspace():
            continue
        tw = width(value, font, size)
        total = tw + (TYPE_GAP if item['type'] else 0.0)
        reserve = 0.0
        if index + 1 < len(items) and items[index + 1]['text'] in ',.;:，。；：、）':
            reserve = width(items[index + 1]['text'], font, size)
        assert total + reserve <= TEXT_WIDTH, ('Entity must remain on one line', value)
        if x and x + total + reserve > TEXT_WIDTH:
            if value.isspace():
                # Let the next word/entity trigger the wrap, so its short
                # connective can move with it rather than being stranded.
                continue
            # Keep a short connective with the final English entity when that
            # entity wraps (e.g. "as well as" or "and assist with"). The text
            # and alignment boundaries stay unchanged; only line placement moves.
            carry = []
            if language == 'EN' and item['type'] and not any(v['type'] for v in items[index + 1:]):
                for prior in reversed(placed):
                    stripped = prior['text'].strip()
                    if prior['row'] != row or prior['type'] or (stripped and stripped in ',.;:'):
                        break
                    carry.insert(0, prior)
                words = sum(bool(v['text'].strip()) for v in carry)
                carry_width = sum(v['total_width'] for v in carry)
                if not (0 < words <= 4 and carry_width + total + reserve <= TEXT_WIDTH):
                    carry = []
                if carry:
                    del placed[-len(carry):]
            row += 1
            x = 0.0
            for prior in carry:
                if not x and prior['text'].isspace():
                    continue
                placed.append(dict(prior, x=x, row=row))
                x += prior['total_width']
            if carry and not carry[-1]['text'].isspace() and index and items[index - 1]['text'].isspace():
                # Restore the source separator discarded at the old line end.
                separator = items[index - 1]
                sw = width(separator['text'], font, size)
                placed.append(dict(separator, x=x, row=row, width=sw, total_width=sw))
                x += sw
            if value.isspace():
                continue
        placed.append(dict(item, x=x, row=row, width=tw, total_width=total))
        x += total
    return placed, row + 1

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--selection', choices=['all', 'main', 'additional'], default='all')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--layout-report', type=Path)
    args = parser.parse_args()
    data = json.loads((ROOT / 'annotation_examples_corpus_20261003.json').read_text(encoding='utf-8'))
    examples = data['examples']
    if args.selection == 'main':
        examples = examples[:3]
    elif args.selection == 'additional':
        examples = examples[3:]
    output = args.output or ROOT / 'annotation_examples_corpus_20261003.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    pdfmetrics.registerFont(TTFont('CN', os.getenv('CNSS_CN_FONT', 'C:/Windows/Fonts/simsun.ttc'), subfontIndex=0))
    pdfmetrics.registerFont(TTFont('EN', os.getenv('CNSS_EN_FONT', 'C:/Windows/Fonts/arial.ttf')))
    pdfmetrics.registerFont(TTFont('ENB', os.getenv('CNSS_EN_BOLD', 'C:/Windows/Fonts/arialbd.ttf')))
    for ex in examples:
        validate_example(ex)
        ex['zh_layout'], ex['zh_lines'] = layout(ex, 'ZH')
        ex['en_layout'], ex['en_lines'] = layout(ex, 'EN')
        # Extra lines increase the card height; font sizes never shrink.
        ex['en_baseline_offset'] = 36 + (ex['zh_lines'] - 1) * CNLEAD + 25
        ex['height'] = ex['en_baseline_offset'] + (ex['en_lines'] - 1) * ENLEAD + 15
    height = sum(e['height'] for e in examples) + 6 * (len(examples) - 1) + 49
    c = canvas.Canvas(str(output), pagesize=(W, height), pageCompression=1)
    c.setTitle('Chinese corpus annotations with aligned English translations')
    c.setAuthor('Chinese-SkillSpan authors')
    def text(x, y, value, font='EN', size=ENFS, color='#202C39'):
        c.setFillColor(HexColor(color))
        c.setFont(font, size)
        c.drawString(x, y, value)
    for row, items in enumerate([[('L', 'Language'), ('K', 'Knowledge-related requirements')],
                                 [('S', 'Occupational skills'), ('T', 'Transversal competencies')]]):
        for col, (code, label) in enumerate(items):
            x, y = 5 + col * 215, height - 17 - row * 20
            c.setFillColor(HexColor(FILL[code]))
            c.roundRect(x, y, 13, 14, 2, fill=1, stroke=0)
            text(x + 3, y + 3, code, 'ENB', 10, EDGE[code])
            text(x + 18, y + 3, label, 'EN', 10.4)
            assert x + 18 + width(label, 'EN', 10.4) < W
    top = height - 49
    report = {'page_size_pt': [W, height], 'text_width_pt': TEXT_WIDTH,
              'english_alignment_is_display_only': True, 'examples': []}
    for index, ex in enumerate(examples):
        bottom = top - ex['height']
        c.setFillColor(white)
        c.setStrokeColor(HexColor('#CBD7E3'))
        c.setLineWidth(.75)
        c.roundRect(.5, bottom + .5, W - 1, ex['height'] - 1, 5, fill=1, stroke=1)
        title = chr(97 + index) + ') ' + ex['title']
        meta = ex['source_id'] + ' | ' + ('excerpt' if ex['extent'] == 'contiguous excerpt' else 'full sentence')
        text(PAD, top - 16, title, 'ENB', 11.2)
        meta_width = width(meta, 'EN', 9)
        assert PAD + width(title, 'ENB', 11.2) + 15 < W - PAD - meta_width
        text(W - PAD - meta_width, top - 16, meta, 'EN', 9, '#536270')
        for language, baseline, font, size, leading in [
                ('ZH', top - 36, 'CN', CNFS, CNLEAD),
                ('EN', top - ex['en_baseline_offset'], 'EN', ENFS, ENLEAD)]:
            text(PAD, baseline + 1, language, 'ENB', 8.8, '#536270')
            for item in ex[language.lower() + '_layout']:
                x, y = TEXT_X + item['x'], baseline - item['row'] * leading
                tw, code = item['width'], item['type']
                if code:
                    c.setFillColor(HexColor(FILL[code]))
                    c.roundRect(x - 1, y - 2, tw + 2, size + 3, 1.5, fill=1, stroke=0)
                    c.setStrokeColor(HexColor(EDGE[code]))
                    c.setLineWidth(.65)
                    c.line(x, y - 2, x + tw, y - 2)
                text(x, y, item['text'], font, size, '#111820')
                if code:
                    text(x + tw + 2, y + 3, code, 'ENB', TYPE_FS, EDGE[code])
                assert y - 2 >= bottom + 8
                assert x + item['total_width'] <= W - PAD + .001
        report['examples'].append({'source_id': ex['source_id'], 'card_height_pt': ex['height'],
                                   'zh_lines': ex['zh_lines'], 'en_lines': ex['en_lines'],
                                   'zh_layout': ex['zh_layout'], 'en_layout': ex['en_layout'],
                                   'display_omissions': ex['display_omissions']})
        top = bottom - 6
    c.showPage()
    c.save()
    if args.layout_report:
        args.layout_report.parent.mkdir(parents=True, exist_ok=True)
        args.layout_report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('Aligned vector figure:', W, height, 'pt;', len(examples), 'records;', output.name)

if __name__ == '__main__':
    main()
