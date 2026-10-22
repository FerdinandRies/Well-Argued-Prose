"""Local, non-destructive surface checks with explicit limitations.

Regex matches are candidates for human inspection. No author-origin prediction,
proof assessment, citation verification, or automatic rewriting is performed.
"""
from __future__ import annotations

from bisect import bisect_right
from pathlib import Path
import re
from typing import Any
import zipfile

from . import __version__
from .catalog import load

MAX_INPUT_BYTES = 10 * 1024 * 1024
MAX_DOCX_EXPANDED_BYTES = 40 * 1024 * 1024
# Small, deliberately conservative patterns for author-year and numeric citations.
NAME = r"(?:Author\s+[A-Z]|Study\s+[A-Z]|[^\W\d_][\w'\u2019-]*)"
AUTHORS = NAME + r"(?:\s+(?:and|&)\s+" + NAME + r"|\s+et\s+al\.?)?"
YEAR = r"(?:18|19|20)\d{2}[a-z]?"
NARRATIVE = re.compile(r"\b(" + AUTHORS + r")\s*\(\s*(" + YEAR + r")\s*\)", re.I)
PAREN = re.compile(r"\([^()]{0,1500}\)")
PAREN_REF = re.compile(r"\b(" + AUTHORS + r")[,\s]+(" + YEAR + r")\b", re.I)
NUMERIC = re.compile(r"\[\s*(\d+(?:\s*[,;\u2013-]\s*\d+)*)\s*\]")
PARADE_NAME = r"(?:Author\s+[A-Z]|Study\s+[A-Z]|[A-Z][A-Za-z'\u2019-]+(?:\s+et\s+al\.?)?)"
PARADE = re.compile(r"\b" + PARADE_NAME + r"(?:\s*\(\s*" + YEAR + r"\s*\))?\s+(?:argues?|develops?|shows?|adds?|states?|suggests?|demonstrates?)\b")


def _blank(value: str) -> str:
    return "".join("\n" if c == "\n" else " " for c in value)


def mask_markdown(text: str, include_references: bool = False) -> str:
    """Mask code, block quotations, and a headed bibliography, retaining offsets.

    Inline prose quotations are left visible because automatic attribution of
    quotation boundaries is unreliable. Reviewers decide whether a match is exempt.
    """
    lines = text.splitlines(keepends=True)
    output: list[str] = []
    fence_char = ""
    fence_length = 0
    reference_level: int | None = None
    for line in lines:
        stripped = line.lstrip()
        fence = re.match(r"^(`{3,}|~{3,})", stripped)
        if fence_char:
            output.append(_blank(line))
            if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_length:
                fence_char = ""
                fence_length = 0
            continue
        if fence:
            fence_char = fence.group(1)[0]
            fence_length = len(fence.group(1))
            output.append(_blank(line))
            continue
        heading = re.match(r"^\s*(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if heading:
            depth = len(heading.group(1))
            title = heading.group(2).strip().lower()
            if reference_level is not None and depth <= reference_level:
                reference_level = None
            if not include_references and title in {"references", "bibliography", "works cited"}:
                reference_level = depth
        if reference_level is not None or stripped.startswith(">"):
            output.append(_blank(line))
        else:
            output.append(line)
    masked = "".join(output)
    # Match inline code with corresponding runs of backticks.
    masked = re.sub(r"(`+)([^`\n]*?)\1", lambda m: _blank(m.group(0)), masked)
    return masked


def read_manuscript(path: Path) -> tuple[str, str]:
    """Return extracted text and location units, never overwrite the input.

    DOCX reading includes body paragraphs and table cells in document order.
    Headers, footers, text boxes, footnotes, and tracked-change fidelity are outside
    this reader's coverage. Locations for DOCX refer to extracted lines, not pages.
    """
    path = Path(path)
    if not path.is_file():
        raise ValueError(f"File does not exist: {path}")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("Input exceeds the 10 MiB file-size limit")
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        try:
            return path.read_text(encoding="utf-8-sig"), "line"
        except UnicodeDecodeError as exc:
            raise ValueError("Text input must be UTF-8 encoded") from exc
    if suffix != ".docx":
        raise ValueError("Supported input extensions: .md, .txt, .docx")
    try:
        from docx import Document
        from docx.table import Table
        from docx.text.paragraph import Paragraph
    except ImportError as exc:
        raise ValueError('DOCX support requires installation with the "docx" extra') from exc
    try:
        with zipfile.ZipFile(path) as archive:
            if sum(i.file_size for i in archive.infolist()) > MAX_DOCX_EXPANDED_BYTES:
                raise ValueError("Expanded DOCX exceeds the 40 MiB limit")
        document = Document(path)
        parts: list[str] = []
        for block in document.iter_inner_content():
            if isinstance(block, Paragraph):
                parts.append(block.text)
            elif isinstance(block, Table):
                seen: set[Any] = set()
                for row in block.rows:
                    for cell in row.cells:
                        # Merged cells may occur repeatedly in the row representation.
                        key = cell._tc
                        if key in seen:
                            continue
                        seen.add(key)
                        parts.extend(p.text for p in cell.paragraphs)
        return "\n\n".join(parts), "extracted_line"
    except (OSError, ValueError, zipfile.BadZipFile) as exc:
        raise ValueError(f"Could not read DOCX: {exc}") from exc
    except Exception as exc:
        raise ValueError(f"Could not parse DOCX: {type(exc).__name__}") from exc


def _numeric_ids(body: str) -> set[str]:
    result: set[str] = set()
    for part in re.split(r"[,;]", body):
        ends = re.split(r"[\u2013-]", part.strip())
        if len(ends) == 1:
            result.add("number:" + str(int(ends[0])))
        elif len(ends) == 2:
            a, b = map(int, ends)
            # Bounded expansion avoids allocating an arbitrary user-specified range.
            if a <= b <= a + 200:
                result.update("number:" + str(n) for n in range(a, b + 1))
    return result


def _source_ids(text: str) -> set[str]:
    result = {re.sub(r"\s+", " ", m.group(1).lower()) + ":" + m.group(2).lower()
              for m in NARRATIVE.finditer(text)}
    for group in PAREN.finditer(text):
        result.update(re.sub(r"\s+", " ", m.group(1).lower()) + ":" + m.group(2).lower()
                      for m in PAREN_REF.finditer(group.group(0)))
    for group in NUMERIC.finditer(text):
        result.update(_numeric_ids(group.group(1)))
    return result


def _special_matches(engine: str, text: str):
    if engine in {"citation_cluster", "citation_size"}:
        for match in PAREN.finditer(text):
            count = len(_source_ids(match.group(0)))
            if (engine == "citation_cluster" and ";" in match.group(0) and count >= 2) or (engine == "citation_size" and count > 2):
                yield match.start(), match.end()
        for match in NUMERIC.finditer(text):
            count = len(_numeric_ids(match.group(1)))
            if (engine == "citation_size" and count > 2) or (engine == "citation_cluster" and ";" in match.group(1) and count >= 2):
                yield match.start(), match.end()
    elif engine in {"citation_density", "author_parade"}:
        for match in re.finditer(r"\S[^\n]*(?:\n(?!\s*\n)[^\n]*)*", text):
            paragraph = match.group(0)
            if engine == "citation_density" and len(_source_ids(paragraph)) >= 5:
                yield match.start(), match.end()
            if engine == "author_parade" and len(list(PARADE.finditer(paragraph))) >= 3:
                yield match.start(), match.end()


def audit_text(text: str, *, unit: str = "line", max_per_check: int = 10,
               markdown: bool = True, include_references: bool = False) -> dict[str, Any]:
    """Return a versioned report; findings contain original-text offsets.

    ``max_per_check`` truncates displayed examples, never total match counts.
    Columns are one-based character columns. End offsets are exclusive.
    """
    if not isinstance(text, str):
        raise ValueError("text must be a string")
    if type(max_per_check) is not int or not 1 <= max_per_check <= 1000:
        raise ValueError("max_per_check must be an integer between 1 and 1000")
    if unit not in {"line", "extracted_line"}:
        raise ValueError("unit must be line or extracted_line")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    candidate = mask_markdown(text, include_references) if markdown else text
    newlines = [m.start() for m in re.finditer("\n", text)]
    checks: list[dict[str, Any]] = []
    for check in load("checks")["checks"]:
        engine = check["engine"]
        if engine == "regex":
            spans = ((m.start(), m.end()) for m in re.finditer(check["pattern"], candidate, re.I))
        else:
            spans = _special_matches(engine, candidate)
        total = 0
        examples = []
        for start, end in spans:
            total += 1
            if len(examples) >= max_per_check:
                continue
            line = bisect_right(newlines, start) + 1
            line_start = newlines[line - 2] + 1 if line > 1 else 0
            examples.append({"line": line, "column": start - line_start + 1,
                             "start": start, "end": end, "match": text[start:end],
                             "context": text[max(0, start - 65):min(len(text), end + 95)].replace("\n", " ")})
        checks.append({"id": check["id"], "title": check["title"], "kind": check["kind"],
                       "rule_ids": check["rule_ids"], "message": check["message"],
                       "total_matches": total, "truncated": total > len(examples), "examples": examples})
    return {"schema_version": 2, "version": __version__, "kind": "surface-review-candidates",
            "unit": unit, "line_endings": "normalized-LF", "check_count": len(checks),
            "total_matches": sum(c["total_matches"] for c in checks),
            "policy_matches": sum(c["total_matches"] for c in checks if c["kind"] == "policy"),
            "checks": checks,
            "limitations": "Pattern matches require human interpretation. Counts are check matches, so overlapping patterns may count the same passage. No AI-authorship determination, proof validation, full grammar assessment, source verification, or publication prediction is performed."}
