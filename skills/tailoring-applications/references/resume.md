# Tailoring the résumé

Output: `applications/<slug>/resume.json`, in JSON Resume format.

Never write to `profile/resume.json`. That is the base, and overwriting it with a
role-specific version poisons every later application. If tailoring turns up a genuine
improvement to the base, note it and hand it to **building-a-resume** — do not fold it in
here.

## Read the general rules first

The rules that hold for any résumé — STAR bullets, verb-first, one or two lines, "true is
necessary not sufficient", merging early roles into one title, the 2026 ATS reality, not
letting it read as generated, bias — live in **building-a-resume**,
`references/resume-principles.md`. Read that first. This file is only the part that is
specific to tailoring an existing base to one posting.

## Before you start

Read `fit.md` sections 4 and 5. Section 4 lists the strong matches and the gaps as the
employer will see them; section 5 says which strength to lead with and which gap to
address. That is the tailoring brief. Do not re-derive it from the posting.

## What to change

**Reorder before you rewrite.** Most of the gain is in putting the relevant work first —
within a role, the highlight that matches the posting goes first; across the résumé, the
sections the posting cares about come before the ones it does not. Reordering carries no
integrity risk at all.

**Lift the posting's vocabulary where it honestly applies.** If the posting says "data
contracts" and the candidate built exactly that but called it "schema agreements", use
their words — once, on the bullet where they did the work. If the candidate did not do the
thing, the phrase does not go in. The difference between tailoring and lying is whether the
underlying fact is true; the difference between tailoring and keyword-stuffing is whether
the term earns its place on that line or is just there to raise a count.

**Rewrite `basics.summary` for this role.** It is the only part of the résumé a human
reads before deciding whether to read the rest. Three or four sentences, leading with
whatever `fit.md` identified as the strongest match.

**Cut.** A tailored résumé is usually shorter than the base. Old roles compress to a line
or two; irrelevant projects come out; the skills block loses the entries nobody is hiring
for here.

## Checking before you hand it over

- Every requirement in the posting that the candidate meets appears somewhere findable.
- Nothing appears that the candidate cannot evidence. Search the output for the skills
  named in `fit.md` as gaps — they should not be there.
- Every bullet starts with a verb and contains no "I".
- The summary would make a hiring manager read the next paragraph.
- It validates: `python3 <job-search-workspace>/scripts/validate_resume.py applications/<slug>/resume.json`
- It is shorter than the base résumé, or there is a reason it is not.
