# Notes — Kestrel Labs, Senior Data Engineer (Streaming Platform)

## Status

`interviewing` — round 2 of 5.

## Timeline

- **2026-08-24** — Found the posting on the company careers page. Saved `job.md`, parsed to
  `job.json`. Checked the gov.uk sponsor register the same day: Kestrel Labs Ltd is listed,
  Worker route, A rating.
- **2026-08-25** — Ran the fit analysis. `STRONGLY APPLY`, confidence Medium, 65% match.
  The location question came out of it as the thing to resolve first.
- **2026-08-26** — Tailored résumé, cover letter, screening answers. Applied.
- **2026-09-01** — Priya Raman (Talent Partner) made contact. Location question answered:
  Farringdon specifically, Tuesdays fixed, travel expensed, second day flexible.
- **2026-09-03** — Intro call. Went fine.
- **2026-09-04** — Moved to technical round.
- **2026-09-06** — Dev Raghunathan messaged directly. One design problem, bring a drawing
  surface.
- **2026-09-08** — Interview prep guide generated.
- **2026-09-11 14:00** — Round 2, with Dev. The design problem.

## Next

- **by 2026-09-10 10:00** — Chase Priya for the second interviewer's name and focus. She
  said Monday and it has not come through.
- **by 2026-09-10** — Fill in the bracket in Talking Point 4 of `interview-prep.md`: what I
  would actually do about the Kubernetes gap in the first month. Not generated on purpose —
  it has to be my own plan or it will not survive a follow-up question.
- Ask about the on-call design in round 3, not round 2. It is a "how do you work" question
  and the Head of Platform is the right person for it.

## Revision log

*Every edit to a generated artifact gets a line here, with the instruction as it was given.
Before revising anything, re-read the original brief **and every prior instruction in this
log** — otherwise revision N quietly undoes the fix from revision N−2. This is the file
that replaces Phoenix's `refinement_history` column.*

### cover-letter.md

- **v1, 2026-08-26** — Generated from `job.md` + `profile/resume.json` +
  `profile/honest-context.md` + `fit.md`.
- **v2, 2026-08-26** — "Too long and the second paragraph is three separate ideas. Cut to
  three paragraphs. Keep the 6h10m → 1h50m number, it's the strongest thing in there."
- **v3, 2026-08-26** — "Put the Kubernetes and Flink gaps in explicitly. I'd rather lose
  the interview now than in round two." *(Note for future revisions: do not remove this.
  It reads risky and a later 'make it more confident' instruction would strip it out —
  that is exactly the regression this log exists to prevent.)*
- **v4, 2026-08-26** — "Third paragraph sounded like a mission-statement quote. Make it
  shorter and end on a real question."

### resume.json

- **v1, 2026-08-26** — Tailored from `profile/resume.json` against `job.json`.
- **v2, 2026-08-26** — "Lead every Halcyon bullet with the migration, not the tooling. And
  the summary buried the migration in the third sentence."
- **v3, 2026-08-26** — "You added 'Kubernetes (working knowledge)' to the skills block.
  Remove it. I have never operated a cluster and I am not implying I have."
  *(Standing rule: nothing goes in this file that is not in `profile/resume.json` or that I
  have not confirmed. Re-check this on every regeneration.)*

### interview-prep.md

- **v1, 2026-09-08** — Generated. Left the interviewer-specific section empty on purpose;
  Priya has not confirmed the second interviewer yet.

## Things not to forget

- Do not say "spearheaded."
- The reconciliation period is the impressive part of the migration story, not the runtime
  number. Lead with the six-week parallel run.
