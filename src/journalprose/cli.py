"""Command-line access to rules, surface review, and human review records."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any

from . import __version__
from .catalog import get_rule, get_workflow, load, validate_catalog
from .checklist import evaluate, make_template
from .review import audit_text, read_manuscript


def dump(value: Any) -> None:
    print(json.dumps(value, ensure_ascii=True, indent=2))


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="journalprose", description="Advanced scholarly writing standards and local review tools.")
    p.add_argument("--version", action="version", version=f"journalprose {__version__}")
    subs = p.add_subparsers(dest="command", required=True)
    ls = subs.add_parser("list", help="List the 50 public rules")
    ls.add_argument("--level", choices=[f"L{i}" for i in range(8)])
    ls.add_argument("--json", action="store_true")
    show = subs.add_parser("show", help="Read one rule, such as JP2-033")
    show.add_argument("rule_id")
    show.add_argument("--json", action="store_true")
    guide = subs.add_parser("guide", help="List workflows or show one task sequence")
    guide.add_argument("task", nargs="?")
    guide.add_argument("--json", action="store_true")
    audit = subs.add_parser("audit", help="Flag surface patterns for human review; never rewrite input")
    audit.add_argument("path", type=Path)
    audit.add_argument("--json", action="store_true")
    audit.add_argument("--max-per-check", type=int, default=10)
    audit.add_argument("--include-references", action="store_true", help="Include Markdown bibliography sections")
    audit.add_argument("--fail-on", choices=["none", "policy", "any"], default="none",
                       help="Optional match-based exit policy; no assessment of manuscript quality")
    ck = subs.add_parser("checklist", help="Create or evaluate an evidence-backed human review record")
    csubs = ck.add_subparsers(dest="check_command", required=True)
    init = csubs.add_parser("init", help="Write an unreviewed checklist")
    init.add_argument("path", type=Path)
    init.add_argument("--force", action="store_true")
    ev = csubs.add_parser("evaluate", help="Check a reviewer-completed record")
    ev.add_argument("path", type=Path)
    ev.add_argument("--json", action="store_true")
    ev.add_argument("--require-complete", action="store_true")
    subs.add_parser("validate", help="Validate the public catalog and cross-references")
    return p


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        if args.command == "list":
            doc = load("rules")
            rules = [r for r in doc["rules"] if args.level is None or r["level"] == args.level]
            if args.json:
                dump(rules)
            else:
                for level in doc["levels"]:
                    if args.level is not None and args.level != level["id"]:
                        continue
                    print(f"\n{level['id']} - {level['title']}")
                    for rule in rules:
                        if rule["level"] == level["id"]:
                            print(f"  {rule['id']}  {rule['title']}")
            return 0
        if args.command == "show":
            rule = get_rule(args.rule_id)
            if args.json:
                dump(rule)
            else:
                print(f"{rule['id']} - {rule['title']}")
                for key in ("standard", "check", "repair"):
                    print(f"\n{key.title()}: {rule[key]}")
                print("\nInvented example")
                for key in ("before", "after", "explanation"):
                    print(f"{key.title()}: {rule['example'][key]}")
                print("\nRelated: " + ", ".join(rule["related_rules"]))
            return 0
        if args.command == "guide":
            if args.task:
                workflow = get_workflow(args.task)
                if args.json:
                    dump(workflow)
                else:
                    print(workflow["title"])
                    for rule_id in workflow["rule_ids"]:
                        print(f"  {rule_id} {get_rule(rule_id)['title']}")
                    print("\nCompletion: " + workflow["completion"])
            elif args.json:
                dump(load("workflows")["workflows"])
            else:
                for workflow in load("workflows")["workflows"]:
                    print(f"{workflow['id']:<13} {workflow['title']}")
            return 0
        if args.command == "audit":
            text, unit = read_manuscript(args.path)
            result = audit_text(text, unit=unit, max_per_check=args.max_per_check,
                                markdown=args.path.suffix.lower() == ".md", include_references=args.include_references)
            result["file"] = str(args.path)
            if args.json:
                dump(result)
            else:
                print(f"Surface review: {args.path}")
                print(f"{result['check_count']} checks; {result['total_matches']} matches; {unit} locations.")
                for item in result["checks"]:
                    if item["total_matches"]:
                        print(f"\n{item['id']} [{item['kind']}] - {item['total_matches']} matches")
                        for match in item["examples"]:
                            print(f"  {match['line']}:{match['column']} {match['match'].replace(chr(10), ' ')}")
                        print("  " + item["message"])
                        if item["truncated"]:
                            print("  Displayed examples are truncated; the total count includes all matches.")
                print("\n" + result["limitations"])
            if args.fail_on == "policy" and result["policy_matches"]:
                return 1
            if args.fail_on == "any" and result["total_matches"]:
                return 1
            return 0
        if args.command == "checklist":
            if args.check_command == "init":
                mode = "w" if args.force else "x"
                with args.path.open(mode, encoding="utf-8") as stream:
                    json.dump(make_template(), stream, ensure_ascii=True, indent=2)
                    stream.write("\n")
                print(f"Wrote unreviewed checklist: {args.path}")
                return 0
            if args.path.stat().st_size > 2 * 1024 * 1024:
                raise ValueError("Checklist exceeds the 2 MiB size limit")
            result = evaluate(json.loads(args.path.read_text(encoding="utf-8-sig")))
            if args.json:
                dump(result)
            else:
                print(result["status"])
                for status, count in result["counts"].items():
                    print(f"  {status}: {count}")
                print(result["limitations"])
            return 1 if args.require_complete and not result["complete"] else 0
        if args.command == "validate":
            issues = validate_catalog()
            if issues:
                for issue in issues:
                    print(issue, file=sys.stderr)
                return 1
            print("Catalog valid: 50 rules, 8 levels, 6 workflows, 21 surface checks.")
            return 0
        raise ValueError("Unknown command")
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"journalprose: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
