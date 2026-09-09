#!/usr/bin/env python3
"""Validate a JSON Resume file, and optionally repair the shapes an LLM gets wrong.

Phoenix had no validation step. Its exporter printed field-name complaints to stdout
and then returned the invalid dictionary anyway, so a resume with `experience` instead
of `work` produced an empty PDF with no error anyone saw. Sentry #7242697871 was that
bug at a 100% failure rate.

This script is the missing feedback loop. It reports problems with a path you can act
on, exits non-zero when the file would not export correctly, and with --fix rewrites
the file into schema-compliant shape.

Standard library only. No network. No API key.

Usage:
    python3 validate_resume.py resume.json
    python3 validate_resume.py resume.json --fix
    python3 validate_resume.py resume.json --fix --output repaired.json
    python3 validate_resume.py resume.json --quiet          # exit code only
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from typing import Any, Dict, List, Tuple

ISO8601 = re.compile(r"^\d{4}(-\d{2}(-\d{2})?)?$")


def iso_valid(value: str) -> bool:
    """ISO 8601 in shape *and* in range.

    The shape regex alone accepts "2025-13", which every downstream renderer then
    quietly degrades to "2025" — the date is wrong on the finished page and nothing
    reported a problem.
    """
    if not isinstance(value, str) or not ISO8601.match(value):
        return False
    parts = value.split("-")
    if len(parts) > 1 and not 1 <= int(parts[1]) <= 12:
        return False
    if len(parts) > 2:
        import calendar
        year, month = int(parts[0]), int(parts[1])
        if not 1 <= int(parts[2]) <= calendar.monthrange(year, month)[1]:
            return False
    return True

# Sections of JSON Resume v1.0.0 and the keys each item may carry.
KNOWN_KEYS: Dict[str, set] = {
    "basics": {"name", "label", "image", "email", "phone", "url", "summary",
               "location", "profiles"},
    "work": {"name", "location", "description", "position", "url", "startDate",
             "endDate", "summary", "highlights"},
    "volunteer": {"organization", "position", "url", "startDate", "endDate",
                  "summary", "highlights"},
    "education": {"institution", "url", "area", "studyType", "startDate",
                  "endDate", "score", "courses"},
    "awards": {"title", "date", "awarder", "summary"},
    "certificates": {"name", "date", "issuer", "url"},
    "publications": {"name", "publisher", "releaseDate", "url", "summary"},
    "skills": {"name", "level", "keywords"},
    "languages": {"language", "fluency"},
    "interests": {"name", "keywords"},
    "references": {"name", "reference"},
    "projects": {"name", "description", "highlights", "keywords", "startDate",
                 "endDate", "url", "roles", "entity", "type"},
}

ARRAY_SECTIONS = [k for k in KNOWN_KEYS if k != "basics"]

# Wrong key -> right key, per section. These are the substitutions an LLM actually
# makes; every one of them is drawn from a resume that broke Phoenix in production.
RENAMES: Dict[str, Dict[str, str]] = {
    "basics": {"title": "label", "website": "url", "headline": "label"},
    "work": {"company": "name", "employer": "name", "organization": "name",
             "role": "position", "title": "position", "jobTitle": "position",
             "bullets": "highlights", "achievements": "highlights",
             "responsibilities": "highlights", "start": "startDate", "end": "endDate"},
    "education": {"school": "institution", "degree": "studyType", "major": "area",
                  "fieldOfStudy": "area", "gpa": "score", "grade": "score",
                  "start": "startDate", "end": "endDate"},
    "projects": {"title": "name", "bullets": "highlights", "tech": "keywords",
                 "technologies": "keywords", "link": "url"},
    "volunteer": {"company": "organization", "role": "position",
                  "bullets": "highlights"},
    "certificates": {"title": "name", "authority": "issuer", "organization": "issuer"},
    "awards": {"name": "title", "issuer": "awarder"},
    "languages": {"name": "language", "level": "fluency"},
    "skills": {"skill": "name", "category": "name"},
}

# Free-text date ranges an LLM writes instead of startDate/endDate.
DATE_RANGE_KEYS = ("dates", "date", "period", "duration", "when")

DATE_FIELDS = {
    "work": ("startDate", "endDate"),
    "volunteer": ("startDate", "endDate"),
    "education": ("startDate", "endDate"),
    "projects": ("startDate", "endDate"),
    "awards": ("date",),
    "certificates": ("date",),
    "publications": ("releaseDate",),
}

MONTHS = {m: i for i, m in enumerate(
    ["jan", "feb", "mar", "apr", "may", "jun",
     "jul", "aug", "sep", "oct", "nov", "dec"], start=1)}


CODE_FENCE = re.compile(r"^```[a-zA-Z0-9_+-]*\n(.+?)\n?```$", re.DOTALL)


def strip_code_fences(text: str) -> str:
    """Unwrap ```json ... ``` around a whole document.

    Inlined from Phoenix's phoenix_lib.utils.text rather than depended on. A model
    asked for JSON returns it fenced often enough that failing with "not valid JSON"
    on an otherwise perfect resume is a bad first experience — and the user cannot
    tell from that message that the fix is deleting three backticks.

    Only strips when the entire content is wrapped; a fence in the middle of a file
    is left alone.
    """
    if not text or not isinstance(text, str):
        return text
    stripped = text.strip()
    if not stripped.startswith("```"):
        return text
    match = CODE_FENCE.match(stripped)
    return match.group(1).strip() if match else text


def load_resume(path: str) -> Any:
    """Read a JSON Resume file, tolerating code fences around it."""
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        unfenced = strip_code_fences(raw)
        if unfenced is raw or unfenced == raw:
            raise
        return json.loads(unfenced)


class Finding:
    __slots__ = ("level", "path", "message", "fixed")

    def __init__(self, level: str, path: str, message: str, fixed: bool = False):
        self.level = level          # "error" | "warning"
        self.path = path
        self.message = message
        self.fixed = fixed

    def render(self) -> str:
        tag = {"error": "ERROR", "warning": "WARN "}[self.level]
        suffix = "  [fixed]" if self.fixed else ""
        return f"  {tag}  {self.path}: {self.message}{suffix}"


# ---------------------------------------------------------------------------
# Date helpers
# ---------------------------------------------------------------------------

def parse_loose_date(text: str) -> str | None:
    """Turn 'Jan 2025', 'January 2025', '2025/01', '01-2025' into ISO 8601.

    Returns None when the string is not recognisably a single date.
    """
    s = text.strip()
    if not s:
        return None
    if ISO8601.match(s):
        return s
    m = re.match(r"^([A-Za-z]{3,9})\.?\s+(\d{4})$", s)
    if m and m.group(1)[:3].lower() in MONTHS:
        return f"{m.group(2)}-{MONTHS[m.group(1)[:3].lower()]:02d}"
    m = re.match(r"^(\d{4})[/.](\d{1,2})$", s)
    if m:
        return f"{m.group(1)}-{int(m.group(2)):02d}"
    m = re.match(r"^(\d{1,2})[/.-](\d{4})$", s)
    if m:
        return f"{m.group(2)}-{int(m.group(1)):02d}"
    if re.match(r"^\d{4}$", s):
        return s
    return None


# One date, in any of the forms people actually write.
_DATE = (r"(?:\d{4}-\d{2}-\d{2}|\d{4}-\d{2}|\d{4}"
         r"|[A-Za-z]{3,9}\.?\s+\d{4}|\d{1,2}[/.]\d{4}|\d{4}[/.]\d{1,2})")
_OPEN = r"(?:present|current|now|ongoing|today)"
# A range is two dates around a separator. Anchored and date-aware on purpose: a naive
# split on the first hyphen tears "2019-05 - 2021-06" apart inside its own start date,
# yielding start=2019 and no end — so a job that finished in June 2021 silently renders
# as "2019 - Present". Repairing a resume into a lie is worse than not repairing it.
_RANGE = re.compile(rf"^\s*({_DATE})\s*(?:-|–|—|to|until|through)\s*({_DATE}|{_OPEN})\s*$",
                    re.IGNORECASE)
_OPEN_ONLY = re.compile(rf"^{_OPEN}$", re.IGNORECASE)


def split_date_range(text: str) -> Tuple[str | None, str | None, bool]:
    """Split 'Jan 2025 - May 2025' or '2021 to Present' into (start, end, is_current)."""
    stripped = text.strip()

    match = _RANGE.match(stripped)
    if match:
        start = parse_loose_date(match.group(1))
        tail = match.group(2).strip()
        if _OPEN_ONLY.match(tail):
            return start, None, True
        return start, parse_loose_date(tail), False

    single = parse_loose_date(stripped)
    return (single, None, False) if single else (None, None, False)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(data: Any, fix: bool) -> Tuple[Dict[str, Any], List[Finding]]:
    """Check a resume and return (repaired copy, findings).

    Validation always runs against a repaired copy, whether or not --fix was asked
    for. Otherwise a file using `experience` instead of `work` would report one
    error and stop, hiding every problem inside the entries themselves — which is
    exactly how Phoenix shipped a 100%-failure export bug without noticing.
    """
    findings: List[Finding] = []
    if not isinstance(data, dict):
        findings.append(Finding("error", "$",
                                f"top level must be an object, got {type(data).__name__}"))
        return {}, findings

    out = copy.deepcopy(data)

    _normalize_root(out, findings, fix)
    _check_basics(out, findings, fix)
    for section in ARRAY_SECTIONS:
        if section in out:
            _check_section(out, section, findings, fix)
    return out, findings


def _normalize_root(data: Dict[str, Any], findings: List[Finding], fix: bool) -> None:
    """Repair the top-level shape before anything else looks at it."""
    if "experience" in data:
        findings.append(Finding(
            "error", "$.experience",
            "JSON Resume has no 'experience' section — work history goes in 'work'. "
            "Exporters read 'work' and produce a resume with no jobs on it without "
            "saying anything", fixed=fix))
        moved = data.pop("experience") or []
        if isinstance(moved, list):
            data["work"] = list(data.get("work") or []) + list(moved)

    _build_basics_from_custom(data, findings, fix)

    basics = data.get("basics")
    if basics is None:
        findings.append(Finding("error", "$.basics", "missing required section"))
    elif not isinstance(basics, dict):
        findings.append(Finding("error", "$.basics",
                                f"must be an object, got {type(basics).__name__}"))

    for section in ARRAY_SECTIONS:
        if section in data and not isinstance(data[section], list):
            findings.append(Finding(
                "error", f"$.{section}",
                f"must be an array, got {type(data[section]).__name__}"))

    _check_skills_shape(data, findings, fix)


def _build_basics_from_custom(data: Dict[str, Any], findings: List[Finding],
                              fix: bool) -> None:
    """Rebuild `basics` from the flat root shape LLMs produce when left unconstrained.

    name / title / summary at the root, contact details under `contact_info`.
    """
    root_keys = {"contact_info", "name", "title", "summary", "headline", "label",
                 "email", "phone", "location", "website", "url", "image"}
    present = {k for k in root_keys if k in data and not isinstance(data.get(k), dict)}
    if "contact_info" in data and isinstance(data["contact_info"], dict):
        present.add("contact_info")
    if not present or isinstance(data.get("basics"), dict) and data["basics"]:
        # Nothing to rebuild, or basics already exists and wins.
        if present and isinstance(data.get("basics"), dict):
            for key in sorted(present):
                findings.append(Finding(
                    "warning", f"$.{key}",
                    "sits at the top level but 'basics' already exists; exporters "
                    "read 'basics' and this value is ignored"))
        return

    findings.append(Finding(
        "error", "$.basics",
        "missing — contact details are at the top level instead. JSON Resume puts "
        f"name, label, email, phone, location and profiles inside 'basics' "
        f"(found {', '.join(sorted(present))} at the root)", fixed=fix))

    basics: Dict[str, Any] = {}
    if isinstance(data.get("name"), str):
        basics["name"] = data.pop("name")
    for src, dst in (("title", "label"), ("headline", "label"), ("label", "label"),
                     ("summary", "summary"), ("website", "url"), ("url", "url"),
                     ("image", "image"), ("email", "email"), ("phone", "phone")):
        if isinstance(data.get(src), str) and dst not in basics:
            basics[dst] = data.pop(src)
    if isinstance(data.get("location"), (str, dict)):
        basics["location"] = data.pop("location")

    contact = data.pop("contact_info", None)
    if isinstance(contact, dict):
        for src, dst in (("email", "email"), ("phone", "phone"), ("url", "url"),
                         ("website", "url")):
            if isinstance(contact.get(src), str) and dst not in basics:
                basics[dst] = contact[src]
        if "location" not in basics and contact.get("location"):
            basics["location"] = contact["location"]
        profiles = []
        for network, label, template in (
                ("linkedin", "LinkedIn", "https://www.linkedin.com/in/{}"),
                ("github", "GitHub", "https://github.com/{}"),
                ("twitter", "Twitter", "https://twitter.com/{}"),
                ("x", "X", "https://x.com/{}")):
            handle = contact.get(network)
            if isinstance(handle, str) and handle:
                url = handle if handle.startswith("http") else template.format(handle)
                profiles.append({"network": label,
                                 "username": handle.rstrip("/").rsplit("/", 1)[-1],
                                 "url": url})
        if profiles:
            basics.setdefault("profiles", profiles)

    data["basics"] = basics


def _check_basics(data: Dict[str, Any], findings: List[Finding], fix: bool) -> None:
    basics = data.get("basics")
    if not isinstance(basics, dict):
        return

    _rename_keys(basics, "basics", "$.basics", findings, fix)
    _check_nulls(basics, "$.basics", findings, fix)

    if not basics.get("name"):
        findings.append(Finding("error", "$.basics.name",
                                "missing — every exporter puts this at the top of the page"))

    loc = basics.get("location")
    if isinstance(loc, str):
        findings.append(Finding(
            "warning", "$.basics.location",
            "should be an object with city/region/countryCode, not a string", fixed=fix))
        basics["location"] = {"address": loc} if "," not in loc else {
            "city": loc.split(",")[0].strip(),
            "region": loc.split(",", 1)[1].strip(),
        }
    elif isinstance(loc, dict):
        _check_unknown(loc, {"address", "postalCode", "city", "countryCode", "region"},
                       "$.basics.location", findings)

    profiles = basics.get("profiles")
    if isinstance(profiles, list):
        for i, p in enumerate(profiles):
            if not isinstance(p, dict):
                findings.append(Finding("error", f"$.basics.profiles[{i}]",
                                        "must be an object with network/username/url"))
                continue
            _check_unknown(p, {"network", "username", "url"},
                           f"$.basics.profiles[{i}]", findings)


def _check_section(data: Dict[str, Any], section: str,
                   findings: List[Finding], fix: bool) -> None:
    items = data.get(section)
    if not isinstance(items, list):
        return

    for i, item in enumerate(items):
        path = f"$.{section}[{i}]"
        if not isinstance(item, dict):
            findings.append(Finding("error", path,
                                    f"must be an object, got {type(item).__name__}"))
            continue

        _rename_keys(item, section, path, findings, fix)
        _check_nulls(item, path, findings, fix)
        _check_list_description(item, section, path, findings, fix)
        _check_date_range(item, section, path, findings, fix)
        _check_dates(item, section, path, findings, fix)
        _check_list_fields(item, section, path, findings, fix)
        _check_required(item, section, path, findings)
        _check_unknown(item, KNOWN_KEYS[section], path, findings)



REQUIRED = {
    "work": {"name": "in JSON Resume 'name' is the COMPANY, not the person",
             "position": "'position' is the job title"},
    "education": {"institution": "the school or university"},
    "skills": {"name": "the skill or skill-group name"},
    "projects": {"name": "the project name"},
}


def _check_required(item: Dict[str, Any], section: str, path: str,
                    findings: List[Finding]) -> None:
    for field, hint in REQUIRED.get(section, {}).items():
        if not item.get(field):
            findings.append(Finding("error", f"{path}.{field}",
                                    f"missing — {hint}"))


def _rename_keys(item: Dict[str, Any], section: str, path: str,
                 findings: List[Finding], fix: bool) -> None:
    for wrong, right in RENAMES.get(section, {}).items():
        if wrong not in item:
            continue
        # 'description' is legal on work and projects; never rename it here.
        if item.get(right) not in (None, "", []):
            findings.append(Finding(
                "warning", f"{path}.{wrong}",
                f"not a JSON Resume field; '{right}' is already set, so this value "
                f"would be dropped on export", fixed=fix))
            item.pop(wrong)
            continue
        findings.append(Finding(
            "error", f"{path}.{wrong}",
            f"not a JSON Resume field — use '{right}'", fixed=fix))
        item[right] = item.pop(wrong)


def _check_list_description(item: Dict[str, Any], section: str, path: str,
                            findings: List[Finding], fix: bool) -> None:
    """The Sentry #7242697871 shape: description as a list of achievements."""
    if section not in ("work", "projects", "volunteer"):
        return
    desc = item.get("description")
    if not isinstance(desc, list):
        return
    findings.append(Finding(
        "error", f"{path}.description",
        "is a list — 'description' must be a string. A list of achievements belongs "
        "in 'highlights'. This exact shape crashed Phoenix's exporter with "
        "\"expected string or bytes-like object, got 'list'\"", fixed=fix))
    if item.get("highlights"):
        item["highlights"] = list(item["highlights"]) + list(desc)
    else:
        item["highlights"] = list(desc)
    item.pop("description")


def _check_date_range(item: Dict[str, Any], section: str, path: str,
                      findings: List[Finding], fix: bool) -> None:
    """A single 'dates' string instead of startDate/endDate."""
    if section not in DATE_FIELDS:
        return
    fields = DATE_FIELDS[section]
    if "startDate" not in fields:
        return
    for key in DATE_RANGE_KEYS:
        if key not in item or not isinstance(item[key], str):
            continue
        start, end, is_current = split_date_range(item[key])
        if start:
            findings.append(Finding(
                "error", f"{path}.{key}",
                f"free-text date range {item[key]!r} — JSON Resume wants ISO-8601 "
                f"'startDate' and 'endDate'", fixed=fix))
            item.setdefault("startDate", start)
            if end:
                item.setdefault("endDate", end)
            elif is_current:
                item.pop("endDate", None)
            item.pop(key)
        else:
            findings.append(Finding(
                "error", f"{path}.{key}",
                f"free-text date range {item[key]!r} that could not be parsed — "
                f"replace by hand with ISO-8601 'startDate' and 'endDate'"))


def _check_dates(item: Dict[str, Any], section: str, path: str,
                 findings: List[Finding], fix: bool) -> None:
    for field in DATE_FIELDS.get(section, ()):
        if field not in item:
            continue
        value = item[field]
        if not isinstance(value, str):
            findings.append(Finding("error", f"{path}.{field}",
                                    f"must be a string, got {type(value).__name__}"))
            continue
        if iso_valid(value):
            continue
        if ISO8601.match(value):
            findings.append(Finding(
                "error", f"{path}.{field}",
                f"{value!r} is ISO-shaped but not a real date — month must be 01-12 "
                f"and day must exist in that month"))
            continue
        repaired = parse_loose_date(value)
        if repaired:
            findings.append(Finding(
                "error", f"{path}.{field}",
                f"{value!r} is not ISO 8601 — use YYYY, YYYY-MM or YYYY-MM-DD",
                fixed=fix))
            item[field] = repaired
        else:
            findings.append(Finding(
                "error", f"{path}.{field}",
                f"{value!r} is not ISO 8601 and could not be parsed — "
                f"use YYYY, YYYY-MM or YYYY-MM-DD"))

    start, end = item.get("startDate"), item.get("endDate")
    if (isinstance(start, str) and isinstance(end, str)
            and iso_valid(start) and iso_valid(end) and end < start):
        findings.append(Finding("warning", f"{path}.endDate",
                                f"{end!r} is before startDate {start!r}"))


def _check_list_fields(item: Dict[str, Any], section: str, path: str,
                       findings: List[Finding], fix: bool) -> None:
    for field in ("highlights", "keywords", "courses", "roles"):
        if field not in item or field not in KNOWN_KEYS[section]:
            continue
        value = item[field]
        if isinstance(value, list):
            for j, entry in enumerate(value):
                if not isinstance(entry, str):
                    findings.append(Finding(
                        "error", f"{path}.{field}[{j}]",
                        f"must be a string, got {type(entry).__name__}"))
        elif isinstance(value, str):
            findings.append(Finding(
                "error", f"{path}.{field}",
                f"must be an array of strings, got a string", fixed=fix))
            item[field] = [line.strip(" -*\t") for line in value.split("\n")
                           if line.strip()]
        else:
            findings.append(Finding("error", f"{path}.{field}",
                                    f"must be an array, got {type(value).__name__}"))


def _check_skills_shape(data: Dict[str, Any], findings: List[Finding],
                        fix: bool) -> None:
    skills = data.get("skills")
    if not isinstance(skills, list) or not skills:
        return
    if all(isinstance(s, str) for s in skills):
        findings.append(Finding(
            "error", "$.skills",
            "is an array of strings — each entry must be an object with 'name' and "
            "optional 'keywords'", fixed=fix))
        data["skills"] = [{"name": s} for s in skills]


def _check_nulls(item: Dict[str, Any], path: str, findings: List[Finding],
                 fix: bool) -> None:
    for key in [k for k, v in item.items() if v is None]:
        findings.append(Finding(
            "warning", f"{path}.{key}",
            "is null — omit absent fields instead of nulling them; exporters render "
            "a null as an empty line rather than skipping the field", fixed=fix))
        item.pop(key)


def _check_unknown(item: Dict[str, Any], allowed: set, path: str,
                   findings: List[Finding]) -> None:
    for key in sorted(set(item) - allowed):
        if key.startswith("_") or key.startswith("$"):
            continue
        findings.append(Finding(
            "warning", f"{path}.{key}",
            "is not part of JSON Resume; it will be ignored by exporters"))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate (and optionally repair) a JSON Resume file.")
    parser.add_argument("path", help="the JSON Resume file to check")
    parser.add_argument("--fix", action="store_true",
                        help="repair what can be repaired and write the result")
    parser.add_argument("--output", "-o",
                        help="where --fix writes (default: overwrite the input)")
    parser.add_argument("--quiet", "-q", action="store_true",
                        help="print nothing; communicate through the exit code")
    args = parser.parse_args(argv)

    try:
        data = load_resume(args.path)
    except FileNotFoundError:
        print(f"{args.path}: no such file", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"{args.path}: not valid JSON — {exc}", file=sys.stderr)
        return 2

    repaired, findings = validate(data, fix=args.fix)

    errors = [f for f in findings if f.level == "error"]
    warnings = [f for f in findings if f.level == "warning"]
    unfixed = [f for f in errors if not f.fixed]

    if not args.quiet:
        print(args.path)
        if findings:
            for finding in findings:
                print(finding.render())
        else:
            print("  valid JSON Resume, no findings")

    if args.fix:
        destination = args.output or args.path
        with open(destination, "w", encoding="utf-8") as fh:
            json.dump(repaired, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
        if not args.quiet:
            fixed_count = sum(1 for f in findings if f.fixed)
            print(f"\n  wrote {destination} ({fixed_count} repaired, "
                  f"{len(unfixed)} still need a human)")
        return 1 if unfixed else 0

    if not args.quiet:
        print(f"\n  {len(errors)} error(s), {len(warnings)} warning(s)")
        if errors:
            print("  re-run with --fix to repair what can be repaired automatically")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
