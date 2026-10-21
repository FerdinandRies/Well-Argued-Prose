# Usage Guide

Well-Argued Prose can be used in four ways: as a **rulebook** you read and cite, as a **command-line toolkit** that operationalizes the rules, as a **prompt set** for working with an AI writing assistant, and as a **human review protocol** for structured editorial assessment. This guide covers all four.

## 1. Read the rulebook

Start with the [complete handbook](handbook.md). Each of the 57 rules states a *Standard*, a *Corpus observation* drawn from twelve published *Mind* articles, an executable *Review action*, and a worked *Example* reconstructed from a published argument. Every example can be traced to its source paper through the [example source map](example-sources.md).

If you are working on a specific part of a manuscript, do not read the handbook cover to cover. Use the [task workflows](workflows.md) — or `well-argued-prose guide` below — to get the rule sequence for your task.

## 2. Use the command-line toolkit

### Install

Requires Python 3.10 or newer. From a clone of this repository:

```bash
python -m pip install -e .
```

For Microsoft Word (`.docx`) support:

```bash
python -m pip install -e ".[docx]"
```

Everything runs locally. No external service is contacted, and no manuscript leaves your machine.

### Commands

**List the rules**, grouped by section:

```bash
well-argued-prose list
well-argued-prose list --section 3
```

**Read one rule in full** (Standard, corpus observation, review action, example, sources):

```bash
well-argued-prose show 37
well-argued-prose show 37 --json
```

**Get a task workflow.** With no argument, the command lists the ten available workflows (abstract, introduction, literature, theory, cases, objections, paragraph, sentence, diction, submission):

```bash
well-argued-prose guide
well-argued-prose guide introduction
```

**Run an advisory audit** on a manuscript in Markdown, plain text, or (with the optional dependency) Word format:

```bash
well-argued-prose audit path/to/manuscript.md
well-argued-prose audit path/to/manuscript.md --json --max-per-check 5
```

The audit flags passages for human inspection — for example generic statements of purpose, unexplained evaluative language, or formulaic negative contrasts — and names the rules each flag answers to. It does not validate arguments, verify scholarship, rewrite prose, or predict publication outcomes. A clean audit is not evidence that a manuscript is good; it is evidence that a fixed set of surface patterns was not found.

**Use the review scorecard** (see §4 below):

```bash
well-argued-prose scorecard init my-review.json
# Edit my-review.json: enter a rating (0, 1, or 2) and supporting evidence for each criterion.
well-argued-prose scorecard evaluate my-review.json
```

**Validate the catalog** (for contributors and anyone who edits the JSON data):

```bash
well-argued-prose validate
python scripts/build_handbook.py --check
python -m unittest discover -s tests -v
```

The module form `python -m well_argued_prose <command>` is equivalent to the `well-argued-prose` entry point throughout.

## 3. Use the AI revision prompts

Two prompt templates apply the rulebook with an AI writing assistant:

- [Manuscript revision prompt](../prompts/manuscript-revision.md) — a rule-governed revision pass over a draft.
- [Pre-submission review prompt](../prompts/pre-submission-review.md) — a final argument-first review before submission.

Paste the prompt together with your text. The prompts instruct the assistant to diagnose before rewriting, to preserve your concepts and theoretical commitments, and to report changes rule by rule. Treat the output as editorial advice to be judged, not as corrections to be accepted automatically.

## 4. Run a human review

The [review protocol](review-protocol.md) sequences a full editorial review: secure the central claim and inferential structure first, then work through definitions, cases, and objections, and only then revise diction. The [scorecard](scorecard.md) operationalizes the protocol as twelve criteria rated 0–2, for a maximum of 24 points:

1. Create a blank scorecard with `well-argued-prose scorecard init`.
2. A human reviewer reads the manuscript and enters one rating plus supporting evidence per criterion.
3. Run `well-argued-prose scorecard evaluate` to total the score. A total below 20/24 calls for further structural revision before the final language pass.

Ratings and evidence must come from the reviewer. The program never invents them, and the total is an internal workflow threshold — it has no statistical relation to journal acceptance.

## A typical revision session

1. `well-argued-prose guide introduction` — get the rule sequence for the section you are revising.
2. `well-argued-prose show <id>` — read each rule in full as you apply it.
3. `well-argued-prose audit draft.md` — catch the surface patterns the rules warn about.
4. Work through the [review protocol](review-protocol.md) for the structural pass.
5. Score the revised draft with the scorecard, and keep the completed JSON with the manuscript as a review record.
