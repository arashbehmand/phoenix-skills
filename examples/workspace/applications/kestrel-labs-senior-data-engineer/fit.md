# 🎯 Strategic Career Analysis

*Kestrel Labs — Senior Data Engineer, Streaming Platform*
*Generated 2026-08-25 · inputs: job.md, job.json, profile/resume.json, profile/honest-context.md, ../../research/kestrel-labs.md*

## 0. Executive Verdict

*   **Recommendation:** **STRONGLY APPLY**
*   **Confidence Score:** Medium
*   **Summary:** This is the exact move you said you wanted — a build role in streaming, at
    a company that is verifiably a licensed sponsor, paying above your floor. Confidence is
    Medium rather than High only because two of their six required items are genuine gaps
    for you, and one of them (Kubernetes) is the kind they can test in twenty minutes.

## 1. Is this a good job? (Role Analysis)

*   **Pros:** Scoped and specific — one system, one migration, an eighteen-month horizon.
    The JD names the current state honestly ("roughly 80% arrives as nightly file drops")
    instead of pretending the platform is already modern, which is a good sign about how
    they talk internally. Ownership is real: contracts with twelve publishing teams is
    design authority, not ticket work. Audit requirements make the correctness bar high,
    which is interesting rather than tedious.
*   **Cons/Risks:** "No on-call rotation for the data team today; that will change as
    streaming goes live and we will design it together" is honest but it is still a
    commitment to future on-call with undefined terms. Three data engineers to run a live
    migration of twelve producing systems is thin. Mentoring two mid-levels is also on the
    list — that is three jobs' worth of surface area if the team does not grow.
*   **Rating:** 8/10

## 2. Is this a good company? (Corporate Analysis)

*   **Market Position:** Series B, 140 people, in a regulatory tailwind — CSRD and UK
    reporting rules make emissions accounting a compliance purchase rather than a
    discretionary one. Two of the four largest UK grocers as customers is real validation
    at this size. Not a market leader; a credible challenger.
*   **Culture Signals:** Glassdoor is thin (31 reviews) and skews positive at 4.1, with the
    usual Series B complaint about process immaturity. Two engineering leads left in Q1
    2026 per LinkedIn — worth asking about, not yet alarming. Six-week cycles with a
    cooldown is a real, specific working pattern rather than "we're agile."
*   **Rating:** 7/10

## 3. Is this a good job for *me*? (Personal Alignment)

*   **Alignment:** Almost point-for-point against your stated wants. Platform still being
    built, not maintained. Streaming rather than batch. Technical ownership without people
    management — the mentoring ask is two engineers, not a team lead line. Nine-person
    platform team clears your "more than three engineers" bar. Two days on site matches
    your ceiling exactly. Salary band starts at £78k, £3k above your floor, and the top of
    the band is £92k.
*   **Misalignment:** London, not Manchester. The JD says Farringdon two days a week and
    your dealbreaker is a commute under about an hour — Manchester to London is not that.
    **This is the thing to resolve before anything else.** Either they mean the London
    office for people who live near it and would take you as remote-with-travel, or this
    role is not viable for you at all. Do not spend three rounds finding out.
*   **Verdict:** Strong — conditional entirely on the location question.

## 4. Am I a good fit for this position? (Candidate Fit)

*   **Strong Matches:** Nine years, comfortably past their 5+ bar. Python and SQL depth is
    not in question. The live-migration requirement is your strongest card — the
    SQL Server to Redshift/dbt migration and the 6h10m to 1h50m pipeline rebuild are both
    exactly the "migrating a live system without downtime" story they asked for, with
    numbers attached. The Kafka stock-movement feed gives you a genuine multi-producer,
    contract-and-schema story. Audited environment maps loosely to your Great Expectations
    and dbt contract-test work.
*   **Gaps/Weaknesses:**
    - **Kubernetes.** They wrote "Strong Kubernetes" and "you will be operating your own
      services, not handing them to an ops team." You have read manifests and deployed to
      someone else's cluster. This is a required item you do not meet, and the honest
      framing is "I have not operated one," not a résumé bullet that implies otherwise.
    - **Production stream processing.** You have run Kafka as transport. You have not owned
      a Flink or Spark Streaming system serving live traffic. They will accept Spark
      Structured Streaming as a substitute — you do not have that either.
    - Spark is 2022-era by your own account, and they are on a modern stack.
    - Five years at one mid-size retailer with no recognisable brand, against a company
      that hires from Series B and above.
*   **Estimated Match %:** 65%

## 5. Strategic Advice

*   **If applying:** Lead with the migration, not the streaming. You cannot out-claim
    somebody who has run Flink in production, so do not try — compete on the thing they
    also asked for and most candidates will not have, which is having moved a live,
    business-critical pipeline without the numbers going wrong. Say the Kubernetes gap out
    loud in the first technical conversation and pair it with what you have actually
    operated. Bluffing it survives the recruiter call and dies in round two.
*   **Key Question to Ask:** "The role is listed as two days a week in Farringdon — I'm
    Manchester-based. Is that two days in that specific office, or two days co-located with
    the team wherever they are?" Ask it on the recruiter call, before anything else.
