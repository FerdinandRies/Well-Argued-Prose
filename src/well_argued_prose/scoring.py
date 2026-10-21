"""Human-supplied scorecard management. No model-generated manuscript ratings."""

from __future__ import annotations

from .catalog import load


def make_template() -> dict:
    return {
        "schema_version": 1,
        "manuscript": "",
        "criteria": [
            {"id": criterion["id"], "score": None, "evidence": "", "revision_note": ""}
            for criterion in load("scorecard")["criteria"]
        ],
    }


def evaluate(payload: dict) -> dict:
    expected = {item["id"]: item for item in load("scorecard")["criteria"]}
    actual = payload.get("criteria")
    if not isinstance(actual, list) or len(actual) != len(expected):
        raise ValueError("A complete scorecard requires exactly 12 criterion entries")
    ids = [item.get("id") for item in actual if isinstance(item, dict)]
    if set(ids) != set(expected) or len(ids) != len(set(ids)):
        raise ValueError("Scorecard criterion IDs are missing, unknown, or duplicated")
    ordered = {item["id"]: item for item in actual}
    results = []
    for key, standard in expected.items():
        item = ordered[key]
        score = item.get("score")
        if type(score) is not int or score not in (0, 1, 2):
            raise ValueError(f"Criterion '{key}' must have an integer score of 0, 1, or 2")
        evidence = item.get("evidence", "")
        if not isinstance(evidence, str) or (score > 0 and not evidence.strip()):
            raise ValueError(f"Criterion '{key}' needs textual evidence for a positive score")
        results.append({"id":key, "title":standard["title"], "score":score,
                        "rule_ids": standard["rule_ids"], "evidence": evidence,
                        "revision_note": item.get("revision_note", "")})
    score = sum(item["score"] for item in results)
    return {"manuscript":payload.get("manuscript", ""), "score":score, "out_of":24,
            "review_threshold_met": score >= 20,
            "verdict": "Proceed to final language review" if score >= 20 else "Return to structural and argumentative revision",
            "criteria":results,
            "caveat":"This is a human-authored editorial checklist. It does not certify journal readiness or predict acceptance."}
