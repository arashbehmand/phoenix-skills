# `profile/tone.md` — why voice is the user's, not the skill's

Every skill here that writes something a human reads checks `profile/tone.md` first. If it
does not exist, offer to create one from the template below and say what the default is.

## Why this is a file

Phoenix was built for one person, and it shows. Its cover-letter prompt said, as a fact
about the user:

> bear in mind that applicant is a non-native speaker, so to have a true tone please keep
> the language simple and avoid complex jargon

That was correct for that user and wrong as a rule. A native speaker with a deliberately
formal register gets flattened by it. Somebody writing in German gets advice calibrated for
English. Somebody applying to a law firm gets a letter pitched at the wrong level.

So the instruction moved out of the skill and into the user's own file. The skills carry no
opinion about who the user is, which is the point: they should be as useful to a barrister
as to a new graduate.

## The default, if the user has not said

Plain English, short sentences, ordinary words, warm but not eager. This travels furthest
across industries and languages, and it is the safest thing to do before someone has told
you otherwise.

**Say which default you used.** "Written plain and fairly short — `profile/tone.md` sets
that, change it there if you want a different voice" is one line and it makes the setting
discoverable.

## The template

```markdown
# Tone — how anything written in my name should sound

## The one-line version

> brief, concise, to the point, friendly, a tad bit casual, plain English, sounds like a
> person, no em-dashes, does not scream AI

## Register
Warm, brief, not eager. No exclamation marks. If it needs to say no, it says no early.

## Language level
Plain English, around IELTS 7. Short sentences. This is a choice, not a limitation —
say so here if you want something more elaborate.

## Words and habits to avoid
Em-dashes. "leverage", "passionate about", "thrilled to", "I am writing to express…"

## Per-thing overrides
Cover letters slightly more formal. Screening answers plainest. Recruiter messages
shortest. Résumé bullets are not prose: verb first, number in it.
```

`examples/workspace/profile/tone.md` in the phoenix-skills repository is a filled-in one.

## Do not make it obvious a model wrote it

This belongs in tone rather than in ethics. In hiring, writing that reads as generated gets
discounted, and the discount lands on the facts too.

The tells, in rough order of frequency:

| Tell | Fix |
|---|---|
| Em-dashes | Comma, full stop, or brackets |
| "I should be upfront…" before the news | Give the news |
| "One thing worth noting:" | Say the thing |
| "I carefully considered each requirement" | Show it or cut it |
| A closing paragraph restating the message | Cut entirely |
| Every paragraph two or three sentences | Vary it. One-line paragraphs are fine |
| Three-item lists in every other sentence | Use two. Or one |
| "…, not a concern, and nothing that affects delivery" | Say it once |

The test that catches most of it: read it aloud and ask whether this person would say this.
A sentence that is true, correct and unsayable is still wrong.

## What tone does not decide

Facts. Voice never changes a number, a date, an employer or a claim. If following the tone
file would require softening something true or hardening something uncertain, follow the
facts and tell the user why the voice bent.
