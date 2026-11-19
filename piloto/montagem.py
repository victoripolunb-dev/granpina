from pathlib import Path
import re
import sys

from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.shared import Cm, Pt
from docx.oxml.ns import qn

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent))
from montar_word import build


def math_node(name, *children):
    node = OxmlElement(f'm:{name}')
    for child in children:
        node.append(child)
    return node


def math_text(text):
    token = math_node('t')
    token.set(qn('xml:space'), 'preserve')
    token.text = text
    return math_node('r', token)


def equation(paragraph, numerator, denominator, outcome=''):
    paragraph.clear()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    paragraph.paragraph_format.first_line_indent = Cm(0)
    fraction = math_node('f', math_node('num', math_text(numerator)), math_node('den', math_text(denominator)))
    content = math_node('oMath', fraction)
    if outcome:
        content.append(math_text(outcome))
    paragraph._p.append(content)


def list_numbering(document, paragraph, start_new, number_id):
    root = document.part.numbering_part.element
    if start_new:
        abstract_id = max(int(n.get(qn('w:abstractNumId'))) for n in root.findall(qn('w:abstractNum'))) + 1
        abstract = OxmlElement('w:abstractNum')
        abstract.set(qn('w:abstractNumId'), str(abstract_id))
        level = OxmlElement('w:lvl')
        level.set(qn('w:ilvl'), '0')
        for name, value in [('start', '1'), ('numFmt', 'lowerLetter'), ('lvlText', '%1.'), ('lvlJc', 'left')]:
            prop = OxmlElement(f'w:{name}')
            prop.set(qn('w:val'), value)
            level.append(prop)
        abstract.append(level)
        first_num = root.find(qn('w:num'))
        if first_num is not None:
            first_num.addprevious(abstract)
        else:
            root.append(abstract)
        number_id = root.add_num(abstract_id).numId
    numpr = paragraph._p.get_or_add_pPr().get_or_add_numPr()
    numpr.get_or_add_ilvl().val = 0
    numpr.get_or_add_numId().val = number_id
    return number_id


def parse(raw):
    blocks = []
    extras = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        kind, text = line.split('|', 1)
        minute = re.search(r' \[(\d+)\]$', text)
        block = {'tipo': 'texto', 'texto': text[:minute.start()] if minute else text}
        if minute:
            block['minuto'] = int(minute[1])
        if kind.endswith('!'):
            kind = kind[:-1]
            block['fim_destaque'] = True
        block['tipo'] = {'H': 'titulo_secundario', 'S': 'subtitulo', 'D': 'destaque'}.get(kind, 'texto')
        blocks.append(block)
        extras.append(kind)
    return blocks, extras


blocks, extras = parse((BASE / 'redacao.txt').read_text(encoding='utf-8-sig'))
document = build({'titulo': 'Planejamento Conservacionista II', 'blocos': blocks})
number_id = None
question = 0
for p, kind in zip(document.paragraphs[1:], extras):
    f = p.paragraph_format
    if kind in {'Q', 'A', 'C', 'G', 'M', 'I'}:
        f.first_line_indent = Cm(0)
    if kind in {'A', 'C', 'G'}:
        f.space_before = Pt(4)
    if kind in {'A', 'C'}:
        f.left_indent = Cm(.55)
        f.first_line_indent = Cm(-.55)
        f.tab_stops.add_tab_stop(Cm(.55))
    if kind == 'Q':
        question += 1
    if kind == 'Q' or p.text.startswith('A soma dos valores percentuais'):
        f.keep_with_next = True
    if kind in {'A', 'C'}:
        f.keep_together = True
        label, first_text = p.runs[0].text.split('. ', 1)
        if kind == 'C' and question == 3 and label in 'abc':
            f.keep_with_next = True
        p.runs[0].text = first_text
        number_id = list_numbering(document, p, label == 'a', number_id)
    if kind == 'M':
        equation(p, *p.text.split('|'))
    if kind == 'I':
        size = Cm(11.5)
        p.clear()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        picture = p.add_run().add_picture(str(BASE / 'bacia.png'), width=size)
        picture._inline.docPr.set('descr', 'Mapa com seis microbacias, divisores de águas, curso principal e exutório.')
        f.keep_with_next = True
    if kind == 'G' and p.text != '3. d':
        f.keep_with_next = True
    if p.text == 'GABARITO':
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
document.save(BASE / 'Planejamento Conservacionista II - 600724 - 261111(5)12.docx')

