#!/usr/bin/env python3
"""Regression cases for charcount.py.

Run directly: exits 0 and prints a summary, or exits 1 listing what changed.

The counter has to ignore the things the template carries that are not the field text —
the trailing `[n/220]` annotation, `<placeholder>` lines, and the "First three lines"
fold-helper line — or it reports a headline as over limit when it is not.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from charcount import check, visible_len  # noqa: E402

# (markdown, field name to inspect, expected count, expected within-limit)
CASES = [
    ("## Headline\nSenior Data Engineer | streaming platforms\n",
     "Headline", 42, True),
    # trailing annotation is not counted
    ("## Headline\nSenior Data Engineer | streaming platforms  `[42/220]`\n",
     "Headline", 42, True),
    # a genuinely over-limit headline
    ("## Headline\n" + "x" * 230 + "\n",
     "Headline", 230, False),
    # About: fold-helper line and <placeholder> are dropped, real text counts
    ("## About\nFirst three lines (above the \"see more\" fold):\n\n"
     "I build streaming data platforms for retail.\n\n<rest of the About>\n",
     "About", 44, True),
    # Experience entries are counted individually against 2000
    ("## Experience\n\n### Senior Data Engineer - Halcyon\nOwned the analytics platform.\n\n"
     "### Data Engineer - Vantiq\nBuilt ingestion services.\n",
     "Experience: Data Engineer - Vantiq", 25, True),
]


def main() -> int:
    wrong = []

    # visible_len drops a trailing annotation
    if visible_len("headline text  `[13/220]`") != len("headline text"):
        wrong.append("visible_len did not strip a trailing `[n/m]` annotation")

    for md, field, want_count, want_ok in CASES:
        rows = {name: (n, ok) for name, n, _limit, ok in check(md)}
        if field not in rows:
            wrong.append(f"{field!r}: not found in check() output for {md!r}")
            continue
        got_count, got_ok = rows[field]
        if (got_count, got_ok) != (want_count, want_ok):
            wrong.append(f"{field!r}: got count={got_count} ok={got_ok}, "
                         f"wanted count={want_count} ok={want_ok}")

    for line in wrong:
        print("  " + line, file=sys.stderr)
    total = len(CASES) + 1
    print(f"charcount: {total - len(wrong)}/{total} cases correct")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
