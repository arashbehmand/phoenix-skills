# LinkedIn profile

*Generated 2026-09-03 · inputs: profile/resume.json, profile/honest-context.md, profile/tone.md, profile/career-plan.md, profile/resume-notes.md*

## Strategy note

Aimed at senior data engineering roles at companies still building a platform, ideally with
streaming in the mix, and all holding a UK sponsor licence. Every section points the same
way: cost and runtime results, not tool lists, and a clear "moving toward streaming"
signal. The current employer is named plainly; nothing here says "actively looking".

## Headline

Senior Data Engineer at Halcyon Retail Group. I make data platforms faster and cheaper, not just bigger. Moving toward streaming and near real time.  `[148/220]`

## About

First three lines (above the "see more" fold, where the hook lands):

I have spent nine years making data pipelines faster and cheaper rather than just bigger. Right now I own the analytics platform for a 400 person UK retailer, serving merchandising, supply chain and finance.

The work I am proudest of is the unglamorous kind. I rebuilt a nightly sales and stock pipeline so it finishes in under two hours instead of six, and moved a 07:00 reporting deadline from missed twice a month to not missed in fourteen months. I took 14 thousand pounds a month off the cloud bill by swapping always on clusters for transient ones. I put contract tests on 240 dbt models and cut schema drift incidents from eleven in a year to two.

What I want next is streaming and near real time. I have run Kafka as a transport layer and built a stock movement feed that got store level latency under 30 seconds. I want to go deeper: event driven platforms that serve live traffic, not another batch warehouse.

Outside work I maintain stockstream, a small open source tool for replaying retail stock events against a local Kafka cluster. It has around 300 stars and is used by a couple of teams I have never met.

Tools I reach for: Python, Spark, Airflow, dbt, Kafka, and AWS. I read Scala. I am currently working through Flink, and learning to operate Kubernetes properly rather than just deploy onto a cluster someone else runs.  `[1339/2600]`

## Experience

### Senior Data Engineer at Halcyon Retail Group

I own the analytics platform for merchandising, supply chain and finance across 180 stores and the e-commerce estate.

Rebuilt the nightly sales and stock pipeline on Spark and Airflow. Critical path runtime went from 6h10 to 1h50, and the 07:00 reporting SLA went from missed twice a month to zero misses in fourteen months.

Cut platform cloud spend by 14 thousand pounds a month, about a third, by replacing 40 always on EMR hours a day with transient clusters and moving cold history to cheaper storage.

Brought in dbt with contract tests and CI on 240 models. Schema drift incidents dropped from eleven in 2023 to two in 2025.

Built a Kafka based stock movement feed that three other teams now consume, replacing a 15 minute polling job and bringing store level stock latency under 30 seconds.

### Data Engineer at Halcyon Retail Group

Migrated 60 legacy SQL Server stored procedures to a Redshift and dbt stack and retired a 40 thousand pound a year licence. Wrote the ingestion framework still used for all 27 supplier feeds, which took new feed onboarding from about three days to half a day.

### Data Engineer at Vantiq Software

Delivered ETL and reporting platforms for six client engagements across insurance and telecoms. Rewrote one client's month end close from a row by row Oracle procedure into set based SQL and took the run from nine hours to 40 minutes.

## Skills, in order

1. Apache Kafka
2. Apache Spark
3. dbt
4. Apache Airflow
5. Python
6. AWS
7. SQL
8. Data pipeline architecture

## Risk notes

- Turning on a public "Open to Work" badge is visible to the current employer. Given the
  situation in honest-context, keep it to "recruiters only", or leave it off and rely on
  the profile being strong.
- The headline names Halcyon. That is normal and fine, but it does mean a colleague who
  looks will see the "moving toward streaming" line. It is not a resignation notice, and it
  is true, so it stays.

## Revision log

- **2026-09-03** · first full draft from the updated résumé.
- **2026-09-03** · "the about read like a brag list" · broke the results into one story per
  paragraph and moved the streaming line up so it is not buried under the cost savings.

## What this profile does not do

- No automation, no scraping, no engagement pods, no bought connections or endorsements.
  If any of that comes up, the answer is a manual approach: a strong profile, real posts
  and comments at a steady pace, and connection requests with a short honest note.
