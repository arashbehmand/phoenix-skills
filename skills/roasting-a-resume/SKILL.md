---
name: roasting-a-resume
description: Use when the candidate wants an adversarial read of their résumé or LinkedIn before applying anywhere — a blunt line-by-line critique, a second opinion on an automated résumé score, or a check on whether they can defend every claim in an interview.
---

# Roasting a résumé

Read the candidate's résumé — or their LinkedIn profile — the way a sceptical recruiter
would, and say what is wrong with it. Blunt, specific, line by line. This writes nothing by
default; it is a critique to act on, not a document to keep.

`building-a-resume` is where the fixes get made. Roast diverges — finds everything wrong;
build converges — decides what to change. Run roast, then build, then roast again if it
helps.

## The bar

> The test for every number and every claim: **could the candidate talk about this for
> thirty minutes in a behavioural interview without it falling apart?** If not, it is a
> liability on the page, not an asset. And the usual failure is not lying — it is
> underselling the real work while overselling the packaging. A roast has to tell those two
> apart, and it has to name what is already good, or the next edit strips it out.

## Read first

| File | Required | If missing |
|---|---|---|
| `profile/resume.json` | yes | Nothing to roast. **job-search-workspace** covers the import. A LinkedIn export pasted in works too. |
| `profile/honest-context.md` | yes | Say so; offer **interviewing-for-context**. Without it a roast cannot tell a thin claim from a solid one that is undersold, and turns into generic résumé advice. |
| `profile/career-plan.md` | no | Read if present — it says which roles the résumé is being judged against. Absent, ask before starting. |
| `profile/preferences.md` | no | Length, banned words, what to lead with. A roast should not fight a standing decision. |
| `profile/resume-notes.md` | no | Read `## Decisions held` if present, so the roast does not re-flag something already settled. |
| an automated résumé score or ATS report | no | Pasted in. Sort its real findings from its noise before acting on any of it — see below. |

## What a roast produces

All in the conversation. Nothing is written unless the candidate asks (see the last
section) — a critique is stale the moment it is acted on, and the decisions that outlast it
belong in `profile/resume-notes.md`, which **building-a-resume** reads.

1. **The roast.** Numbered. Each item: quote the line, say how a recruiter for the target
   roles reads it, then the fix. `references/rubric.md` is the checklist of what to go
   after.
2. **What is already good.** A short list of what not to touch. A roast that is all attack
   gets the candidate to strip out their best material in the next pass.
3. **A prioritised action list.**
   - **Critical** — fix before applying anywhere. Rough minutes each.
   - **High** — worth doing this week.
   - **Polish** — next iteration, marginal.
4. **One honest closing line.** Usually some version of which way the résumé is
   miscalibrated: underselling the substance, overselling the packaging, aimed at the
   wrong level.

## A pasted résumé score

Tools like Jobscan, Resume Worded and the rest produce a mix of real findings and noise.
Before acting on any of it:

- **Noise, usually:** a fixed keyword-match percentage, "add more keywords", a hard word
  count, "remove the second page", a demand for a skills wall. Density is penalised now,
  not rewarded (`building-a-resume/references/resume-principles.md`).
- **Signal, usually:** a specific term the candidate genuinely has experience in and did
  not mention; a bullet with no verb; a date-format inconsistency; passive voice; an
  actual parsing failure.

Put the noise in a short "ignore these, and why" list, and roast only the rest.

## Not the same as assessing-job-fit

`assessing-job-fit` section 4 reads the résumé against **one posting** — match this
candidate to this job. A roast reads the résumé **cold**, against the kind of roles the
candidate is aiming at, with no posting in play. If there is a specific posting, that is
`assessing-job-fit`, and then `tailoring-applications`.

## Tone

The candidate asked to be roasted; do it. Blunt, specific, no cushioning clause before the
criticism. Quote the offending line so it is unambiguous. But every item gets a fix, and
the "what is good" list is not optional — a roast the candidate cannot act on is just
discouraging.

Do not roast the person. "This bullet claims architecture ownership the rest of the résumé
does not support" is the job. "You clearly overreached here" is not.

## If the candidate wants it written down

Offer to append a dated block to `profile/resume-notes.md`: the action list, and — the part
that matters later — anything the roast raised that the candidate has decided **not** to
act on, and why. That is what stops the same point being re-raised every time the résumé is
opened. Ask first, and write it in their words.

## If the environment has more tools

Nothing here requires them. This reads local files and talks. Web search is not a way to
check a claim about the candidate — that comes from the workspace and from them. If a
LinkedIn MCP server is already running and the candidate wants their live profile roasted,
pulling the text that way is fine; their account, their call.

## Next

- Act on the roast → **building-a-resume**
- Same lens on the public profile → **writing-a-linkedin-profile**
- The roast keeps landing on "you are aiming at the wrong roles" → **aligning-career-targets**
