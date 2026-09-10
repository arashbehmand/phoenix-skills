---
name: tailoring-applications
description: Use when applying to a specific job — tailoring a résumé to a posting, writing a cover letter for it, or answering the screening questions on its application form.
---

# Tailoring applications

Three artifacts, same inputs, one job:

| Output | Path | Reference |
|---|---|---|
| Tailored résumé | `applications/<slug>/resume.json` | `references/resume.md` |
| Cover letter | `applications/<slug>/cover-letter.md` | `references/cover-letter.md` |
| Screening answers | `applications/<slug>/questions.md` | `references/screening-questions.md` |

Read the reference for whichever is being produced. They share the inputs and the
integrity rule below; everything else differs.

Not all three are always wanted. Many applications need only the résumé. Produce what was
asked for, and mention the others exist rather than generating them unasked.

## The rule that outranks everything else

> **Integrity**: NEVER invent or exaggerate experience. Optimize the presentation of existing facts.
>
> **Bias Mitigation**: Avoid gendered or biased language.

This is not boilerplate. The pressure to break it is structural: a posting lists ten
requirements, the candidate meets seven, and every instinct in a language model is to
close the gap with language. Do not.

What this rules out, concretely:

- Adding a skill to the résumé because the posting asks for it. If it is not in
  `profile/resume.json` or `profile/honest-context.md`, it does not go in.
- Upgrading "worked with" into "owned", or "contributed to" into "led".
- Inventing a number. If a bullet needs a metric to land, **ask the candidate for it** —
  they usually know it, and a real number is better than the one you would have guessed.
- Widening a date range, or leaving out an end date so a role reads as current.
- Answering a screening question with an experience the candidate does not have.

What it permits, and what the job actually is:

- Reordering, so the relevant work is first.
- Rewriting a bullet to lead with the outcome the posting cares about.
- Using the posting's own vocabulary for something the candidate genuinely did.
- Cutting what is irrelevant to this role.
- Saying a gap out loud, when the candidate has decided to be upfront about it.

If a posting's central requirement is genuinely absent, say so before writing anything.
That is a `fit.md` finding, and it may mean the application is not worth making.

## Read first

| File | Required | If missing |
|---|---|---|
| `applications/<slug>/fit.md` | **yes** | Run **assessing-job-fit** first. |
| `applications/<slug>/job.md` | yes | Ask for the posting. |
| `profile/resume.json` | yes | See **job-search-workspace**. |
| `profile/honest-context.md` | yes | Say so; offer to write one. |
| `profile/tone.md` | yes, if writing prose | **Read before writing.** It decides the voice. Absent, default to plain and say so. |
| `profile/preferences.md` | no | Read it if present — it is where standing instructions live. |
| `research/<company>.md` | no | Read it if present. |
| `applications/<slug>/contacts.md` | no | Read it if present; a prior exchange changes the tone and may already have committed to something. |
| `applications/<slug>/notes.md` | no | **Read the revision log before editing an existing artifact.** |

**`fit.md` is a real prerequisite, not a nicety.** Phoenix listed it as a required input
for both the cover letter and the tailored résumé, so the fit analysis always ran first.
It carries the decisions that make tailoring good rather than generic: which strength to
lead with, which gap to address and how, and what the candidate is actually walking into.
Without it you are pattern-matching a résumé against a posting, which is what every
free tool already does badly.

## Order

Résumé first, then cover letter, then screening answers. The cover letter should not claim
anything the tailored résumé does not support, and the screening answers should not
contradict either. Working in this order makes that automatic.

## Revising

Before editing any of these files, read the revision log in `notes.md` — all of it — and
apply the new instruction on top of every earlier one. Then append a line recording what
was asked, in the candidate's own words.

This matters most here. The realistic failure: the candidate says "put the skills gap in
explicitly, I'd rather lose the interview now than in round two", and three revisions later
says "make it sound more confident" — and the disclosure quietly disappears, because
nothing carried the earlier instruction forward. When an instruction exists to keep
something uncomfortable in, note that in the log.

## After writing

- Validate any `resume.json` you wrote:
  `python3 <job-search-workspace>/scripts/validate_resume.py applications/<slug>/resume.json`
- Update `applications.md` — stage `applied` once it has actually gone in, with the date.
- Add a dated line to `notes.md`, and put anything still owed — a form to finish, a
  portfolio link to send — under `## Next`.
- Read the cover letter back to the candidate before it is sent anywhere. Do not send
  anything on their behalf without being asked to.

## If the environment has more tools

Genuinely none needed — this skill reads local files and writes local files, and the only
executable it uses is the résumé validator, which is standard library and offline.

A filesystem MCP server is fine if that is how the workspace is reached. Do not reach for
web search to "check" a claim about the candidate: the workspace is the source of truth
about them, and anything not in it needs to come from the candidate, not the internet.

## Next

- Application submitted, interview booked → **preparing-for-interviews**
- A recruiter replied → **drafting-outreach-replies**
- Need a PDF → **job-search-workspace**, `references/reactive-resume-export.md`
