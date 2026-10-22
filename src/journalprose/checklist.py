"""Evidence-backed human review records, without aggregate quality scoring."""
from __future__ import annotations

from typing import Any
from . import __version__
from .catalog import load


def make_template() -> dict[str, Any]:
    return {"schema_version": 2, "rulebook_version": __version__, "manuscript": "", "reviewer": "",
            "task_scope": "", "criteria": [
                {"id": c["id"], "status": "not_reviewed", "evidence": "", "note": ""}
                for c in load("checklist")["criteria"]]}


def evaluate(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict) or type(payload.get("schema_version")) is not int or payload["schema_version"] != 2:
        raise ValueError("A version-2 checklist object is required; legacy numerical scorecards are unsupported")
    if payload.get("rulebook_version") != __version__:
        raise ValueError("Checklist rulebook_version must match the installed version")
    for key in ("manuscript", "reviewer", "task_scope"):
        if not isinstance(payload.get(key), str) or not payload[key].strip():
            raise ValueError(f"Checklist requires a nonempty {key}")
    actual = payload.get("criteria")
    expected = load("checklist")["criteria"]
    known = {c["id"] for c in expected}
    if not isinstance(actual, list) or not all(isinstance(x, dict) for x in actual):
        raise ValueError("criteria must be a list of objects")
    ids = [c.get("id") for c in actual]
    if not all(isinstance(i, str) for i in ids) or set(ids) != known or len(ids) != len(known):
        raise ValueError("Checklist criterion IDs are missing, duplicated, or unknown")
    statuses = load("checklist")["statuses"]
    counts = {status: 0 for status in statuses}
    indexed = {c["id"]: c for c in actual}
    result = []
    for spec in expected:
        item = indexed[spec["id"]]
        if set(item) != {"id", "status", "evidence", "note"}:
            raise ValueError(f"{item['id']}: expected id, status, evidence, and note only")
        status = item.get("status")
        if not isinstance(status, str) or status not in statuses:
            raise ValueError(f"{item['id']}: invalid status")
        if not all(isinstance(item.get(k), str) for k in ("evidence", "note")):
            raise ValueError(f"{item['id']}: evidence and note must be strings")
        if status in {"pass", "revise"} and not item["evidence"].strip():
            raise ValueError(f"{item['id']}: a reviewed decision requires textual evidence")
        if status in {"revise", "not_applicable"} and not item["note"].strip():
            raise ValueError(f"{item['id']}: revision or non-applicability requires a reason")
        if status == "not_applicable" and item["id"] in {"scope", "delivery"}:
            raise ValueError(f"{item['id']}: baseline and final disposition must be reviewed")
        counts[status] += 1
        result.append({**spec, **item})
    complete = counts["not_reviewed"] == 0 and counts["revise"] == 0
    state = "needs-revision" if counts["revise"] else ("incomplete" if counts["not_reviewed"] else "recorded-review-complete")
    return {"schema_version": 2, "rulebook_version": __version__, "manuscript": payload["manuscript"],
            "reviewer": payload["reviewer"], "task_scope": payload["task_scope"],
            "status": state, "complete": complete, "counts": counts, "criteria": result,
            "limitations": "Decisions and evidence are supplied by the reviewer. The program checks record completeness; it does not independently verify those decisions or certify publication readiness."}
