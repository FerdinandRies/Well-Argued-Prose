import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from well_argued_prose.catalog import get_rule, get_workflow, load, validate_catalog


class CatalogTests(unittest.TestCase):
    def test_catalog_integrity(self):
        self.assertEqual([], validate_catalog())

    def test_rule_count_order_and_content(self):
        rules = load("rules")["rules"]
        self.assertEqual(57, len(rules))
        self.assertEqual(list(range(1, 58)), [item["id"] for item in rules])
        for item in rules:
            for key in ("title", "scope", "standard", "corpus_observation", "review_action", "example"):
                self.assertGreater(len(item[key]), 5, (item["id"], key))

    def test_sections_and_workflows(self):
        self.assertEqual(9, len(load("rules")["sections"]))
        self.assertEqual(10, len(load("workflows")))
        self.assertEqual(37, get_rule(37)["id"])
        self.assertIn(14, get_workflow("introduction")["rule_ids"])

    def test_invalid_catalog_lookup(self):
        with self.assertRaises(ValueError):
            get_rule(58)
        with self.assertRaises(ValueError):
            get_workflow("no-such-task")
        with self.assertRaises(ValueError):
            load("../something")

    def test_reference_metadata(self):
        corpus = load("corpus")
        self.assertEqual(12, len(corpus))
        for entry in corpus:
            self.assertEqual("Mind", entry["journal"])
            self.assertTrue(entry["doi"].startswith("10.1093/mind/"))

    def test_example_provenance_is_complete(self):
        corpus = load("corpus")
        known = {x["id"] for x in corpus}
        used = set()
        for rule in load("rules")["rules"]:
            self.assertTrue(rule["example_sources"])
            self.assertTrue(set(rule["example_sources"]).issubset(known))
            used.update(rule["example_sources"])
        self.assertEqual(known, used)  # all twelve corpus articles inform examples

    def test_attribution_and_release_metadata(self):
        self.assertIn("FerdinandRies", (ROOT / "AUTHORS.md").read_text())
        self.assertIn("FerdinandRies", (ROOT / "CITATION.cff").read_text())
        self.assertIn("FerdinandRies", (ROOT / "LICENSE").read_text())
        self.assertIn("FerdinandRies", (ROOT / "LICENSE-CONTENT.md").read_text())

    def test_generated_rulebook_is_complete(self):
        content = (ROOT / "docs" / "handbook.md").read_text(encoding="utf-8")
        for number in range(1, 58):
            self.assertIn(f"### Rule {number:02d} —", content)
        self.assertEqual(57, content.count("**Corpus observation.**"))
        self.assertEqual(57, content.count("**Example.**"))
        self.assertEqual(57, content.count("**Source article(s).**"))
        mapping = (ROOT / "docs" / "example-sources.md").read_text()
        self.assertEqual(57, mapping.count("| [Rule "))
