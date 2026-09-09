# Applications

The index. One row per application, hand-editable, diffable, renders on GitHub, needs no
tool to open.

Its job is lookup, not workflow. When a message arrives that names only a company, this
table is what resolves "Priya at Kestrel" to a folder containing the job description, the
fit analysis, the tailored résumé and the prior thread. The folder slug is the join key.

**Stage** is one word and only answers "is this live?" — `interested`, `applied`,
`interviewing`, `offer`, `closed`. Longer status vocabularies go stale in a file people
edit by hand, and nothing here depends on them.

| Company | Role | Posting | Source | Applied | Stage | Folder |
|---|---|---|---|---|---|---|
| Kestrel Labs | Senior Data Engineer, Streaming Platform | [posting](https://example.com/kestrel-labs/careers/senior-data-engineer-streaming) | Careers page | 2026-08-26 | `interviewing` | [kestrel-labs-senior-data-engineer](applications/kestrel-labs-senior-data-engineer/) |
| Orbital Freight | Data Platform Engineer | [posting](https://example.com/orbital-freight/jobs/data-platform-engineer) | LinkedIn | — | `interested` | [orbital-freight-data-platform-engineer](applications/orbital-freight-data-platform-engineer/) |
| Trellis Bio | Analytics Engineer | [posting](https://example.com/trellis-bio/careers/analytics-engineer) | Agency (Hannah Beckett) | — | `closed` | [trellis-bio-analytics-engineer](applications/trellis-bio-analytics-engineer/) |

## Conventions

- **Folder slug** is `<company>-<role>`, lowercased, non-alphanumerics collapsed to
  hyphens. It is stable for the life of the application — renaming it breaks every link
  that resolves an inbound message to its context.
- **Applied** is the date the application actually went in. `—` means it has not.
- **Closed** covers every ending: rejected, withdrawn, declined, went quiet. The folder's
  `notes.md` says which. Trellis Bio was closed by the candidate on the first read, and
  keeping the row is the point — it stops the same posting being reconsidered in a month
  because the match score looked good.
- **Research** lives at `research/<company>.md`, one file per company rather than per
  application, because a company can produce more than one role.
