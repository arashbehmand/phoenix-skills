# Senior Data Engineer, Streaming Platform — Kestrel Labs

- **Source:** company careers page
- **URL:** https://example.com/kestrel-labs/careers/senior-data-engineer-streaming
- **Captured:** 2026-08-24
- **Location:** London (Farringdon), hybrid — 2 days a week on site
- **Salary:** £78,000 – £92,000 + equity
- **Visa:** "We are a licensed sponsor and can support Skilled Worker visas."

---

## About Kestrel Labs

Kestrel Labs builds carbon-accounting infrastructure for logistics and freight. Our API
turns raw shipment and telematics data into audited emissions figures that our customers
report to regulators and to their own customers. We are 140 people, Series B, with
customers across UK and EU freight and two of the four largest UK grocery retailers.

Emissions data is only useful if it is current. Our platform is moving from overnight
batch to continuous processing, and this role owns that move.

## The role

You will join the Platform team (nine engineers, three of them on data) and take ownership
of our streaming ingestion and processing layer. Today roughly 80% of customer data
arrives as nightly file drops and is processed in Spark. We want the majority of it flowing
through Kafka and Flink within eighteen months, without breaking the audit guarantees our
customers depend on.

This is a build role, not a maintenance one. The batch platform works; we are choosing to
replace it.

## What you will do

- Design and own the streaming ingestion layer: Kafka topics, schema registry, contracts
  with the twelve teams and partners who publish into it.
- Build stateful stream processing in Flink for emissions calculations that must be
  reproducible and auditable months after the fact.
- Run the migration from the existing Spark batch pipelines, path by path, with no gaps in
  the customer-facing figures.
- Set the standard for data quality and lineage across the platform — we are subject to
  external audit and need to be able to explain any published number.
- Work directly with the Emissions Science team to turn methodology changes into
  production changes.
- Mentor the two mid-level engineers on the data side.

## What we are looking for

**Required**

- 5+ years building production data platforms.
- Deep Python and SQL. You should be comfortable owning the design, not just the code.
- Production experience with a stream processing framework — Flink strongly preferred,
  Spark Structured Streaming or Kafka Streams considered.
- Strong Kubernetes. Our entire platform runs on EKS and you will be operating your own
  services, not handing them to an ops team.
- Experience with data contracts, schema evolution and backwards compatibility in a
  multi-producer environment.
- A track record of migrating a live system without downtime.

**Nice to have**

- Iceberg or Delta Lake at scale.
- Terraform.
- Exposure to a regulated or audited data environment.
- Interest in climate — you do not need a background in it, but you will be reading
  methodology documents.

## How we work

Two days a week in the Farringdon office, Tuesdays plus one you choose. Async-first
otherwise. Six-week cycles with a two-week cooldown. No on-call rotation for the data team
today; that will change as streaming goes live and we will design it together.

## Benefits

- £78,000 – £92,000 depending on experience, plus equity
- 28 days holiday plus bank holidays, plus the week between Christmas and New Year
- £1,500 annual learning budget
- Private medical, 6% employer pension
- Skilled Worker visa sponsorship available

## Process

1. 30-minute intro call with the recruiter
2. 60-minute technical conversation with two platform engineers — systems design, no
   live coding
3. Take-home (3 hours, paid) or a walkthrough of your own prior work, your choice
4. 45 minutes with the Head of Platform
5. 30 minutes with the Emissions Science lead

We aim to complete this in three weeks.
