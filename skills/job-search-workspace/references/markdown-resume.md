# The plain-text résumé

Some application forms want pasted text, some ATS uploads prefer it, and it is the
fastest way to read a tailored résumé back to the user for approval. This is the format
Phoenix rendered — ported from `templates/resume_markdown.j2` — with the same section
order and the same omission rules.

Write it from `resume.json`. Do not maintain it as a separate document; it goes stale.

## Format

```
MIRELA IONESCU
Senior Data Engineer

mirela.ionescu@example.com
+44 7700 900142
Manchester, England GB
https://www.linkedin.com/in/mirela-ionescu-example
https://github.com/mirela-example

Summary
=======
Data engineer with nine years building batch and event-driven pipelines...

Experience
==========

Senior Data Engineer
Halcyon Retail Group
2023-04 - Present
Manchester, UK
Own the analytics platform serving merchandising, supply chain and finance.
- Rebuilt the nightly sales and stock pipeline on Spark and Airflow, cutting...
- Reduced AWS spend on the data platform by £14k per month (31%)...

Education
=========

MSc: Data Science
University of Manchester
2020-09 - 2021-09

Skills
======
Data engineering (Advanced)
- Apache Spark
- Apache Airflow

Projects
========

stockstream
Open-source toolkit for replaying retail stock-movement events...
- Replays 2M recorded events at configurable rates against a local broker.

Languages
=========
- Romanian (Native speaker)
- English (Full professional proficiency)

Certifications
==============

AWS Certified Data Engineer - Associate
Amazon Web Services, 2024-06
```

## Rules

- **Name in caps**, headline underneath, then contact details one per line.
- Section headings are underlined with `=`, in this order: Summary, Experience, Education,
  Skills, Projects, Awards, Languages, Certifications.
- Within a work entry the order is **position, company, dates, location, summary,
  highlights**. Position first — this is the opposite of how most templates do it and it
  is what the original template rendered.
- Dates stay in the ISO form from the JSON. This format is for parsing and pasting, not
  for looking elegant; leave the pretty formatting to the PDF.
- Highlights and keywords are `- ` bullets.
- Location renders as `city, region countryCode`, with the separators dropped when a part
  is missing.

Two places to improve on the original template rather than copy it:

- **A current role gets `- Present`.** The template rendered `startDate` alone when
  `endDate` was absent, so an ongoing job printed as a bare `2023-04` and read like a
  one-month stint. Write `2023-04 - Present`.
- **Omit a section entirely when it is empty**, and never leave a blank line where an
  absent field would have gone. The template emitted both, so a résumé with no summary
  or no awards had unexplained gaps in it.

## When to use which export

| Situation | Format |
|---|---|
| Applying through a form that wants pasted text | this |
| An ATS upload with no format preference | PDF via Reactive Resume |
| Reading a tailored résumé back for approval | this |
| Anything the user will look at | PDF via Reactive Resume |
| Handing the data to another tool | `resume.json` as-is |
