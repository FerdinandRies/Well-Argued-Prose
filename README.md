# JournalProse

## Advanced Scholarly Writing Standards

**An argument-first framework for precise academic English and natural scholarly prose.**

JournalProse is a practical rulebook and local review toolkit for researchers
preparing English-language manuscripts for selective peer-reviewed journals.
The **v0.2.0 Core edition** contains **50 rules in eight levels**, with a check,
a repair, and an invented before-and-after example for every rule.

Its emphasis is argument-driven scholarship in the humanities and social sciences.
General language and reasoning rules also support work in other disciplines.

## Start with the rulebook

Read the [handbook](docs/handbook.md), choose a [task workflow](docs/workflows.md),
and apply the relevant [revision prompt](prompts/manuscript-revision.md).
Python is optional for this route.

The core covers manuscript structure, basic reasoning, paragraph progression,
English grammar, formulaic-style control, citation discipline, and
argument-preserving compression. Examples are invented and carry no claims
about actual studies or researchers.

## Use the local tools

Requires Python 3.10 or later. From the extracted repository directory:

```bash
python -m pip install .
journalprose list
journalprose show JP2-033
journalprose guide compression
journalprose audit examples/sample-manuscript.md
journalprose checklist init my-review.json
```

Optional Word input: `python -m pip install ".[docx]"`.
For development, use `python -m pip install -e ".[dev,docx]"`.
An installed wheel can also be used without a source checkout.

The CLI reads `.md`, `.txt`, and optional `.docx` input. It provides **21 surface
checks**, location-specific findings, JSON output, and an evidence-backed human
review checklist. It works locally and never rewrites a manuscript or sends it
to an external service.

```bash
journalprose audit examples/sample-manuscript.md --json
journalprose audit examples/sample-manuscript.md --fail-on policy
journalprose checklist evaluate my-review.json --json
```

A pattern match requires interpretation. The toolkit does not determine AI
authorship, validate proofs, verify sources, provide full grammar checking, or
predict publication decisions. See [coverage and limits](docs/checks.md).

## Read further

| Resource | Purpose |
|---|---|
| [Rulebook](docs/handbook.md) | The 50 public rules and worked examples |
| [Review protocol](docs/review-protocol.md) | Apply the rules without changing the author's position |
| [Human checklist](docs/checklist.md) | Record decisions, evidence, and unresolved issues |
| [Input and output](docs/formats.md) | CLI behavior, locations, and JSON versions |
| [Migration](docs/migration.md) | Replace v0.1.x files and update references |
| [Publishing](docs/publishing.md) | Prepare the repository and release assets |

## Development

```bash
python -m unittest discover -s tests -v
python scripts/build_handbook.py --check
python scripts/check_release.py
journalprose validate
```

See [CONTRIBUTING.md](CONTRIBUTING.md). This release uses `JP2-001` through
`JP2-050`; earlier numeric rule IDs have different meanings.

**Maintainer:** FerdinandRies. **Code:** [MIT](LICENSE).
**Editorial content:** [CC BY 4.0](LICENSE-CONTENT.md).
