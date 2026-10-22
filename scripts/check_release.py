"""Check a public-source allowlist; no confidential vocabulary is embedded here."""
from __future__ import annotations

import json
from pathlib import Path, PurePosixPath
import sys

ROOT = Path(__file__).resolve().parents[1]
# Standard source-distribution metadata is excluded from the source ZIP.
PACKAGING_FILES = {"PKG-INFO", "setup.cfg"}
IGNORED_PARTS = {".git", ".venv", "venv", "build", "dist", "__pycache__", ".pytest_cache", "htmlcov"}


def approved_paths(root: Path = ROOT) -> list[str]:
    doc = json.loads((root / "release-manifest.json").read_text(encoding="utf-8"))
    paths = doc.get("files")
    if doc.get("version") != "0.2.0" or not isinstance(paths, list) or not all(isinstance(p, str) for p in paths):
        raise ValueError("Invalid release manifest")
    if paths != sorted(set(paths)):
        raise ValueError("Manifest paths must be sorted and unique")
    for path in paths:
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts or "\\" in path or str(pure) != path:
            raise ValueError("Manifest contains an unsafe or noncanonical path")
    return paths


def check(root: Path = ROOT) -> list[str]:
    try:
        expected = set(approved_paths(root))
    except (OSError, ValueError, TypeError) as exc:
        return [str(exc)]
    issues = []
    actual = set()
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if relative.as_posix() in PACKAGING_FILES:
            continue
        if any(part in IGNORED_PARTS or part.endswith(".egg-info") for part in relative.parts):
            continue
        if path.is_symlink():
            issues.append("Symlink is outside the source-release policy: " + relative.as_posix())
        elif path.is_file():
            actual.add(relative.as_posix())
    for path in sorted(expected - actual):
        issues.append("Missing approved file: " + path)
    for path in sorted(actual - expected):
        issues.append("Unapproved file: " + path)
    for relative in sorted(expected & actual):
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeError:
            issues.append("Non-text file in public source: " + relative)
            continue
        if "\x00" in text:
            issues.append("Binary marker in public source: " + relative)
        if not text.endswith("\n"):
            issues.append("Missing final newline: " + relative)
    return issues


def main() -> int:
    issues = check()
    if issues:
        print("\n".join(issues), file=sys.stderr)
        return 1
    print(f"Public source allowlist verified: {len(approved_paths())} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
