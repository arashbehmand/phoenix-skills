---
name: assessing-job-fit
description: Use when there is a job posting in hand and the question is whether to apply at all — before tailoring a résumé, writing a cover letter, answering screening questions, or replying to a recruiter about a specific role.
---

# Assessing job fit

Produce an honest go/no-go on a specific posting and write it to
`applications/<company>-<role>/fit.md`.

This is the hub of the workspace. `tailoring-applications` and
`preparing-for-interviews` both read `fit.md`, and Phoenix required it before it would
write a cover letter or a tailored résumé — so the fit analysis silently ran first, every
time. That dependency is worth keeping explicit: tailoring an application to a job the
candidate should not take is the most expensive kind of wasted evening.

## The structural idea

Four questions get conflated into "is this a good opportunity", and separating them is
most of the value here:

1. **Is this a good job?** — the role on its own terms, regardless of who is offering it.
2. **Is this a good company?** — the employer, regardless of this particular role.
3. **Is this a good job for *me*?** — against what this candidate actually wants and will
   not accept.
4. **Am I a good fit — as they will see me?** — not "could I do the job", but "will the
   person reading this résumé think so".

A role can score well on 1 and 2 and still be wrong on 3. A candidate can be right for a
job on 4 and still be reading a bad one on 1. Answer them separately and say so when they
disagree.

## Several postings at once

More than about three postings, or "which of these is worth a look", is triage rather than
analysis: a line each, a score, and a decision about which ones earn the full treatment.
`references/triage.md` is the procedure.

Two things belong here rather than only there. A dealbreaker is a `drop` whatever the score
says — the same rule as below. And triage writes nothing: its number is a skim, not the
`Estimated Match %`, and copying it into a `fit.md` turns a guess into a finding.

## Read first

| File | Required | If missing |
|---|---|---|
| `applications/<slug>/job.md` | yes | There is nothing to assess. Ask for the posting. |
| `profile/resume.json` | yes | Ask for it; **job-search-workspace** covers the import. |
| `profile/honest-context.md` | yes | Say so and offer to write one. See below. |
| `research/<company>.md` | no | Mark section 2 "not assessed" and say why. |
| the UK sponsor register | when sponsorship is a stated constraint | Run the lookup below — do **not** write "could not be checked". |
| `profile/preferences.md` | no | Skip. |
| `applications/<slug>/contacts.md` | no | Read it if present — it tells you what stage this is at and what has already been said. |
| `applications/<slug>/notes.md` | no | Read it if present. |

**Without `honest-context.md` this skill degrades into a generic résumé-to-posting
comparison**, which is worth very little — the model has no idea what the candidate wants,
what they will not accept, or what they are weak at. Say that plainly and offer to run the
interview in `job-search-workspace`, `references/honest-context-interview.md` — fifteen
minutes of it is enough to make this analysis worth reading. Do not silently substitute
plausible assumptions about someone's salary expectations or visa situation.

If there is no company research, do not invent it. Section 2 says what could not be
assessed and section 0's confidence score drops accordingly. Offer to run
**researching-companies** first — for anything past a first-round conversation it is worth
the ten minutes.

## Check the hard constraints before anything else

`honest-context.md` usually names some hard limits, and what they are differs completely
per person: work authorisation, a salary floor, a commute, a sector, a shift pattern, a
notice period. Do not go looking for a fixed set. Read what this person wrote, and check it
against the posting first.

When one is clearly violated, say so in the verdict and keep the rest of the analysis
short. Still write the file, and still record the match percentage: a posting that is an
80% match on paper and an immediate `AVOID` on a dealbreaker is exactly the one that gets
reconsidered in a month, and the record is what prevents that.

Do not soften a dealbreaker into a "consideration". If the candidate wrote that they need
visa sponsorship and the posting says sponsorship is not available, that is the answer,
and three paragraphs of encouragement around it wastes their evening.

**Work authorisation is checkable, so check it rather than deferring it.** When
`honest-context.md` says the candidate needs sponsorship and the employer is UK-based, the
**researching-companies** skill ships a credential-free lookup against the Home Office
register:

```bash
python3 <researching-companies>/scripts/uk_visa_sponsor_lookup.py "<company>" --town "<city>"
```

It needs one request to gov.uk and no key. Recording "sponsorship could not be verified"
in `fit.md` when that lookup was available is a worse outcome than a slow answer — it goes
into the permanent record and the question gets re-asked every time the file is read. If
the lookup genuinely cannot run, say which of the two it is: not run, or run and
inconclusive.

## Work through it in this order

1. **Job quality audit.** Read the posting for red flags, unrealistic requirements, and
   vagueness. Three jobs bundled into one description. A seniority level that does not
   match the responsibilities. Salary absent. Assess the role's actual impact and market
   value.
2. **Company health check.** Stability, growth, market position, culture — from the
   research file if there is one, and from the posting's own language if there is not.
3. **Personal alignment.** Against `honest-context.md` specifically. Not "is this a good
   career move" in the abstract — does it serve what this person said they want.
4. **Candidate fit, as they will see it.** Go requirement by requirement. Score what is
   actually evidenced in the résumé, not what the candidate could probably do.
5. **Synthesise.** Combine into one recommendation.

## Output

Write `applications/<company>-<role>/fit.md` in exactly this structure. The headings are a
contract — other skills read this file.

```markdown
# 🎯 Strategic Career Analysis

*<Company> — <Role>*
*Generated <date> · inputs: <the files actually read>*

## 0. Executive Verdict

*   **Recommendation:** [**STRONGLY APPLY** / **PROCEED WITH CAUTION** / **AVOID**]
*   **Confidence Score:** [High/Medium/Low]
*   **Summary:** A 2-sentence bottom line on why this is the verdict.

## 1. Is this a good job? (Role Analysis)
*Objective assessment of the role itself.*
*   **Pros:** (e.g., "High-impact role," "modern tech stack").
*   **Cons/Risks:** (e.g., "Vague responsibilities," "Seems like three jobs in one").
*   **Rating:** [1-10]

## 2. Is this a good company? (Corporate Analysis)
*Assessment of the employer.*
*   **Market Position:** (e.g., "Market leader," "Struggling startup").
*   **Culture Signals:** (e.g., "Values innovation," "Reviews suggest burnout").
*   **Rating:** [1-10]

## 3. Is this a good job for *me*? (Personal Alignment)
*Based on your Honest Context and Resume.*
*   **Alignment:** (e.g., "Matches your goal to move into mgmt").
*   **Misalignment:** (e.g., "Requires travel you wanted to avoid").
*   **Verdict:** [Strong/Weak/Neutral]

## 4. Am I a good fit for this position? (Candidate Fit)
*Based on how they will see you.*
*   **Strong Matches:** (Your X experience perfectly fits their Y need).
*   **Gaps/Weaknesses:** (You lack Z which is listed as required).
*   **Estimated Match %:** [e.g., 85%]

## 5. Strategic Advice
*   **If applying:** Focus on [Key Strength]. Address [Key Gap].
*   **Key Question to Ask:** One critical question to ask them to verify assumptions.
```

The inputs line matters. Six months later the question "was this written before or after
the company research" has an answer.

**Estimated Match %** is how the hiring side will read the résumé against the
requirements, not how well the candidate would do the job. Those differ, often by a lot,
and conflating them is how people talk themselves into applications that get filtered out
at the first automated pass.

**Key Question to Ask** is one question, chosen because its answer would change the
verdict. Not a list, and not something the posting already answers. If the analysis turned
up an assumption the whole thing rests on, that assumption is the question.

## Tone

Blunt, compact, honest. Brief actionable advice, no fluff, no sugar-coating, no
unnecessary explanation. Assume the candidate is in a hurry.

Be brutally honest — a career consultant who only agrees with you is worth nothing. If a
required skill is missing, say it is missing. If the company looks like a bad bet, say so.
If the candidate is over-qualified and would be bored in six months, that is a finding too.

Concretely, that means:

- **Name the gap in the candidate's own terms.** "You have not operated a Kubernetes
  cluster" beats "limited Kubernetes exposure".
- **A high match percentage is not a recommendation.** Say so when they diverge.
- **Do not hedge the verdict.** Three options, pick one. "Proceed with caution" is a real
  verdict, not a way to avoid choosing.
- **Do not pad.** If sections 1 and 2 are short because the posting is thin, let them be
  short and say the posting is thin.

## If the environment has more tools

Nothing here requires any of them. **Web search or fetch** covers a posting that is a URL
and the sanity checks section 2 needs without a research file — it is not a substitute for
**researching-companies**. A **LinkedIn MCP server**, if the user already runs one, answers
team-size questions; their account, their decision.

## After writing it

Update the row in `applications.md` — stage `interested`, or `closed` if the verdict is
`AVOID` and the candidate agrees. Add a dated line to the `## Timeline` in `notes.md`
recording the verdict, and put whatever the verdict says to do next under `## Next`.

Then say what is worth doing next, based on the verdict — not automatically:

- `STRONGLY APPLY` / `PROCEED WITH CAUTION` → **tailoring-applications**
- Section 2 was not assessed, or the company matters → **researching-companies**
- `AVOID` on a recruiter approach → **drafting-outreach-replies**, to decline well

`examples/workspace/` in the phoenix-skills repository has two worked outputs: the Kestrel
Labs one reaches `STRONGLY APPLY` at 65% while naming two unmet requirements, and the
Trellis Bio one is an `AVOID` at an 80% paper match.
