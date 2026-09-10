# Triage — reading several postings at once

The full analysis is a five-section instrument with ratings, a match percentage, a
confidence score and a sponsor check. It is the right tool for a posting somebody is
seriously considering and the wrong one for eleven open tabs.

Triage decides which postings earn that evening. It is a skim, deliberately.

## When

- More than about three postings handed over at once.
- "Which of these is worth a look", or a pile pasted with no question attached.

**One posting is not triage.** The full analysis takes a few minutes and is better. If the
user has already decided to apply, skip both and go to **tailoring-applications**.

## Read

`profile/honest-context.md` and `profile/resume.json`. Nothing else.

No research files, no sponsor register lookups, no fetching the company. Those are
per-company and turn a five-minute skim into an afternoon. They belong in the full analysis,
once the list is down to three.

A dealbreaker visible in the posting text itself still counts — that costs nothing to read.

## Produce

A table, one row per posting:

| Role | Score | Why | Action |
|---|---|---|---|
| Senior Data Engineer, Kestrel Labs | 65 | Streaming platform being built, Kafka depth matches. No Kubernetes, no Flink. | full analysis |
| Analytics Engineer, Trellis Bio | 80 | Strongest paper match here. Cannot sponsor. | drop |
| Data Platform Engineer, Orbital | 70 | Right direction, explicitly flexible on the streaming gap. Leeds three days. | full analysis |
| BI Developer, Marchetti | 35 | Reporting role with a platform title. | drop |

**The score answers the same question as section 4 of the full analysis** — not "could they
do this job" but "will the person reading this résumé think so".

Be harsh. Triage exists to spend attention, and a column where everything is a 70 has spent
none. If several genuinely tie, say that instead of inventing separation.

**Actions are one of three:**

- `full analysis` — worth the evening
- `park` — plausible but not now, and the reason has to be real: waiting on something,
  worse than another live option, closing date far out. Not indecision.
- `drop` — with the reason in the same line

## The rule that makes triage safe

**A dealbreaker in `honest-context.md` is a `drop` whatever the number says.** No softening
it into "worth a conversation".

The worked Trellis Bio case is exactly this: 80% on paper, the strongest match in the
folder, and an immediate no because the employer cannot sponsor. A triage that promotes it
on the score has cost the candidate an evening and then a rejection.

## What triage does not do

- **It writes nothing.** No `fit.md`, no folders, no files. It is a conversation.
- **Its number is not the `Estimated Match %`.** That figure comes out of the full analysis
  against the honest context and the company. Copying a skim score into a `fit.md` launders
  a guess into a finding. Never do it.
- **It does not research.** No claims about funding, culture or stability from anywhere but
  the posting. If a posting is too thin to judge, the honest row says so and the action is
  `full analysis` if the role looks right — "cannot tell" is not the same as "no".
- **It does not rank on salary.** A band above the floor is a gate, not a score.

## Close

Name the ones worth the full analysis, in the order to do them, and ask which to start with.

Then offer to keep the result, because triage that evaporates was wasted:

- Postings going to the full analysis → save into `applications/<slug>/job.md` and add the
  row to `applications.md` at `interested`. See **job-search-workspace**.
- Anything dropped **on a dealbreaker** → worth a `closed` row with the reason, for the same
  reason the Trellis Bio folder is kept: it stops the same posting being reconsidered in a
  month because the score looked good.
- Everything else dropped → no record needed.
