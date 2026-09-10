# Example workspace

A small, complete, fictional workspace. Nothing in it is real: **Mirela Ionescu** does not
exist, and neither do Kestrel Labs, Orbital Freight or Trellis Bio. Phone numbers use the
Ofcom range reserved for drama, and every URL points at `example.com`.

Use it two ways:

1. **As a reference for shape.** Every file here is what the corresponding skill is
   supposed to produce. If output does not look like this, something is wrong.
2. **As a fixture.** Point an agent at this directory as its workspace and give it a real
   request — "tailor my résumé for this posting," "draft a reply to Priya" — to check the
   skills find the right files and write to the right paths.

## Layout

```
profile/
  resume.json          JSON Resume. The single source of truth about the candidate.
  honest-context.md    Who she is, what she wants, what she will not accept.
  tone.md              How anything written in her name should sound.
  preferences.md       Everything else she wants done a particular way.

applications/<company>-<role>/
  job.md               The posting as captured.
  job.json             Parsed structured form.
  fit.md               Go/no-go analysis. Everything downstream depends on it.
  resume.json          Tailored résumé for this role.
  cover-letter.md
  questions.md         Screening-question answers.
  interview-prep.md
  contacts.md          Per-contact conversation threads, in sentinel blocks.
  notes.md             Dated timeline, what is next, revision log.

research/<company>.md  Due diligence. One per company, not per application.

applications.md        The index. Lookup, not pipeline.
```

## What each example is here to demonstrate

**`profile/tone.md`** decides the voice of every letter, answer and recruiter reply. It is
a file rather than a setting inside the skills because Phoenix hardcoded *"the applicant is
a non-native speaker"* as a fact about its one user. That was right for him and wrong for
everyone else. Whatever is written here wins, including "write like a barrister" if that is
the truth.

**`profile/honest-context.md`** is the piece with no off-the-shelf equivalent, and the
reason output does not read like generic AI filler. Note that it is prose, not a form —
it names a visa constraint, a salary floor, four dealbreakers, and five weaknesses the
candidate would not put in front of an employer. It gates nearly everything else.

**`applications/kestrel-labs-senior-data-engineer/`** is the fully worked case: a posting
the candidate should apply for, carried all the way from capture to interview prep.

- `fit.md` reaches `STRONGLY APPLY` and still says the match is 65% and names two required
  skills the candidate does not have. A fit analysis that only ever agrees with you is
  worth nothing.
- `resume.json` lifts the job description's language where it can honestly be claimed —
  data contracts, schema evolution, migration without downtime — and contains the words
  "Kubernetes," "Flink" and "EKS" **nowhere**, because the candidate has not done those
  things. That is the integrity rule in practice.
- `cover-letter.md` is three paragraphs and under 400 words, in plain sentences, with no
  header and no sign-off, and it discloses the gaps rather than papering over them.
- `interview-prep.md` runs the full enforced mix — 6 behavioural, 5 technical, 4
  situational, 3 fit, 2 career-vision — with a rationale per question, and marks with ⚠️
  everything built on speculative data. The interviewer-specific section is deliberately
  empty and says why: no interviewer background was available, so inventing one was the
  only alternative.
- `contacts.md` shows two threads in `<phoenix-pilot-messages>` blocks keyed by contact
  name. Blocks are upserted, so re-capturing Priya's thread never touches Dev's.
- `notes.md` carries the revision log. Read the `cover-letter.md` v3 entry: it records an
  instruction that a later "make it more confident" would silently undo. Re-reading this
  log before every edit is what stops revision N regressing the fix from revision N−2.
  Its `## Timeline` also holds Friday's interview as a future-dated entry with a time, and
  its `## Next` holds two things due today — which is what `reviewing-the-search` reads to
  answer "what needs attention". Orbital's `## Next` is undated because nothing there has
  a clock on it, and Trellis Bio has no `## Next` at all because it is closed.

**`applications/trellis-bio-analytics-engineer/`** is the opposite case and the more
useful one. An 80% paper match that is an immediate `AVOID`, because the employer cannot
sponsor. It is kept rather than deleted so the same posting is not reconsidered later on
the strength of the match score.

**`applications/orbital-freight-data-platform-engineer/`** is an application at rest: a
posting saved, nothing generated yet, and a note saying which check to run first and why
nothing should be tailored before the fit analysis.

**`research/kestrel-labs.md`** opens with company verification, because a name collision is
the top failure mode — the first page of search results for this company describes a
Colorado medical-device firm. Estimated figures are labelled as estimates every time,
including a revenue range with its derivation shown and an explicit "do not repeat this in
an interview as fact."
