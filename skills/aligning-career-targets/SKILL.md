---
name: aligning-career-targets
description: Use when the question is what to apply for rather than whether to apply to one posting — sorting a set of job descriptions into role archetypes, picking a primary and secondary target track, and naming the gap between the candidate's profile and the roles they want.
---

# Aligning career targets

Work out what the candidate should be aiming at, and write it to `profile/career-plan.md`:
a primary track, a secondary track, the gap between where they are and where they want to
be, and whether they are aiming about right. One page, dated.

This is one level up from `assessing-job-fit`. That skill answers "should I apply to *this*
posting" and writes `fit.md`. This one answers "what kind of roles should I be putting
evenings into at all", and it never scores a posting or writes a `fit.md`.

## The rules that keep it honest

> Base every claim strictly on the materials the candidate gave you. Where you are
> inferring, say so; where the information is not there, say that too. A closeable skills
> gap and a values-or-constraint mismatch are different findings — do not blur "you could
> learn this in six months" into "this is not for you". And where money, health, a location
> anchor or visa risk is in play, optimise the recommendation for sustainability, not
> prestige.

## Read first

| File | Required | If missing |
|---|---|---|
| `profile/honest-context.md` | yes | Say so; offer **interviewing-for-context**. This skill reads the honest context; it does not build it. Without it there is nothing to align the targets *to*. |
| `profile/resume.json` | yes | The record the targets get assessed against. **job-search-workspace** covers the import. |
| a set of job descriptions | no | Three to eight, pasted. Without them this is a conversation about what the candidate wants; with them it can name archetypes and gaps concretely. Ask for a handful of the roles they have been eyeing. |
| `profile/career-plan.md` | no | If it exists, read it — you are revising a prior decision, not starting fresh. |
| `profile/preferences.md` | no | Read it if present. |

## How it works

`references/method.md` is the detail. The shape:

1. **Sort the postings into archetypes.** A set of "senior data engineer" ads usually
   splits three or four ways — platform-build, analytics-engineering, streaming
   specialist, generalist-at-a-small-company. Name the clusters and say which postings sit
   in each.
2. **Place the candidate.** Which archetype does the résumé already evidence? Which is a
   stretch, and how far? Go on what is on the page and in the honest context, not on
   potential.
3. **Name the gap, and its kind.** For each thing standing between the candidate and the
   track they want: is it a skill or a piece of experience they can close (roughly how, and
   how long), or is it a mismatch with something they will not compromise on? Those get
   different advice.
4. **Pick a primary and a secondary track.** Primary is where the record and the wants
   line up best right now. Secondary is the fallback or the stretch, with a sentence on
   what makes it second.
5. **Calibrate.** Aiming high, about right, or low — one line, with the reason. The market
   is slow; aiming two rungs above the record burns months.

## Output

Write `profile/career-plan.md`:

```markdown
# Career plan

*Generated <date> · inputs: <files and postings read>*
*Revisit after: a rejection that stung, an offer, or a dealbreaker tested in real life. Stale after about three months.*

## Primary track

One or two sentences: the role archetype to aim at, and why it fits the record and the
honest context.

## Secondary track

One or two sentences: the fallback or the stretch, and what makes it second.

## The gap

- **<skill or experience>** — closeable (how, roughly how long) / not closeable (a values
  or constraint mismatch, not a skills problem).

## Calibration

Aiming high / about right / low — one line, with the reason.

## Sustainability check

The life-context constraints that should override prestige if they ever pull against it.
```

Keep it to a page. If it runs longer, it has turned into advice the candidate will not
re-read.

## Out of scope for v1

- Comparing two live offers against each other. That is its own conversation.
- Whether to change field, retrain, or relocate. This skill works within roughly the
  candidate's current direction, not a reinvention of it.

Say so if the candidate asks for those, rather than half-doing them here.

## Tone

Blunt and specific, the same register as `assessing-job-fit`. "Your streaming experience is
one Kafka transport layer, and the specialist roles want someone who has run Flink in
production" beats "you have some streaming exposure". A plan that only tells the candidate
what they want to hear wastes the months they spend acting on it.

## If the environment has more tools

Nothing here requires them. **Web search** can check what a given archetype's postings
currently ask for, if the candidate has not supplied enough of them — it is not a source of
facts about the candidate. Everything about the candidate comes from the workspace and from
them.

## After writing it

- Tell the candidate the plan is a page they should argue with; expect a correction or two.
- Point out that `assessing-job-fit` will read this file, and `building-a-resume` and
  `writing-a-linkedin-profile` will build toward the primary track.
- Suggest a git commit; do not make one.

## Next

- Know the target, now make the résumé match it → **building-a-resume**, then **roasting-a-resume**
- Target set and there is a posting → **assessing-job-fit**
- Several postings to sort quickly against the plan → **assessing-job-fit**, `references/triage.md`
