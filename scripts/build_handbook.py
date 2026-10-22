"""Generate the handbook, workflows, checklist, and coverage from public JSON."""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from journalprose.catalog import load, validate_catalog


def rule_link(rule_id: str) -> str:
    return f"[{rule_id}](handbook.md#{rule_id.lower()})"


def handbook() -> str:
    doc = load("rules")
    lines = ["# JournalProse", "", "## Advanced Scholarly Writing Standards", "",
             "**Core edition | v0.2.0 | FerdinandRies**", "",
             "50 rules in eight levels for rigorous reasoning, precise academic English, and natural scholarly prose.", "",
             "## How to use the core", "",
             "Identify the text and authorized task. Review meaning and support before changing substantive prose. "
             "Use the task workflows to select relevant rules. Language-only work remains within its agreed scope.", "",
             "Each rule states a standard, an inspection, a repair, and an invented worked example. "
             "The examples are teaching material: their names, dates, quantities, and studies make no claims "
             "about actual publications or events. Examples are licensed as project editorial content.", "",
             "The house style excludes specified rhetorical contrast templates, citation piles, mechanical author "
             "parades, empty contribution claims, and writing-process announcements. Necessary logical negation, "
             "exact quotations, formulas, and fixed technical expressions retain their meaning. "
             "An exception requires contextual review and a recorded reason.", "",
             "The style rules apply to authored manuscript prose. Diagnostic examples and descriptions of "
             "prohibited patterns necessarily display those patterns. Rulebook tables and review checklists "
             "serve documentation functions; they are not manuscript prose templates.", "",
             "A concept's complexity alone is no reason to replace it. A revision must preserve the author's "
             "claims, terms, scope, and supported force. During compression, protect the inferential chain, "
             "concept criteria, test cases, objection replies, and detailed source reconstructions.", "",
             "The CLI offers surface candidates for review. Basic reasoning, full grammar, source accuracy, "
             "and semantic retention require human judgment. No scan or checklist certifies publication readiness.", "",
             "## Levels", "", "| Level | Focus | Rules |", "|---|---|---|"]
    for level in doc["levels"]:
        ids = level["rule_ids"]
        lines.append(f"| {level['id']} | {level['title']} | {ids[0]} to {ids[-1]} |")
    for level in doc["levels"]:
        lines += ["", f"## {level['id']} - {level['title']}", ""]
        for rule in doc["rules"]:
            if rule["level"] != level["id"]:
                continue
            lines += [f'<a id="{rule["id"].lower()}"></a>', "", f"### {rule['id']} - {rule['title']}", ""]
            for label, key in (("Standard", "standard"), ("Check", "check"), ("Repair", "repair")):
                lines += [f"**{label}.** {rule[key]}", ""]
            lines += ["**Invented example**", "", f"**Before:** {rule['example']['before']}", "",
                      f"**After:** {rule['example']['after']}", "",
                      f"**Why:** {rule['example']['explanation']}", "",
                      "**Related rules:** " + ", ".join(f"[{i}](#{i.lower()})" for i in rule["related_rules"]), ""]
    lines += ["---", "", "[Workflows](workflows.md) | [Human checklist](checklist.md) | [Software coverage](checks.md)", ""]
    return "\n".join(lines)


def workflows() -> str:
    lines = ["# Task workflows", "", "Select the task before editing. These sequences identify relevant rules; "
             "they do not authorize an expanded editing scope.", ""]
    for item in load("workflows")["workflows"]:
        lines += [f"## {item['title']}", "", f"CLI task: `{item['id']}`", "",
                  "**Sequence:** " + ", ".join(rule_link(x) for x in item["rule_ids"]), "",
                  "**Completion:** " + item["completion"], ""]
    return "\n".join(lines)


def checklist_doc() -> str:
    lines = ["# Human review checklist", "",
             "This checklist records a reviewer's decisions with evidence. It has no aggregate score or acceptance threshold.", "",
             "| Criterion | Rules |", "|---|---|"]
    for criterion in load("checklist")["criteria"]:
        lines.append(f"| {criterion['title']} | {', '.join(rule_link(i) for i in criterion['rule_ids'])} |")
    lines += ["", "## Record a decision", "",
              "`not_reviewed` means no decision has been recorded. `pass` requires textual evidence. "
              "`revise` requires evidence and a note explaining the repair. `not_applicable` requires "
              "a reason tied to the agreed task. Baseline scope and final disposition must be reviewed.", "",
              "A single `revise` status keeps the record in `needs-revision`. An unreviewed item keeps it "
              "incomplete. `recorded-review-complete` means that the required reviewer entries are present "
              "and none requests revision; the program has not independently verified those entries.", "",
              "```bash", "journalprose checklist init my-review.json",
              "# Fill in manuscript, reviewer, task_scope, decisions, and evidence.",
              "journalprose checklist evaluate my-review.json --json",
              "journalprose checklist evaluate my-review.json --require-complete", "```", "",
              "Store review records outside the public repository. A new template contains no pre-filled passes.", ""]
    return "\n".join(lines)


def coverage() -> str:
    checks = load("checks")["checks"]
    rules = load("rules")["rules"]
    lines = ["# Software coverage and limits", "",
             "The 50-rule handbook and the 21 surface checks have different scopes. A lexical match "
             "identifies a passage to inspect. The program performs no rewriting, AI-authorship "
             "determination, proof validation, source verification, or publication prediction.", "",
             "## Implemented checks", "", "| Check | Kind | Rules |", "|---|---|---|"]
    for c in checks:
        lines.append(f"| `{c['id']}`: {c['title']} | {c['kind']} | {', '.join(rule_link(i) for i in c['rule_ids'])} |")
    lines += ["", "`policy` marks a configured house-style match. `advisory` marks a possible issue "
              "that depends on context. Both need interpretation; a quoted expression can legitimately "
              "contain a prohibited pattern. The optional failure exit policy operates on raw match counts.", "",
              "## Rule-by-rule coverage", "", "| Rule | Automated candidate checks | Human review |", "|---|---|---|"]
    for rule in rules:
        related = [f"`{c['id']}`" for c in checks if rule["id"] in c["rule_ids"]]
        lines.append(f"| {rule_link(rule['id'])} | {', '.join(related) if related else 'None'} | Required |")
    lines += ["", "## Interpretation limits", "",
              "Citation checks recognize common author-year forms and numeric reference lists. They count "
              "distinct work labels, with a multi-author work treated as one source position. They cannot "
              "reliably distinguish every citation style, resolve a full bibliography, or determine whether "
              "two sources perform the same argumentative function. Numeric ranges longer than 200 are not expanded.", "",
              "The agreement and countability checks cover narrow patterns. The complete grammar rules "
              "remain a human review task. Mechanical triads, paragraph symmetry, conceptual precision, "
              "actual inferential validity, unsupported comparisons, and semantic loss during compression "
              "cannot be certified by this scanner.", "",
              "Text inside Markdown code and block quotations is skipped. Headed bibliography sections "
              "are skipped by default. Inline prose quotation contexts and complex document structures "
              "require manual inspection. Read [formats](formats.md) for input and location details.", "",
              "No corpus-level precision or recall estimate is claimed. Regression tests demonstrate the "
              "recorded examples and software behavior; they do not establish general linguistic accuracy.", ""]
    return "\n".join(lines)


def outputs() -> dict[str, str]:
    return {"handbook.md": handbook(), "workflows.md": workflows(),
            "checklist.md": checklist_doc(), "checks.md": coverage()}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true")
    args = p.parse_args()
    errors = validate_catalog()
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    failed = []
    for name, text in outputs().items():
        path = ROOT / "docs" / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != text:
                failed.append(name)
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
            print("Wrote docs/" + name)
    if failed:
        print("Out-of-date documentation: " + ", ".join(failed), file=sys.stderr)
        return 1
    if args.check:
        print("All generated documentation matches the public catalogs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
