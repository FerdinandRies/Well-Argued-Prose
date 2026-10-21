"""Generate complete English documentation from JSON (single source of truth).

Run from any working directory:
    python scripts/build_handbook.py
    python scripts/build_handbook.py --check
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from well_argued_prose.catalog import load, validate_catalog  # noqa: E402


def handbook() -> str:
    data = load("rules")
    lines = [
        "# The Well-Argued Prose Rulebook", "",
        "**57 rules · 9 levels · argument-first scholarly writing**", "",
        "The governing principle is simple: **a concept must earn its place in an argument.** "
        "Precise concepts emerge from actual inferential pressure and continue to perform identifiable work.", "",
        "**Scope.** English-language philosophy, ethics, value theory, and argument-driven normative scholarship; "
        "other disciplines may adapt the standards to their evidence and conventions.", "",
        "**How to read each rule.** *Standard* defines the requirement; *Corpus observation* describes a transferable writing move from the twelve-paper reference corpus; *Review action* supplies an executable inspection; *Example* illustrates its application. These **source-linked examples are newly written editorial paraphrases**, not verbatim excerpts or the original authors' exact sentences. Corpus observations are interpretive, not official journal instructions.", "",
        "## Contents", "",
    ]
    for section in data["sections"]:
        slug = section["name"].lower().replace(" ", "-")
        lines.append(f"- [{section['id']}. {section['name']}](#{section['id']}-{slug}) — Rules {section['rule_ids'][0]}–{section['rule_ids'][-1]}")
    lines += ["", "---", ""]
    source_by_id = {paper["id"]: paper for paper in load("corpus")}
    for section in data["sections"]:
        lines += [f"## {section['id']}. {section['name']}", ""]
        for r in data["rules"]:
            if r["section"] != section["id"]:
                continue
            lines += [
                f'<a id="rule-{r["id"]:02d}"></a>', "",
                f"### Rule {r['id']:02d} — {r['title']}", "",
                f"**Scope:** {r['scope']}", "",
                f"**Standard.** {r['standard']}", "",
                f"**Corpus observation.** {r['corpus_observation']}", "",
                f"**Review action.** {r['review_action']}", "",
                f"**Example.** {r['example']}", "",
                "**Source article(s).** " + "; ".join(
                    f"[{source_by_id[sid]['authors']} ({source_by_id[sid]['year']})]"
                    f"(https://doi.org/{source_by_id[sid]['doi']})"
                    for sid in r['example_sources']
                ), "",
            ]
    lines += ["---", "", "For a task-oriented entry point, see [Workflows](workflows.md). For human review, see the [24-point scorecard](scorecard.md).", ""]
    return "\n".join(lines)


def workflows() -> str:
    lines = ["# Task-Oriented Workflows", "", "Use these sequences as entry points into the rulebook. The numbers are authoritative rule IDs.", ""]
    for item in load("workflows"):
        links = ", ".join(f"[Rule {n}](handbook.md#rule-{n:02d})" for n in item["rule_ids"])
        lines += [f"## {item['title']}", "", f"**Rule sequence:** {links}", "",
                  f"**Completion test:** {item['exit_check']}", ""]
    lines += ["The original one-page index contained several mismatched rule numbers. All numbers here have been checked against the 57-rule catalog.", ""]
    return "\n".join(lines)


def scorecard_doc() -> str:
    s = load("scorecard")
    lines = [
        "# Human Review Scorecard", "",
        "Rate each of the twelve criteria from **0 to 2**: 0 = absent, 1 = present but weak, 2 = clear and operative. "
        "A total below **20/24** calls for further structural revision before the final language pass. "
        "A passing score is an internal workflow threshold and has no statistical relation to journal acceptance.", "",
        "| Criterion | Standard for 2 points | Rules |", "|---|---|---|",
    ]
    for criterion in s["criteria"]:
        lines.append(f"| {criterion['title']} | {criterion['two_point_standard']} | {', '.join(map(str, criterion['rule_ids']))} |")
    lines += ["", "## Mandatory cross-cutting checks", ""]
    for item in s["cross_cutting_checks"]:
        lines.append(f"- **{item['title']} (Rules {', '.join(map(str, item['rule_ids']))}).** {item['instruction']}")
    lines += ["", "## Use in the CLI", "", "```bash", "well-argued-prose scorecard init my-review.json", "# Edit each rating (0, 1, or 2) and enter supporting evidence.", "well-argued-prose scorecard evaluate my-review.json", "```", "", "The ratings are supplied by the reviewer, never invented by the program.", ""]
    return "\n".join(lines)


def corpus_doc() -> str:
    lines = ["# Reference Corpus: Twelve Articles in *Mind*", "", "The rulebook is informed by an interpretive comparison of these essays. "
             "The journal has not endorsed this project, and the derived editorial guidelines are not its formal submission requirements.", "",
             "All references link to the articles' DOI landing pages. Article text is not redistributed.", ""]
    for i, item in enumerate(load("corpus"), 1):
        lines += [f"{i}. **{item['authors']} ({item['year']}).** [{item['title']}](https://doi.org/{item['doi']}). *{item['journal']}*.  ",
                  f"   **Transferable move:** {item['writing_move']}", ""]
    return "\n".join(lines)


def example_sources_doc() -> str:
    """A rule-by-rule bibliography mapping, without reproducing article text."""
    rules = load("rules")["rules"]
    papers = {item["id"]: item for item in load("corpus")}
    lines = [
        "# Published-Article Example Sources", "",
        "Each of the 57 rule-level examples is an **original editorial reconstruction** grounded in "
        "a published *Mind* paper, not a quotation from the author's manuscript. "
        "The DOI links point to the original publication. No article text is redistributed here.", "",
        "| Rule | Supporting *Mind* paper(s) |", "|---|---|",
    ]
    for rule in rules:
        refs = "; ".join(
            f"[{papers[sid]['authors']} ({papers[sid]['year']})](https://doi.org/{papers[sid]['doi']})"
            for sid in rule["example_sources"]
        )
        lines.append(f"| [Rule {rule['id']:02d}](handbook.md#rule-{rule['id']:02d}) | {refs} |")
    lines += ["", "See the [reference corpus](corpus.md) for titles and the "
              "[editorial notes](source-notes.md) for limits on interpretation.", ""]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Fail if generated files are out of sync")
    args = ap.parse_args()
    problems = validate_catalog()
    if problems:
        raise SystemExit("Invalid catalog: " + "; ".join(problems))
    output = {
        "handbook.md":handbook(),
        "workflows.md":workflows(),
        "scorecard.md":scorecard_doc(),
        "corpus.md":corpus_doc(),
        "example-sources.md":example_sources_doc(),
    }
    for name, content in output.items():
        path = ROOT / "docs" / name
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                print(f"Out of date: {path}", file=sys.stderr)
                return 1
        else:
            path.write_text(content, encoding="utf-8")
            print(f"Wrote {path.relative_to(ROOT)}")
    if args.check:
        print("Generated documentation matches catalog.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
