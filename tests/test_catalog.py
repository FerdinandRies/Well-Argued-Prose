from copy import deepcopy
import unittest

from journalprose import __version__
from journalprose.catalog import NAMES, get_rule, get_workflow, load, validate_catalog


class CatalogTests(unittest.TestCase):
    def test_catalog_valid(self):
        self.assertEqual(validate_catalog(), [])

    def test_fifty_rules_eight_levels(self):
        doc = load("rules")
        self.assertEqual(len(doc["rules"]), 50)
        self.assertEqual(len(doc["levels"]), 8)
        self.assertEqual([i for l in doc["levels"] for i in l["rule_ids"]], [r["id"] for r in doc["rules"]])

    def test_version_and_maintainer(self):
        self.assertEqual(load("rules")["version"], __version__)
        self.assertEqual(__version__, "0.2.0")
        self.assertEqual(load("rules")["maintainer"], "FerdinandRies")

    def test_examples_invented_and_complete(self):
        for rule in load("rules")["rules"]:
            with self.subTest(rule=rule["id"]):
                self.assertEqual(rule["example"]["status"], "invented")
                self.assertTrue(all(rule["example"][k].strip() for k in ("before", "after", "explanation")))

    def test_load_returns_copy(self):
        value = load("rules")
        value["rules"][0]["title"] = "changed"
        self.assertNotEqual(load("rules")["rules"][0]["title"], "changed")

    def test_get_rule(self):
        self.assertEqual(get_rule("JP2-033")["level"], "L5")

    def test_legacy_id_rejected(self):
        for value in (33, "33", "JP-033", "JP2-33"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                get_rule(value)

    def test_unknown_rule(self):
        with self.assertRaises(ValueError):
            get_rule("JP2-099")

    def test_unknown_catalog(self):
        with self.assertRaises(ValueError):
            load("../../example")

    def test_workflows(self):
        flows = load("workflows")["workflows"]
        self.assertEqual(len(flows), 6)
        self.assertIn("JP2-047", get_workflow("compression")["rule_ids"])

    def test_unknown_workflow(self):
        with self.assertRaises(ValueError):
            get_workflow("unknown")

    def test_check_count(self):
        self.assertEqual(len(load("checks")["checks"]), 21)

    def test_no_claim_of_complete_automation(self):
        kinds = {r["automation"] for r in load("rules")["rules"]}
        self.assertEqual(kinds, {"human", "advisory", "pattern"})
        automated = {rid for check in load("checks")["checks"] for rid in check["rule_ids"]}
        self.assertLess(len(automated), 50)

    def test_missing_example_rejected(self):
        docs = {n: load(n) for n in NAMES}
        del docs["rules"]["rules"][0]["example"]
        self.assertTrue(validate_catalog(docs))

    def test_unknown_rule_field_rejected(self):
        docs = {n: load(n) for n in NAMES}
        docs["rules"]["rules"][0]["extra_material"] = "unauthorized"
        self.assertTrue(validate_catalog(docs))

    def test_bad_reference_rejected(self):
        docs = {n: load(n) for n in NAMES}
        docs["workflows"]["workflows"][0]["rule_ids"] = ["JP2-999"]
        self.assertTrue(validate_catalog(docs))

    def test_duplicate_check_rejected(self):
        docs = {n: load(n) for n in NAMES}
        docs["checks"]["checks"].append(deepcopy(docs["checks"]["checks"][0]))
        self.assertTrue(validate_catalog(docs))

    def test_bad_regex_rejected(self):
        docs = {n: load(n) for n in NAMES}
        docs["checks"]["checks"][0]["pattern"] = "["
        self.assertTrue(validate_catalog(docs))

    def test_empty_match_regex_rejected(self):
        docs = {n: load(n) for n in NAMES}
        docs["checks"]["checks"][0]["pattern"] = "x*"
        self.assertTrue(validate_catalog(docs))

    def test_non_object_document_rejected(self):
        self.assertTrue(validate_catalog([]))

    def test_schema_boolean_rejected(self):
        docs = {n: load(n) for n in NAMES}
        docs["rules"]["schema_version"] = True
        self.assertTrue(validate_catalog(docs))

    def test_source_collection_is_not_a_runtime_catalog(self):
        self.assertEqual(NAMES, {"rules", "workflows", "checks", "checklist"})


if __name__ == "__main__":
    unittest.main()
