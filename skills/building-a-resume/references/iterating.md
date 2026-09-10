# The build loop

How to make changes to `profile/resume.json` so the candidate can follow what changed and
why, and so the file gets better rather than just different.

## One change, three lines

Every proposed edit is a triplet:

```
Original:  Responsible for the data pipeline and its maintenance.
Optimised: Rebuilt the ingestion pipeline around change-data-capture, cutting nightly
           batch time from 6h to 40min.
Rationale: STAR with the result first (resume-principles.md, "Bullets"). "Rebuilt" and
           the two numbers replace "responsible for". The 6h -> 40min is the candidate's,
           confirmed in this session.
```

The rationale names the principle it serves and, when a number is involved, where the
number came from. If the candidate does not have the number, the Optimised line carries a
`[metric]` placeholder and the rationale says so — it is a to-do left in the open, not a
gap to paper over.

Group triplets by section when there are several. Do not rewrite the whole résumé in one
pass and hand it back; the candidate cannot see what moved.

## Risk Note

Some edits are a judgement call with a real downside. Flag those instead of making the call
silently:

```
Risk Note: Dropping the 2011 graduation year removes an age signal, which usually helps.
           It also leaves a fifteen-year career with no start date, which a careful reader
           notices. Your call.
```

Cases that earn a Risk Note: dropping graduation years, leaving a short or awkward role
off entirely, cutting a project the candidate is attached to, merging roles under one
title, moving a contract role's framing between "employee" and "independent". Present the
trade-off in a sentence or two and let the candidate decide.

## Master and variant

`profile/resume.json` is the master: everything true and worth keeping, in the best general
form. It can run longer than a résumé you would actually submit — `tailoring-applications`
selects and trims from it per posting.

A second base — `profile/resume-<track>.json` — is allowed only when
`aligning-career-targets` has named a genuine second track that needs a different lead and
a different ordering, not just different wording. One variant at most. If you find yourself
wanting a third, the honest answer is usually that the tailoring step is where the
per-target work belongs.

## When to stop

A base résumé improves fast for the first pass or two and then starts going sideways:
synonyms swapped for synonyms, a bullet reworded to undo last round's rewording, length
traded back and forth. When the edits stop changing how a hiring manager would read the
page, stop, and say so. Come back to it after a roast, or after the next real role goes on
it, not the same afternoon.

## What not to do here

- Do not tailor to a posting. If a posting is in play, that is `tailoring-applications`,
  working on a copy.
- Do not add a skill or a tool because it is in demand. If it is not something the
  candidate did, it does not go on, however the market is trending.
- Do not quietly reinstate something the `## Decisions held` log says was left off. If you
  think the decision was wrong, say so and ask.
