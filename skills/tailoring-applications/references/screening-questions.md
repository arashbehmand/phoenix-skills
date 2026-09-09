# Screening question answers

Output: `applications/<slug>/questions.md`.

These are the free-text questions on an application form — "Why do you want to work here?",
"Describe a time you…", "Do you require sponsorship?". They are read by a filter first and
a person second, often the shortest-attention reader in the process.

## Format

One `###` heading per question, carrying the question text as it appeared on the form,
followed immediately by the answer.

```markdown
### Why do you want to work at <Company>?

<answer>

### Describe a time you migrated a production system without downtime.

<answer>
```

Use the form's exact wording in the heading. When the candidate copies an answer back, the
heading is how they find the right one, and a paraphrased question makes that harder.

Do not restate the instructions, and do not preface answers with "Great question" or
"Certainly".

## The answers

**Three to five sentences**, unless the question asks for more or specifies a word count.
These forms are read fast. A twelve-sentence answer to a four-sentence question reads as
someone who cannot judge what matters.

**Evidence, in STAR form, with real numbers.** Situation, task, action, result, compressed
so the result is visible. Take the numbers from `profile/resume.json` or
`applications/<slug>/resume.json`. If an answer needs a number nobody has, ask the
candidate — do not estimate one.

**Use the posting's vocabulary naturally.** Some of these forms are keyword-filtered before
anyone reads them, and the terms the posting uses are the ones being matched. Naturally is
the operative word: an answer stuffed with terminology reads badly to the human who gets it
next.

**Company values, where they are real.** If `research/<company>.md` has verified values or
culture signals, use them. If it does not, do not invent them — an answer praising a value
the company has never claimed is worse than an answer that does not mention values at all.

**Plain professional language**, roughly IELTS band 7, same reasoning as the cover letter:
the answer has to sound like the person who then turns up to the interview.

**Answer the question that was asked.** Screening questions are frequently answered
sideways — "Describe a conflict with a colleague" gets an answer about a technical
challenge. Answer the actual question, including when it is uncomfortable.

## Honesty

Base every answer strictly on what is in the workspace. Do not invent experience.

When the honest answer to a question is weak, **give the weak honest answer and flag it**
so the candidate can decide. Do not quietly upgrade it. A flag looks like:

> *This answer is thin — the strongest example available is from 2019. Worth adding
> something more recent if you have one.*

Keep the flag out of the answer itself; put it after, in italics, so the answer can be
copied cleanly.

## Specific question types

**"Do you require visa sponsorship?"** — answer from `honest-context.md`, exactly and
without hedging. This question exists to filter, and a vague answer gets read as the
expensive one. State the current status, what would be needed, and whether relocation is
involved.

**"What are your salary expectations?"** — check `honest-context.md` for a floor and
`preferences.md` for how the candidate wants this handled. If the posting has a band and it
clears the floor, engaging with the band is usually right. If there is no band, a range or
a deferral both work; the candidate's stated preference decides. Never write a number below
their floor.

**"Why are you leaving your current role?"** — honest, brief, forward-looking, and never
critical of the current employer. `honest-context.md` usually has the real reason; the
answer is the professional version of the true reason, not a different reason.

**"Why us?"** — needs one specific thing from `job.md` or `research/<company>.md`. Without
one, this answer is interchangeable with every other candidate's.

**Anything with a word or character limit** — respect it exactly. An answer truncated by
the form is worse than a short one.

## Before handing over

- Every question from the form has an answer.
- No answer contradicts the résumé or the cover letter.
- Nothing is invented, and weak answers are flagged rather than inflated.
- Each answer is in the three-to-five sentence range unless there was a reason.
- Answers can be copied and pasted without editing out commentary.
