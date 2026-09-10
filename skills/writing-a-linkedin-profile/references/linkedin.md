# LinkedIn, in detail

## How recruiter search actually weights the profile

Recruiters find people through a keyword search over the profile. The fields are not weighted
equally:

- **The headline and the current job title carry most of it.** A specialty named in the
  headline does more for search rank than the same specialty three times in the About.
- **Consistency compounds.** If the headline says "streaming data platforms", the About
  tells streaming stories, the current role's title contains "Data Engineer", and the
  skills list has "Apache Kafka" and "Apache Flink", the profile ranks well because every
  signal agrees. One section pointing a different way dilutes all of them.
- **Repetition past a point works against you.** The same term five times in the headline
  or ten times across the About is read as manipulation by the ranker and as desperation by
  a person. Use the important terms once or twice each, in a real sentence.
- **Recent edits and recent activity help.** A profile updated this month ranks above the
  same profile last touched a year ago.

## The fold

The About shows its first ~3 lines (about 220 characters on desktop, fewer on mobile)
before a "see more". Everything that has to land — what the candidate does, for whom, and
the one number worth leading with — goes above that break. No throat-clearing, no "I am a
passionate professional with a proven track record".

## Rough limits

These move; `scripts/charcount.py` reports the current text's length and the candidate
should confirm in LinkedIn before saving.

| Field | Limit |
|---|---|
| Headline | 220 |
| About | 2,600 |
| Experience entry description | 2,000 |
| Connection request note | 300 |

## The full profile audit

1. **First impressions.** Custom URL set? Banner not the default? Photo a head-and-
   shoulders, not a cropped group shot? These are quick wins and worth a line each.
2. **Headline.** Is it a sentence about what the candidate does and for whom, or a pipe-
   separated keyword list? Give the current one, then an optimised one, with counts.
3. **Content deep dive.** The About: does the hook land above the fold, is it first person,
   does it tell one or two real stories with numbers rather than list adjectives? The
   experience entries: do the bullets lead with outcomes, STAR-compressed, the way a
   résumé bullet does?
4. **Skills and endorsements.** Are the top three skills the ones the target roles search
   for? Are there skills listed that the experience does not evidence? Reorder so the
   highest-search-weight skills are first.
5. **Action items.** One to three things to change now, prioritised, each a few minutes.

## The headline

Good: a specialty, the function or domain, and something that differentiates — a scale, a
niche, a result.

> Senior Data Engineer | streaming and near-real-time platforms | cut a retailer's
> pipeline cost 30% while halving runtime

Bad, and penalised: the keyword list.

> Data Engineer | Data Engineering | Big Data | ETL | Spark | Kafka | Airflow | dbt | SQL |
> Python | AWS | Data Pipelines | Data Warehouse

## Numbers and gaps

Every claim of impact wants a number, and you must not invent one. If the candidate has it,
use it; if not, write `[metric]` and leave it for them to fill. A gap the candidate is
closing is a real, linkable project or a portfolio page — never a fabricated role or a
company that does not exist. The old habit of inventing an employer to cover an employment
gap is a serious risk in an interview and in a reference check; do not do it, and say so if
asked.

## What this skill will not do

LinkedIn's terms forbid automation, scraping, and inauthentic engagement, and a profile
built on those is fragile. If asked to set up connection automation, buy connections or
endorsements, join or run an engagement pod, or generate fake activity, decline and offer
the manual version: a good profile, a steady cadence of real posts and comments, and
targeted connection requests with a short honest note.
