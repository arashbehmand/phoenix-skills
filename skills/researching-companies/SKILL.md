---
name: researching-companies
description: Use when someone needs to know who they would actually be working for — before applying, before an interview, before accepting an offer, or when a recruiter names a company nobody recognises.
---

# Researching companies

Produce due diligence on an employer and write it to `research/<company>.md`. One file per
company, not per application — a company can produce several roles.

Phoenix ran ten scrapers to feed this, across two paid APIs, a Cloudflare solver and a
residential proxy. They are not ported, because the report prompt already tells the model
to search the web itself and the scraped JSON was only ever seed data. What is ported is
the prompt, the required coverage, and the one dataset that is genuinely unobtainable by
search — see `scripts/uk_visa_sponsor_lookup.py`.

## Two rules that decide whether this is useful

### 1. Verify you have the right company

**Name collision is the top failure mode**, and it produces confident, detailed, entirely
wrong reports.

Phoenix's own shipped test fixture is the cautionary case: a search for **OpenAI** matched
a London company called **Morena** at a similarity score of 66, and the code then recorded
`is_visa_sponsor: True`. Nothing downstream could tell that the report was about a
different organisation.

So before writing anything, pin down which entity this is: the registered legal name, the
country, the industry, and roughly the size. Then check every result against it. When the
first page of search results is dominated by a better-known company with the same name,
**say so in the report** — a short section at the top listing who is who is worth more
than anything else on the page, because it is what stops the reader quoting the wrong
company's revenue in an interview.

If you cannot establish which company this is, say that rather than guessing.

### 2. Estimate where the data is private — and label it

Most companies worth researching are private and do not publish revenue. A model asked
for financial health with no permission to estimate will simply decline and return
nothing useful.

So estimation is explicitly permitted: use industry benchmarks, headcount, funding stage
and typical margins to give a range. Phoenix's prompt said this, and it is why the reports
were worth reading.

**Every estimate must be labelled as an estimate, with its derivation shown.** Phoenix's
prompt did not require this, which is the one place its output was actively dangerous — a
candidate who repeats an inferred revenue figure in an interview as though it were fact
has damaged themselves with something you told them.

The form that works:

> **Estimated ARR: $8M–$14M.** Derived from 140 employees at a typical growth-stage B2B
> SaaS ratio of $70k–$100k per employee. **This is an estimate. Do not repeat it in an
> interview as fact.**

A sourced figure and an estimated one must never look alike on the page.

## Required coverage

Adapt the structure to the company — a public multinational and a twelve-person startup
do not want the same report — but cover all of this, and say explicitly when something
could not be found:

- **Business overview and company phase** — what they sell, to whom, mission and values,
  and whether they are a startup, growing, mature or public.
- **Financial health, funding and revenue** — funding rounds, investors, revenue streams,
  profitability, and any financial risk. Estimates permitted and labelled.
- **Culture and employee satisfaction** — reviews and ratings, work-life balance,
  management quality, career development, diversity and inclusion.
- **Red flags** — layoffs, turnover, poor management reviews, lawsuits, concerning
  trends. Look for these deliberately; they do not surface on their own.
- **Salary ranges in local currency** for the relevant roles.
- **Interview process and difficulty** — stages, format, common questions, candidate
  reports.
- **Benefits and perks.**

Two more, when the candidate's `honest-context.md` calls for them:

- **Work authorisation** — if they need sponsorship, this goes first and everything else
  is secondary. See below.
- **Anything else named as a dealbreaker** — if they will not work in a given industry or
  reporting structure, check for it explicitly.

`references/sources.md` covers where to look and what each source uniquely offers.

## Visa sponsorship (UK)

For a candidate who needs a Skilled Worker visa this is binary and comes before everything
else: an employer without a licence cannot hire them.

```bash
python3 <skill>/scripts/uk_visa_sponsor_lookup.py "Kestrel Labs"
python3 <skill>/scripts/uk_visa_sponsor_lookup.py "Acme" --town London --json
```

It downloads the Home Office register (about 143,000 organisations), caches it for a week,
and shows the rows that plausibly match. **No API key, one request to gov.uk.**

Exit codes: `0` rows found, `1` nothing plausible, `2` the lookup failed.

The script deliberately does not decide. It shows what the register says and leaves the
identification to you, because that is exactly where Phoenix's version went wrong. Read
its output the way it asks to be read:

- On the register means they **hold a licence**, not that they will sponsor this role.
- The route matters — a Temporary Worker or Student licence is not a Skilled Worker one.
- Absent is strong evidence, not proof. Try the registered name (Companies House has it),
  the parent company, the UK subsidiary, and any former name. Deliveroo is on the register
  as "Roofoods Ltd t/a Deliveroo".
- Matches labelled *shares only the leading word* are almost always a different business.

Outside the UK there is no equivalent single register; check the employer's careers page,
ask the recruiter directly, and treat the answer as unverified until it is in writing.

## Optional: UK Companies House

A free API key from [developer.company-information.service.gov.uk](https://developer.company-information.service.gov.uk/)
unlocks the highest signal-per-line in the whole exercise, and none of it is obtainable by
searching: officer rosters with appointment and resignation dates, persons with
significant control and their natures of control, `has_insolvency_history`,
`has_been_liquidated`, and whether accounts or the confirmation statement are overdue.

Three directors resigning in one quarter, or accounts filed late two years running, is the
kind of thing no press release mentions.

Everything else in this skill works without it. Do not treat it as required, and do not
ask the user to get one unless the company's solvency is genuinely in question.

## Output

Write `research/<company>.md`. Adapt the headings to the company; the required coverage
above is the contract, not a fixed template.

Open with company verification whenever there is any ambiguity about identity, and close
with a sources list and a confidence statement that distinguishes what was sourced from
what was estimated:

> **Confidence:** High on sponsorship, solvency, benefits and process — all directly
> sourced. Medium on culture and turnover — small review samples and one inference from
> LinkedIn. Low on revenue, runway and equity — all explicitly estimated and labelled.

Date the file. Company research goes stale, and a reader six months later needs to know.

## Do not

- Report on a company you have not confirmed is the right one.
- State an estimate as a fact, or leave a figure's provenance ambiguous.
- Present a single Glassdoor review as a pattern. Give the sample size — 31 reviews for a
  140-person company moves on two disgruntled leavers, and saying so is part of the
  finding.
- Infer things about named individuals from their social media and present it as company
  research. "Two engineering leads appear to have left in Q1" is a weaker class of
  evidence than a filing, and must be marked as such.
- Scrape LinkedIn. Phoenix's Voyager scraper is not ported: rotating query ids, cookies
  that expire in weeks, a terms-of-service violation and a real risk of the user's account
  being banned. If a LinkedIn MCP server is available and the user has chosen to use it,
  that is their decision to make, not yours.
- Pad the report. If a company is small and private and there is little to find, a short
  honest report that says so beats a long one built on inference.

## Next

- Deciding whether to apply → **assessing-job-fit**
- Applying → **tailoring-applications**
- An interview is booked → **preparing-for-interviews**
