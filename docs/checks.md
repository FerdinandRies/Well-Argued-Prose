# Software coverage and limits

The 50-rule handbook and the 21 surface checks have different scopes. A lexical match identifies a passage to inspect. The program performs no rewriting, AI-authorship determination, proof validation, source verification, or publication prediction.

## Implemented checks

| Check | Kind | Rules |
|---|---|---|
| `contrast-not-but`: Formulaic negative contrast | policy | [JP2-033](handbook.md#jp2-033) |
| `contrast-not-merely`: Prohibited phrase: not merely | policy | [JP2-033](handbook.md#jp2-033) |
| `contrast-not-only`: Prohibited phrase: not only | policy | [JP2-033](handbook.md#jp2-033) |
| `contrast-rather`: Prohibited phrase: rather than | policy | [JP2-033](handbook.md#jp2-033) |
| `contrast-instead`: Prohibited phrase: instead of | policy | [JP2-033](handbook.md#jp2-033) |
| `contrast-opposed`: Prohibited phrase: as opposed to | policy | [JP2-033](handbook.md#jp2-033) |
| `contrast-no-longer`: Formulaic temporal negative contrast | policy | [JP2-033](handbook.md#jp2-033) |
| `translated-contrast`: Translated negative-contrast template | policy | [JP2-033](handbook.md#jp2-033) |
| `purpose-template`: Template purpose or argument announcement | policy | [JP2-036](handbook.md#jp2-036) |
| `process-announcement`: Writing-process announcement | policy | [JP2-036](handbook.md#jp2-036) |
| `promotional-language`: Promotional or empty evaluative claim | policy | [JP2-035](handbook.md#jp2-035) |
| `shallow-ranking`: Possible unsupported hierarchy | advisory | [JP2-037](handbook.md#jp2-037) |
| `vague-reference`: Potentially unclear demonstrative | advisory | [JP2-026](handbook.md#jp2-026) |
| `stacked-hedge`: Stacked uncertainty words | advisory | [JP2-015](handbook.md#jp2-015), [JP2-040](handbook.md#jp2-040) |
| `agreement-candidate`: Possible plural subject agreement error | advisory | [JP2-025](handbook.md#jp2-025) |
| `article-mass-noun`: Possible article or countability error | advisory | [JP2-028](handbook.md#jp2-028) |
| `repeated-word`: Repeated adjacent word | advisory | [JP2-039](handbook.md#jp2-039) |
| `citation-cluster`: Semicolon-separated citation cluster | policy | [JP2-042](handbook.md#jp2-042), [JP2-046](handbook.md#jp2-046) |
| `citation-size`: More than two works in a parenthesis | policy | [JP2-042](handbook.md#jp2-042) |
| `citation-density`: Five or more cited positions in a paragraph | policy | [JP2-043](handbook.md#jp2-043) |
| `author-parade`: Possible author-by-author literature sequence | advisory | [JP2-044](handbook.md#jp2-044) |

`policy` marks a configured house-style match. `advisory` marks a possible issue that depends on context. Both need interpretation; a quoted expression can legitimately contain a prohibited pattern. The optional failure exit policy operates on raw match counts.

## Rule-by-rule coverage

| Rule | Automated candidate checks | Human review |
|---|---|---|
| [JP2-001](handbook.md#jp2-001) | None | Required |
| [JP2-002](handbook.md#jp2-002) | None | Required |
| [JP2-003](handbook.md#jp2-003) | None | Required |
| [JP2-004](handbook.md#jp2-004) | None | Required |
| [JP2-005](handbook.md#jp2-005) | None | Required |
| [JP2-006](handbook.md#jp2-006) | None | Required |
| [JP2-007](handbook.md#jp2-007) | None | Required |
| [JP2-008](handbook.md#jp2-008) | None | Required |
| [JP2-009](handbook.md#jp2-009) | None | Required |
| [JP2-010](handbook.md#jp2-010) | None | Required |
| [JP2-011](handbook.md#jp2-011) | None | Required |
| [JP2-012](handbook.md#jp2-012) | None | Required |
| [JP2-013](handbook.md#jp2-013) | None | Required |
| [JP2-014](handbook.md#jp2-014) | None | Required |
| [JP2-015](handbook.md#jp2-015) | `stacked-hedge` | Required |
| [JP2-016](handbook.md#jp2-016) | None | Required |
| [JP2-017](handbook.md#jp2-017) | None | Required |
| [JP2-018](handbook.md#jp2-018) | None | Required |
| [JP2-019](handbook.md#jp2-019) | None | Required |
| [JP2-020](handbook.md#jp2-020) | None | Required |
| [JP2-021](handbook.md#jp2-021) | None | Required |
| [JP2-022](handbook.md#jp2-022) | None | Required |
| [JP2-023](handbook.md#jp2-023) | None | Required |
| [JP2-024](handbook.md#jp2-024) | None | Required |
| [JP2-025](handbook.md#jp2-025) | `agreement-candidate` | Required |
| [JP2-026](handbook.md#jp2-026) | `vague-reference` | Required |
| [JP2-027](handbook.md#jp2-027) | None | Required |
| [JP2-028](handbook.md#jp2-028) | `article-mass-noun` | Required |
| [JP2-029](handbook.md#jp2-029) | None | Required |
| [JP2-030](handbook.md#jp2-030) | None | Required |
| [JP2-031](handbook.md#jp2-031) | None | Required |
| [JP2-032](handbook.md#jp2-032) | None | Required |
| [JP2-033](handbook.md#jp2-033) | `contrast-not-but`, `contrast-not-merely`, `contrast-not-only`, `contrast-rather`, `contrast-instead`, `contrast-opposed`, `contrast-no-longer`, `translated-contrast` | Required |
| [JP2-034](handbook.md#jp2-034) | None | Required |
| [JP2-035](handbook.md#jp2-035) | `promotional-language` | Required |
| [JP2-036](handbook.md#jp2-036) | `purpose-template`, `process-announcement` | Required |
| [JP2-037](handbook.md#jp2-037) | `shallow-ranking` | Required |
| [JP2-038](handbook.md#jp2-038) | None | Required |
| [JP2-039](handbook.md#jp2-039) | `repeated-word` | Required |
| [JP2-040](handbook.md#jp2-040) | `stacked-hedge` | Required |
| [JP2-041](handbook.md#jp2-041) | None | Required |
| [JP2-042](handbook.md#jp2-042) | `citation-cluster`, `citation-size` | Required |
| [JP2-043](handbook.md#jp2-043) | `citation-density` | Required |
| [JP2-044](handbook.md#jp2-044) | `author-parade` | Required |
| [JP2-045](handbook.md#jp2-045) | None | Required |
| [JP2-046](handbook.md#jp2-046) | `citation-cluster` | Required |
| [JP2-047](handbook.md#jp2-047) | None | Required |
| [JP2-048](handbook.md#jp2-048) | None | Required |
| [JP2-049](handbook.md#jp2-049) | None | Required |
| [JP2-050](handbook.md#jp2-050) | None | Required |

## Interpretation limits

Citation checks recognize common author-year forms and numeric reference lists. They count distinct work labels, with a multi-author work treated as one source position. They cannot reliably distinguish every citation style, resolve a full bibliography, or determine whether two sources perform the same argumentative function. Numeric ranges longer than 200 are not expanded.

The agreement and countability checks cover narrow patterns. The complete grammar rules remain a human review task. Mechanical triads, paragraph symmetry, conceptual precision, actual inferential validity, unsupported comparisons, and semantic loss during compression cannot be certified by this scanner.

Text inside Markdown code and block quotations is skipped. Headed bibliography sections are skipped by default. Inline prose quotation contexts and complex document structures require manual inspection. Read [formats](formats.md) for input and location details.

No corpus-level precision or recall estimate is claimed. Regression tests demonstrate the recorded examples and software behavior; they do not establish general linguistic accuracy.
