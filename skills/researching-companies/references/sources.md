# Where to look, and what each place uniquely gives you

A checklist for searching, not for scraping. Every one of these is readable in a browser
and most are search-indexed; none needs a paid API. Phoenix built extractors against
several of them and the extractors are not ported — they were seed data for a model that
searches anyway, and they broke on somebody else's schedule.

Work down this list roughly in order. Stop when you have what the candidate actually
needs; a twelve-person startup will exhaust the useful sources in fifteen minutes.

## Identity first

**Companies House** (UK) · `find-and-update.company-information.service.gov.uk` — free,
no key needed to browse. The registered name, company number, incorporation date,
registered office, SIC codes, filing history, officers and persons with significant
control. This is how you settle *which* company you are researching, and it is the answer
to most name collisions.

Equivalents: OpenCorporates (multi-jurisdiction, patchy), the SEC's EDGAR (US public
companies), and the local business register elsewhere.

**The company's own site** — products, customers, mission, values, leadership, careers.
The careers page often states visa policy, office locations and the interview process more
plainly than the job posting does. The about page tells you what they think they are.

## Money

**Crunchbase** — funding rounds, amounts, dates, investors, acquisitions. The free tier
shows enough. Round *size and date* is the useful part: a large round eighteen months ago
with visible hiring is a different company from the same round with a hiring freeze.

**Companies House filings** (UK) — the accounts. For a private company this is the only
real financial data that exists. Even abridged accounts give you whether they filed on
time, whether there is an insolvency history, and the direction of travel.

**News and trade press** — funding announcements, layoffs, contract wins, executive
changes. Search the company name with `layoffs`, `redundancies`, `funding`, `acquisition`,
`lawsuit`.

**Public markets** — for a listed company, the annual report and investor calls are
authoritative and nothing else is needed.

Where none of this exists, estimate and label it. See the SKILL.md rule.

## People and culture

**Glassdoor** — the densest single source, and the one that needs the most care.

- Overall rating, plus the sub-ratings that actually differentiate: work-life balance,
  compensation and benefits, senior management, career opportunities. **Senior management
  and career opportunities are the two that predict whether someone stays.**
- Recommend-to-a-friend and CEO approval.
- **Interview reviews are a separate section** and carry a difficulty score plus
  descriptions of each stage. For interview prep this is the highest-value thing on the
  internet about a company.
- Read the most recent twelve months first. A 4.1 average that was 3.2 last year, or the
  reverse, is the finding — not the average.
- Always state the sample size. Thirty reviews for a 140-person company is thin enough
  that two angry leavers move it.

**Indeed** — a second review sample, usually a different population than Glassdoor's
(more non-engineering roles). Useful as a cross-check.

**LinkedIn** — headcount and its trend over time, which teams are growing, who leads what,
and how long people stay. Read it in a browser as a person would. Do not scrape it: see
the SKILL.md note.

**Blind** — candid, engineering-heavy, US-skewed, and unmoderated. Treat as rumour worth
knowing rather than evidence.

## Money for the role specifically

**levels.fyi** — the best compensation data that exists for technology roles, broken down
by level and location, and it distinguishes base, equity and bonus. Coverage is strongest
for large US companies and thins out fast for small European ones.

**Glassdoor salaries** — broader coverage, less reliable, self-reported.

**The posting itself** — UK and EU postings increasingly state a band, and several US
states require one. If a band is published, it is better than any estimate.

**Local market data** — Hays, Robert Half and Reed publish annual UK salary guides;
equivalents exist elsewhere. Useful for sanity-checking a band against the market.

## Risk

**layoffs.fyi** — tracked layoffs at technology companies with dates and headcounts.
Absence is not proof of none, particularly outside the US and outside tech. Phoenix
harvested this through signed Airtable URLs with eight hardcoded column ids; read the site.

**Court and tribunal listings** — UK employment tribunal decisions are published and
searchable. A pattern of claims is a real signal.

**The regulator**, where the industry has one — the FCA register for UK financial
services, the CQC for care, and so on. Enforcement history is public.

**Trustpilot and app-store reviews** — customer sentiment, not employee sentiment. Useful
mainly to tell whether the product is actually working, which correlates with whether the
company is calm.

## Work authorisation

**gov.uk register of licensed sponsors** — use `scripts/uk_visa_sponsor_lookup.py`. The
register is the authority; nothing else settles this for the UK.

**The employer**, in writing. A recruiter saying "we're open to sponsorship" is not the
same as a licence, and the difference has cost people months.

## What each source is bad at

| Source | Do not use it for |
|---|---|
| Glassdoor | Small samples; anything about a company under ~50 people |
| levels.fyi | Non-US companies, non-technical roles, small companies |
| Crunchbase | Revenue. It has funding, which is a different thing |
| LinkedIn headcount | Precision — it counts profiles, not employees |
| Blind | Anything you would repeat as fact |
| The careers page | Culture. It is marketing |
| layoffs.fyi | Proving a company has *not* had layoffs |

## A note on effort

Match the depth to the decision. Before a first application, twenty minutes: identity,
sponsorship if relevant, obvious red flags, salary band. Before a final round or an offer,
do the whole list — that is the point at which solvency, management churn and the
compensation band are worth an hour.
