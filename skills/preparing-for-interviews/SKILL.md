---
name: preparing-for-interviews
description: Use when an interview is booked — any stage, including a recruiter screen — or when someone asks what they will be asked, how to tell a particular story, or what to ask the interviewer.
---

# Preparing for interviews

Produce a preparation guide and write it to `applications/<slug>/interview-prep.md`.

The point is a guide the candidate could not have written for themselves in an hour: the
questions they will actually be asked, tied to the requirements those questions test, and
the stories they should have ready. Generic advice — "research the company", "be
confident" — is worse than nothing, because it uses up the time they had.

## Read first

| File | Required | If missing |
|---|---|---|
| `applications/<slug>/job.md` | yes | Ask for the posting. |
| `profile/resume.json` | yes | See **job-search-workspace**. |
| `applications/<slug>/resume.json` | no | Prefer it if present — it is what they actually sent. |
| `research/<company>.md` | no | **See the anti-hallucination rule.** Offer to run **researching-companies** first. |
| `profile/honest-context.md` | no | Read it — it carries the weaknesses worth rehearsing and the questions they dread. |
| `applications/<slug>/fit.md` | no | Read it — sections 4 and 5 are the gap analysis, already done. |
| `applications/<slug>/contacts.md` | no | Read it — it says which round this is, who is in it, and what has already been committed to. |
| `applications/<slug>/cover-letter.md`, `questions.md` | no | Read them. The candidate will be asked about what they wrote. |

Ask which round it is and who is in it if the workspace does not say. The right guide for
a recruiter screen and for a final panel are not the same document.

## The rule that keeps this honest

> **Anti-Hallucination:** Do not invent company values, news, or interviewer details not present in the Input. If data is missing (e.g., interviewer name), state that you cannot provide specific advice for it, rather than guessing.

This is the one that gets broken, because a guide with a confident "Interviewer X will
care about system design" reads better than one that says the interviewer is unknown. It
is also the one whose failure costs most: a candidate who walks in having rehearsed
invented company values will use them, and it will land badly.

In practice:

- **No company research?** Section 1's company entry says so. Do not reconstruct values
  from the careers page's marketing copy.
- **No interviewer information?** Say it is not available and suggest asking the recruiter
  for names and focus areas — a normal request that usually gets answered — rather than
  guessing what someone cares about.
- **Anything inferred rather than known** gets ⚠️ and a note saying what it rests on. A
  question built on "two leads appear to have left, per LinkedIn" is speculative; label
  it, because the candidate must not raise it as established fact.

Better to hand back a guide with a visible hole in it than a complete-looking one with an
invented patch.

## Output

Write `applications/<slug>/interview-prep.md` in this structure.

```markdown
# 🎯 Personalized Interview Preparation Guide

*<Company> — <Role> · <which round, format, date>*
*Generated <date> · inputs: <files actually read>*

## 0. Executive Summary & Top Priorities

*   **Top Priority 1:** (specific, e.g. rehearse the X story because it matches
    requirement Y)
*   **Top Priority 2:**
*   **Top Priority 3:**
*   **Estimated Prep Time:** [e.g. "6-8 hours over the next 3 days"]

## 1. Essential Knowledge & Strategic Checklist

*   **Company Deep Dive:** (mission, values, products, recent news, culture, competitors)
*   **Job Role Mastery:** (responsibilities, required vs desired skills, team, impact)
*   **Résumé Alignment & Storytelling:** (experiences mapped to requirements, STAR stories)
*   **Interviewer Insights & Research:** (their role, focus, questions to ask them)
*   **Logistics & Etiquette:** (format, timing, platform, follow-up plan)
*   **Mindset & Confidence:** (specific to this candidate, not general encouragement)

## 2. Top 20 Tailored Interview Questions

*Exactly 20, each with a one-line rationale naming the requirement it tests.*

1. "..." (Rationale: tests the 'X' requirement in the job description.)
...
20. "..."

*(Behavioural: 6 | Technical/Role-Specific: 5 | Situational: 4 | Company/Role Fit: 3 |
Career Vision: 2)*

### Honourable Mentions

*5-10 more, including curveballs. ⚠️ flags anything built on speculative data.*

## 3. Strategic Insights & Beyond the Ordinary

*   **Anticipated Format & Unspoken Expectations:**
*   **Interviewer-Specific Angles:**
*   **Common Pitfalls to Avoid:**

## 4. Crafting Your Narrative: Key Talking Points

*3-5 story frameworks. Each maps to a named job requirement AND a company value.*

*   **Talking Point 1 — <theme>**
    *   **Theme:**
    *   **Connects to:** JD requirement ("...") & Company Value ("...")
    *   **Story Snippet:** "..." (written out, in the candidate's voice)

## 5. Extended Preparation Toolkit

*   **Targeted Mock Interviews:**
*   **"Elevator Pitch" Refinement:**
*   **Portfolio/Project Deep Dive:**
*   **Industry-Specific Research:**

---

### AI Confidence, Disclaimer & Feedback Loop

*   **Guide Confidence Score:** [High/Medium/Low] — and what would raise it.
*   **Disclaimer:** Generated from the inputs listed above. No real-time data, no human
    intuition. A supplement to your own research, not a substitute.
*   **Next Steps:** Offer to go deeper on any section, or to regenerate when more is known.
```

### The parts that carry the weight

**The question mix is enforced: 6 behavioural, 5 technical, 4 situational, 3 fit, 2 career
vision.** Twenty questions, and the counts are stated at the end of the section. Without
the quota a generated list drifts into whichever category is easiest, which is usually
behavioural — and then the candidate is unprepared for the four situational questions
that decide the round.

**Every question carries a rationale naming a real requirement.** "Rationale: tests the
'Stakeholder Management' skill listed in the JD." This is what makes the list preparation
rather than trivia — the candidate can see which requirement each question is probing and
answer the requirement, not the question.

**Include the questions they will not enjoy.** The gap from `fit.md`. The five years at
one employer with no promotion. The thing `honest-context.md` says they dread. Being asked
for the first time in the room is far worse than reading it here. If `preferences.md` asks
for it harsh, honour that.

**Talking points map to a requirement *and* a company value**, and the story snippet is
written out rather than described. A candidate cannot rehearse "prepare a story about
cross-functional work"; they can rehearse three sentences. Write them in the candidate's
voice, from their real experience, with their real numbers. If a value cannot be sourced,
map to the requirement alone and say the value is unknown.

**`Estimated Prep Time` is a real estimate** — hours and a window. It tells the candidate
whether to start tonight.

**`Guide Confidence Score` reflects the inputs, not the writing.** Say what would raise
it: usually the interviewer's name, or company research.

## Tone

Blunt, compact, honest. No sugar-coating. If a critical skill is missing, flag it. No
generic advice — every item should be something the candidate could not have written
themselves, specific to this role, this company and this résumé.

Assume they are in a hurry and reading this the night before.

## If the environment has more tools

Nothing here requires any of them, and the anti-hallucination rule above outranks all of
them — a tool that returns nothing means the data is missing, not that you should guess.

- **Web search or fetch** — the honest way to fill the company section when
  `research/<company>.md` does not exist. Prefer running **researching-companies** properly
  and writing the file, so the next skill benefits too.
- **A LinkedIn MCP server**, if the user already runs one — an interviewer's public role
  and background is the single input that moves the confidence score most. Read only what
  the person has published, do not infer from activity, and say where it came from. The
  simpler route is usually asking the recruiter for names and focus areas.
- **Calendar access** — only to confirm the time and format you were told about.

## After writing

Add a line to `notes.md` with the interview date and what was generated. If anything was
deliberately left blank — an unknown interviewer, missing research — record it as an open
question, so it is obvious what to fill in when the recruiter replies.

Offer to run a mock interview afterwards. Reading twenty questions is not the same as
having answered them out loud, and the candidate can only find the sentences that do not
work by saying them.

## Next

- Post-interview follow-up, or a recruiter reply → **drafting-outreach-replies**
- Company research was missing → **researching-companies**
- The round changed the picture → revisit **assessing-job-fit**
