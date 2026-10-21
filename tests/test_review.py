from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from well_argued_prose.review import audit_text, read_manuscript


class ReviewTests(unittest.TestCase):
    def test_flags_are_advisory_and_located(self):
        text = "This paper aims to discuss identity.\nTherefore, this structure must be explained.\n"
        result = audit_text(text)
        found = {row["code"]: row for row in result["checks"]}
        self.assertEqual(1, found["generic-purpose"]["total_matches"])
        self.assertEqual(1, found["inferential-connective"]["total_matches"])
        self.assertEqual(2, found["inferential-connective"]["examples"][0]["line"])
        self.assertEqual(1, found["unclear-demonstrative"]["total_matches"])
        self.assertIn("not proven errors", result["disclaimer"])

    def test_noncontrasting_prose_not_flagged_as_pivot(self):
        text = "The premise is not certain. We should test it."
        found = {row["code"]:row for row in audit_text(text)["checks"]}
        self.assertEqual(0, found["negative-pivot"]["total_matches"])

    def test_input_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "manuscript.md"
            path.write_text("Academic argument.\nSecond sentence.\n", encoding="utf-8")
            text, unit = read_manuscript(path)
            self.assertEqual("line", unit)
            self.assertIn("Second sentence", text)
            unsupported = Path(tmp) / "unsupported.pdf"
            unsupported.write_bytes(b"not a supported file")
            with self.assertRaisesRegex(ValueError, "Supported manuscript types"):
                read_manuscript(unsupported)

    def test_max_per_check_validation(self):
        with self.assertRaises(ValueError):
            audit_text("abc", max_per_check=0)
