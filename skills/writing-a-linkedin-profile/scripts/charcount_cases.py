#!/usr/bin/env python3
"""Regression cases for charcount.py.

Run directly: exits 0 and prints a summary, or exits 1 listing what changed.

The counter has to ignore the things the template carries that are not the field text —
the trailing `[n/220]` annotation, `<placeholder>` lines, and the "First three lines"
fold-helper line — or it reports a headline as over limit when it is not.

It also has to read that annotation back and compare it against the real count. A count
written by hand while drafting goes stale as soon as a sentence is edited, and a stale one
is worse than none: it looks checked.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from charcount import check, claimed_len, visible_len  # noqa: E402

# (markdown, field name to inspect, expected count, expected within-limit, expected claim)
CASES = [
    ("## Headline\nSenior Data Engineer | streaming platforms\n",
     "Headline", 42, True, None),
    # trailing annotation is not counted, and is read back as the claim
    ("## Headline\nSenior Data Engineer | streaming platforms  `[42/220]`\n",
     "Headline", 42, True, 42),
    # a stale claim: the text was edited, the hand-written count was not
    ("## Headline\nSenior Data Engineer | streaming platform  `[42/220]`\n",
     "Headline", 41, True, 42),
    # a genuinely over-limit headline
    ("## Headline\n" + "x" * 230 + "\n",
     "Headline", 230, False, None),
    # About: fold-helper line and <placeholder> are dropped, real text counts
    ("## About\nFirst three lines (above the \"see more\" fold):\n\n"
     "I build streaming data platforms for retail.\n\n<rest of the About>\n",
     "About", 44, True, None),
    # the About's claim sits at the end of the section, after several paragraphs
    ("## About\nFirst three lines:\n\nI build platforms.\n\n"
     "I also break them.  `[37/2600]`\n",
     "About", 37, True, 37),
    # Experience entries are counted individually against 2000
    ("## Experience\n\n### Senior Data Engineer - Halcyon\nOwned the analytics platform.\n\n"
     "### Data Engineer - Vantiq\nBuilt ingestion services.\n",
     "Experience: Data Engineer - Vantiq", 25, True, None),
]


def main() -> int:
    wrong = []

    # visible_len drops a trailing annotation; claimed_len reads it back
    if visible_len("headline text  `[13/220]`") != len("headline text"):
        wrong.append("visible_len did not strip a trailing `[n/m]` annotation")
    if claimed_len("headline text  `[13/220]`") != 13:
        wrong.append("claimed_len did not read back a trailing `[n/m]` annotation")
    if claimed_len("headline text") is not None:
        wrong.append("claimed_len invented a claim for a field that carries none")

    for md, field, want_count, want_ok, want_claim in CASES:
        rows = {name: (n, ok, claimed) for name, n, _limit, ok, claimed in check(md)}
        if field not in rows:
            wrong.append(f"{field!r}: not found in check() output for {md!r}")
            continue
        got_count, got_ok, got_claim = rows[field]
        if (got_count, got_ok, got_claim) != (want_count, want_ok, want_claim):
            wrong.append(f"{field!r}: got count={got_count} ok={got_ok} claim={got_claim}, "
                         f"wanted count={want_count} ok={want_ok} claim={want_claim}")

    for line in wrong:
        print("  " + line, file=sys.stderr)
    total = len(CASES) + 3
    print(f"charcount: {total - len(wrong)}/{total} cases correct")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
