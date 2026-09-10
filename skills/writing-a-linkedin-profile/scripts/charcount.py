#!/usr/bin/env python3
"""Character counts for a profile/linkedin.md against LinkedIn's field limits.

The limits move and LinkedIn counts URLs and emoji in ways a plain count does not, so this
is a guide, not a gate: confirm anything close in LinkedIn before saving. Standard library
only, no network.

Usage:
    python3 charcount.py profile/linkedin.md
    cat profile/linkedin.md | python3 charcount.py

Exit 0 if every counted field is within its limit, 1 if any is over, 2 on a read error.
"""

from __future__ import annotations

import re
import sys

# Field name (as it appears after "## " or "### ") -> character limit.
LIMITS = {
    "Headline": 220,
    "About": 2600,
    "Connection request": 300,
}
EXPERIENCE_ENTRY_LIMIT = 2000

_ANNOTATION = re.compile(r"\s*`\[\s*\d+\s*/\s*\d+\s*\]`\s*$")
_PLACEHOLDER_LINE = re.compile(r"^\s*<[^>]+>\s*$")
_FOLD_HELPER = re.compile(r"^\s*First three lines\b", re.IGNORECASE)


def visible_len(text: str) -> int:
    """Length of a field's text, minus a trailing `[n/m]` annotation and surrounding space."""
    return len(_ANNOTATION.sub("", text).strip())


def _clean_body(lines: list[str]) -> str:
    kept = [
        ln for ln in lines
        if ln.strip()
        and not _PLACEHOLDER_LINE.match(ln)
        and not _FOLD_HELPER.match(ln)
    ]
    return _ANNOTATION.sub("", "\n".join(kept)).strip()


def sections(md: str) -> list[tuple[str, str]]:
    """(field name, body text) for each ## / ### heading, in order."""
    out: list[tuple[str, str]] = []
    name: str | None = None
    buf: list[str] = []
    for line in md.splitlines():
        m = re.match(r"^#{2,3}\s+(.*?)\s*$", line)
        if m:
            if name is not None:
                out.append((name, _clean_body(buf)))
            name, buf = m.group(1), []
        elif name is not None:
            buf.append(line)
    if name is not None:
        out.append((name, _clean_body(buf)))
    return out


def check(md: str) -> list[tuple[str, int, int, bool]]:
    """(field, count, limit, within_limit) for every field that has a limit."""
    rows: list[tuple[str, int, int, bool]] = []
    in_experience = False
    for name, body in sections(md):
        if name == "Experience":
            in_experience = True
            continue
        if name.startswith(("Strategy note", "Skills", "Risk notes", "Revision log",
                            "What this profile")):
            in_experience = False
            continue
        if name in LIMITS:
            in_experience = False
            n = visible_len(body)
            rows.append((name, n, LIMITS[name], n <= LIMITS[name]))
        elif in_experience and body:
            n = visible_len(body)
            rows.append((f"Experience: {name}", n, EXPERIENCE_ENTRY_LIMIT,
                         n <= EXPERIENCE_ENTRY_LIMIT))
    return rows


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] not in ("-", "/dev/stdin"):
        try:
            md = open(argv[1], encoding="utf-8").read()
        except OSError as e:
            print(f"cannot read {argv[1]}: {e}", file=sys.stderr)
            return 2
    else:
        md = sys.stdin.read()

    rows = check(md)
    if not rows:
        print("no countable fields found (expected ## Headline, ## About, ## Experience)")
        return 0

    width = max(len(r[0]) for r in rows)
    over = False
    for name, n, limit, ok in rows:
        flag = "ok  " if ok else "OVER"
        if not ok:
            over = True
        print(f"  {flag}  {name.ljust(width)}  {n:>5} / {limit}")
    return 1 if over else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
