#!/usr/bin/env python3
"""Check that an application's artifacts do not contradict each other.

A tailored resume, a cover letter and a set of screening answers are read together
by the same interviewer. A figure that appears in one and not the others, or the same
figure attached to two different systems, is what gets a candidate caught in a room.

What it checks: every number claimed in the cover letter or the screening answers
appears somewhere in the resume, the posting, or the honest context. That catches an
invented figure, which is the common failure.

What it does NOT catch, and you should not rely on it to: a figure that is real but
attached to the wrong thing. The bug that prompted this script was exactly that — a
live agent run found the example cover letter claiming "schema contracts across
twenty-seven external publishers" for the Kafka feed, when the resume attributes 27
feeds to the ingestion framework and three consumers to Kafka. Both numbers were true
and both appear in the evidence, so this script passes it. Two true facts welded into
one false sentence needs a reader, and an interviewer holding the CV is that reader.

Usage: python3 check_consistency.py <application-folder> [--profile <profile-dir>]
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

# Written-out numbers a cover letter uses instead of digits.
WORDS = {
    "one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6",
    "seven": "7", "eight": "8", "nine": "9", "ten": "10", "eleven": "11",
    "twelve": "12", "fourteen": "14", "twenty": "20", "thirty": "30",
    "forty": "40", "sixty": "60", "hundred": "100",
}
COMPOUND = re.compile(
    r"\b(twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety)[-\s]"
    r"(one|two|three|four|five|six|seven|eight|nine)\b", re.I)
TENS = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50,
        "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90}
UNITS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
         "six": 6, "seven": 7, "eight": 8, "nine": 9}


ISO_DATE = re.compile(r"\b\d{4}-\d{2}(?:-\d{2})?\b")


def figures(text: str) -> set[str]:
    """Every numeric claim in a piece of prose, normalised to digits.

    Dates are stripped first: "2026-08-26" is not three claims about 2026, 8 and 26.
    """
    text = ISO_DATE.sub(" ", text)
    found = set(re.findall(r"\d[\d,]*(?:\.\d+)?", text))
    found = {f.replace(",", "") for f in found}
    for tens, units in COMPOUND.findall(text):
        found.add(str(TENS[tens.lower()] + UNITS[units.lower()]))
    for word, digit in WORDS.items():
        if re.search(rf"\b{word}\b", text, re.I):
            found.add(digit)
    return found


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folder")
    parser.add_argument("--profile", default=None)
    args = parser.parse_args()

    app = pathlib.Path(args.folder)
    profile = pathlib.Path(args.profile) if args.profile else app.parent.parent / "profile"

    # The evidence base: what the candidate can actually support.
    evidence = ""
    for path in (app / "resume.json", profile / "resume.json",
                 app / "job.md", profile / "honest-context.md"):
        if path.exists():
            evidence += path.read_text() + "\n"
    if not evidence:
        print(f"{app}: no resume.json or job.md to check against", file=sys.stderr)
        return 2
    supported = figures(evidence)

    problems = []
    for name in ("cover-letter.md", "questions.md"):
        path = app / name
        if not path.exists():
            continue
        for claim in sorted(figures(path.read_text())):
            # Ignore years and small ordinals that are almost always prose.
            if claim in supported or len(claim) < 2 or re.match(r"^(19|20)\d\d$", claim):
                continue
            problems.append(f"{name}: the figure {claim!r} appears nowhere in the "
                            f"resume, the posting or the honest context")

    print(f"{app.name}")
    if problems:
        for p in problems:
            print(f"  FAIL  {p}")
    else:
        print(f"  ok    every figure claimed is supported "
              f"({len(supported)} figures in the evidence base)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
