"""Monte o Word-base do Gran a partir de blocos editoriais em JSON."""

import argparse
from io import BytesIO
import json
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor


STYLES = {
    "texto": "Normal",
    "titulo_secundario": "Gran Título Secundário",
    "subtitulo": "Gran Subtítulo",
    "citacao": "Gran Citação",
    "destaque": "Gran Destaque",
    "marcador": "List Bullet",
}
UPPERCASE = {"titulo_secundario"}


def configure_document(document):
    section = document.sections[0]
    section.page_width = Cm(21.59)
    section.page_height = Cm(27.94)
    section.top_margin = section.bottom_margin = Cm(2.5)
    section.left_margin = section.right_margin = Cm(2.5)

    normal = document.styles["Normal"]
    normal.font.name = "Arial"
    normal.font.size = Pt(11)
    normal.font.color.rgb = RGBColor(0, 0, 0)
    fonts = normal.element.get_or_add_rPr().get_or_add_rFonts()
    for attribute in ("asciiTheme", "hAnsiTheme", "eastAsiaTheme", "cstheme"):
        fonts.attrib.pop(qn(f"w:{attribute}"), None)
    for attribute in ("eastAsia", "cs"):
        fonts.set(qn(f"w:{attribute}"), "Arial")
    lang = OxmlElement("w:lang")
    lang.set(qn("w:val"), "pt-BR")
    normal.element.get_or_add_rPr().append(lang)

    body = normal.paragraph_format
    body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    body.first_line_indent = Cm(1.25)
    body.line_spacing = 1.5
    body.space_before = Pt(12)
    body.space_after = Pt(0)
    body.widow_control = True

    for name in ("Gran Título", STYLES["titulo_secundario"], STYLES["subtitulo"], STYLES["destaque"]):
        style = document.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.base_style = normal
        style.font.bold = True
        fmt = style.paragraph_format
        fmt.first_line_indent = Cm(0)
        fmt.keep_with_next = True
        fmt.alignment = WD_ALIGN_PARAGRAPH.LEFT
    document.styles["Gran Título"].paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

    citation = document.styles.add_style(STYLES["citacao"], WD_STYLE_TYPE.PARAGRAPH)
    citation.base_style = normal
    citation.font.size = Pt(10)
    citation.paragraph_format.left_indent = Cm(3.81)
    citation.paragraph_format.first_line_indent = Cm(0)


def add_block(document, block, last_time):
    if not isinstance(block, dict):
        raise ValueError("Cada bloco deve ser um objeto.")
    unknown = set(block) - {"tipo", "texto", "minuto", "fim_destaque"}
    if unknown:
        raise ValueError(f"Campos desconhecidos no bloco: {', '.join(sorted(unknown))}.")
    kind = block.get("tipo")
    if not isinstance(kind, str) or kind not in STYLES:
        raise ValueError(f"Tipo de bloco desconhecido: {kind!r}.")
    text = block.get("texto")
    if not isinstance(text, str) or not text.strip() or any(ch in text for ch in "\r\n"):
        raise ValueError("Cada bloco deve ter um parágrafo de texto não vazio.")
    paragraph = document.add_paragraph(
        text.strip().upper() if kind in UPPERCASE else text.strip(), style=STYLES[kind]
    )

    end_callout = block.get("fim_destaque", False)
    if type(end_callout) is not bool:
        raise ValueError("fim_destaque deve ser verdadeiro ou falso.")
    if end_callout:
        border = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        for key, value in {"val": "single", "sz": "4", "space": "4", "color": "000000"}.items():
            bottom.set(qn(f"w:{key}"), value)
        border.append(bottom)
        paragraph._p.get_or_add_pPr().append(border)

    if "minuto" not in block:
        return last_time
    minute = block["minuto"]
    if type(minute) is not int or minute != last_time + 5:
        raise ValueError(f"Esperava a marcação de {last_time + 5} min neste bloco.")
    paragraph.add_run(f" {minute} min").bold = True
    return minute


def build(data):
    if not isinstance(data, dict) or set(data) != {"titulo", "blocos"}:
        raise ValueError("Informe exatamente os campos titulo e blocos.")
    title, blocks = data["titulo"], data["blocos"]
    if not isinstance(title, str) or not title.strip() or any(ch in title for ch in "\r\n"):
        raise ValueError("Informe um título em uma única linha.")
    if not isinstance(blocks, list) or not blocks:
        raise ValueError("Informe pelo menos um bloco de conteúdo.")

    document = Document()
    configure_document(document)
    document.core_properties.title = title.strip()
    document.add_paragraph(title.strip().upper(), style="Gran Título")
    last_time = 0
    for index, block in enumerate(blocks, 1):
        try:
            last_time = add_block(document, block, last_time)
        except ValueError as error:
            raise ValueError(f"Bloco {index}: {error}") from error
    return document


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("entrada", type=Path, help="Arquivo JSON UTF-8")
    parser.add_argument("saida", type=Path, help="Caminho de um novo arquivo DOCX")
    args = parser.parse_args()
    if args.saida.suffix.lower() != ".docx":
        parser.error("A saída deve ter extensão .docx.")
    try:
        document = build(json.loads(args.entrada.read_text(encoding="utf-8-sig")))
        buffer = BytesIO()
        document.save(buffer)
        with args.saida.open("xb") as output:
            output.write(buffer.getbuffer())
    except (OSError, ValueError) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
