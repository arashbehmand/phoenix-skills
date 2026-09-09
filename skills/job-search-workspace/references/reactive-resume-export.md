# Exporting to Reactive Resume (and getting a PDF)

[Reactive Resume](https://rxresu.me/) is a free, open-source résumé builder. It imports
JSON, gives a visual editor and a dozen templates, and exports a PDF. That is the whole
PDF story here: convert, import, adjust, download.

Phoenix shipped twelve Jinja themes and a WeasyPrint renderer to do this. They were
replaced by a JSON file and someone else's editor, and the result is better because the
user can nudge a line break themselves instead of asking for a re-render.

## The flow

```bash
python3 <skill>/scripts/to_rxresume.py profile/resume.json -o resume.rxresume.json
```

`<skill>` is this skill's directory — the one holding `SKILL.md`.

Then, at [rxresu.me](https://rxresu.me/): create a free account → **Create Resume** →
**Import** → upload the file → edit → **Download PDF**.

Self-hosting works too; the import format is identical.

## Options

```bash
--schema v5        # default; the current import format
--schema v4        # the older format, if the instance you are importing into wants it
--template onyx    # default template
--seed 7           # deterministic item ids, so two runs produce identical files
--strict           # refuse a résumé with validation errors instead of repairing it
```

If an import is rejected, try the other `--schema`. That is almost always the cause.

## What it does before converting

The script runs the résumé through the same validator as `validate_resume.py`, repairs
what it can, and says on stderr how many problems it repaired. So a résumé in the broken
`experience`/`role`/`dates` shape still converts correctly — but you should still run
`validate_resume.py` and fix the source file, because everything else in the workspace
reads that file too.

With `--strict` it refuses instead, which is what you want in a check.

## What it will not do

**It will not write output that would fail to import.** It checks the generated document
— required fields present, no nulls, every custom section actually referenced by the page
layout — and exits non-zero with the reasons instead of writing.

This is the one behaviour worth understanding, because Phoenix did the opposite. Its
converter ran the same check, `print()`ed any failure, and returned the malformed
document anyway. A broken export was indistinguishable from a good one until someone
tried to import it.

## Two things the port fixes, and one it keeps

### company and position are not swapped

In JSON Resume, `work[].name` is the company and `work[].position` is the job title. In
Reactive Resume, `company` is the company and `position` is the job title. They map
straight across.

Phoenix had them crossed for several commits:

```python
"company": work.get("position", ""),   # wrong
"position": work.get("name", ""),      # wrong
```

justified by a code comment claiming *"In Onyx, company field is the role title."* It is
not, and the comment is why the bug survived review. Every résumé exported in that window
listed the job title where the employer should be.

If you ever find yourself editing this mapping, check a generated file first: the company
name belongs in `company`.

### Dates in `YYYY` and `YYYY-MM` are formatted

Phoenix parsed only `YYYY-MM-DD` and returned anything else unchanged, so `"2023-04"` —
a form the schema explicitly allows and most people write — printed on the finished PDF
as `2023-04`. All three ISO shapes now render as `Apr 2023` or `2023`.

Related: a range with no start date now still shows its end, rather than rendering empty.

### "Experience Cont." is kept, deliberately

Reactive Resume will not break a section across a page boundary. A work history longer
than one page does not flow onto page two — it overflows and is cut off, silently.

The workaround: estimate how many rendered lines each work entry needs, keep what fits on
page one in the `experience` section, and move the rest into a custom section titled
**Experience Cont.** that is placed at the top of page two.

```
page 1: Experience          Principal Engineer, Staff Engineer, Lead Engineer, ...
page 2: Experience Cont.    Research Assistant
```

Order is preserved end to end, and once one entry overflows every later entry follows it,
so the history never reads out of sequence across the break.

The estimate lives in `SplitConfig`: 72 characters per line, 2 lines of header per entry,
one blank line between entries, 70 lines of budget on page one. Those numbers are tuned
for the Onyx template at the default typography. If you change template or font size, the
split point moves and the numbers are worth revisiting — they are a heuristic, not a
measurement.

To see it work:

```bash
# examples/fixtures/long-resume.json lives in the phoenix-skills repository
python3 <skill>/scripts/to_rxresume.py examples/fixtures/long-resume.json --seed 1 -o /tmp/long.json
```

The stderr line says `(work history split across two pages)` when it triggers.

## Checking a conversion by eye

Open the output and confirm:

- `basics.name` is the person and `sections.experience.items[].company` is an employer.
  If those are swapped, something has regressed the mapping above.
- Periods read like `Apr 2023 - Present`, not `2023-04 - Present`.
- A current role shows `Present`, which comes from omitting `endDate` in the source.
- If there is a `customSections` entry, its id appears in
  `metadata.layout.pages[1].main` (v5) or in the second page of `metadata.layout` (v4).
