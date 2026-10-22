# Contributing

Propose a specific problem, a reasoned repair, and an invented before-and-after
example. Keep the public core practical and compact. Describe the new rule's
relationship to an existing rule before proposing another identifier.

All public examples must be original, self-contained teaching material. Do not
submit private manuscripts, research frameworks, unpublished findings, copied
article passages, or material you lack permission to redistribute. A maintainer
must approve content for release before it enters the public catalog.

Edit `src/journalprose/data/rules.json` as the rule text's source of truth.
Update checks and tests only for behavior the software can actually detect.
Regenerate documentation with `python scripts/build_handbook.py`.

For code changes, add regression tests covering the repaired behavior and a nearby
false-positive case. Do not report semantic validation from lexical matching.
All documentation and public identifiers use English.

Before proposing changes, run:

```bash
python -m unittest discover -s tests -v
python scripts/build_handbook.py --check
python scripts/check_release.py
journalprose validate
```

New files require an explicit update to `release-manifest.json`. Inspect the diff
before adding a path. Keep manuscripts and review output outside the repository.

Contributions are accepted under the license applicable to the affected component:
AGPL-3.0-only for code and CC BY-SA 4.0 for editorial content. Submit only material you are
authorized to license. Respect the [code of conduct](CODE_OF_CONDUCT.md).
