# Getting things into the workspace

Three sources: a document on disk, a URL, or pasted text.

## Documents — PDF, DOCX, and the rest

Use [`markitdown`](https://github.com/microsoft/markitdown). It handles PDF, DOCX, XLSX,
PPTX, HTML, EPUB and images, and produces Markdown rather than a wall of text.

```bash
pip install markitdown        # or: uv tool install markitdown
markitdown resume.pdf > resume.md
```

### The one detail that is not obvious

**Write the file with its original extension.** MarkItDown dispatches on the extension.
Hand it a temporary file called `tmp` or `upload.tmp` and it will not pick the right
converter — and it does not raise; it returns something plausible and wrong.

Phoenix's `extract_text_from_file` carries the comment and the fix:

```python
suffix = os.path.splitext(filename)[1] if filename else ""
if not suffix:
    suffix = ".tmp"
with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
    tmp.write(file_content)
```

So when you are handling bytes rather than a path — a download, a clipboard payload —
preserve the extension when you write the temp file.

### Before reaching for markitdown

Try decoding as UTF-8 first. A `.txt`, `.md` or `.json` résumé needs no conversion, and
running it through a document converter only degrades it.

### If markitdown is not available

- **PDF**: `pdftotext -layout file.pdf -` (poppler) keeps columns readable. Without
  `-layout`, a two-column CV interleaves into nonsense.
- **DOCX**: it is a zip. `unzip -p file.docx word/document.xml` then strip tags — ugly but
  it works with nothing installed.
- Ask the user to paste the text. This is often faster than any of the above and always
  more accurate.

Always check the conversion before building on it. Two-column CV templates are the common
failure: the output interleaves left and right columns line by line, and a résumé parsed
from that is subtly wrong everywhere. If the Markdown looks shuffled, ask for the text
rather than guessing.

## A résumé, once converted

The Markdown is an intermediate, not the artifact. Turn it into `profile/resume.json` in
JSON Resume shape — see `json-resume.md` — then validate:

```bash
python3 <skill>/scripts/validate_resume.py profile/resume.json
```

Keep the original file somewhere the user can find it. Parsing loses things, and the
first thing they will ask is what was in the original.

Do not invent. If a date is ambiguous or a job title is unreadable, ask. A résumé is a
factual document and a plausible guess in it is a lie the candidate then has to defend in
an interview.

## A job posting from a URL

Fetch it yourself. Phoenix had a `UrlImporter` that never actually fetched anything — it
stored the URL and returned an empty artifact — so there is nothing to port.

Save the readable text to `applications/<company>-<role>/job.md` with a header:

```markdown
# <Role> — <Company>

- **Source:** LinkedIn / careers page / agency / referral
- **URL:** https://...
- **Captured:** 2026-09-09
- **Location:** ...
- **Salary:** ... (or "not stated")
- **Visa:** what the posting says about sponsorship, or "not mentioned"

---

<the posting body>
```

Capture the whole posting, not a summary. `fit.md` and `interview-prep.md` both quote
specific requirements back, and a summary loses the exact phrasing that matters — "strong
Kubernetes" and "familiarity with Kubernetes" are different jobs.

Record salary and visa even when absent, as "not stated". Absence is information, and
noting it stops the same question being re-asked three files later.

If the URL is behind a login or a bot wall, ask the user to paste the text. Do not
reconstruct a posting from a search-result snippet.

## Pasted text

Save it as given, then structure it. Keep the raw paste if it contains anything the
structure loses — a recruiter's covering note above a job description often carries the
salary, the reason for the approach, or a name.

## Optional structured form

`job.json` is optional and useful when a posting is long enough that re-reading it costs
something. It follows the JSON Job schema: `title`, `company`, `type`, `date`,
`description`, `location` (object), `remote` (`Full` | `Hybrid` | `None`), `salary`,
`experience`, `responsibilities`, `qualifications`, `skills`, `meta.canonical`.

Extra keys are allowed. The example workspace in the phoenix-skills repository adds a
`visaSponsorship` block to its `job.json` —
whether it is offered, the posting's own wording, and whether it was checked against a
register — because for a candidate who needs sponsorship that is the field that decides
whether anything else is worth reading.

`job.md` stays the record of what was advertised. `job.json` is a convenience derived from
it, and if the two disagree, `job.md` wins.

## If the environment has more tools

A LinkedIn MCP server that exposes conversations can capture recruiter threads directly;
see **drafting-outreach-replies** for the format `contacts.md` expects. Browser automation
can read a posting behind a login the same way a person would. Neither is required —
pasting text works everywhere and is the assumed path.
