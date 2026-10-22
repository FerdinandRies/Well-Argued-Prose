import ast
import importlib.util
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest

from journalprose.catalog import load
from journalprose.review import audit_text

ROOT = Path(__file__).resolve().parents[1]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ReleaseTests(unittest.TestCase):
    def test_generated_docs_match(self):
        generator = module_at("journalprose_doc_generation", ROOT / "scripts/build_handbook.py")
        for name, content in generator.outputs().items():
            self.assertEqual((ROOT / "docs" / name).read_text(encoding="utf-8"), content)

    def test_public_allowlist(self):
        checker = module_at("journalprose_release_check", ROOT / "scripts/check_release.py")
        self.assertEqual(checker.check(ROOT), [])

    def test_unapproved_file_detected(self):
        checker = module_at("journalprose_release_check", ROOT / "scripts/check_release.py")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "release-manifest.json").write_text(json.dumps({"version":"0.2.0","files":["release-manifest.json"]}) + "\n")
            (root / "unapproved-notes.txt").write_text("Do not publish.\n")
            self.assertTrue(any("Unapproved" in s for s in checker.check(root)))

    def test_distribution_metadata_is_outside_zip_allowlist(self):
        checker = module_at("journalprose_release_check", ROOT / "scripts/check_release.py")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "release-manifest.json").write_text(json.dumps({"version":"0.2.0","files":["release-manifest.json"]}) + "\n")
            (root / "PKG-INFO").write_text("Name: example\n")
            (root / "setup.cfg").write_text("[egg_info]\n")
            self.assertEqual(checker.check(root), [])
            self.assertNotIn("PKG-INFO", checker.approved_paths(root))
            self.assertNotIn("setup.cfg", checker.approved_paths(root))

    def test_unsafe_manifest_path_rejected(self):
        checker = module_at("journalprose_release_check", ROOT / "scripts/check_release.py")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "release-manifest.json").write_text(json.dumps({"version":"0.2.0","files":["../example"]}) + "\n")
            self.assertTrue(checker.check(root))

    def test_all_rule_anchors_exist_once(self):
        text = (ROOT / "docs/handbook.md").read_text(encoding="utf-8")
        for rule in load("rules")["rules"]:
            self.assertEqual(text.count(f'<a id="{rule["id"].lower()}"></a>'), 1)

    def test_local_markdown_links_resolve(self):
        for path in ROOT.rglob("*.md"):
            if any(x in path.parts for x in ("build", "dist", ".git")):
                continue
            text = path.read_text(encoding="utf-8")
            for target in re.findall(r"\]\(([^)\s]+)\)", text):
                if target.startswith(("http://", "https://", "mailto:")):
                    continue
                file_part, _, anchor = target.partition("#")
                dest = (path.parent / file_part).resolve() if file_part else path
                self.assertTrue(dest.exists(), f"{path}: missing {target}")
                if anchor.startswith("jp2-"):
                    self.assertIn(f'id="{anchor}"', dest.read_text(encoding="utf-8"))

    def test_metadata_versions_and_author(self):
        for filename in ("pyproject.toml", "CITATION.cff", "AUTHORS.md", "LICENSE", "LICENSE-CONTENT.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            self.assertIn("FerdinandRies", text)
        self.assertIn('version = "0.2.0"', (ROOT / "pyproject.toml").read_text())
        self.assertIn('version: 0.2.0', (ROOT / "CITATION.cff").read_text())

    def test_python_310_syntax(self):
        for folder in ("src", "scripts", "tests"):
            for path in (ROOT / folder).rglob("*.py"):
                ast.parse(path.read_text(encoding="utf-8"), filename=str(path), feature_version=(3, 10))

    def test_sample_revision_has_no_policy_matches(self):
        text = (ROOT / "examples/sample-revision.md").read_text(encoding="utf-8")
        self.assertEqual(audit_text(text)["policy_matches"], 0)

    def test_sample_manuscript_has_demonstrated_findings(self):
        text = (ROOT / "examples/sample-manuscript.md").read_text(encoding="utf-8")
        result = audit_text(text)
        self.assertGreater(result["policy_matches"], 0)
        self.assertGreater(next(c for c in result["checks"] if c["id"] == "citation-density")["total_matches"], 0)


if __name__ == "__main__":
    unittest.main()
