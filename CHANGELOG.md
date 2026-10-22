# Changelog

## 0.2.0 - 2026-10-22

### Editorial changes

- Introduced the Advanced Scholarly Writing Standards Core edition: 50 rules in eight levels.
- Added foundational reasoning, explicit grammar review, strict formulaic-style control, literature discipline, and protected-content compression.
- Replaced all rule-level examples with invented examples and removed source-specific framing.
- Added six workflows and a ten-criterion, evidence-backed human review record.

### Software changes

- Added 21 local surface checks, Markdown masking, citation heuristics, and optional match-based exit codes.
- Added body-table extraction for optional Word input and explicit input limitations.
- Added release allowlisting, synchronized documentation, and regression tests.
- Retained MIT for code and CC BY 4.0 for editorial content, with FerdinandRies attribution.

### Migration

Rule IDs and JSON schemas change in this release. `JP2-001` through `JP2-050`
replace legacy numeric IDs. The `checklist` command replaces the numerical
`scorecard` command. See [migration instructions](docs/migration.md) before
updating an existing checkout. No remote repository is modified by these tools.
