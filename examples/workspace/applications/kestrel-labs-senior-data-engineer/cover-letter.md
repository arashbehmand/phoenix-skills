Dear Hiring Manager,

Your job description says that roughly 80% of customer data still arrives as nightly file
drops, and that you are choosing to replace a batch platform that works. That is the part
that made me apply. I have spent the last three years doing the unglamorous version of
this at Halcyon Retail Group: moving live pipelines that finance and merchandising depend
on every morning, without the numbers changing while I did it. When I rebuilt our nightly
sales and stock pipeline, the critical path went from six hours ten minutes to one hour
fifty, and the 07:00 reporting deadline went from being missed twice a month to not being
missed at all in fourteen months. Before that I moved sixty live SQL Server procedures
onto Redshift and dbt in staged cutovers with no reporting gap.

I should be straight with you about where I do not match the description. I have run Kafka
as a transport layer, with schema contracts across twenty-seven external publishers and
three internal consumers, and I built an open-source tool for replaying event streams
against local brokers. I have not owned a Flink or Spark Streaming system serving live
traffic, and my Kubernetes is reading manifests and deploying to a cluster somebody else
operated. You asked for strong Kubernetes and production stream processing, so you should
know that from me rather than find it in round two. What I bring instead is the migration
itself — twelve producing teams, an audit trail that has to survive being questioned
months later, and a cutover where nobody downstream notices. That is the risky part of
your eighteen-month plan, and it is the part I have done.

The work also matters to me in a way that is easy to claim and harder to prove, so I will
keep it short: emissions figures that customers report to regulators have to be right, and
I like problems where being roughly right is not good enough. I would welcome the chance
to talk about how you are handling reproducibility of calculations across a methodology
change — that is the design question I would want to get right first.
