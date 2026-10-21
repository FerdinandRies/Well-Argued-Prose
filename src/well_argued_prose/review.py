"""Transparent lexical prompts for *human* editorial review.

A match is a place to inspect, never an automatic declaration of an error.
The program does not parse logic, judge conceptual novelty, or verify citations.
"""

from __future__ import annotations

from bisect import bisect_right
from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Check:
    code: str
    title: str
    rule_ids: tuple[int, ...]
    pattern: str
    why: str


CHECKS = (
    Check("generic-purpose", "Generic statement of purpose", (1, 3, 42, 49),
          r"\b(?:this (?:paper|article|study) (?:aims? to |seeks? to )?(?:discuss|explore|provide (?:a |an )?(?:comprehensive|nuanced) (?:account|framework|discussion))\b|the purpose of this (?:paper|article) is to discuss\b)",
          "Check whether the sentence advances a research problem or only announces a topic."),
    Check("self-praise", "Unexplained evaluative language", (39, 46, 49, 56),
          r"\b(?:groundbreaking|revolutionary|profound|highly important|unprecedented|comprehensive and nuanced)\b",
          "Replace self-appraisal with a stated condition, mechanism, or result when appropriate."),
    Check("negative-pivot", "Possible formulaic negative contrast", (41, 56),
          r"\b(?:is|are|was|were)\s+not\b[^.?!;\n]{0,95}\bbut\b",
          "A contrast is legitimate if it excludes a real alternative; otherwise state the positive relations."),
    Check("inferential-connective", "Strong inferential connective", (37, 45, 55),
          r"\b(?:therefore|thus|hence|accordingly)\b",
          "Find the intermediate premise that actually supports the announced inference."),
    Check("unclear-demonstrative", "Potentially unclear demonstrative", (20, 39, 55),
          r"\b(?:this|that)\s+(?:structure|framework|process|approach|problem|relationship|account|result)\b",
          "Confirm that the demonstrative has an explicit, unique antecedent."),
)


def read_manuscript(path: Path) -> tuple[str, str]:
    """Return (text, unit). Units are source lines or DOCX paragraphs."""
    if not path.exists() or not path.is_file():
        raise ValueError(f"File does not exist: {path}")
    extension = path.suffix.lower()
    if extension in (".txt", ".md"):
        try:
            return path.read_text(encoding="utf-8-sig"), "line"
        except UnicodeDecodeError as exc:
            raise ValueError("Text files must be UTF-8 encoded") from exc
    if extension == ".docx":
        try:
            from docx import Document
        except ImportError as exc:
            raise ValueError('DOCX requires: pip install "well-argued-prose[docx]"') from exc
        try:
            paragraphs = [p.text for p in Document(path).paragraphs]
        except Exception as exc:
            raise ValueError(f"Could not read DOCX: {exc}") from exc
        return "\n".join(paragraphs), "paragraph"
    raise ValueError("Supported manuscript types: .md, .txt, .docx")


def audit_text(text: str, unit: str = "line", max_per_check: int = 10) -> dict:
    """Run deterministic regex checks; no quality score is computed."""
    if max_per_check < 1:
        raise ValueError("max_per_check must be at least 1")
    offsets = [-1] + [idx for idx, char in enumerate(text) if char == "\n"]
    lines = text.split("\n")
    rows: list[dict] = []
    for check in CHECKS:
        matches = list(re.finditer(check.pattern, text, flags=re.IGNORECASE))
        items = []
        for match in matches[:max_per_check]:
            position = bisect_right(offsets, match.start())
            sample = lines[position - 1].strip()
            if len(sample) > 220:
                start = max(0, match.start() - (offsets[position - 1] + 1) - 55)
                sample = sample[start:start + 220].strip()
            items.append({unit: position, "match": match.group(0), "context": sample})
        rows.append({"code":check.code, "title":check.title, "rule_ids":list(check.rule_ids),
                     "reason":check.why, "total_matches":len(matches), "examples":items})
    return {"kind":"advisory-language-audit", "unit":unit, "checks":rows,
            "disclaimer":"Flags are prompts for human review, not proven errors or a quality/acceptance score."}
