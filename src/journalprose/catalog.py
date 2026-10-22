"""Read and validate the public editorial catalog.

No unpublished material or external source collection is loaded at runtime.
"""
from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
from importlib import resources
import json
import re
from typing import Any

from . import __version__

NAMES = frozenset({"rules", "workflows", "checks", "checklist"})


@lru_cache(maxsize=4)
def _read(name: str) -> dict[str, Any]:
    if name not in NAMES:
        raise ValueError(f"Unknown catalog: {name}")
    content = resources.files("journalprose.data").joinpath(name + ".json").read_text(encoding="utf-8")
    result = json.loads(content)
    if not isinstance(result, dict):
        raise ValueError(f"Catalog {name} must contain an object")
    return result


def load(name: str) -> dict[str, Any]:
    """Return an independent copy; callers cannot mutate the cached catalog."""
    return deepcopy(_read(name))


def get_rule(rule_id: str) -> dict[str, Any]:
    if not isinstance(rule_id, str) or not re.fullmatch(r"JP2-\d{3}", rule_id):
        raise ValueError("Use a v0.2 rule ID such as JP2-033. Legacy numeric IDs are not interchangeable.")
    for rule in load("rules")["rules"]:
        if rule["id"] == rule_id:
            return rule
    raise ValueError(f"Unknown rule: {rule_id}")


def get_workflow(name: str) -> dict[str, Any]:
    for workflow in load("workflows")["workflows"]:
        if workflow["id"] == name:
            return workflow
    raise ValueError(f"Unknown workflow: {name}")


def validate_catalog(documents: dict[str, Any] | None = None) -> list[str]:
    """Validate shape, references, example provenance, and configured patterns.

    Validation concerns catalog integrity, never the soundness of a manuscript.
    """
    docs = {name: load(name) for name in NAMES} if documents is None else documents
    issues: list[str] = []
    if not isinstance(docs, dict) or set(docs) != NAMES:
        return ["Exactly rules, workflows, checks, and checklist catalogs are required"]
    for name, doc in docs.items():
        if not isinstance(doc, dict) or type(doc.get("schema_version")) is not int or doc["schema_version"] != 2:
            issues.append(f"{name}: schema_version must be 2")
    if issues:
        return issues
    document = docs["rules"]
    if document.get("version") != __version__:
        issues.append("Rule catalog and software version differ")
    if document.get("maintainer") != "FerdinandRies":
        issues.append("Rule catalog maintainer is missing or inconsistent")
    rules = document.get("rules")
    levels = document.get("levels")
    if not isinstance(rules, list) or not all(isinstance(r, dict) for r in rules):
        return issues + ["rules must be a list of rule objects"]
    expected = [f"JP2-{n:03d}" for n in range(1, 51)]
    ids = [r.get("id") for r in rules]
    if ids != expected:
        issues.append("The Core edition requires the ordered IDs JP2-001 through JP2-050")
    known = set(expected)
    if not isinstance(levels, list) or not all(isinstance(x, dict) for x in levels):
        return issues + ["levels must be a list of level objects"]
    if [x.get("id") for x in levels] != [f"L{i}" for i in range(8)]:
        issues.append("The Core edition requires levels L0 through L7")
    level_ids = {x.get("id") for x in levels if isinstance(x.get("id"), str)}

    def nonempty(value: Any) -> bool:
        return isinstance(value, str) and bool(value.strip())

    def references(value: Any, label: str, allow_empty: bool = False) -> None:
        if not isinstance(value, list) or not all(isinstance(x, str) for x in value):
            issues.append(f"{label}: expected a list of rule IDs")
        elif (not value and not allow_empty) or len(value) != len(set(value)) or not set(value) <= known:
            issues.append(f"{label}: missing, duplicate, or unknown rule reference")

    for rule in rules:
        tag = rule.get("id", "unknown")
        required = {"id", "level", "title", "standard", "check", "repair", "example", "related_rules", "automation"}
        if set(rule) != required:
            issues.append(f"{tag}: unexpected or missing rule fields")
        for key in ("title", "standard", "check", "repair"):
            if not nonempty(rule.get(key)):
                issues.append(f"{tag}: missing {key}")
        if not isinstance(rule.get("level"), str) or rule["level"] not in level_ids:
            issues.append(f"{tag}: invalid level")
        example = rule.get("example")
        if not isinstance(example, dict) or set(example) != {"status", "before", "after", "explanation"}:
            issues.append(f"{tag}: example must have status, before, after, and explanation")
        elif example.get("status") != "invented" or not all(nonempty(example.get(k)) for k in ("before", "after", "explanation")):
            issues.append(f"{tag}: incomplete invented example")
        references(rule.get("related_rules"), str(tag), allow_empty=True)
        if isinstance(rule.get("related_rules"), list) and tag in rule["related_rules"]:
            issues.append(f"{tag}: self-reference is unnecessary")
        if not isinstance(rule.get("automation"), str) or rule["automation"] not in {"human", "advisory", "pattern"}:
            issues.append(f"{tag}: invalid automation label")
    for level in levels:
        references(level.get("rule_ids"), f"Level {level.get('id')}")
        actual = [r.get("id") for r in rules if r.get("level") == level.get("id")]
        if level.get("rule_ids") != actual:
            issues.append(f"Level {level.get('id')}: rule membership differs")
        if not nonempty(level.get("title")):
            issues.append("Level title is missing")
    for catalog, key in (("workflows", "workflows"), ("checks", "checks"), ("checklist", "criteria")):
        entries = docs[catalog].get(key)
        if not isinstance(entries, list) or not entries or not all(isinstance(x, dict) for x in entries):
            issues.append(f"{catalog}: entries must be a nonempty list of objects")
            continue
        entry_ids = [x.get("id") for x in entries]
        if not all(nonempty(x) for x in entry_ids) or len(entry_ids) != len(set(map(str, entry_ids))):
            issues.append(f"{catalog}: invalid or duplicate entry IDs")
        for entry in entries:
            label = f"{catalog}/{entry.get('id')}"
            references(entry.get("rule_ids"), label)
            if not nonempty(entry.get("title")):
                issues.append(f"{label}: missing title")
            if catalog == "workflows" and not nonempty(entry.get("completion")):
                issues.append(f"{label}: missing completion condition")
            if catalog == "checks":
                engine = entry.get("engine")
                if not isinstance(engine, str) or engine not in {"regex", "citation_cluster", "citation_size", "citation_density", "author_parade"}:
                    issues.append(f"{label}: unknown engine")
                if not isinstance(entry.get("kind"), str) or entry["kind"] not in {"policy", "advisory"}:
                    issues.append(f"{label}: invalid check kind")
                if not nonempty(entry.get("message")):
                    issues.append(f"{label}: missing message")
                if engine == "regex":
                    try:
                        pattern = entry.get("pattern")
                        if not nonempty(pattern):
                            raise ValueError("empty pattern")
                        compiled = re.compile(pattern, re.IGNORECASE)
                        if compiled.search(""):
                            raise ValueError("pattern matches empty input")
                    except (re.error, TypeError, ValueError) as exc:
                        issues.append(f"{label}: invalid pattern ({exc})")
    if docs["checklist"].get("statuses") != ["not_reviewed", "pass", "revise", "not_applicable"]:
        issues.append("Checklist status vocabulary is inconsistent")
    return issues
