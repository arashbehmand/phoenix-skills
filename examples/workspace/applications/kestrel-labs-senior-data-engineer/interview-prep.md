# 🎯 Personalized Interview Preparation Guide

*Kestrel Labs — Senior Data Engineer, Streaming Platform · round 2 of 5, 60-minute
technical conversation with two platform engineers, 2026-09-11 14:00*
*Generated 2026-09-08 · inputs: job.md, job.json, fit.md, profile/resume.json,
profile/honest-context.md, ../../research/kestrel-labs.md, contacts.md*

## 0. Executive Summary & Top Priorities

*   **Top Priority 1:** Rehearse the parallel-run reconciliation story from the Halcyon
    pipeline migration until it is thirty seconds long with the numbers in it. This is your
    strongest match against their stated "track record of migrating a live system without
    downtime," and it is the only requirement where you are likely to be stronger than the
    other finalists.
*   **Top Priority 2:** Write and say out loud, once, the sentence you will use for the
    Kubernetes gap. You have decided to disclose it; disclosure that sounds rehearsed and
    calm reads as senior, disclosure that sounds apologetic reads as a problem. Suggested
    shape: what you have operated, what you have not, what you would do in the first month.
*   **Top Priority 3:** Prepare a whiteboard-ready design for exactly-once emissions
    calculation over a replayable event stream, including what you would do when the
    Emissions Science team changes a coefficient and six months of history needs
    recomputing. Their JD says calculations "must be reproducible and auditable months
    after the fact" — this is the design question the role exists to answer.
*   **Top Priority 4:** You interview badly in the first twenty minutes by your own
    account. This is a 60-minute session, so a slow start costs you a third of it. Have the
    opening answer automatic.
*   **Estimated Prep Time:** 5-7 hours over the next three days.

## 1. Essential Knowledge & Strategic Checklist

*   **Company Deep Dive:** Carbon accounting for logistics and freight; API turns shipment
    and telematics data into audited emissions figures. 140 people, Series B. Customers
    include UK/EU freight operators and two of the four largest UK grocers. Regulatory
    tailwind from CSRD and UK reporting rules — worth being able to say the words
    "Scope 3" and mean them, since freight emissions are their customers' Scope 3.
    ⚠️ Their published mission and values statements were not in the research file; do not
    quote values back at them, because the ones you would be quoting would be invented.
*   **Job Role Mastery:** Required — 5+ years production platforms, deep Python and SQL,
    production stream processing (Flink preferred), strong Kubernetes on EKS, data
    contracts and schema evolution across multiple producers, live migration without
    downtime. Nice to have — Iceberg or Delta, Terraform, regulated/audited environment,
    interest in climate. You meet four of six required outright, partially meet one
    (streaming), and do not meet one (Kubernetes). Team is nine platform engineers, three
    on data. Six-week cycles, two-week cooldown.
*   **Résumé Alignment & Storytelling:** Halcyon pipeline rebuild → live migration
    requirement. SQL Server to Redshift/dbt cutover → second live migration data point.
    Kafka stock-movement feed and the 27-feed ingestion framework → data contracts and
    schema evolution. dbt contract tests, 11 → 2 incidents → data quality and lineage in an
    audited setting. stockstream → genuine curiosity about streaming behaviour, and the
    only evidence you have that is about streams rather than transport.
*   **Interviewer Insights & Research:** ⚠️ You have the names from the recruiter's email —
    Dev Raghunathan and one other engineer not yet named — and nothing else. No LinkedIn
    background, no talks, no repos in the research file. Do not prepare
    interviewer-specific angles you cannot support; ask the recruiter for the second name
    and their focus areas instead. That request is normal and gets answered.
*   **Logistics & Etiquette:** 60 minutes, systems design, no live coding. Confirm the
    platform and whether they expect you to share a screen or use a shared drawing tool.
    Have a diagramming surface ready either way. Follow up within 24 hours with a short
    note that adds one thing you did not say in the room.
*   **Mindset & Confidence:** Your gaps are real and you have already decided to name them.
    That decision removes the thing that usually makes people tense in these rooms.
    Go in on the basis that they invited a candidate whose CV visibly does not say Flink or
    Kubernetes, which means they read it and wanted to talk anyway.

## 2. Top 20 Tailored Interview Questions

1.  "Walk us through the nightly pipeline migration at Halcyon. What did the cutover
    actually look like?" (Rationale: directly probes the JD's "track record of migrating a
    live system without downtime.")
2.  "Tell us about a time you had to keep a system correct while changing it underneath.
    How did you know it was still correct?" (Rationale: behavioural framing of the audit
    and reproducibility requirement.)
3.  "Describe a disagreement with a data consumer about a contract or a schema change. How
    did it end?" (Rationale: they will have twelve publishing teams and you would own the
    contracts; conflict handling is the real skill there.)
4.  "You mentored two juniors at Halcyon. Give a specific example of something one of them
    got wrong and what you did." (Rationale: the JD includes mentoring two mid-level
    engineers; generic mentoring answers are worthless here.)
5.  "Tell us about a time you shipped something you later regretted technically."
    (Rationale: standard senior-level probe for self-assessment; your Spark-era answer or
    the reconciliation-period answer both work.)
6.  "Describe a time you pushed back on a deadline or a scope." (Rationale: six-week cycles
    plus a live migration means scope negotiation is part of the job.)
7.  "How would you design exactly-once emissions calculation over a replayable event
    stream?" (Rationale: the central technical requirement — stateful stream processing
    that must be reproducible and auditable.)
8.  "The Science team changes a coefficient. Six months of published figures are now wrong.
    What happens?" (Rationale: JD says "translate methodology changes into production
    changes"; this is that requirement as a design problem.)
9.  "How do you handle schema evolution when you have twelve producers and you cannot make
    them all deploy at once?" (Rationale: the JD's exact phrasing on backwards
    compatibility in a multi-producer environment.)
10. "Talk us through how you would run this service on Kubernetes — deployment,
    autoscaling, what breaks at 3am." (Rationale: the "strong Kubernetes, you operate your
    own services" requirement. **This is your weakest question. Prepare the honest answer,
    not a bluffed one.**)
11. "Compare Flink and Spark Structured Streaming for this workload." (Rationale: they will
    accept reasoning over experience here, but you need to have actually read enough to
    reason — watermarking, state backends, checkpointing semantics.)
12. "80% of data arrives as nightly file drops today. Which path do you migrate first and
    why?" (Rationale: the JD says "path by path, with no gaps"; they want to hear
    sequencing judgement, not enthusiasm.)
13. "A customer says an emissions figure we published last quarter is wrong. Walk us
    through the next hour." (Rationale: situational test of lineage and auditability
    thinking under pressure.)
14. "You are three data engineers running a migration of twelve producing systems. Halfway
    through, one of the three leaves. What changes?" (Rationale: their team is thin and
    they know it; tests prioritisation realism.)
15. "You inherit a Flink job you did not write and it is falling behind. First moves?"
    (Rationale: situational, and deliberately in your gap area — they are testing whether
    you can reason about an unfamiliar system methodically.)
16. "On-call does not exist for the data team today and will once streaming is live. How
    would you want it designed?" (Rationale: the JD explicitly flags this as an open
    question to be designed together — they will genuinely want your answer.)
17. "Why Kestrel, and why now?" (Rationale: fit; you have been at one company for five
    years and they will want to know what changed.)
18. "How do you feel about the two-days-in-Farringdon arrangement, given you are in
    Manchester?" (Rationale: they know your location from the CV; this will come up and
    your answer needs to be settled beforehand, not improvised.)
19. "Where do you want to be in three years — deeper technically, or leading a team?"
    (Rationale: career vision; your honest context says explicitly you do not want to
    manage in the next two years and that you let interviewers talk you out of saying so.)
20. "What would make you turn this role down?" (Rationale: career vision and honesty probe;
    a candidate with no answer reads as either desperate or evasive.)

*(Behavioural: 6 — Q1-Q6 | Technical/Role-Specific: 5 — Q7-Q11 | Situational: 4 —
Q12-Q15 | Company/Role Fit: 3 — Q16-Q18 | Career Vision: 2 — Q19-Q20)*

### Honourable Mentions

*   "What is the largest volume you have personally been responsible for, in events or rows
    per day?"
*   "How do you decide what belongs in dbt versus in the pipeline?"
*   "What did stockstream teach you that your day job did not?"
*   "Describe your ideal first ninety days here."
*   ⚠️ "Two of our engineering leads left earlier this year — do you have questions about
    that?" (Speculative: the departures are inferred from LinkedIn activity in the research
    file, not from anything Kestrel has said. They may not raise it, and you should not
    imply you have been researching individuals.)
*   ⚠️ "How would you approach our Iceberg migration?" (Speculative: Iceberg appears only
    in the nice-to-haves; there is no evidence they have a migration underway.)
*   ⚠️ "What do you think of our API design?" (Speculative: no public API documentation was
    found during research. If asked, say you have not seen the docs rather than
    improvising an opinion.)

## 3. Strategic Insights & Beyond the Ordinary

*   **Anticipated Format & Unspoken Expectations:** The recruiter's email says "systems
    design, no live coding" and that both engineers are from the platform team rather than
    the data side. Expect them to probe operational thinking — deployment, failure,
    on-call — more than data modelling. That is also where your Kubernetes gap lives, so it
    is not a question of whether it comes up but when.
*   **Interviewer-Specific Angles:** ⚠️ Not available. You have one name, Dev Raghunathan,
    and no background information. Anything written here about what they personally care
    about would be invented. Ask the recruiter.
*   **Common Pitfalls to Avoid:**
    - Do not let "I've worked with Kafka" stand in for "I've built streaming systems." Two
      platform engineers will hear the difference immediately and the recovery is much
      worse than the disclosure.
    - Do not lead with dbt. Your own preferences file notes that every CV that led with dbt
      produced analytics-engineering interviews; the same is true in the room.
    - Do not describe the Halcyon migration as a rewrite. It was a migration with a
      six-week parallel run, and the parallel run is the impressive part.
    - Avoid the word "spearheaded," per your own standing instruction.

## 4. Crafting Your Narrative: Key Talking Points

⚠️ These map to job requirements only. Each one should also connect to a stated company
value, and none does, because Kestrel publishes no values statement that the research
turned up — see section 1. Do not substitute a value inferred from their marketing copy;
if you find a real one before Friday, add it here.

*   **Talking Point 1 — Changing the engine without stopping the car**
    *   **Theme:** Live migration with verified correctness.
    *   **Connects to:** JD requirement ("A track record of migrating a live system without
        downtime") and the role's central eighteen-month objective.
    *   **Story Snippet:** "Our nightly sales and stock pipeline missed its 07:00 SLA about
        twice a month and ran six hours ten. I moved it to Spark and Airflow while finance
        read the same numbers every morning. I ran both pipelines in parallel for six weeks
        and reconciled row by row before moving a single consumer. Runtime dropped to one
        hour fifty and we have not missed the SLA since — fourteen months. The parallel run
        was the expensive part and it was the part that made it safe."

*   **Talking Point 2 — Contracts across producers you do not control**
    *   **Theme:** Schema evolution and backwards compatibility in a multi-producer world.
    *   **Connects to:** JD requirement ("data contracts, schema evolution and backwards
        compatibility in a multi-producer environment") and their twelve publishing teams.
    *   **Story Snippet:** "I designed the ingestion framework for 27 third-party supplier
        feeds, none of whom I could tell to deploy on my schedule. The framework versioned
        the contract rather than the payload, so a producer could move ahead without
        breaking consumers, and onboarding a new feed went from three days to half a day.
        Later I put contract tests in CI across 240 dbt models and schema-drift incidents
        in production went from eleven a year to two."

*   **Talking Point 3 — Being able to explain a number six months later**
    *   **Theme:** Auditability and lineage as a design constraint, not a reporting feature.
    *   **Connects to:** JD requirement ("reproducible and auditable months after the fact"
        and "explain any published number").
    *   **Story Snippet:** "Retail pricing has a milder version of your audit problem: when
        a supplier price feed was corrupted, the question was not just 'fix it' but 'which
        published figures are affected and how do we know.' We caught that one before it
        reached the pricing team because we validated at the boundary rather than in the
        warehouse. The habit that generalises is designing so that every number carries the
        version of the logic that produced it."

*   **Talking Point 4 — The gap, said once, calmly**
    *   **Theme:** Honest self-assessment.
    *   **Connects to:** JD requirements you do not meet (strong Kubernetes; production
        stream processing) and your own standing instruction to represent yourself
        honestly.
    *   **Story Snippet:** "I've run Kafka as transport with contracts across 27 producers.
        I have not owned a Flink job serving live traffic, and my Kubernetes is reading
        manifests and deploying to a cluster someone else operated — I've never been the
        person paged for it. I'd rather you hear that from me now. What I'd do about it in
        the first month is [specific plan]. What I bring in the meantime is the migration
        itself, which is the part of your eighteen-month plan that can actually go wrong in
        front of a customer."
    *   *Fill in the bracket before the interview. A gap disclosed without a plan is just a
        gap.*

## 5. Extended Preparation Toolkit

*   **Targeted Mock Interviews:** Do one 20-minute mock of the design question in Q7-Q8
    only, out loud, with a whiteboard. The failure mode is talking through it in your head,
    where it always sounds fluent.
*   **"Elevator Pitch" Refinement:** Thirty seconds, ending on the migration rather than
    the current job title. Rehearse this to the point of boredom given your slow start.
*   **Portfolio/Project Deep Dive:** Be ready to open stockstream and explain a design
    decision in it. It is the only artefact you have that they can read.
*   **Industry-Specific Research:** Read one primer on Scope 3 freight emissions
    methodology and one on Flink's state backends and checkpointing. Two hours total, and
    the Flink one is the higher-value of the two.

---

### AI Confidence, Disclaimer & Feedback Loop

*   **Guide Confidence Score:** Medium — the job description, the résumé and the company
    research are all detailed, so role and fit advice is well grounded. Interviewer-specific
    preparation is absent because no interviewer background was available, and the company
    values section is deliberately empty for the same reason. Getting the second
    interviewer's name and role from the recruiter would move this to High.
*   **Disclaimer:** This guide is generated by an AI based on the inputs listed at the top
    of the file. It has no real-time data and no human intuition. It supplements your own
    research and judgement; it does not replace them.
*   **Next Steps:** Ask for deeper drilling on any section, or regenerate after the
    recruiter supplies the second interviewer's details.
