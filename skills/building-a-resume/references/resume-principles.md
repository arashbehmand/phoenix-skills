# Résumé principles

The rules that hold whether you are building the base résumé or tailoring a copy to a
posting. **building-a-resume** works from these directly; **tailoring-applications**,
`references/resume.md` reads them and adds the posting-specific brief on top.

Output is always JSON Resume. Field names are documented once, in **job-search-workspace**,
`references/json-resume.md`; the five that cause the most damage are repeated at the end.

## Bullets

**One or two lines each.** A three-line bullet is two bullets, or one that needs cutting.

**Verb first, past tense, no "I".** Analysed, Built, Cut, Delivered, Designed, Drove, Led,
Migrated, Rebuilt, Reduced, Shipped. No "responsible for", no "worked on", no personal
pronouns — a résumé has no "I" or "my" in it.

**STAR, compressed so the result is the visible part.** Situation and task in a clause,
action in the verb, result with a number. "Cut deployment time 50% by rebuilding the
release pipeline around blue-green cutover" beats "Was responsible for improving
deployments".

**Every bullet wants a number, and you must not invent one.** If a bullet has no figure,
either it should be cut or the candidate has the number and has not written it down — ask.
Do not reach for a plausible one. A `[metric]` placeholder is a to-do, not a value, and a
base résumé does not ship with one still in it.

**3 to 5 bullets per recent role, 3 to 4 projects.** More than that and the reader stops
reading. Old roles compress to a line.

## True is necessary, not sufficient

The integrity rule says never invent. It says nothing about facts that are true and
unhelpful, and that gap is where real damage happens.

A live run put "27 GitHub stars" on a résumé. The number was true and came from the
candidate's own notes. But the base résumé deliberately left it out, and 27 is a small
number: stating it invites the reader to weigh it. "Open-source, OpenAI-compatible API for
agentic multi-model orchestration" is stronger with no count attached.

Before adding a fact that is not already on the résumé, ask whether it helps:

- **A small number is usually worse than no number.** Stars, downloads, team size, users.
  Include a figure when it is impressive on its own, or when the target asks for scale.
- **If the base résumé omits something the candidate clearly knows, treat that as a
  decision, not an oversight.** Do not reinstate it without asking. `profile/resume-notes.md`
  is where those decisions are recorded — read it.
- **Precision cuts both ways.** "Six months" reads shorter than "2024–2025" for the same
  period. Neither is dishonest; pick the one that does not mislead.

Adding a true fact that weakens the application is not a lie, but it is still a mistake.

## Merging roles: one title, do not concatenate

Compressing three early jobs into one entry is usually right. Joining their titles with
commas is not.

A live run produced `"position": "Embedded Systems Engineer, Software Developer, Software
Developer"`. Honest, and it looks like a bug on the page.

Write a single title that honestly covers the span — `Software & Embedded Systems
Engineer`. Check the candidate's own files first: someone who has merged those roles before
has already chosen the wording, and theirs beats yours. Put the individual employers and
dates in the entry body if they matter.

## ATS, in 2026

Applicant tracking systems parse the file before a human reads it, and then a human reads
it. Both stages have moved on from the advice that is still everywhere.

- **Stuffing keywords is not the win it is sold as.** The advice to repeat a term until the
  parser notices is old, and the systems have been moving against it for years. Exactly how
  much any one of them docks for density is not knowable from outside, so do not plan
  around a number. Plan around the part that is certain: a person reads the file after the
  parser does, and a term used more often than natural writing would produce it is obvious
  to them. Use a skill or tool name **once, in context, on the bullet where the candidate
  actually did the thing.** Three genuine uses beat ten. A "Skills" wall of eighty keywords
  reads as padding to a parser and as noise to a human.
- **The rejection is still a human's.** The parser feeds a database; a person searches it
  and decides. A résumé does not get auto-binned for a missing keyword nearly as often as
  the internet claims — but a person who sees keyword-stuffing stops reading.
- **Standard section names.** "Where I've Worked" does not parse; "Experience" does. JSON
  Resume's section names are already right.
- **ISO 8601 dates** in the JSON; the exporter renders them. A current role omits
  `endDate` rather than setting it to "Present".
- **Single-column layout** when the PDF is going through an upload. Tables, columns, text
  boxes, headers and footers, and images are not a risk in the JSON, but a PDF template can
  reintroduce them.

This section is dated in its heading on purpose. The mechanics move every year or two; the
direction has been steady for a decade, which is less gaming and more writing. Where a rule
here stops matching what candidates actually report back, believe them and change it.

## Do not let it read as generated

Recruiters now read a great many applications a model wrote, and they have got fast at
spotting them. Some bin those on sight. More simply discount everything on the page,
including the parts that are true and took years to earn. The candidate pays either way,
and the fix costs nothing. The moves that matter:

- **Vary the bullets.** Not every one opening "Built / Developed / Led / Implemented". Not
  every one the same length.
- **Cut the buzzwords.** "spearheaded", "leveraged", "passionate about", "innovative",
  "cutting-edge", "seamless", "expertise in", "results-driven". Say what was done.
- **No objective statement.** "Seeking a challenging role that leverages my skills in…" is
  dead weight.
- **Earn the claims.** Replace "picks up new tools quickly" with the time they shipped in
  an unfamiliar stack.
- **No suspiciously round or extreme numbers.** "Improved performance 40x" reads as
  invented unless the context makes it obviously real. Every number has to survive the
  candidate explaining it for thirty minutes in an interview.
- **Collapse ancient history.** Everything past about eight years ago is a short "Early
  career" line unless a specific role still earns its place.

## Bias

Avoid gendered and coded vocabulary — "aggressive", "ninja", "rockstar", "young and
dynamic". Describe what was done and what resulted.

This cuts both ways: do not soften a candidate's achievements into collaborative language
either. "Helped the team deliver" where the work was "delivered" is a documented pattern in
how résumés get written for women, and it costs them.

## The five field names that bite

`work` not `experience` · `work[].name` is the **company** · `work[].position` is the job
title · `work[].highlights` not `bullets` · `education[].studyType` not `degree`.

Dates are ISO 8601 — `2024`, `2024-06`, or `2024-06-29`. Validate every file:

```bash
python3 <job-search-workspace>/scripts/validate_resume.py <path>
```

Getting a field name wrong does not raise an error. It produces a résumé with a section
silently missing.
