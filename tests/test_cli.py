from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from well_argued_prose.cli import main


class CliTests(unittest.TestCase):
    def run_cli(self, argv):
        output, errors = StringIO(), StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            code = main(argv)
        return code, output.getvalue(), errors.getvalue()

    def test_cli_commands(self):
        self.assertEqual(0, self.run_cli(["validate"])[0])
        self.assertIn("57 rules", self.run_cli(["validate"])[1])
        self.assertIn("Rule 37", self.run_cli(["show", "37"])[1])
        self.assertIn("Source article(s)", self.run_cli(["show", "37"])[1])
        self.assertIn("introduction", self.run_cli(["guide"])[1])
        self.assertIn("14", self.run_cli(["guide", "introduction"])[1])
        self.assertIn("Manuscript Architecture", self.run_cli(["list", "--section", "1"])[1])

    def test_cli_audit_json(self):
        code, output, errors = self.run_cli(["audit", str(ROOT / "examples" / "sample-manuscript.md"), "--json"])
        self.assertEqual(0, code, errors)
        payload = json.loads(output)
        self.assertEqual("advisory-language-audit", payload["kind"])
        self.assertTrue(any(item["total_matches"] for item in payload["checks"]))

    def test_cli_scorecard_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "review.json"
            self.assertEqual(0, self.run_cli(["scorecard", "init", str(path)])[0])
            self.assertEqual(2, self.run_cli(["scorecard", "init", str(path)])[0])
            self.assertEqual(2, self.run_cli(["scorecard", "evaluate", str(path)])[0])
            payload = json.loads(path.read_text(encoding="utf-8"))
            for row in payload["criteria"]:
                row["score"] = 1
                row["evidence"] = "Example paragraph evaluated by a reviewer."
            path.write_text(json.dumps(payload), encoding="utf-8")
            code, output, _ = self.run_cli(["scorecard", "evaluate", str(path)])
            self.assertEqual(0, code)
            self.assertIn("12/24", output)

    def test_invalid_rule_error(self):
        code, _, errors = self.run_cli(["show", "99"])
        self.assertEqual(2, code)
        self.assertIn("does not exist", errors)
