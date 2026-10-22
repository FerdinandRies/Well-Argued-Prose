from contextlib import redirect_stdout, redirect_stderr
import io
import json
from pathlib import Path
import tempfile
import unittest

from journalprose.cli import main
from journalprose.checklist import make_template


def invoke(args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = main(args)
    return code, out.getvalue(), err.getvalue()


class CliTests(unittest.TestCase):
    def test_validate(self):
        code, out, err = invoke(["validate"])
        self.assertEqual(code, 0)
        self.assertIn("50 rules", out)
        self.assertEqual(err, "")

    def test_list_json(self):
        code, out, _ = invoke(["list", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)), 50)

    def test_list_one_level(self):
        code, out, _ = invoke(["list", "--level", "L7", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)), 4)

    def test_show(self):
        code, out, _ = invoke(["show", "JP2-033", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["id"], "JP2-033")

    def test_show_legacy_numeric_is_error(self):
        code, _, err = invoke(["show", "33"])
        self.assertEqual(code, 2)
        self.assertIn("Legacy numeric", err)

    def test_guide_all(self):
        code, out, _ = invoke(["guide", "--json"])
        self.assertEqual(code, 0)
        self.assertEqual(len(json.loads(out)), 6)

    def test_guide_one(self):
        code, out, _ = invoke(["guide", "compression"])
        self.assertEqual(code, 0)
        self.assertIn("JP2-047", out)

    def test_bad_workflow(self):
        self.assertEqual(invoke(["guide", "absent"])[0], 2)

    def test_audit_default_exit_and_json(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "example.txt"
            p.write_text("not only a record", encoding="utf-8")
            code, out, err = invoke(["audit", str(p), "--json"])
            self.assertEqual(code, 0)
            self.assertEqual(json.loads(out)["policy_matches"], 1)
            self.assertEqual(err, "")

    def test_audit_failure_policies(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "example.txt"
            p.write_text("not only a record", encoding="utf-8")
            self.assertEqual(invoke(["audit", str(p), "--fail-on", "policy"])[0], 1)
            p.write_text("This shows a difference.", encoding="utf-8")
            self.assertEqual(invoke(["audit", str(p), "--fail-on", "policy"])[0], 0)
            self.assertEqual(invoke(["audit", str(p), "--fail-on", "any"])[0], 1)

    def test_audit_missing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            code, _, err = invoke(["audit", str(Path(directory) / "absent.txt")])
            self.assertEqual(code, 2)
            self.assertNotIn("Traceback", err)

    def test_audit_invalid_limit(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "example.txt"
            p.write_text("text", encoding="utf-8")
            self.assertEqual(invoke(["audit", str(p), "--max-per-check", "0"])[0], 2)

    def test_checklist_init_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "review.json"
            self.assertEqual(invoke(["checklist", "init", str(p)])[0], 0)
            before = p.read_bytes()
            self.assertEqual(invoke(["checklist", "init", str(p)])[0], 2)
            self.assertEqual(p.read_bytes(), before)

    def test_checklist_init_force(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "review.json"
            p.write_text("old", encoding="utf-8")
            self.assertEqual(invoke(["checklist", "init", str(p), "--force"])[0], 0)
            self.assertEqual(json.loads(p.read_text())["schema_version"], 2)

    def test_incomplete_review_exit(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "review.json"
            payload = make_template()
            payload.update(manuscript="Invented draft", reviewer="Example reviewer", task_scope="Editing")
            p.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(invoke(["checklist", "evaluate", str(p)])[0], 0)
            self.assertEqual(invoke(["checklist", "evaluate", str(p), "--require-complete"])[0], 1)

    def test_malformed_json_returns_error(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / "review.json"
            p.write_text("{", encoding="utf-8")
            code, _, err = invoke(["checklist", "evaluate", str(p)])
            self.assertEqual(code, 2)
            self.assertNotIn("Traceback", err)

    def test_version(self):
        out = io.StringIO()
        with redirect_stdout(out), self.assertRaises(SystemExit) as caught:
            main(["--version"])
        self.assertEqual(caught.exception.code, 0)
        self.assertEqual(out.getvalue().strip(), "journalprose 0.2.0")


if __name__ == "__main__":
    unittest.main()
