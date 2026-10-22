# Publishing v0.2.0

Use the contents of the `journalprose` directory as the repository root. Keep hidden
files, including `.github`, `.gitignore`, and `.editorconfig`. For an existing
repository, follow [migration](migration.md) and remove the listed obsolete paths.

## Local checks

```bash
python -m pip install -e ".[dev,docx]"
python -m unittest discover -s tests -v
python scripts/build_handbook.py --check
python scripts/check_release.py
journalprose validate
python -m build
```

For a deterministic source ZIP using the checked allowlist:

```bash
python scripts/package_release.py --output ../journalprose-0.2.0-source.zip
```

The ZIP writer includes only approved paths. The source checker ignores build caches,
`*.egg-info`, and the standard source-distribution metadata files `PKG-INFO` and
`setup.cfg`; the ZIP allowlist excludes them. Keep the output outside the source
root. The allowlist is a safeguard against accidental inclusion; it does not judge
the confidentiality of the approved file contents.

## GitHub release

Review the actual diff and the staged file list before committing. Confirm the
repository path in your own checkout; this snapshot embeds no assumed repository
URL. Use tag `v0.2.0` and the prepared text in
[release notes](release-notes-0.2.0.md). Upload the wheel and source distribution
only after checking their contents. Repository creation, pushing, tagging, release
publication, and package-index publication are separate actions performed by the
maintainer.

The workflow configures Python 3.10-3.14 on Linux and Python 3.13 on Windows and
macOS. A configured matrix is not evidence that those jobs have run; inspect their
actual results after pushing. No CI success badge is pre-filled.

Keep internal assessment notes, manuscript inputs, personal rule collections,
private tests, and unapproved materials out of the repository and release assets.
Audit earlier public history separately when relevant.

## Technical references

The packaging configuration follows the [Python Packaging User Guide](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/)
and the [setuptools configuration reference](https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html).
The workflow uses GitHub's [Python build and test guidance](https://docs.github.com/en/actions/tutorials/build-and-test-code/python).
For the limits of removing earlier content, consult GitHub's
[history-removal guidance](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).
