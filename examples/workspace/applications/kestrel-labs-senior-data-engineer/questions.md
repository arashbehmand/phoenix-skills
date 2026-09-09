# Screening question answers: Kestrel Labs

*Drafted 2026-08-26 from the application form. Questions as they appeared on the form.*

### Why do you want to work at Kestrel Labs?

Your platform is at the point I find most interesting. The batch system works and you are
choosing to replace it, which means the migration has to be done well rather than done
fast. I have spent three years moving live pipelines that a business depends on every
morning, so I know what that costs and I would rather do it somewhere the correctness bar
is externally audited than somewhere the worst case is a stale dashboard. The emissions
domain matters to me, but I would be applying for the engineering problem even if it did
not.

### Describe a time you migrated a production system without downtime.

At Halcyon Retail Group our nightly sales and stock pipeline missed its 07:00 reporting SLA
about twice a month, and the critical path ran six hours ten minutes. I had to move it to
Spark and Airflow while finance and merchandising kept reading the same numbers every
morning, so I ran both pipelines in parallel for six weeks and reconciled outputs
row-by-row before cutting any consumer over. Runtime came down to one hour fifty minutes
and we have not missed the SLA in the fourteen months since. The reconciliation period was
the expensive part and it is the part I would not skip again.

### What is your experience with stream processing?

I have run Kafka as a transport layer in production: a stock-movement feed with published
schema contracts, three downstream consumers, and store-level stock latency under thirty
seconds, replacing a fifteen-minute polling job. I also maintain an open-source tool that
replays two million recorded events against a local cluster to test consumer backpressure
and ordering. What I have not done is own a stateful Flink or Spark Streaming application
serving live traffic, and I would rather say that here than have it come out later. This
role is a step into that, not a continuation of it.

### How do you approach data quality in a regulated environment?

I treat the contract as the artefact, not the test. At Halcyon I introduced contract tests
in CI across 240 dbt models and schema validation on the ten highest-impact tables, which
took schema-drift incidents in production from eleven in 2023 to two in 2025 and caught a
corrupted supplier price feed before the pricing team saw it. The habit that matters most
is being able to explain a number after the fact, knowing which upstream version produced
it and what changed since. That is the same requirement your audit obligations create, at
lower stakes.

### Do you require sponsorship to work in the UK?

Yes. I hold a Skilled Worker visa sponsored by my current employer, valid to August 2028,
so a move would need a new Certificate of Sponsorship rather than a first-time application.
I am already in the UK and there is no relocation involved.

### What are your salary expectations?

Your posted range of £78,000 to £92,000 works for me and I would expect to land in the
middle of it based on nine years of experience and the migration ownership this role asks
for. I am happy to discuss the specific number once we both know whether the fit is right.
