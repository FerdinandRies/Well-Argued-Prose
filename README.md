# Well-Argued Prose

**Argument-first standards for top-tier scholarly writing.**

> Most writing tools check your sentences. Top-tier journals judge your arguments.

Every existing checker works at the surface: passive voice, weasel words, clichés, house style. Prompt collections hand you templates. Neither touches the layer where manuscripts actually succeed or fail at journals such as *Mind*: whether the central claim is load-bearing, whether a concept is defined by the work it does, whether the strongest objection is met where it belongs, whether each paragraph performs one argumentative move and no more.

**Well-Argued Prose is the first open-source framework built for that layer** — and the first to combine all four of the following in a single system:

## What is new here

1. **Argument-level rules, not sentence-level tips.** Fifty-seven rules across nine levels govern how an opening creates pressure, how a core concept earns a structural definition, how cases and citations are made to work, where objections must enter, and how a conclusion states what the field can now judge differently. Every rule pairs a *Standard* with an executable *Review action*.
2. **Corpus-grounded, not impressionistic.** Each rule is anchored in a comparative study of **12 published articles in *Mind***, and each worked example is an original editorial reconstruction of a real published argument, linked to its source by DOI. A complete [provenance map](docs/example-sources.md) lets any reader trace every example back to the paper it reconstructs.
3. **A rulebook engineered like software.** The rules live in a versioned, machine-readable JSON catalog — the single source of truth. The handbook is generated from that catalog and consistency-checked against it; a Python CLI browses rules, runs advisory audits, and validates the catalog; a unit-test suite guards the whole system.
4. **A formal human review protocol.** A 12-criterion, **24-point scorecard** turns "revise the prose" into an evidence-backed editorial procedure. Ratings are supplied by human reviewers, never invented by the program.

The guiding principle: **a concept must earn its place in an argument.**

The initial emphasis is philosophy, ethics, and argument-driven humanities and social-science scholarship.

## What's included

- A complete [57-rule English handbook](docs/handbook.md) with review actions and **source-linked examples based on published *Mind* arguments**.
- [Task-based workflows](docs/workflows.md) for abstracts, introductions, arguments, cases, objections, and revision.
- A [12-criterion, 24-point human scorecard](docs/scorecard.md).
- A local Python CLI for browsing rules, advisory prose checks, and scorecard handling.
- A linked [reference corpus](docs/corpus.md) and a versioned JSON rule catalog.

## Quick start

Requires Python 3.10 or newer.

```bash
python -m pip install -e .
well-argued-prose list
well-argued-prose show 37
well-argued-prose guide introduction
well-argued-prose audit examples/sample-manuscript.md
well-argued-prose scorecard init my-review.json
```

For Microsoft Word support: `python -m pip install -e ".[docx]"`.

The audit works locally on `.md`, `.txt`, or (with the optional dependency) `.docx` files. It **flags passages for human inspection**; it cannot validate arguments, verify scholarship, correct prose automatically, or predict publication outcomes. No external service is used.

## Explore

| Resource | Purpose |
|---|---|
| [Usage guide](docs/usage.md) | All four ways to use the project, step by step |
| [Rulebook](docs/handbook.md) | All 57 rules, published-article case examples |
| [Workflows](docs/workflows.md) | Find the right sequence for a writing task |
| [Scorecard](docs/scorecard.md) | Evidence-backed, human-scored editorial review |
| [Corpus](docs/corpus.md) | Twelve reference articles and their writing moves |
| [Example source map](docs/example-sources.md) | Paper-level provenance for all 57 examples |
| [Review protocol](docs/review-protocol.md) | An argument-first revision procedure |
| [Source and editorial notes](docs/source-notes.md) | Scope, provenance, normalized references |
| [Publishing guide](docs/publishing.md) | Open this project on GitHub |
| [AI revision prompts](prompts/manuscript-revision.md) | Apply the rulebook with a writing assistant |

## Contribute

Rule improvements need a specific failure mode, a worked example, and a reasoned justification. See [CONTRIBUTING.md](CONTRIBUTING.md). Run `python -m well_argued_prose validate` and `python -m unittest discover -s tests -v` before submitting changes.

## Licensing

Python code is licensed under **MIT** ([LICENSE](LICENSE)). Original rulebook text, examples, and editorial data are under **CC BY 4.0** ([content license](LICENSE-CONTENT.md)). Examples are original editorial paraphrases with DOI provenance, **not passages copied from the papers**. Journal articles remain the property of their respective rights holders. This is an independent project, unaffiliated with *Mind* or its publisher.

**Maintainer:** [Ferdinand Ries](https://github.com/FerdinandRies).
