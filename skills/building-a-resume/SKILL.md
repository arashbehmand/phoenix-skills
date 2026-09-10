---
name: building-a-resume
description: Use when improving the base résumé itself rather than tailoring it to a posting — rewriting weak bullets, adding a role or project, cutting length, working through a roast's action list, or maintaining a second base résumé for a different target track.
---

# Building a résumé

Improve the base résumé — `profile/resume.json` — and log every change in
`profile/resume-notes.md`. This is the résumé work that happens before there is a posting:
fixing weak bullets, adding a role or a project, cutting length, working through a roast.

`tailoring-applications` does the other job — adapting a *copy* to one posting. Build
touches `profile/resume.json` and never an application folder; tailor touches
`applications/<slug>/resume.json` and never `profile/`.

The general rules — STAR bullets, verb-first, one or two lines, "true is necessary not
sufficient", merging early roles, the 2026 ATS reality, not letting it read as generated,
bias — are in `references/resume-principles.md`. Read that first; this page is the loop and
the discipline around it.

## The rule, and the corollary

> **Integrity**: NEVER invent or exaggerate experience. Optimize the presentation of
> existing facts.

The corollary that bites when building rather than tailoring: **every bullet wants a
number, and you must not guess one.** If the candidate has the figure, ask for it. If they
do not, write `[metric]` and leave it — a placeholder is a to-do, not a value, and the base
résumé does not ship with one still in it. "Improved throughput" with no number is a weaker
bullet than the reader deserves; a made-up "improved throughput 3x" is worse than either.

## Read first

| File | Required | If missing |
|---|---|---|
| `profile/resume.json` | yes | Import it first — **job-search-workspace**, `references/importing-documents.md`. |
| `profile/honest-context.md` | yes | Say so; offer **interviewing-for-context**. Area 5 — what the candidate will and will not claim — is what stops this thickening a thin bullet. |
| `profile/resume-notes.md` | yes, if it exists | **Read the whole log before editing.** Apply the new instruction on top of every earlier one. If it does not exist, create it with this session's first entry. |
| `profile/preferences.md` | no | Length, order, banned words, sections to lead with. Follow them. |
| `profile/career-plan.md` | no | Which track the base is built toward. Absent, ask what roles this is for. |
| a roast — this conversation, or a `## Roast` block in `resume-notes.md` | no | The ideal input. None → offer **roasting-a-resume** first. |
| `profile/tone.md` | no | Résumé bullets carry no voice. Read only the "Résumé bullets" per-thing override, if there is one. |

## The compassion note

`honest-context.md` carries what the candidate is going through and what they are hard on
themselves about. That shapes how you talk them through the work. It does not lower the read
of what their record is worth. Someone underselling a solid three years still did the three
years — build the bullet from the evidence, and adjust the delivery, not the assessment.

## The loop

`references/iterating.md` is the detail. In short:

1. **One change at a time, with a rationale.** `Original:` / `Optimised:` / `Rationale:`.
   The rationale names which principle it serves. A change with a trade-off gets a
   `Risk Note` — dropping a graduation year, leaving a short role off, cutting a project
   the candidate likes.
2. **Apply on top of every earlier instruction.** The log in `resume-notes.md` is why
   revision six does not undo the fix from revision two. Read all of it first.
3. **Stop when the marginal edit stops helping.** A base résumé polished four times in one
   sitting is usually worse than after two.

## Output

- `profile/resume.json`, edited in place. Git is the undo; suggest a commit after a
  meaningful change, do not make one.
- A dated line appended to `profile/resume-notes.md` every time, in the candidate's own
  words. The file:

```markdown
# Résumé notes — base CV revision log

*Every change to `profile/resume.json` gets a dated line here, in the candidate's own
words. Read this whole file before editing the résumé. This is what stops revision N
undoing the fix from revision N-2 — the rule the per-application notes already use.*

## Changes

- **<date>** — <what was asked, in their words> · <what changed>

## Decisions held

- <a fact deliberately kept off the résumé, and why>

## Roast — <date>

What the last roast raised, what was acted on, and what was deliberately not, with the
reason. One block per roast, newest first.
```

  `## Decisions held` is the important half. "Left the 27 GitHub stars off — a small number
  invites the reader to weigh it" is the kind of thing a later edit would otherwise
  reinstate as an oversight.

- Optionally `profile/resume-<track>.json`: a second base, and only one, and only when
  `aligning-career-targets` has established a real second track. Not a version per
  application — that is what `tailoring-applications` and git history are for.

Validate whatever you wrote:

```bash
python3 <job-search-workspace>/scripts/validate_resume.py profile/resume.json
```

## After writing it

- Validate. A wrong field name produces a résumé with a section silently missing.
- Append the `resume-notes.md` line. Do not log what you deliberately left out by naming
  it; "kept a disclosure decision from an earlier session" carries the same weight and
  names nothing.
- Suggest a git commit.

**This skill runs before any application, so it does not touch `applications.md` or any
`applications/<slug>/notes.md`.** If a change here should feed a live application, say so
and let the candidate decide.

## If the environment has more tools

Nothing here requires them. The only executable is the résumé validator, which is standard
library and offline. A filesystem MCP server is fine for reaching the workspace. Do not use
web search to "verify" something about the candidate — the workspace and the candidate are
the only sources for that.

## Next

- Make the public profile say the same thing → **writing-a-linkedin-profile**
- The base is solid and there is a posting → **assessing-job-fit**
- Need a PDF or a Markdown copy → **job-search-workspace**, `references/reactive-resume-export.md`
- Want it torn apart first → **roasting-a-resume**
