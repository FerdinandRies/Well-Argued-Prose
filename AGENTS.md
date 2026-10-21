# Agent Instructions for Well-Argued Prose

Use `src/well_argued_prose/data/rules.json` as the authoritative version of the 57 rules and `docs/handbook.md` as its generated English rendering.

1. Start with the paper's central claim and inferential structure; revise diction only after that work is secure.
2. Preserve a manuscript's established concepts, theoretical commitments, and justified originality. Never simplify away a warranted conceptual distinction solely to make it familiar.
3. Diagnose a precise failure before proposing a revision. A strong claim requires an appropriate warrant; a concern about readability is not itself a counterargument.
4. Every cited work must perform a substantive function. Never invent citations, reading history, textual evidence, or verification.
5. Preserve examples, failure cases, the strongest objections, and the boundaries they reveal. Avoid formulaic negative pivots and empty self-description.
6. Do not award automated quality scores. Scorecard ratings and supporting evidence must come from a human reviewer.
7. Keep the repository in English, including documentation, tests, comments, and public-facing examples.
8. Keep every rule-level example linked to at least one stable reference ID in `corpus.json`. Write original case reconstructions and cite the source DOI; do not misrepresent paraphrases as article quotations or copy article text into this CC BY repository.
9. Update the JSON data, regenerate documentation, and run all checks whenever a substantive rule changes.

Commands:

```bash
python scripts/build_handbook.py
python -m well_argued_prose validate
python -m unittest discover -s tests -v
```
