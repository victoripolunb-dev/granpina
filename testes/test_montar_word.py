import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn


FIXTURE = Path(__file__).with_name("amostra.json")
SCRIPT = FIXTURE.parent.parent / "montar_word.py"


def run_generator(source, output):
    return subprocess.run(
        [sys.executable, SCRIPT, source, output], capture_output=True, text=True
    )


class GenerateWordTest(unittest.TestCase):
    def test_generated_word_matches_base_styles(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "amostra.docx"
            result = run_generator(FIXTURE, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            doc = Document(output)

        title = doc.paragraphs[0]
        self.assertEqual(title.text, "AMOSTRA DE FORMATAÇÃO")
        self.assertEqual(title.style.paragraph_format.alignment, WD_ALIGN_PARAGRAPH.CENTER)
        self.assertTrue(title.style.font.bold)
        normal = doc.styles["Normal"]
        self.assertEqual((normal.font.name, normal.font.size.pt), ("Arial", 11))
        self.assertEqual(normal.paragraph_format.line_spacing, 1.5)
        self.assertEqual(normal.paragraph_format.alignment, WD_ALIGN_PARAGRAPH.JUSTIFY)
        self.assertAlmostEqual(normal.paragraph_format.first_line_indent.cm, 1.25, places=2)
        for side in ("left", "right", "top", "bottom"):
            self.assertAlmostEqual(getattr(doc.sections[0], side + "_margin").cm, 2.5, places=2)
        quote = doc.paragraphs[3].style
        self.assertEqual(quote.font.size.pt, 10)
        self.assertAlmostEqual(quote.paragraph_format.left_indent.cm, 3.81, places=2)
        self.assertEqual(doc.paragraphs[5].style.name, "List Bullet")
        self.assertIsNotNone(doc.paragraphs[8]._p.pPr.find(qn("w:pBdr")))
        self.assertTrue(doc.paragraphs[2].text.endswith(" 5 min"))
        self.assertTrue(doc.paragraphs[-1].text.endswith(" 10 min"))

    def test_reject_skipped_timestamp(self):
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        data["blocos"][-1]["minuto"] = 15
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "invalida.json"
            source.write_text(json.dumps(data), encoding="utf-8")
            output = Path(folder) / "invalida.docx"
            result = run_generator(source, output)
            self.assertEqual(result.returncode, 1)
            self.assertIn("10 min", result.stderr)
            self.assertFalse(output.exists())

    def test_protect_existing_output(self):
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / "existente.docx"
            original = b"arquivo existente"
            output.write_bytes(original)
            self.assertEqual(run_generator(FIXTURE, output).returncode, 1)
            self.assertEqual(output.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
