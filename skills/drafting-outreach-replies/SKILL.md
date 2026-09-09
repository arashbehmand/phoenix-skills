---
name: drafting-outreach-replies
description: Use when a recruiter or hiring manager has sent an email or a LinkedIn message and a reply is needed — including declining, chasing a silent thread, following up after an interview, or turning a rough draft into something sendable.
---

# Drafting outreach replies

Refine a reply to a recruiter, in the candidate's voice, with the context of the job they
are actually talking about.

The distinctive thing here — and what makes it better than asking a chatbot to "write a
reply to this recruiter" — is that it starts from the candidate's own rough draft, in
whatever language they wrote it, and it knows which role the conversation is about,
what stage it is at, and what has already been said.

## Start from their draft

Ask for one if there is not one. "What do you want to say?" gets a better answer than any
blank-page reply, because the candidate already knows what they mean; what they want is
for it to land properly in a professional register.

Refine what they wrote. Keep their points, their emphasis, and their decisions. If the
draft says no, the reply says no. Do not add enthusiasm they did not express, and do not
quietly drop a point because it is awkward.

With no draft, write from context and say plainly that this is a first attempt at what
they might want to say, not a finished message.

## Multilingual

**A draft in any language produces a reply in that language**, professional and coherent.
This is a first-class case, not a fallback: a candidate writing to a German recruiter
often drafts in German, and translating to English and back would lose the register.

Match the language of the conversation, not the language of the workspace. If the thread
is in French and the draft is in English, ask which they want.

## Read first

| File | Required | If missing |
|---|---|---|
| The message being replied to | yes | Ask for it, pasted. |
| `profile/honest-context.md` | yes | Say so. It is how the reply comes out as theirs, and it holds whatever constraint this particular reply has to state. |
| `applications/<slug>/contacts.md` | no | **Read the whole thread**, not just the last message. |
| `applications/<slug>/job.md` | no | Read it if the conversation is about a specific role. |
| `applications/<slug>/fit.md` | no | Read it — it says which strength to lead with and whether this is worth pursuing. |
| `profile/tone.md` | yes | **Read before drafting.** It decides the voice. Absent, default to plain and short, and say so. |
| `profile/preferences.md` | no | Read it if present. |
| `research/<company>.md` | no | Read it if present. |

### Resolving which job this is

An inbound message often names only a company, or only a person. Resolve it:

1. Grep `applications.md` for the company or the person's name.
2. Open that folder. `contacts.md` has the thread, `job.md` the posting, `fit.md` the
   assessment.
3. If several applications match the same company, the contact name in `contacts.md`
   decides.
4. If nothing matches, this is a new approach. Ask whether to create a folder for it.

This is why the tracking index exists. A reply that references the actual job description
and the actual prior exchange is the whole point.

## What the thread tells you

Read the history before drafting, for three things:

- **What stage this is.** A reply to a first approach and a reply after a final round are
  different messages.
- **What has already been committed to.** A date agreed, a salary figure mentioned, a
  question already answered. Contradicting an earlier message is the worst outcome here.
- **The register.** Match how this person writes. A recruiter writing in short informal
  lines does not want four formal paragraphs back.

**Calibrate formality to the recipient.** An agency recruiter, an in-house talent partner,
a hiring manager and a future colleague are four different registers. When in doubt, one
notch more formal than the incoming message, never two.

## Email versus LinkedIn

The same job, with two differences.

**Email** needs a subject line — reuse the thread's if replying, and keep `Re:`. It needs
a greeting and a sign-off, correct spelling and grammar throughout, and paragraphs rather
than one block.

**LinkedIn** is shorter and has no subject line. Two or three short paragraphs at most.
Long formal messages read wrong in a chat window. A sign-off is optional; a name is not
needed when the profile is attached.

## Writing

- **Voice comes from `profile/tone.md`.** Read it first. It is the user's file and it
  decides register, formality and vocabulary; nothing here overrides it. Without one,
  default to short sentences and ordinary words, and say in one line that you did.
- **Do not let it read as generated.** This matters more here than anywhere else in the
  toolkit. A recruiter who thinks a reply was machine-written reads the candidate as low
  effort, and that judgement attaches to the application, not just the message. The tells
  are in **job-search-workspace**, `references/tone.md`. The em-dash is the most common,
  "I hope this email finds you well" the most obvious, and a closing paragraph that
  restates the message the most avoidable.
- **Answer what was asked**, first, before anything else.
- **Be brief.** Recruiters read on a phone between meetings.
- **Say no clearly.** If the reply declines, decline in the first two sentences and be
  warm after that, not before. A long preamble before a no wastes the reader's time and
  reads as evasive. Give the reason if it is a clean one — sponsorship, salary, location —
  because it saves you both the next three approaches.
- **Never invent.** Not a date the candidate has not confirmed, not a salary expectation
  they have not given, not availability. If the reply needs a fact you do not have, leave a
  clearly marked gap and ask.
- **`honest-context.md` is background.** It tells you what the candidate actually wants
  and what they will not accept, so the reply is theirs rather than generic. What they
  hold privately stays private, and that includes not writing a note about what you left
  out: a file recording which private topics were avoided has just recorded them.

## Before it is sent

**Show the draft to the candidate and let them send it.** This goes out under their name
into a live professional relationship. Do not send anything on someone's behalf unless
they have explicitly asked you to, in this conversation, for this message.

## After

Append the sent message to `contacts.md` in that contact's block — see
`references/contacts-format.md` for the format and the upsert rule. Update the stage in
`applications.md` if this moved things along, and add a line to `notes.md` for anything
committed to: a date, a number, a decision.

## If the environment has more tools

Nothing here requires any of them. Pasting the thread is the assumed path and works
everywhere, and it lets the candidate redact before pasting.

- **A LinkedIn MCP server**, if the user already runs one — typically `get_inbox` and
  `get_conversation`, which captures a thread without a browser extension. Message sending
  exists too; do not use it without an explicit, in-the-moment instruction to send.
- **The Phoenix Pilot browser extension** — captures the open LinkedIn or Gmail thread in
  the format `contacts.md` expects. See `docs/chrome-extension.md`.
- **Browser automation or a Gmail connector** — reads the thread as a person would.

`references/contacts-format.md` has the full ordering and the reason LinkedIn is never
scraped directly.

## Next

- An interview came out of it → **preparing-for-interviews**
- A new company approached you → **assessing-job-fit**, once you have the posting
- Declining because the fit is wrong → record it in `fit.md` so it stays decided
