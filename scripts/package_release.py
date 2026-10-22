"""Create a deterministic source ZIP containing only approved public files."""
from __future__ import annotations

import argparse
from pathlib import Path
import zipfile

from check_release import ROOT, approved_paths, check


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args()
    out = args.output.resolve()
    if out.is_relative_to(ROOT.resolve()):
        p.error("Place the release archive outside the source directory")
    problems = check()
    if problems:
        p.error("Release check failed: " + "; ".join(problems))
    if out.exists():
        p.error("Output already exists; choose a new path or remove it deliberately")
    out.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in approved_paths():
            info = zipfile.ZipInfo("journalprose/" + name, date_time=(2026, 10, 22, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, (ROOT / name).read_bytes(), compresslevel=9)
    print(f"Wrote {out.name}: {len(approved_paths())} approved files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
