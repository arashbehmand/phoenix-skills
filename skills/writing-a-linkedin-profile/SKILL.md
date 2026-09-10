---
name: writing-a-linkedin-profile
description: Use when writing or revising the candidate's own LinkedIn profile — drafting the headline, About and experience copy, ordering the skills, choosing between headline options, or checking the profile points recruiters at the same thing the résumé does. Writes and maintains profile/linkedin.md; for a critique that changes nothing, that is roasting-a-resume.
---

# Writing a LinkedIn profile

Draft and maintain the candidate's public profile — headline, About, experience copy,
skills order — in `profile/linkedin.md`. That file is the source of truth for the profile
text; the candidate pastes from it into LinkedIn and adjusts on screen.

Do the résumé first. The profile is the same facts in a different form, and a profile that
disagrees with the CV is worse than a thin one. `building-a-resume` comes before this.

## What has changed, and what the profile is for

> Keyword-stuffing is penalised now, not rewarded — a term repeated past what natural
> writing would produce gets the profile ranked down, and reads as desperate to a person.
> The headline carries most of the recruiter-search weight, so it gets the most care.
> Every section points the same way: the headline's specialty, the About's stories, the
> experience titles and the skills all name the same kind of work. A gap gets a real,
> published project or portfolio page — never a fabricated role, a fake company, or a
> "façade" site.

## Read first

| File | Required | If missing |
|---|---|---|
| `profile/resume.json` | yes | The facts come from here. **job-search-workspace** covers the import. |
| `profile/honest-context.md` | yes | Say so; offer **interviewing-for-context**. It carries what the candidate wants next, what not to claim, and what a recruiter pauses at — which a public profile has to survive. |
| `profile/tone.md` | yes | **Read before writing.** This copy goes out under the candidate's name and strangers read it. Absent, default to plain and say which default you used. |
| `profile/linkedin.md` | no | If it exists, read all of it — you are revising. Follow its `## Revision log`. |
| `profile/career-plan.md` | no | The primary track. Every section bends toward it. |
| `profile/resume-notes.md` | no | Read `## Decisions held` so the profile and the résumé keep telling the same story. |

## Getting the current profile in

An audit or a rewrite needs what is on the profile today, and the candidate should not have
to copy it out by hand. LinkedIn exports it: **More → Save to PDF** on their own profile,
then import it the way any document gets imported — **job-search-workspace**,
`references/importing-documents.md` has the command and the two traps, one of which is that
character counts must never come from the PDF. Pasting works as well, and for a headline on
its own it is quicker.

However it arrives, `profile/linkedin.md` is the file that gets maintained. The export is an
import, not a second copy to keep in step.

## Modes

All three write the one file.

- **Full profile audit** — First Impressions (banner, photo, custom URL), Headline,
  Content Deep Dive (About hook and Experience), Skills, then a short prioritised action
  list. `references/linkedin.md` has the structure.
- **Headline** — generate two to four options, each with its character count and a line on
  who it is aimed at; or take the candidate's shortlist and pick one, saying why and naming
  the runner-up.
- **Section rewrite** — the About, or one experience entry, to the contract below.

## The voice

Comes from `profile/tone.md`, same as everything written in the candidate's name. Read it
first; nothing here overrides it. The About is first person — "I build…", not "Mirela
builds…" — and it should not read as generated: the tells are in **job-search-workspace**,
`references/tone.md`, and the em-dash is the most common one.

## Output

`profile/linkedin.md`:

```markdown
# LinkedIn profile

*Generated <date> · inputs: <files actually read>*

## Strategy note

Two to four sentences: who this profile is aimed at, and the one thing every section is
bent toward.

## Headline

<text>  `[NNN/220]`

## About

First three lines (above the "see more" fold, where the hook lands):

<hook>

<rest of the About>  `[NNNN/2600]`

## Experience

### <Role> at <Company>

<copy, first person>

## Skills, in order

1. <highest recruiter-search weight first>
2. ...

## Risk notes

- <e.g. turning on a public "Open to Work" badge is visible to your current employer>

## Revision log

- **<date>** · <what was asked, in the candidate's words> · <what changed>

## What this profile does not do

- No automation, no scraping, no engagement pods, no bought connections. If asked for any
  of those, decline and offer a manual, organic approach instead.
```

**Character counts are an estimate.** Run `scripts/charcount.py` on the file to get real
counts, and tell the candidate to confirm in LinkedIn before saving — the limits move and
LinkedIn counts some things (URLs, emoji) in ways a plain count does not.

Where a number is missing, write `[metric]` and leave it. Do not invent one for a public
profile any more than for a résumé.

## After writing it

- `python3 <writing-a-linkedin-profile>/scripts/charcount.py profile/linkedin.md` and fix
  anything over a limit.
- Append the `## Revision log` line, in the candidate's words.
- Suggest a git commit; do not make one.
- This runs before any application — no `applications.md` change.

## If the environment has more tools

Nothing here requires them. **Web search** can check what strong profiles for the target
role currently look like, which helps calibrate a headline — it is not a source of facts
about the candidate. A **LinkedIn MCP server**, if the candidate already runs one, can pull
their current profile text and save the export step. It is a convenience, not the normal
path — the PDF above needs no server and no account access. Sending or changing anything on
the account needs an explicit, in-the-moment instruction, and even then the file is the
draft and LinkedIn is where they apply it.

## Next

- A recruiter has already messaged → **drafting-outreach-replies**
- The profile work surfaced "what am I actually aiming at" → **aligning-career-targets**
- A weekly catch-up on the whole search → **reviewing-the-search**
