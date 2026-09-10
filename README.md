# Phoenix Skills

A job search toolkit for coding agents. Works with Claude Code, Codex, Cursor, and anything
else that reads skill files.

Your CV, your notes and your applications live in a folder on your computer. The agent reads
them and helps you apply.

## What it does

One application eats an evening. You rewrite the CV, write the cover letter, read up on the
company, answer the screening questions, then try to remember what you told the recruiter
last week.

Twelve skills, in two groups.

**Before you apply to anything**, they help you get your own material in order:

- **Interview you for honest context.** Fifteen minutes on what you actually want, what you
  will not accept, and what you are not good at yet. Every other skill reads the result.
- **Work out what to aim for.** Sort the jobs you have been eyeing into a primary and a
  secondary track, and name the gap between where you are and where you want to be.
- **Roast your CV.** A blunt, line-by-line read the way a sceptical recruiter would do it,
  with a list of what to fix first and what not to touch.
- **Build the base CV**, iteratively, keeping a log of what changed and what you left off
  on purpose.
- **Write your LinkedIn profile** so it points recruiters at the same thing your CV does.

**Then, per application**, they share the evening's work:

- **Decide whether to apply.** An honest read of the job, the company, and how a recruiter
  will see you. It will tell you to skip one.
- **Research the company** before you spend time on it: funding, reviews, salary ranges, red
  flags, and whether they hold a UK visa sponsor licence.
- **Rewrite your CV for the job.** It reorders, cuts and rephrases what you have already
  done. It will not add anything you have not.
- **Write the cover letter and the screening answers**, using your own numbers.
- **Prepare you for the interview.** Twenty questions, including the ones you are dreading,
  and the answers worth having ready.
- **Draft replies to recruiters** that know which job they are about, what stage you are at,
  and what you already agreed to.
- **Tell you what you have forgotten.** What is due, what is booked, and who has gone
  quiet, read off your own notes.

Everything is saved as plain Markdown and JSON in your folder. You can read it without any of
this installed, edit it by hand, and keep it in git if you like.

## What you need

An agent that reads `SKILL.md` files, and a folder.

No API keys. No account. No server. Nothing runs in the background. Your files stay on your
machine, and nothing is sent anywhere unless you ask for a web search.

## Install

Copy the skill folders where your agent looks for them.

```bash
git clone https://github.com/arashbehmand/phoenix-skills.git
cd phoenix-skills

# Claude Code
mkdir -p ~/.claude/skills && cp -R skills/* ~/.claude/skills/

# Codex
mkdir -p ~/.codex/skills && cp -R skills/* ~/.codex/skills/

# other agents often read this one
mkdir -p ~/.agents/skills && cp -R skills/* ~/.agents/skills/
```

If yours does none of these, point it at the `skills/` folder and tell it to read `SKILL.md`
when it needs to. There is nothing inside them tied to a particular tool.

Check the scripts run on your machine:

```bash
./examples/fixtures/verify.sh
```

## Start

**Make a folder.** Anywhere. Your own git repository is a good place.

```bash
mkdir ~/job-search && cd ~/job-search
```

**Add three files to `profile/`.** Ask your agent to do it, or write them yourself.

- `resume.json` is your CV in [JSON Resume](https://jsonresume.org/schema/) format. If you
  only have a PDF or a Word file, hand it over and ask for it to be converted.
- `honest-context.md` is the private one. See below.
- `tone.md` says how anything written in your name should sound. Everything else you want
  done a particular way goes in `preferences.md`. Both optional, both worth ten minutes.

**Save a job ad** to `applications/<company>-<role>/job.md`, or paste the link and ask for it
to be saved.

**Then just ask.** In your own words:

> Interview me for my honest context.

> Roast my CV, then help me fix it.

> What kinds of roles should I be aiming at?

> Should I apply to this?

> Research them before I answer this recruiter.

> Tailor my CV and write the cover letter.

> I have an interview on Friday. Prep me.

> Priya just messaged me. Here is what she said. Draft a reply.

You never name a skill. The agent picks the right one.

## The private file

`profile/honest-context.md` is where you write the things you would not put in a cover
letter. What you actually want. What you will not accept. Your salary floor. Your visa
situation. What you are genuinely not good at yet.

It never goes to an employer. Without it the agent has to guess at your situation, and it
usually guesses something cheerful and wrong.

The best way to write it is not to write it. Say "interview me for my honest context" and
answer the questions — it takes about fifteen minutes, and being asked "what would make you
turn down an offer you otherwise wanted?" gets further than staring at an empty file.

Otherwise: badly and quickly beats not at all. Half a page is enough to start, and there is a
[filled-in example](examples/workspace/profile/honest-context.md) if you want a shape to copy.

The skills run without it and will tell you the answer is weaker for it.

## The skills

| Skill | When it runs |
|---|---|
| [`job-search-workspace`](skills/job-search-workspace/) | Setting up the folder, importing a CV, exporting one |
| [`interviewing-for-context`](skills/interviewing-for-context/) | Before any job ad: recording what you want, will not accept, and are not good at yet |
| [`aligning-career-targets`](skills/aligning-career-targets/) | You are not sure what to apply for; sorting roles into a primary and secondary track |
| [`roasting-a-resume`](skills/roasting-a-resume/) | You want your CV or LinkedIn torn apart before you send it anywhere |
| [`building-a-resume`](skills/building-a-resume/) | Improving the base CV itself, not tailoring it to a posting |
| [`writing-a-linkedin-profile`](skills/writing-a-linkedin-profile/) | Writing or auditing your own headline, About and experience copy |
| [`assessing-job-fit`](skills/assessing-job-fit/) | You have a job ad and want a straight answer on whether to apply |
| [`tailoring-applications`](skills/tailoring-applications/) | You are applying: CV, cover letter, screening answers |
| [`researching-companies`](skills/researching-companies/) | Before applying, before an interview, or before accepting |
| [`preparing-for-interviews`](skills/preparing-for-interviews/) | An interview is booked |
| [`drafting-outreach-replies`](skills/drafting-outreach-replies/) | A recruiter emailed or messaged you |
| [`reviewing-the-search`](skills/reviewing-the-search/) | You want to know what needs attention across all of it |

`assessing-job-fit` comes first once you have a job ad. Before that, the honest-context
interview is worth fifteen minutes, and if you are not sure what to apply for or the CV
needs work, the four skills above it help. The tailoring and interview skills read the file
`assessing-job-fit` writes, so you find out a job is wrong before you spend the evening on
it rather than after.

## Getting a PDF

This does not render PDFs. Ask for the Reactive Resume export, import the file at
[rxresu.me](https://rxresu.me/), adjust it on screen, and download the PDF from there. The
converter handles the field mapping, and it splits a long work history across two pages so
the last job does not get cut off.

You can also ask for a Markdown version to paste into an email.

## Keeping track

One file, `applications.md`, with one row per application and one word for the stage.

It is there for the moment a message arrives naming only a company. Search the table, open
the folder it points to, and the job ad, the fit analysis and the earlier conversation are
all sitting in it.

What is *due* lives somewhere else: each application's `notes.md` keeps a dated timeline —
including things that have not happened yet, like Friday's interview — and a `Next` list.
Ask "what needs attention this week" and you get it read back off those, sorted, with
whatever has gone quiet. Nothing runs in the background and there is no second file holding
a copy of your status.

## See it filled in

[`examples/workspace/`](examples/workspace/) is a complete example: one fictional candidate,
three applications at three stages, and a company research file. It is the quickest way to
see what you actually get.

## What it will not do

- It does not find jobs. You bring the ad.
- It does not apply or send anything for you. You read every draft first.
- It will not put experience on your CV that you do not have. Push it and it will still
  refuse, and say plainly in the cover letter what you have not done.

## Where it came from

Phoenix was a job application assistant I built in 2024. Six repositories, a web app, a
database, a message queue, a scraper fleet and a PDF renderer. Reading it back, most of that
was scaffolding. The value sat in nine prompts and a short list of things I only learned
after something broke in production.

Agents handle the rest on their own now, so this is the part worth keeping. A few things that
cost me real time are baked in: the CV field names that quietly produce an empty export when
you get them wrong, the two fields that stayed swapped for weeks because a code comment said
they should be, and the rule that stops the fourth edit undoing the fix from the second.

## Licence

MIT. See [LICENSE](LICENSE). Use it however you like.
