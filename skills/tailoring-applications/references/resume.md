# Tailoring the résumé

Output: `applications/<slug>/resume.json`, in JSON Resume format.

Never write to `profile/resume.json`. That is the base, and overwriting it with a
role-specific version poisons every later application.

## Before you start

Read `fit.md` sections 4 and 5. Section 4 lists the strong matches and the gaps as the
employer will see them; section 5 says which strength to lead with and which gap to
address. That is the tailoring brief. Do not re-derive it from the posting.

## What to change

**Reorder before you rewrite.** Most of the gain is in putting the relevant work first —
within a role, the highlight that matches the posting goes first; across the résumé, the
sections the posting cares about come before the ones it does not. Reordering carries no
integrity risk at all.

**Rewrite bullets in STAR form with the outcome quantified.** Situation, task, action,
result — but compressed, so the result is the visible part. "Reduced deployment time by
50%" beats "Was responsible for deployment improvements". If a bullet has no number,
either it should be cut or the candidate should be asked for the number. Do not invent one.

**Open every bullet with a strong past-tense action verb.** Analysed, Built, Cut,
Designed, Delivered, Led, Migrated, Rebuilt, Reduced. No passive voice, no "responsible
for", and no personal pronouns — a résumé has no "I" or "my" in it.

**Lift the posting's vocabulary where it honestly applies.** If the posting says "data
contracts" and the candidate built exactly that but called it "schema agreements", use
their words. This is what gets past keyword filters and it costs nothing in accuracy. If
the candidate did not do the thing, the phrase does not go in — the difference between
tailoring and lying is whether the underlying fact is true.

**Keep bullets to one or two lines.** A three-line bullet is two bullets or one that needs
cutting.

**Rewrite `basics.summary` for this role.** It is the only part of the résumé a human
reads before deciding whether to read the rest. Three or four sentences, leading with
whatever `fit.md` identified as the strongest match.

**Cut.** A tailored résumé is usually shorter than the base. Old roles compress to a line
or two; irrelevant projects come out; the skills block loses the entries nobody is hiring
for here.

**True is necessary, not sufficient.** The integrity rule says never invent. It says
nothing about facts that are true and unhelpful, and that gap is where real damage happens.

A live run put "27 GitHub stars" on a résumé. The number was true and came from the
candidate's own notes. But the base résumé deliberately left it out, and 27 is a small
number: stating it invites the reader to weigh it. "Open-source, OpenAI-compatible API for
agentic multi-model orchestration" is stronger with no count attached.

So, before adding a fact that is not in the base résumé, ask whether it helps. Specifically:

- **A small number is usually worse than no number.** Stars, downloads, team size, users.
  Include a figure when it is impressive on its own, or when the posting asks for scale.
- **If the base résumé omits something the candidate clearly knows**, treat that as a
  decision, not an oversight. Do not reinstate it without asking.
- **Precision cuts both ways.** "Six months" reads shorter than "2024–2025" for the same
  period. Neither is dishonest; pick the one that does not mislead.

Adding a true fact that weakens the application is not a lie, but it is still your mistake.

**Merging roles: write one title, do not concatenate.** Compressing three early jobs into
one entry is usually right. What is not right is joining their titles with commas.

A live run produced `"position": "Embedded Systems Engineer, Software Developer, Software
Developer"`. Honest, and it looks like a software bug on the page.

Write a single title that honestly covers the span: `Software & Embedded Systems Engineer`.
Check the candidate's own files first, because someone who has merged those roles before
has already chosen the wording, and theirs beats yours. Put the individual employers and
dates in the entry body if they matter.

## ATS

Applicant tracking systems parse before a human reads. What breaks them:

- Tables, columns, text boxes, headers and footers, images. None of these are a risk when
  the artifact is JSON Resume — but they are exactly what the PDF template can reintroduce,
  so prefer a single-column template when the résumé is going through an ATS upload.
- Non-standard section names. "Where I've Worked" does not parse; "Experience" does. The
  JSON Resume section names handle this.
- Dates in odd formats. ISO 8601 in the JSON; the exporter renders them.
- Skills invented as a wall of eighty keywords. Filters look for matches in context; a
  keyword dump reads as one to a human and often scores worse.

## Schema

Field names are their own hazard and are documented once, in **job-search-workspace**,
`references/json-resume.md`. The five that cause most of the damage:

`work` not `experience` · `work[].name` is the **company** · `work[].position` is the job
title · `work[].highlights` not `bullets` · `education[].studyType` not `degree`.

Dates are ISO 8601 — `2024`, `2024-06` or `2024-06-29`. A current role **omits**
`endDate`; it does not set it to `"Present"`.

Always validate what you wrote:

```bash
python3 <job-search-workspace>/scripts/validate_resume.py applications/<slug>/resume.json
```

Getting a field name wrong does not produce an error. It produces a résumé with a section
missing, and nobody notices until an employer does.

## Bias

Avoid gendered language and the coded vocabulary that goes with it — "aggressive",
"ninja", "rockstar", "young and dynamic". Describe what was done and what resulted.

This cuts both ways: do not soften a candidate's achievements into collaborative language
either, which is a documented pattern in how résumés get written for women and shows up as
"helped the team deliver" where a man's résumé says "delivered".

## Checking before you hand it over

- Every requirement in the posting that the candidate meets appears somewhere findable.
- Nothing appears that the candidate cannot evidence. Search the output for the skills
  named in `fit.md` as gaps — they should not be there.
- Every bullet starts with a verb and contains no "I".
- The summary would make a hiring manager read the next paragraph.
- It validates.
- It is shorter than the base résumé, or there is a reason it is not.
