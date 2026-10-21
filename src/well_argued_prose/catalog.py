"""Load the versioned editorial catalog from package resources."""

from __future__ import annotations

from functools import lru_cache
from importlib import resources
import json


@lru_cache(maxsize=None)
def load(name: str):
    allowed = {"rules", "workflows", "scorecard", "corpus"}
    if name not in allowed:
        raise ValueError(f"Unknown catalog: {name}")
    raw = resources.files("well_argued_prose.data").joinpath(f"{name}.json").read_text(encoding="utf-8")
    return json.loads(raw)


def get_rule(rule_id: int):
    """Return a rule with a stable integer ID or raise ValueError."""
    for rule in load("rules")["rules"]:
        if rule["id"] == rule_id:
            return rule
    raise ValueError(f"Rule {rule_id} does not exist (valid range: 1–57)")


def get_workflow(workflow_id: str):
    for item in load("workflows"):
        if item["id"] == workflow_id:
            return item
    raise ValueError(f"Unknown workflow '{workflow_id}'")


def validate_catalog() -> list[str]:
    """Check cross-file integrity. Returns error strings, not a passing grade."""
    issues: list[str] = []
    rules_doc = load("rules")
    rules = rules_doc["rules"]
    ids = [rule.get("id") for rule in rules]
    expected_ids = list(range(1, 58))
    if ids != expected_ids:
        issues.append("Rule IDs must be unique and run consecutively from 1 through 57")
    sections = rules_doc["sections"]
    if len(sections) != 9 or [s.get("id") for s in sections] != list(range(1, 10)):
        issues.append("Exactly nine ordered sections are required")
    for rule in rules:
        for field in ("title", "scope", "standard", "corpus_observation", "review_action", "example"):
            if not isinstance(rule.get(field), str) or not rule[field].strip():
                issues.append(f"Rule {rule.get('id')} lacks {field}")
        if rule.get("section") not in range(1, 10):
            issues.append(f"Rule {rule.get('id')} has an invalid section")
    for section in sections:
        relevant = [r["id"] for r in rules if r["section"] == section["id"]]
        if relevant != section["rule_ids"]:
            issues.append(f"Section {section['id']} has inconsistent rule references")
    ids_set = set(ids)
    for item in load("workflows"):
        if not item["rule_ids"] or not set(item["rule_ids"]).issubset(ids_set):
            issues.append(f"Workflow '{item['id']}' references invalid rules")
    scorecard = load("scorecard")
    criteria = scorecard["criteria"]
    if len(criteria) != 12 or scorecard["maximum"] != 24 or scorecard["threshold"] != 20:
        issues.append("The scorecard must have 12 criteria and a 20/24 review threshold")
    if len({c["id"] for c in criteria}) != 12:
        issues.append("The scorecard contains duplicate IDs")
    for criterion in criteria:
        if not set(criterion["rule_ids"]).issubset(ids_set):
            issues.append(f"Criterion '{criterion['id']}' has invalid rule references")
    for item in scorecard["cross_cutting_checks"]:
        if not set(item["rule_ids"]).issubset(ids_set):
            issues.append("Cross-cutting review references invalid rules")
    corpus = load("corpus")
    if len(corpus) != 12 or len({entry["doi"] for entry in corpus}) != 12:
        issues.append("The reference corpus must contain 12 distinct articles")
    source_ids = [entry.get("id") for entry in corpus]
    if len(set(source_ids)) != 12 or not all(isinstance(x, str) and x for x in source_ids):
        issues.append("Reference corpus needs twelve distinct stable source IDs")
    known = set(source_ids)
    for rule in rules:
        sources = rule.get("example_sources")
        if not isinstance(sources, list) or not sources:
            issues.append(f"Rule {rule.get('id')} is missing example provenance")
        elif len(set(sources)) != len(sources) or not set(sources).issubset(known):
            issues.append(f"Rule {rule.get('id')} has invalid article sources")
    return issues
