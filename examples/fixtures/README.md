# Test fixtures

Three résumés used to check that the `job-search-workspace` scripts behave, and to show
what the failure cases actually look like. All fictional.

| File | What it is for |
|---|---|
| `../workspace/profile/resume.json` | A clean, valid JSON Resume. The baseline. |
| `malformed-resume.json` | The Sentry #7242697871 shape — `experience` instead of `work`, `role` instead of `position`, `description` as a **list**, a single `dates` string, contact details stranded at the top level, skills as bare strings. This exact shape produced a 100% résumé-export failure rate in Phoenix. |
| `long-resume.json` | A twenty-year career, long enough to overflow page one and trigger the `Experience Cont.` split. |

## Verify

```bash
./verify.sh
```

Runs every case and prints a pass/fail line for each. No network, no API key, standard
library only. Exits non-zero if anything regressed.
