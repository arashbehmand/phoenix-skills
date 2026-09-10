#!/usr/bin/env python3
"""Policy checks on the skills themselves.

These guard three things that a live run showed are easy to get wrong and impossible to
notice by reading:

1. The skills must carry no assumption about who the user is. Phoenix hardcoded
   "the applicant is a non-native speaker" because it was built for one person. Voice
   belongs in the user's own profile/tone.md.

2. Private material in honest-context must be framed as background, not as a secret to be
   guarded. Prohibition wording makes a model announce its compliance, and a live session
   wrote the private categories into two more files in order to say it had excluded them.

3. The example workspace must obey its own profile/tone.md. It is the reference; a
   reference that contradicts itself teaches the contradiction.

Usage: python3 check_skills.py [repo-root]
"""

from __future__ import annotations

import pathlib
import re
import sys

# Phrases that assume a fact about the user. Allowed only where the text is explicitly
# quoting Phoenix as the thing not to do.
USER_ASSUMPTIONS = re.compile(
    r"the (applicant|candidate) is a non-native|"
    r"the candidate may be a non-native|"
    r"\bAim at roughly IELTS\b|"
    r"roughly IELTS band \d+, same reasoning",
    re.IGNORECASE)

# Wording that turns background into a secret and invites a compliance announcement.
PROHIBITION = re.compile(
    r"never (leaves|goes to|reaches) (the workspace|an employer)|"
    r"do not quote `?honest-context|"
    r"its wording never reaches",
    re.IGNORECASE)

# Skills that write prose a human reads must point at the tone file.
WRITING_SKILLS = ["tailoring-applications", "drafting-outreach-replies",
                  "writing-a-linkedin-profile"]


def main(root: str = ".") -> int:
    repo = pathlib.Path(root)
    skills = repo / "skills"
    problems: list[str] = []

    for md in sorted(skills.rglob("*.md")):
        text = md.read_text()
        rel = md.relative_to(repo)
        for match in USER_ASSUMPTIONS.finditer(text):
            line_no = text[:match.start()].count("\n") + 1
            line = text.splitlines()[line_no - 1]
            # A cautionary quote names Phoenix or says it was wrong as a rule.
            window = text[max(0, match.start() - 400):match.end() + 400]
            if re.search(r"Phoenix|hardcoded|wrong as a rule|its one user", window):
                continue
            problems.append(f"{rel}:{line_no} assumes who the user is: {line.strip()[:70]}")
        for match in PROHIBITION.finditer(text):
            line_no = text[:match.start()].count("\n") + 1
            problems.append(f"{rel}:{line_no} guards honest-context instead of framing it "
                            f"as background: {match.group(0)!r}")

    for skill in WRITING_SKILLS:
        if not (skills / skill).is_dir():
            problems.append(f"skills/{skill} is missing, so nothing checks its voice")
            continue
        blob = "\n".join(p.read_text() for p in (skills / skill).rglob("*.md"))
        if "profile/tone.md" not in blob:
            problems.append(f"skills/{skill} writes prose but never reads profile/tone.md")

    # The example workspace must follow its own tone file.
    tone = repo / "examples/workspace/profile/tone.md"
    if tone.exists():
        forbids_emdash = "em-dash" in tone.read_text().lower()
        outbound = list((repo / "examples/workspace/applications").glob("*/cover-letter.md"))
        outbound += list((repo / "examples/workspace/applications").glob("*/questions.md"))
        outbound += [tone]
        # The LinkedIn profile is published copy strangers read, same as a cover letter.
        # honest-context.md / career-plan.md / resume-notes.md are private and not checked.
        linkedin = repo / "examples/workspace/profile/linkedin.md"
        if linkedin.exists():
            outbound += [linkedin]
        else:
            problems.append("examples/workspace/profile/linkedin.md is missing; the "
                            "published-copy check has nothing to run on")
        if forbids_emdash:
            for f in outbound:
                n = f.read_text().count("—")
                if n:
                    problems.append(f"{f.relative_to(repo)} has {n} em-dash(es); "
                                    f"profile/tone.md forbids them")
    else:
        problems.append("examples/workspace/profile/tone.md is missing")

    for p in problems:
        print(f"  FAIL  {p}")
    if not problems:
        print("  ok    skills carry no assumption about the user, honest-context reads as "
              "background,\n        and the example obeys its own tone file")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
