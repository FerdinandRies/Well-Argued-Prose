from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from well_argued_prose.scoring import make_template, evaluate


class ScorecardTests(unittest.TestCase):
    def test_template_is_never_auto_scored(self):
        payload = make_template()
        self.assertEqual(12, len(payload["criteria"]))
        self.assertTrue(all(item["score"] is None for item in payload["criteria"]))
        with self.assertRaisesRegex(ValueError, "must have an integer score"):
            evaluate(payload)

    def test_score_requires_specific_evidence(self):
        payload = make_template()
        for item in payload["criteria"]:
            item["score"] = 2
        with self.assertRaisesRegex(ValueError, "needs textual evidence"):
            evaluate(payload)

    def test_24_point_review_threshold(self):
        payload = make_template()
        for index, item in enumerate(payload["criteria"]):
            item["score"] = 2 if index < 10 else 0
            item["evidence"] = "Relevant manuscript passage and inferential role are specified." if item["score"] else ""
        result = evaluate(payload)
        self.assertEqual(20, result["score"])
        self.assertTrue(result["review_threshold_met"])
        payload["criteria"][9]["score"] = 1
        self.assertEqual(19, evaluate(payload)["score"])
        self.assertFalse(evaluate(payload)["review_threshold_met"])

    def test_reject_duplicate_ids_and_boolean_scores(self):
        payload = make_template()
        for item in payload["criteria"]:
            item["score"] = 0
        payload["criteria"][0]["score"] = True
        with self.assertRaisesRegex(ValueError, "integer score"):
            evaluate(payload)
        payload["criteria"][0]["score"] = 0
        payload["criteria"][0]["id"] = payload["criteria"][1]["id"]
        with self.assertRaisesRegex(ValueError, "duplicated"):
            evaluate(payload)
