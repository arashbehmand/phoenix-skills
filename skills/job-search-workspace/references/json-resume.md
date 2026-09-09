# JSON Resume: the field names, and why each one bites

`profile/resume.json` and every tailored `resume.json` use [JSON Resume
v1.0.0](https://jsonresume.org/schema/). It is a small schema and the temptation is to
write it from memory. Do not — the names below are the ones a model reliably gets wrong,
and getting one wrong does not produce an error. It produces a résumé with a section
missing.

Phoenix learned this the expensive way. Sentry #7242697871 was a 100% failure rate on
résumé export caused entirely by field names, and it shipped because the exporter printed
its complaints to a log nobody read and then exported the broken document anyway.

Run `scripts/validate_resume.py` instead of trusting your memory of this file.

## The five that cause most of the damage

| Write this | Not this | What happens if you get it wrong |
|---|---|---|
| `work` | `experience` | The résumé exports with **no jobs on it**. Nothing errors. |
| `work[].name` | `company` | Company name vanishes from every entry. |
| `work[].position` | `role`, `title`, `jobTitle` | Job title vanishes from every entry. |
| `work[].highlights` | `bullets`, `achievements`, `responsibilities` | All the achievements vanish. |
| `education[].studyType` | `degree` | The degree vanishes. |

`work[].name` is the **company**, not the person's name. This reads wrong every time and
is worth checking twice. `basics.name` is the person.

## Full field reference

**`basics`** — `name`, `label` (the professional headline, not `title`), `image`, `email`,
`phone`, `url` (not `website`), `summary`, `location`, `profiles`.

`location` is an object: `address`, `postalCode`, `city`, `countryCode` (ISO-3166-1
alpha-2, so `GB` not `UK`), `region`. Not a string.

`profiles` is an array of `{network, username, url}`.

**`work[]`** — `name` (company), `position`, `location`, `description` (a *string*
describing the company, rarely used), `url`, `startDate`, `endDate`, `summary`,
`highlights` (array of strings).

**`education[]`** — `institution` (not `school`), `url`, `area` (the field of study, not
`major`), `studyType` (the degree), `startDate`, `endDate`, `score` (not `gpa`),
`courses`.

**`skills[]`** — `{name, level, keywords}`. An array of *objects*, never an array of
strings.

**`projects[]`** — `name`, `description` (a **string**), `highlights` (array), `keywords`,
`startDate`, `endDate`, `url`, `roles`, `entity`, `type`.

**`certificates[]`** — `name`, `date`, `issuer`, `url`. Note `certificates`, not
`certifications`.

**`awards[]`** — `title`, `date`, `awarder`, `summary`.
**`publications[]`** — `name`, `publisher`, `releaseDate`, `url`, `summary`.
**`languages[]`** — `language`, `fluency`. Not `name`/`level`.
**`interests[]`** — `name`, `keywords`.
**`references[]`** — `name`, `reference`.
**`volunteer[]`** — `organization`, `position`, `url`, `startDate`, `endDate`, `summary`,
`highlights`.

## Dates

ISO 8601, and only these three shapes:

```
2024            2024-06            2024-06-29
```

Not `June 2024`, not `06/2024`, not `Jan 2025 - May 2025` in a single field. A date range
is always two fields, `startDate` and `endDate`.

**A current role omits `endDate` entirely.** Do not write `"Present"`, `"current"` or
`null` — exporters render the omission as "Present" themselves, and render the string as
the literal text.

## Omit, do not null

If a field is absent, leave it out. `"url": null` is worse than no `url` at all: an
exporter checks whether the key exists, finds it, and renders an empty line where a link
should be.

## The shape that broke everything

This is what an unconstrained model produces, and it is the exact shape behind Sentry
#7242697871:

```json
{
  "experience": [{
    "company": "Builder.ai",
    "role": "AI / ML Scientist",
    "description": ["Architected an end-to-end RAG system",
                    "Engineered a multi-stage LLM pipeline"],
    "dates": "Jan 2025 - May 2025"
  }]
}
```

Four errors in six lines: `experience` should be `work`; `company` should be `name`;
`role` should be `position`; `description` as a **list** should be `highlights`; and
`dates` should be `startDate` plus `endDate`. The list-valued `description` is what
actually crashed the exporter, with `TypeError: expected string or bytes-like object, got
'list'`.

The correct form:

```json
{
  "work": [{
    "name": "Builder.ai",
    "position": "AI / ML Scientist",
    "highlights": ["Architected an end-to-end RAG system",
                   "Engineered a multi-stage LLM pipeline"],
    "startDate": "2025-01",
    "endDate": "2025-05"
  }]
}
```

The phoenix-skills repository carries a full résumé in this broken shape at
`examples/fixtures/malformed-resume.json`. Running `validate_resume.py --fix` on it
produces a clean one, which is a faster way to see the difference than reading this
section.

## Checking

```bash
python3 <skill>/scripts/validate_resume.py resume.json        # report; exits 1 on errors
python3 <skill>/scripts/validate_resume.py resume.json --fix  # repair in place
python3 <skill>/scripts/validate_resume.py resume.json --fix -o fixed.json
```

Errors are things that will break or silently empty an export. Warnings are things an
exporter will ignore — a stray key, a null. `--fix` handles field renames, date parsing,
list-valued descriptions, string-array skills, and contact details stranded at the top
level. Anything it cannot fix is listed and left alone, and the exit code stays non-zero.

Run it after writing any `resume.json`, including a tailored one.
