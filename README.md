# Phoenix Skills

A job-application toolkit as agent skills. Plain Markdown, a folder of your own files, and
no service to run.

This is the knowledge from [Phoenix][phoenix], a job-application assistant built in the
GPT-4o era, re-expressed for agents that can already plan, search the web, read files and
write them. Delivering this in 2025 meant shipping a platform: six repositories, FastAPI,
Postgres with pgvector, RabbitMQ, Caddy, a declarative pipeline engine, a SvelteKit web
app, a Telegram bot and a PDF renderer. Almost none of that was the value. The value was
nine prompts and a handful of hard-won details, and an agent in Claude Code, Codex or
Cursor does the rest natively.

So: keep the knowledge, drop the machinery.

## What it does

You have found a job posting. From there:

- Decides honestly whether to apply at all, and tells you when not to.
- Researches the company, including whether they can actually sponsor your visa.
- Tailors your résumé, writes the cover letter, answers the screening questions.
- Prepares you for the interview with twenty questions you will not enjoy reading.
- Drafts replies to recruiters that know what stage you are at and what you already said.
- Keeps track of all of it in files you own and can read without any of this installed.

**It does not find jobs.** Scope starts at "I have a job description." You find postings
however you already do — browsing, LinkedIn, a job board, a browser extension. Everything
after that is what lives here.

## What you need

An agent that can read `SKILL.md` files, and a folder. That is the whole list.

No API keys. No accounts. No `docker compose up`. Nothing runs in the background. Every
skill's happy path works with no credential set anywhere — the two optional integrations
(a LinkedIn MCP server, a free UK Companies House key) add signal but nothing depends on
them.

Your data stays in a directory on your machine, in Markdown and JSON, versioned in your own
git repository if you want it versioned.

## The skills

Each lands at `skills/<name>/`. See [Status](#status) for what has shipped so far.

| Skill | Use it when |
|---|---|
| [`job-search-workspace`](skills/job-search-workspace/) | Setting up the folder, importing a CV or a posting, exporting a résumé to PDF |
| `assessing-job-fit` | You have a posting and want an honest go/no-go before spending an evening on it |
| `tailoring-applications` | You have decided to apply: résumé, cover letter, screening answers |
| `researching-companies` | Due diligence before applying, before an interview, or before accepting |
| `preparing-for-interviews` | An interview is booked |
| `drafting-outreach-replies` | A recruiter emailed or messaged you on LinkedIn |

### How they fit together

`assessing-job-fit` is the hub. Phoenix required its output before it would write a cover
letter or a tailored résumé, which meant it silently ran the fit analysis first every time.
That dependency is real and the skills keep it: tailoring an application to a job you
should not take is the most expensive kind of wasted evening.

```
   profile/resume.json        ────┐
   profile/honest-context.md  ────┤
   profile/preferences.md     ────┤
   applications/<slug>/job.md ────┼──→  assessing-job-fit  ──→  fit.md
   research/<company>.md      ────┘                    │
   ▲                                                   │
   │                                                   ├──→  tailoring-applications
   researching-companies                               │      resume.json
                                                       │      cover-letter.md
                                                       │      questions.md
                                                       │
                                                       ├──→  preparing-for-interviews
                                                       │      interview-prep.md
                                                       │
                                                       └──→  drafting-outreach-replies
                                                              contacts.md

   job-search-workspace underlies all of it: the layout, the schemas, the import and
   export paths, and the revision discipline.
```

Read it as: everything needs `profile/`, most things want `research/`, and the three
producing skills on the right all read `fit.md`.

`profile/honest-context.md` is the piece with no equivalent in off-the-shelf tools. It is
your private, unvarnished statement of what you actually want, what you will not accept,
what your visa and salary situation really is, and what you are genuinely bad at. It never
goes to an employer. It is the difference between output that sounds like you and output
that sounds like a language model being encouraging.

## Install

Each skill is a directory containing `SKILL.md`, plus optional `references/` and
`scripts/`. That layout is the same across Claude Code, Codex and most other agents, so
installing is copying folders.

```bash
git clone https://github.com/arashbehmand/phoenix-skills.git
cd phoenix-skills
```

**Claude Code** — personal, available in every project:

```bash
mkdir -p ~/.claude/skills
cp -R skills/* ~/.claude/skills/
```

Or per project, committed alongside the work: copy into `.claude/skills/` instead.

**Codex** — skills live under `$CODEX_HOME/skills`, which defaults to `~/.codex/skills`:

```bash
mkdir -p ~/.codex/skills
cp -R skills/* ~/.codex/skills/
```

**Other agents** — several read `~/.agents/skills`:

```bash
mkdir -p ~/.agents/skills
cp -R skills/* ~/.agents/skills/
```

If yours does none of these, point it at the `skills/` directory in this repository and
tell it to read `SKILL.md` when relevant. There is nothing runtime-specific inside them.

To update later, `git pull` and copy again.

`examples/` stays in the cloned repository — it is reference material and fixtures, not
part of a skill. To check that the scripts work in your environment:

```bash
./examples/fixtures/verify.sh
```

## Quickstart

**1. Make a workspace.** Anywhere you like; your own git repository is a good place.

```bash
mkdir ~/job-search && cd ~/job-search && git init
mkdir -p profile applications research
```

**2. Fill in `profile/`.** Three files, and the second one matters most.

- `profile/resume.json` — your CV in [JSON Resume][jsonresume] format. If you have a PDF or
  a Word document, hand it to the agent and ask it to convert; `job-search-workspace`
  covers the import.
- `profile/honest-context.md` — the private one. Write it badly and quickly rather than not
  at all. Salary floor, visa situation, what you will not do, what you are weak at.
  [Here is a filled-in example.](examples/workspace/profile/honest-context.md)
- `profile/preferences.md` — how you want output written. Optional, but it is where
  "never use the word spearheaded" goes.

**3. Save a posting** to `applications/<company>-<role>/job.md`.

**4. Ask for what you want.** In plain language:

> Should I apply to this? — `applications/kestrel-labs-senior-data-engineer/job.md`

> Research Kestrel Labs before I answer this recruiter.

> Tailor my CV and write a cover letter for the Kestrel Labs role.

> I have an interview Friday. Prep me.

> Priya just messaged me — here is what she said. Draft a reply.

The agent picks the skill. You do not invoke them by name.

**5. Get a PDF.** There is no renderer here and there does not need to be one. Export to
Reactive Resume v5 JSON, import it at [rxresu.me][rxresume], adjust it visually, download
the PDF. `job-search-workspace` has the converter and the field-mapping details that make
the import land correctly.

### See it filled in first

[`examples/workspace/`](examples/workspace/) is a complete fictional workspace — one
candidate, three applications at three different stages, and a company research file. It
is worth five minutes before you write your own `honest-context.md`.

## Tracking

There is no board, no daemon and no status enum. Tracking is
[`applications.md`](examples/workspace/applications.md): one Markdown table, one row per
application, one word for the stage.

It exists to answer one question — when a message arrives naming only a company, which
folder holds that job description, that fit analysis and that thread? The folder slug does
the work. The table is how you find it.

Markdown because you can edit it by hand, diff it, and read it on GitHub without any of
this installed.

## Status

Under construction, one skill at a time.

- [x] Repo scaffold, example workspace
- [x] `job-search-workspace`
- [ ] `assessing-job-fit`
- [ ] `tailoring-applications`
- [ ] `researching-companies`
- [ ] `preparing-for-interviews`
- [ ] `drafting-outreach-replies`
- [ ] `docs/chrome-extension.md`, `docs/design-notes.md`

## Where this came from

Phoenix was six repositories and a hosted service. Reading it carefully, the pipeline
engine was dead code, the company researcher's ten scrapers existed to seed a model that
searched the web anyway, and the job watcher computed a similarity score and threw it away
into a placeholder string. Meanwhile nine prompt files carried nearly all the value, along
with a handful of details that only show up after something has broken in production.

Those details are ported deliberately and they are the reason this is not just a folder of
prompts: the JSON Resume field names that silently produce an empty résumé when you get
them wrong, the company-and-position mapping that was swapped for several commits on the
strength of an incorrect code comment, the section-overflow split that works around a
résumé builder refusing to break a block across pages, and the revision discipline that
stops edit number four from undoing the fix from edit number two.

`docs/design-notes.md` will record what was dropped and why, so it does not get added back.

## Licence

MIT. See [LICENSE](LICENSE).

[phoenix]: https://github.com/arashbehmand/phoenix
[jsonresume]: https://jsonresume.org/schema/
[rxresume]: https://rxresu.me/
