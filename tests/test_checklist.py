from copy import deepcopy
import unittest

from journalprose.checklist import evaluate, make_template


def record():
    p = make_template()
    p.update(manuscript="Invented draft 1", reviewer="Example reviewer", task_scope="Complete editorial review")
    return p


def complete_record():
    p = record()
    for item in p["criteria"]:
        item.update(status="pass", evidence="Invented review evidence at paragraph 2.")
    return p


class ChecklistTests(unittest.TestCase):
    def test_template_has_no_passes(self):
        p = make_template()
        self.assertEqual(len(p["criteria"]), 10)
        self.assertTrue(all(c["status"] == "not_reviewed" for c in p["criteria"]))

    def test_blank_identity_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(make_template())

    def test_unreviewed_record_stays_incomplete(self):
        result = evaluate(record())
        self.assertEqual(result["status"], "incomplete")
        self.assertFalse(result["complete"])

    def test_filled_record_reports_review_completeness_only(self):
        result = evaluate(complete_record())
        self.assertTrue(result["complete"])
        self.assertEqual(result["status"], "recorded-review-complete")
        self.assertNotIn("score", result)
        self.assertIn("does not independently verify", result["limitations"])

    def test_one_revision_blocks_completion(self):
        p = complete_record()
        p["criteria"][3].update(status="revise", note="Repair the missing premise.")
        result = evaluate(p)
        self.assertEqual(result["status"], "needs-revision")
        self.assertFalse(result["complete"])

    def test_pass_requires_evidence(self):
        p = complete_record()
        p["criteria"][0]["evidence"] = " "
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_revision_requires_note(self):
        p = complete_record()
        p["criteria"][3]["status"] = "revise"
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_nonapplicable_requires_reason(self):
        p = complete_record()
        p["criteria"][8]["status"] = "not_applicable"
        with self.assertRaises(ValueError):
            evaluate(p)
        p["criteria"][8]["note"] = "No compression was requested."
        self.assertTrue(evaluate(p)["complete"])

    def test_scope_cannot_be_nonapplicable(self):
        p = complete_record()
        p["criteria"][0].update(status="not_applicable", note="Proposed exception")
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_delivery_cannot_be_nonapplicable(self):
        p = complete_record()
        p["criteria"][-1].update(status="not_applicable", note="Proposed exception")
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_duplicate_ids_rejected(self):
        p = complete_record()
        p["criteria"][-1] = deepcopy(p["criteria"][0])
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_unknown_status_rejected(self):
        p = complete_record()
        p["criteria"][0]["status"] = True
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_wrong_schema_rejected(self):
        p = record()
        p["schema_version"] = 1
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_wrong_rulebook_version_rejected(self):
        p = record()
        p["rulebook_version"] = "0.1.1"
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_unknown_criterion_fields_rejected(self):
        p = complete_record()
        p["criteria"][0]["score"] = 2
        with self.assertRaises(ValueError):
            evaluate(p)

    def test_non_object_payload_rejected(self):
        with self.assertRaises(ValueError):
            evaluate([])

    def test_no_mutation_of_input(self):
        p = complete_record()
        before = deepcopy(p)
        evaluate(p)
        self.assertEqual(p, before)


if __name__ == "__main__":
    unittest.main()
