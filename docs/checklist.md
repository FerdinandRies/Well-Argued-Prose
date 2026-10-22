# Human review checklist

This checklist records a reviewer's decisions with evidence. It has no aggregate score or acceptance threshold.

| Criterion | Rules |
|---|---|
| Baseline and authorized scope | [JP2-001](handbook.md#jp2-001), [JP2-002](handbook.md#jp2-002), [JP2-004](handbook.md#jp2-004) |
| Problem, governing claim, and conclusion | [JP2-005](handbook.md#jp2-005), [JP2-006](handbook.md#jp2-006), [JP2-009](handbook.md#jp2-009), [JP2-010](handbook.md#jp2-010) |
| Definitions and stable terminology | [JP2-007](handbook.md#jp2-007), [JP2-008](handbook.md#jp2-008), [JP2-039](handbook.md#jp2-039) |
| Basic inferences and their support | [JP2-011](handbook.md#jp2-011), [JP2-012](handbook.md#jp2-012), [JP2-013](handbook.md#jp2-013), [JP2-014](handbook.md#jp2-014), [JP2-015](handbook.md#jp2-015), [JP2-016](handbook.md#jp2-016), [JP2-017](handbook.md#jp2-017), [JP2-018](handbook.md#jp2-018) |
| Connected paragraph progression | [JP2-019](handbook.md#jp2-019), [JP2-020](handbook.md#jp2-020), [JP2-021](handbook.md#jp2-021), [JP2-022](handbook.md#jp2-022), [JP2-023](handbook.md#jp2-023) |
| Sentence meaning and grammar | [JP2-024](handbook.md#jp2-024), [JP2-025](handbook.md#jp2-025), [JP2-026](handbook.md#jp2-026), [JP2-027](handbook.md#jp2-027), [JP2-028](handbook.md#jp2-028), [JP2-029](handbook.md#jp2-029), [JP2-030](handbook.md#jp2-030), [JP2-031](handbook.md#jp2-031), [JP2-032](handbook.md#jp2-032) |
| Strict scholarly voice policy | [JP2-033](handbook.md#jp2-033), [JP2-034](handbook.md#jp2-034), [JP2-035](handbook.md#jp2-035), [JP2-036](handbook.md#jp2-036), [JP2-037](handbook.md#jp2-037), [JP2-038](handbook.md#jp2-038), [JP2-039](handbook.md#jp2-039), [JP2-040](handbook.md#jp2-040) |
| Source accuracy and literature functions | [JP2-003](handbook.md#jp2-003), [JP2-041](handbook.md#jp2-041), [JP2-042](handbook.md#jp2-042), [JP2-043](handbook.md#jp2-043), [JP2-044](handbook.md#jp2-044), [JP2-045](handbook.md#jp2-045), [JP2-046](handbook.md#jp2-046) |
| Compression retention and edit traceability | [JP2-004](handbook.md#jp2-004), [JP2-046](handbook.md#jp2-046), [JP2-047](handbook.md#jp2-047), [JP2-048](handbook.md#jp2-048), [JP2-049](handbook.md#jp2-049) |
| Final consistency and unresolved findings | [JP2-050](handbook.md#jp2-050) |

## Record a decision

`not_reviewed` means no decision has been recorded. `pass` requires textual evidence. `revise` requires evidence and a note explaining the repair. `not_applicable` requires a reason tied to the agreed task. Baseline scope and final disposition must be reviewed.

A single `revise` status keeps the record in `needs-revision`. An unreviewed item keeps it incomplete. `recorded-review-complete` means that the required reviewer entries are present and none requests revision; the program has not independently verified those entries.

```bash
journalprose checklist init my-review.json
# Fill in manuscript, reviewer, task_scope, decisions, and evidence.
journalprose checklist evaluate my-review.json --json
journalprose checklist evaluate my-review.json --require-complete
```

Store review records outside the public repository. A new template contains no pre-filled passes.
