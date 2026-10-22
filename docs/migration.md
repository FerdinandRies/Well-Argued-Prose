# Migrating from v0.1.x

Use a branch or backup of the current repository. This release is a complete public
snapshot. A file overlay alone leaves obsolete files behind.

## Remove obsolete tracked files

The following v0.1.x paths are absent from v0.2.0 and must be removed from the
updated working tree when present:

```text
docs/corpus.md
docs/example-sources.md
docs/source-notes.md
docs/scorecard.md
src/journalprose/data/corpus.json
src/journalprose/data/scorecard.json
src/journalprose/scoring.py
tests/test_scoring.py
```

Replace the remaining project files with this snapshot. Preserve `.git` and any
unrelated repository settings deliberately; inspect the complete diff. The release
checker reports additional working-tree files that are outside the public allowlist.
Do not solve a privacy warning by adding a private file to that allowlist.

## Update references and integrations

- The public rules now use `JP2-001` through `JP2-050`. Earlier integer IDs name
  different rules. Remap references by meaning; there is no automatic one-to-one map.
- Use `list --level L0` through `L7` in place of the earlier numbered section filter.
- Use `checklist init` and `checklist evaluate` in place of `scorecard` commands.
  Old numerical ratings are not converted into new review decisions.
- Catalog and report schemas are version 2. Consumers must update their field
  handling. Source-observation and article-link fields are removed.
- `guide` offers revision, polish, argument, citations, compression, and final.

## Verify the replacement

```bash
python -m pip install -e ".[docx]"
python -m unittest discover -s tests -v
python scripts/build_handbook.py --check
python scripts/check_release.py
journalprose validate
```

A new release changes the current snapshot. It does not erase previous commits,
tags, release attachments, forks, or other copies. Review historical disclosure
separately before publishing; history changes require a deliberate repository-owner
decision. This package contains no automatic history-rewriting or upload command.
