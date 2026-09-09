# Contacts — Kestrel Labs

One sentinel block per contact, keyed by `username`. Blocks are **upserted, not appended**:
re-capturing a thread replaces that contact's block and leaves every other block alone, so
two recruiters on the same role never clobber each other. Anything outside the blocks —
these notes, your own scratch — survives an upsert untouched.

Message lines are `[HH:MM] Name: message`, which is what the Phoenix Pilot extension emits
and what a LinkedIn or Gmail capture pastes in as.

## Who is who

- **Priya Raman** — Talent Partner, Kestrel Labs. First contact, owns scheduling.
- **Dev Raghunathan** — Senior Platform Engineer. One of the two round-2 interviewers.

<phoenix-pilot-messages username="Priya Raman" headline="Talent Partner at Kestrel Labs" linkedin_url="https://www.linkedin.com/in/priya-raman-example" updated="2026-09-04T16:12:00Z">
[14:03] Priya Raman: Hi Mirela, thanks for applying to the Senior Data Engineer role on the Streaming Platform team. I've had a look at your background — the pipeline migration work at Halcyon is very relevant to what we're doing. Do you have 30 minutes this week for an intro call?
[18:41] Mirela Ionescu: Hi Priya, thanks for reaching out. Yes, happy to talk. Thursday or Friday afternoon both work for me. Before we book it, one thing I'd like to check early: the posting says two days a week in Farringdon and I'm based in Manchester. Is that two days in that specific office, or two days co-located with the team?
[09:15] Priya Raman: Good question and I'm glad you asked now. It's the Farringdon office specifically for the platform team — Tuesdays are fixed. We do have a few people who travel in from outside London and expense it, and one who does a fortnightly pattern instead of weekly, so there's some flexibility, but it isn't a remote role. Would a Tuesday-plus-one arrangement with travel covered be workable for you?
[12:30] Mirela Ionescu: That helps, thank you. Tuesday plus one with travel covered is workable if the second day can be flexible week to week. Let's book the call — Thursday 2pm if that's still free.
[13:02] Priya Raman: Booked for Thursday 2pm, invite sent. And yes, the second day is genuinely flexible. One more thing so you're not surprised: we do ask about visa status early. The posting is accurate, we're a licensed sponsor and we've issued CoS twice this year.
[15:48] Mirela Ionescu: Perfect, and useful to know. I'm on a Skilled Worker visa sponsored by my current employer to August 2028, so it would be a CoS transfer rather than a first application. See you Thursday.
[11:20] Priya Raman: Thanks for Thursday, the team was positive. Moving you to the technical round — 60 minutes, systems design, no live coding. You'll be with Dev Raghunathan (Senior Platform Engineer) and one other engineer from the team. Friday 11th September, 2pm. Does that work?
[13:05] Mirela Ionescu: Friday 11th at 2pm works, thank you. Could you tell me who the second engineer will be and roughly what areas each of them will focus on? It helps me prepare properly.
[16:12] Priya Raman: Of course — I'll confirm the second name once the rota is fixed, should be by Monday. Dev will lead on the streaming and ingestion design side. The other will likely cover platform operations and how you'd run things day to day.
</phoenix-pilot-messages>

<phoenix-pilot-messages username="Dev Raghunathan" headline="Senior Platform Engineer at Kestrel Labs" linkedin_url="https://www.linkedin.com/in/dev-raghunathan-example" updated="2026-09-06T10:02:00Z">
[09:47] Dev Raghunathan: Hi Mirela — Priya passed your CV over ahead of Friday. I had a look at stockstream, nice tool. Quick heads up so you can prepare: I'd like to spend most of the hour on one design problem rather than a tour of your CV. No prep needed beyond a way to draw.
[10:02] Mirela Ionescu: Thanks Dev, that's how I'd prefer to spend it too. I'll have a drawing surface ready. See you Friday.
</phoenix-pilot-messages>
