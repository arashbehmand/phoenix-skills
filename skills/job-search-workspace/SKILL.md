---
name: job-search-workspace
description: Use when setting up or working inside a job-search workspace — creating the folder, importing a résumé or job posting from a PDF, DOCX, URL or pasted text, working out where an artifact belongs, revising a file that was generated earlier, keeping the application index current, or exporting a résumé to Markdown, JSON Resume, or Reactive Resume for a PDF.
---

# Job-search workspace

Every other skill in this set reads and writes this layout. It is plain files in a
directory the user owns — no database, no service, no lock file.

## Layout

```
profile/
  resume.json          JSON Resume. The single source of truth about the candidate.
  honest-context.md    Who they are, what they want, what they will not accept.
  tone.md              How anything written in their name should sound.
  preferences.md       Everything else they want done a particular way. Optional.

applications/<company>-<role>/
  job.md               The posting as captured.
  job.json             Parsed structured form (optional).
  fit.md               Go/no-go analysis. Everything downstream reads it.
  resume.json          Tailored résumé for this role.
  cover-letter.md
  questions.md         Screening-question answers.
  interview-prep.md
  contacts.md          Per-contact conversation threads, in sentinel blocks.
  notes.md             Timeline, revision log, open questions.

research/<company>.md  Due diligence. One per company, not per application.

applications.md        The index.
```

A filled-in version of exactly this layout lives in the phoenix-skills repository at
`examples/workspace/`. When unsure what a file should look like, read that rather than
inventing a shape. (It is not copied into the installed skill; fetch it from the repo if
it is not to hand.)

### Rules that matter

- **The folder slug is the join key.** `applications/<company>-<role>/`, lowercased,
  non-alphanumerics collapsed to single hyphens, no trailing hyphen. It is how an inbound
  message naming only a company gets resolved to a job description and a prior thread.
  Once created, do not rename it.

  **Fold accents to ASCII first**: `Nestlé` → `nestle`, `Ørsted` → `orsted`,
  `Société Générale` → `societe-generale`. A slug carrying a `é` still works on disk but
  stops matching when someone later types the plain-ASCII name, which is the one thing the
  slug exists to do. The same applies to `research/<company>.md`.
- **One research file per company**, at `research/<company>.md`, because one company can
  produce several applications.
- **Never write to `profile/` while working on an application.** `profile/resume.json` is
  the base; a tailored résumé goes in the application folder. Overwriting the base with a
  tailored version is unrecoverable without git and quietly poisons every later
  application.
- **`honest-context.md` is background, not source material.** Read it, understand who you
  are writing for, then write. It shapes what you say and rarely appears in what you say.
  Anything the user clearly holds privately works like something a colleague told you in
  confidence: it informs your judgement and does not get repeated, including in a note
  explaining that you did not repeat it.

## Starting a workspace

```bash
mkdir -p profile applications research
git init      # optional, and the whole versioning story if used
```

### `profile/` holds the defaults

Three files carry across every application and every skill, so they get written once and
are not re-asked:

1. `resume.json` — see `references/importing-documents.md` if it starts as a PDF or DOCX.
   Validate it before relying on it (below).
2. `honest-context.md` — the one that changes output quality most. Ask for it in the
   user's own words: what they want next, what they will not accept, what their situation
   actually is, and what they are genuinely weak at. Prose, not a form. A short honest one
   beats a long tidy one. There is no schema and there should not be one; the parts that
   matter differ per person.
3. `tone.md` — how anything written in their name should sound. See `references/tone.md`
   for the template, and for why voice is a file the user owns rather than something the
   skills assume.

`preferences.md` is optional: résumé length, sections to lead with, how salary questions
get handled. A per-application override beats any default — record it in that
application's `notes.md` rather than editing `profile/tone.md` for one job.

If `honest-context.md` is missing, say so before producing anything that depends on it,
and offer to write it from a few questions. Do not silently proceed with a generic
substitute — that is the difference between this and any other résumé tool.

## Intake

Full detail in `references/importing-documents.md`. The short version:

- **PDF, DOCX, XLSX, PPTX** → convert with `markitdown`. Write the bytes to a temp file
  **with the original extension** first; MarkItDown dispatches on the extension and
  silently mis-parses a file named `.tmp`.
- **A job URL** → fetch it yourself. Save the readable text as `job.md` with the source
  URL and capture date at the top.
- **Pasted text** → save as-is, then structure it.

Always keep the original text. `job.md` is the record of what was actually advertised; a
posting can change or disappear while an application is live.

## Revising a generated file

This is the part that goes wrong quietly, so it has a hard rule.

**Before editing any generated artifact, read the revision log in that application's
`notes.md` — the whole log, not the last entry.**

Then apply the new instruction on top of every earlier one, and append a line to the log
recording what was asked, in the user's own words.

Log what was asked and what changed. Do not log what you deliberately left out, and never
by naming it: a line listing the private topics you avoided has just filed them somewhere
new.

Without this, revision 4 undoes the fix from revision 2. The realistic case: the user says
"put the skills gap in explicitly, I'd rather lose the interview now than in round two,"
and three revisions later says "make it sound more confident" — and the gap disclosure
disappears, because nothing was carrying that earlier instruction forward. When an
instruction exists specifically to keep something uncomfortable in, note that in the log
so a later instruction does not quietly reverse it.

If a later instruction genuinely conflicts with an earlier one, say so and ask which wins
rather than picking silently.

Files plus git replace what a database would have done here. Suggest a commit after a
meaningful change; do not commit automatically.

## Keeping the index current

`applications.md` at the workspace root is one Markdown table: company, role, link to the
posting, source, date applied, one-word stage, relative link to the folder.

Stage is one word — `interested`, `applied`, `interviewing`, `offer`, `closed` — and only
answers "is this live?". Do not invent a longer vocabulary; a hand-edited file with a
fifteen-stage enum goes stale within a month.

Update the row whenever the folder changes state. Keep closed applications: a row
recording that a role was declined, and why, is what stops the same posting being
reconsidered in a month.

## Exporting

| Want | Do this |
|---|---|
| A PDF | `scripts/to_rxresume.py` → import at [rxresu.me](https://rxresu.me/) → adjust → download. See `references/reactive-resume-export.md`. |
| A plain-text/Markdown résumé | Render per `references/markdown-resume.md`. |
| JSON Resume | It already is. Validate before handing it over. |

There is no PDF renderer here on purpose. Reactive Resume is free, open source, and gives
the user a visual editor and a dozen templates; reproducing that would be work with no
payoff.

## Scripts

Standard library only, no network, no API key.

Both live in this skill's own `scripts/` directory — substitute its real path for
`<skill>` below, or `cd` there first.

```bash
# Check a résumé, and see exactly what is wrong with it
python3 <skill>/scripts/validate_resume.py profile/resume.json

# Repair the field names, date formats and shapes that can be repaired
python3 <skill>/scripts/validate_resume.py profile/resume.json --fix

# Convert for Reactive Resume (v5 default; --schema v4 for the older import format)
python3 <skill>/scripts/to_rxresume.py profile/resume.json -o resume.rxresume.json
```

`validate_resume.py` exits non-zero when the file has errors, so it works in a check
before an export. Run it after any skill writes a `resume.json` — the field names are
easy to get wrong and wrong ones produce a résumé that is missing entire sections without
anything reporting a failure. `references/json-resume.md` explains which names, and why
each one bites.

`to_rxresume.py` repairs the input first and tells you it did. It refuses to write output
that would not import, rather than writing a broken file that looks fine.

## If the environment has more tools

None of this requires them, but when they are present: a filesystem MCP server is fine
for reading and writing the workspace; `markitdown` installed locally makes document
intake work without any conversion service; git gives versioning and is the only reason
the revision log is recoverable if something is overwritten.

## Next

- Have a posting and want to know whether to apply → **assessing-job-fit**
- Decided to apply → **tailoring-applications**
- Want to know who you would be working for → **researching-companies**
