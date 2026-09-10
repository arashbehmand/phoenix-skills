---
name: reviewing-the-search
description: Use when the question is about the job search as a whole rather than one application — what needs attention this week, what is overdue, who has not replied, where everything stands, whether anything has been forgotten, or a weekly catch-up on all of it at once.
---

# Reviewing the search

Read every application in the workspace and say what needs attention. This is the only
skill here that works across applications rather than inside one.

It answers the question people actually ask on a Monday morning: *what have I forgotten?*

## Get today's date first

Check it rather than assuming. Everything below is relative to it, and an agenda computed
against the wrong day is worse than no agenda — it will report a booked interview as
overdue, or miss one entirely.

## Read

| File | What it gives |
|---|---|
| `applications.md` | The roster and the stage of each application |
| `applications/*/notes.md` | `## Timeline` for what has happened and what is booked; `## Next` for what is outstanding |
| `applications/*/contacts.md` | The date of the last message in each thread, where one exists |
| `profile/career-plan.md`, `honest-context.md`, `linkedin.md`, `resume-notes.md` | **Their dates only.** See "The profile goes stale too" below |

`job-search-workspace` documents both note conventions: timeline entries are dated and may
be in the future, `## Next` items may carry a `**by <date>**`. Applications written before
those conventions will have neither — say so rather than reporting them as having nothing
outstanding.

Do not read `fit.md`, `resume.json` or the other artifacts. This is a review of state, not
of content, and reading everything makes it slow enough that nobody runs it. The `profile/`
files are the one exception, and only for their dates — a date is state, and those four
files are the only things in the workspace that go stale without anyone touching them.

## What to produce

An agenda, in the conversation. **Do not write it to a file** unless asked — an
`agenda.md` is stale the moment anything happens, and a second copy of the truth is a
second thing to keep right. The notes are the record; this is a view of them.

Group it:

- **Overdue** — dated, in the past, still open
- **Today and tomorrow**
- **The rest of this week**
- **Open, no date** — real work with no clock on it
- **Gone quiet** — a live application with nothing recorded for a while
- **One closing line** for anything closed, so the count reconciles against
  `applications.md`

Skip empty groups rather than printing them with "none". Lead with the shape of it in one
sentence — *"Two things today, both Kestrel, and Orbital has been sitting untouched for
three days"* — then the list.

Each item names the application, what is to be done, and when. Keep the user's own wording
from `## Next`; they wrote it in the terms that will make sense to them.

## The profile goes stale too

Every application-side file gets updated because something happened. The `profile/` files
do not: nobody gets an email that says the career plan is now nine weeks old. So this is
the only skill that will ever notice, and it is the reason those files carry a date at the
top — a `Last updated:` line, a `*Generated <date>*` line, or the newest dated entry in
their log. **Read that line, not the file.**

What each one is waiting for:

- **`honest-context.md`** — a rejection that stung, an offer, a dealbreaker tested for
  real, or about three months. The events matter more than the calendar: a file written
  last month with two rejections behind it is staler than one from the spring with none.
- **`career-plan.md`** — the same triggers, and it names its own in a `Revisit after:`
  line. Read that line and use what it says.
- **`resume-notes.md`** — applications going out for weeks while the base résumé has not
  been touched. Tailoring papers over a weak base once per application; fixing it once is
  cheaper.
- **`linkedin.md`** — last edited before the target changed, which means it is pointing
  recruiters at the old thing.

**Report this as one closing line, not a group of its own.** Nothing here is due on a
date, and none of it should push the actual week's work down the page. "Your honest context
is from 12 May and three rejections have landed since, which is the trigger it names" is
the whole report. When nothing is stale, there is no line — the same rule as any other
empty group. If the user wants to act on it, the skill that owns the file does the work.

If a file does not exist at all, say so once, name the skill that writes it, and move on.
A missing `career-plan.md` is not overdue work; it is a thing they have not done yet.

## Gone quiet is a judgement, not a threshold

Ten days of silence means different things at different stages, and a fixed number gets
this wrong in both directions:

- After **applying**, two weeks of nothing is ordinary. Three is worth a note, not alarm.
- After an **interview**, a week is worth chasing — that is the stage where a nudge is
  normal and being forgotten is expensive.
- After an employer said they would come back **by a date**, the date is the deadline.
  That belongs in `## Next` with a `by`, and if it is not there, add it.

**Say what the silence actually is.** "Nothing recorded since 3 September" is a fact about
the file. "They have not replied since 3 September" is a claim about the employer, and it
is wrong whenever something happened and did not get written down. Report the first, and
ask which it was.

## Rules

- **Do not invent urgency.** If nothing is dated, the honest report is that the search has
  nothing scheduled. Do not manufacture deadlines to make the agenda look busy — a week
  with two real things in it is a week with two real things in it.
- **Closed applications generate nothing.** They stay in the record because a closed row
  stops a posting being reconsidered on the strength of its match score; they are not work.
- **Do not restate private material.** `honest-context.md` shapes advice about what to
  chase. It does not get quoted into an agenda that might be read over a shoulder.
- **Do not do the work while reporting it.** If four things need doing, say so and ask
  which to start. An agenda that turns into an hour of drafting was not an agenda.

## Then record what comes back

Reading the agenda is when the user remembers what actually happened. Offer to write it
down as they say it — this is what keeps the notes worth reading, and without it the
convention rots inside a fortnight.

- "They replied on Tuesday" → a dated timeline entry, and clear the `## Next` item it
  answers.
- "The interview moved to the 15th" → correct the timeline entry, do not add a second one.
- "I need to send them the take-home by Friday" → a new `## Next` item with the date.
- Anything that changes the stage → update the row in `applications.md` too.

Ask before writing, and write in their words.

## Shape of the output

```markdown
Two things today, both Kestrel — and Orbital has been sitting three days with the
sponsor check not run.

**Today**
- Kestrel Labs — chase Priya for the second interviewer's name (was due 10:00)
- Kestrel Labs — fill in Talking Point 4 yourself, before tomorrow

**Tomorrow**
- Kestrel Labs — round 2, 14:00, systems design with Dev

**Open, no date**
- Orbital Freight — sponsor licence check, then the fit analysis if it passes

Trellis Bio is closed. Nothing else in the workspace.
```

Nothing in that example is stale, so it carries no closing line about the profile. When
something is, it goes last, after the reconciliation line.

## If the environment has more tools

None are needed; this reads local files. If a calendar connector is available and the user
asks, a booked interview can be put in the calendar — ask first, and the timeline entry in
`notes.md` stays the record either way.

## Next

- Something needs chasing, or a reply is due → **drafting-outreach-replies**
- An interview is on the agenda → **preparing-for-interviews**
- A posting is sitting at `interested` with nothing run against it → **assessing-job-fit**
- The notes are thin because the conventions are not being followed → **job-search-workspace**
- The honest context is stale → **interviewing-for-context**
- The plan is stale, or the rejections are all on one track → **aligning-career-targets**
- The base résumé has gone untouched while applications went out → **building-a-resume**
