"""The Well-Argued Prose command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from . import __version__
from .catalog import get_rule, get_workflow, load, validate_catalog
from .review import audit_text, read_manuscript
from .scoring import evaluate, make_template


def _dump(data) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="well-argued-prose", description="Argument-first standards for advanced scholarly writing."
    )
    parser.add_argument("--version", action="version", version=f"well-argued-prose {__version__}")
    subs = parser.add_subparsers(dest="command", required=True)
    sub_list = subs.add_parser("list", help="Show all 57 rules grouped by section")
    sub_list.add_argument("--section", type=int, choices=range(1, 10), metavar="1-9")

    sub_show = subs.add_parser("show", help="Show the complete text of one rule")
    sub_show.add_argument("rule_id", type=int)
    sub_show.add_argument("--json", action="store_true")

    sub_guide = subs.add_parser("guide", help="Show a task-specific rule sequence")
    sub_guide.add_argument("task", nargs="?", help="Name of workflow; omit to list workflows")
    sub_guide.add_argument("--json", action="store_true")

    sub_audit = subs.add_parser("audit", help="Advisory surface checks on a manuscript")
    sub_audit.add_argument("path", type=Path, help=".md, .txt, or .docx manuscript")
    sub_audit.add_argument("--json", action="store_true")
    sub_audit.add_argument("--max-per-check", type=int, default=10)

    sub_score = subs.add_parser("scorecard", help="Create or evaluate a human-scored 24-point checklist")
    score_subs = sub_score.add_subparsers(dest="score_command", required=True)
    sub_init = score_subs.add_parser("init", help="Create a scorecard JSON file with blank ratings")
    sub_init.add_argument("path", type=Path)
    sub_init.add_argument("--force", action="store_true", help="Overwrite an existing file")
    sub_eval = score_subs.add_parser("evaluate", help="Evaluate a manually completed scorecard")
    sub_eval.add_argument("path", type=Path)
    sub_eval.add_argument("--json", action="store_true")

    subs.add_parser("validate", help="Check catalog IDs, references, and schema")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "list":
            catalog = load("rules")
            for section in catalog["sections"]:
                if args.section and section["id"] != args.section:
                    continue
                print(f"\n{section['id']}. {section['name']}")
                for rule in catalog["rules"]:
                    if rule["section"] == section["id"]:
                        print(f"  {rule['id']:02d}  {rule['title']}")
            return 0

        if args.command == "show":
            rule = get_rule(args.rule_id)
            if args.json:
                _dump(rule)
            else:
                print(f"Rule {rule['id']}: {rule['title']}")
                for label, key in (
                    ("Scope", "scope"), ("Standard", "standard"),
                    ("Corpus observation", "corpus_observation"),
                    ("Review action", "review_action"), ("Example", "example")
                ):
                    print(f"\n{label}: {rule[key]}")
                articles = {entry["id"]: entry for entry in load("corpus")}
                print("\nSource article(s):")
                for source_id in rule["example_sources"]:
                    paper = articles[source_id]
                    print(f"  {paper['authors']} ({paper['year']}), {paper['title']}; "
                          f"https://doi.org/{paper['doi']}")
                print("Examples are original editorial paraphrases, not verbatim quotations.")
            return 0

        if args.command == "guide":
            if not args.task:
                for workflow in load("workflows"):
                    print(f"{workflow['id']:<14} {workflow['title']}")
                return 0
            workflow = get_workflow(args.task)
            if args.json:
                _dump(workflow)
            else:
                print(workflow["title"])
                for number in workflow["rule_ids"]:
                    print(f"  {number:02d} {get_rule(number)['title']}")
                print(f"\nReview criterion: {workflow['exit_check']}")
            return 0

        if args.command == "audit":
            text, unit = read_manuscript(args.path)
            result = audit_text(text, unit=unit, max_per_check=args.max_per_check)
            result["file"] = str(args.path)
            if args.json:
                _dump(result)
            else:
                print(f"Advisory audit: {args.path} ({unit} references)")
                for row in result["checks"]:
                    print(f"\n{row['title']}: {row['total_matches']} match(es) [rules {', '.join(map(str, row['rule_ids']))}]")
                    print(f"  {row['reason']}")
                    for item in row["examples"]:
                        print(f"  {unit} {item[unit]}: {item['context']}")
                print(f"\n{result['disclaimer']}")
            return 0

        if args.command == "scorecard":
            if args.score_command == "init":
                if args.path.exists() and not args.force:
                    raise ValueError(f"Refusing to overwrite {args.path}; use --force")
                args.path.parent.mkdir(parents=True, exist_ok=True)
                args.path.write_text(json.dumps(make_template(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                print(f"Blank human scorecard created: {args.path}")
                return 0
            if args.score_command == "evaluate":
                result = evaluate(json.loads(args.path.read_text(encoding="utf-8")))
                if args.json:
                    _dump(result)
                else:
                    print(f"Human score: {result['score']}/{result['out_of']}")
                    print(result["verdict"])
                    print(result["caveat"])
                return 0

        if args.command == "validate":
            issues = validate_catalog()
            if issues:
                for issue in issues:
                    print(f"ERROR: {issue}", file=sys.stderr)
                return 1
            print("Catalog valid: 57 rules, 9 sections, 10 workflows, 12 scorecard criteria, 12 corpus articles.")
            return 0

    except (ValueError, KeyError, json.JSONDecodeError, OSError) as exc:
        print(f"well-argued-prose: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
