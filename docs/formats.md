# Input, output, and CLI behavior

## Input

UTF-8 `.md` and `.txt` files require no runtime dependency. Optional `.docx` input
requires `python-docx>=1.1`. The Word reader extracts body paragraphs and table-cell
paragraphs in document order. It does not cover headers, footers, footnotes, text
boxes, nested-table traversal, or reliable tracked-change interpretation. Export a
clean text copy when those elements matter. It performs no layout validation.

The file limit is 10 MiB; the expanded Word archive limit is 40 MiB. The input is
read-only. No command sends it to an external service.

For Markdown, fenced and inline code, block quotations, and sections headed
`References`, `Bibliography`, or `Works Cited` are excluded from the default scan.
`--include-references` includes those bibliography sections. A later heading at the
same or a higher level ends a bibliography exclusion. Inline prose quotations remain
visible and require manual interpretation. Plain text is scanned without Markdown
masking. Tables are not semantically parsed by the style checker.

## Reports

`audit --json` returns schema version 2. Every check reports its rule IDs, match
count, message, and displayed examples. An example has `line`, `column`, `start`,
`end`, `match`, and `context`. Line and column numbers are one-based. Offsets are
zero-based characters with an exclusive end. CRLF and CR are normalized to LF before
location calculation. Word locations identify extracted lines, never page numbers.

`--max-per-check` accepts 1 through 1000 and limits displayed examples only.
`truncated` identifies omitted examples; total counts remain complete. Different
checks can match one passage, so a count is a count of check matches.

## Exit codes

| Command | 0 | 1 | 2 |
|---|---|---|---|
| `audit` | Completed under the selected exit policy | Matches meet `--fail-on policy` or `--fail-on any` | Invalid input or options |
| `validate` | Catalog checks passed | Catalog problems found | Read or input error |
| `checklist evaluate` | Record evaluated | Incomplete or unresolved with `--require-complete` | Invalid record |
| Other commands | Completed | Reserved | Invalid request or input |

The default audit exit policy is `none`. A zero exit code means the command ran;
it carries no semantic quality verdict. A nonzero match-policy result also requires
human interpretation, particularly for quotations and citation heuristics.

## Data versions

Catalogs, reports, and review records use schema version 2. Rules use the `JP2-`
namespace; legacy numeric IDs are rejected. The current checklist also records
`rulebook_version`. Record compatibility is checked explicitly.

The runtime reads only four bundled catalogs: `rules`, `workflows`, `checks`, and
`checklist`. It does not fetch or load other rule collections.
