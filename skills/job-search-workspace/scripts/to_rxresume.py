#!/usr/bin/env python3
"""Convert a JSON Resume file to Reactive Resume import JSON (v5 or v4).

Take the output to https://rxresu.me/, import it, adjust it visually, download the
PDF. That is the whole PDF story — there is no renderer in this repository and there
does not need to be one.

Ported from Phoenix's reactive_resume_v5_converter.py / _v4_converter.py, with the
mistakes that cost real production time already corrected:

  * company/position are mapped the right way round. Phoenix had them swapped for
    several commits on the strength of a code comment claiming "In Onyx, company
    field is the role title". It is not. `work[].name` is the company and
    `work[].position` is the job title, in both JSON Resume and Reactive Resume.
  * dates in YYYY and YYYY-MM are formatted, not passed through. Phoenix parsed
    only YYYY-MM-DD, so "2023-04" printed as "2023-04" on the page.
  * a date range with no start still renders its end.
  * location is built from city/region/countryCode, not just address-or-city.
  * invalid output is an error. Phoenix printed validation failures to stdout and
    returned the malformed dictionary anyway, which is how a broken export reached
    users looking like a successful one.

The "Experience Cont." overflow split is ported as-is, because it works around real
Reactive Resume behaviour: it will not break a section across a page boundary, so a
long work history silently overflows and is cut off. Overflow entries move into a
custom section that starts on page two.

Standard library only. No network. No API key.

Usage:
    python3 to_rxresume.py resume.json -o resume.rxresume.json
    python3 to_rxresume.py resume.json --schema v4
    python3 to_rxresume.py resume.json --seed 1        # deterministic ids
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import string
import sys
from math import ceil
from typing import Any, Dict, List, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from validate_resume import validate  # noqa: E402

_rng = random.Random()

ENTITY = re.compile(r"&(?:[a-zA-Z][a-zA-Z0-9]{1,31}|#\d{1,7}|#[xX][0-9a-fA-F]{1,6});")
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

PROFILE_ICONS = {
    "linkedin": "linkedin-logo", "github": "github-logo",
    "twitter": "twitter-logo", "x": "twitter-logo",
    "gitlab": "gitlab-logo", "stackoverflow": "stack-overflow-logo",
    "website": "link", "portfolio": "link", "blog": "link",
}


# ---------------------------------------------------------------------------
# Page-fit estimation for the Experience Cont. split
# ---------------------------------------------------------------------------

class SplitConfig:
    """Line-budget model for how much experience fits on page one."""

    def __init__(self, chars_per_line: int = 72, header_lines_per_item: int = 2,
                 item_gap_lines: int = 1, experience_page1_budget: int = 70):
        self.chars_per_line = chars_per_line
        self.header_lines_per_item = header_lines_per_item
        self.item_gap_lines = item_gap_lines
        self.experience_page1_budget = experience_page1_budget


def estimate_item_lines(work_item: Dict[str, Any], config: SplitConfig) -> int:
    summary = work_item.get("summary") or ""
    lines = config.header_lines_per_item
    if summary:
        lines += ceil(len(summary) / config.chars_per_line)
    for highlight in work_item.get("highlights") or []:
        lines += ceil(len(str(highlight)) / max(config.chars_per_line - 4, 1))
    return lines + config.item_gap_lines


def split_work_items(items: List[Dict[str, Any]], config: SplitConfig
                     ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Split work items into (page one, overflow) by line budget.

    Always keeps at least one item on page one. Order is preserved within each
    group; once anything overflows, everything after it follows, so the history
    never reads out of sequence across the page break.
    """
    if not items:
        return [], []
    page1: List[Dict[str, Any]] = []
    overflow: List[Dict[str, Any]] = []
    used = 0
    for item in items:
        item_lines = estimate_item_lines(item, config)
        if not overflow and (used + item_lines <= config.experience_page1_budget
                             or not page1):
            page1.append(item)
            used += item_lines
        else:
            overflow.append(item)
    return page1, overflow


# ---------------------------------------------------------------------------
# Small helpers
# ---------------------------------------------------------------------------

def generate_cuid2() -> str:
    return "".join(_rng.choices(string.ascii_lowercase + string.digits, k=24))


def format_date(value: Any, mode: str = "m") -> str:
    """ISO 8601 -> 'Apr 2023' (mode 'm') or '2023' (mode 'y').

    Accepts YYYY, YYYY-MM and YYYY-MM-DD. Phoenix accepted only the last of the
    three and returned the other two unchanged, so a resume using YYYY-MM — which
    the schema explicitly allows, and which is what most people write — printed
    raw ISO dates on the finished page.
    """
    if not isinstance(value, str) or not value:
        return ""
    match = re.match(r"^(\d{4})(?:-(\d{2}))?(?:-(\d{2}))?$", value.strip())
    if not match:
        return value
    year, month = match.group(1), match.group(2)
    if mode.lower() == "y" or not month:
        return year
    index = int(month)
    if not 1 <= index <= 12:
        return year
    return f"{MONTH_NAMES[index - 1]} {year}"


def format_period(start: Any, end: Any) -> str:
    """'Apr 2023 - Present', 'Sep 2018 - Aug 2020', or just an end date."""
    formatted_start = format_date(start, "m")
    formatted_end = format_date(end, "m") if end else "Present"
    if not formatted_start:
        # Phoenix returned "" here, discarding a known end date along with the
        # missing start.
        return "" if not end else formatted_end
    return f"{formatted_start} - {formatted_end}"


def normalize_to_string(value: Any) -> str:
    """Flatten a value that might be a list into a string."""
    if not value:
        return ""
    if isinstance(value, list):
        return "\n".join(str(item) for item in value if item)
    return str(value)


def md_to_html(text: Any) -> str:
    """Preserve **bold**, *italic* and line breaks as the HTML Reactive Resume uses.

    A bare '&' is escaped so it survives as an ampersand ("Marks & Spencer"); an
    existing entity is left alone. '<' and '>' are deliberately not escaped, because
    JSON Resume text fields are allowed to carry inline HTML and Phoenix's own
    resumes did.
    """
    text = normalize_to_string(text)
    if not text:
        return ""
    text = ENTITY.sub(lambda m: "\x00" + m.group(0)[1:], text)
    text = text.replace("&", "&amp;").replace("\x00", "&")
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    return text.replace("\n", "<br>")


def html_block(summary: Any, highlights: Any, keywords: Any = None) -> str:
    """Build the paragraph + bullet-list HTML that every item description uses.

    Empty parts are omitted rather than emitted as <p></p>, which is what left
    Phoenix's exports with blank lines where a description should have been.
    """
    parts: List[str] = []
    summary_html = md_to_html(summary)
    if summary_html:
        parts.append(f"<p>{summary_html}</p>")
    if highlights:
        bullets = "".join(f"<li><p>{md_to_html(h)}</p></li>"
                          for h in highlights if str(h).strip())
        if bullets:
            parts.append(f"<ul>{bullets}</ul>")
    if keywords:
        joined = ", ".join(str(k) for k in keywords if str(k).strip())
        if joined:
            parts.append(f"<p><em>Keywords: {joined}</em></p>")
    return "".join(parts)


def location_string(location: Any) -> str:
    """Render a JSON Resume location object as one line.

    Phoenix used `address or city`, which dropped the region and country from a
    location that had no street address — the common case.
    """
    if isinstance(location, str):
        return location
    if not isinstance(location, dict):
        return ""
    parts = [location.get("address"), location.get("city"),
             location.get("region"), location.get("postalCode"),
             location.get("countryCode")]
    return ", ".join(str(p).strip() for p in parts if p and str(p).strip())


def text(value: Any) -> str:
    """Coerce to the plain string the Reactive Resume schema requires."""
    if value is None:
        return ""
    if isinstance(value, (list, dict)):
        return normalize_to_string(value) if isinstance(value, list) else ""
    return str(value)


def website(url: Any, label: str = "") -> Dict[str, str]:
    return {"url": text(url), "label": label}


# ---------------------------------------------------------------------------
# v5
# ---------------------------------------------------------------------------

V5_SECTION_DEFAULTS = [
    ("profiles", "Profiles", 3, False),
    ("experience", "Experience", 1, False),
    ("education", "Education", 2, False),
    ("projects", "Projects", 2, False),
    ("skills", "Skills", 2, False),
    ("languages", "Languages", 1, True),
    ("interests", "Interests", 1, True),
    ("awards", "Awards", 1, False),
    ("certifications", "Certifications", 1, False),
    ("publications", "Publications", 1, True),
    ("volunteer", "Volunteering", 1, True),
    ("references", "References", 1, True),
]


def _v5_item(**fields: Any) -> Dict[str, Any]:
    item = {"id": generate_cuid2(), "hidden": False,
            "options": {"showLinkInTitle": False}}
    item.update(fields)
    return item


def _v5_experience(work: Dict[str, Any]) -> Dict[str, Any]:
    return _v5_item(
        # JSON Resume: work[].name is the COMPANY, work[].position is the JOB TITLE.
        # Reactive Resume: company is the company, position is the job title.
        # Phoenix had these two lines swapped. Do not "fix" them back.
        company=text(work.get("name") or work.get("company")),
        position=text(work.get("position")),
        location=location_string(work.get("location")),
        period=text(work.get("_period")) or format_period(work.get("startDate"),
                                                          work.get("endDate")),
        website=website(work.get("url")),
        description=html_block(work.get("summary"), work.get("highlights")),
    )


def convert_v5(resume: Dict[str, Any], template: str = "onyx") -> Dict[str, Any]:
    basics = resume.get("basics") or {}
    work_items = resume.get("work") or []
    page1_work, overflow_work = split_work_items(work_items, SplitConfig())

    sections: Dict[str, Any] = {
        key: {"title": title, "columns": columns, "hidden": hidden, "items": []}
        for key, title, columns, hidden in V5_SECTION_DEFAULTS
    }

    sections["profiles"]["items"] = [
        _v5_item(network=text(p.get("network")), username=text(p.get("username")),
                 icon=text(p.get("network")).lower(), website=website(p.get("url")))
        for p in basics.get("profiles") or []
    ]
    sections["experience"]["items"] = [_v5_experience(w) for w in page1_work]
    sections["education"]["items"] = [
        _v5_item(school=text(e.get("institution")), degree=text(e.get("studyType")),
                 area=text(e.get("area")), grade=text(e.get("score")),
                 location=location_string(e.get("location")),
                 period=format_period(e.get("startDate"), e.get("endDate")),
                 website=website(e.get("url")),
                 description=(f"<p><strong>Courses:</strong></p><ul>" +
                              "".join(f"<li><p>{md_to_html(c)}</p></li>"
                                      for c in e["courses"]) + "</ul>")
                 if e.get("courses") else "")
        for e in resume.get("education") or []
    ]
    sections["projects"]["items"] = [
        {**_v5_item(name=text(p.get("name")),
                    period=format_period(p.get("startDate"), p.get("endDate")),
                    website=website(p.get("url")),
                    description=html_block(p.get("description"), p.get("highlights"),
                                           p.get("keywords"))),
         "options": {"showLinkInTitle": True}}
        for p in resume.get("projects") or []
    ]
    sections["skills"]["items"] = [
        _v5_item(icon="", name=text(s.get("name")), proficiency=text(s.get("level")),
                 level=0, keywords=[text(k) for k in s.get("keywords") or []])
        for s in resume.get("skills") or []
    ]
    sections["certifications"]["items"] = [
        _v5_item(title=text(c.get("name")), issuer=text(c.get("issuer")),
                 date=format_date(c.get("date"), "m"), website=website(c.get("url")),
                 description=md_to_html(c.get("summary") or c.get("description")))
        for c in resume.get("certificates") or []
    ]
    sections["awards"]["items"] = [
        _v5_item(title=text(a.get("title")), awarder=text(a.get("awarder")),
                 date=format_date(a.get("date"), "m"), website=website(a.get("url")),
                 description=md_to_html(a.get("summary")))
        for a in resume.get("awards") or []
    ]
    sections["languages"]["items"] = [
        _v5_item(language=text(l.get("language")), fluency=text(l.get("fluency")),
                 level=0)
        for l in resume.get("languages") or []
    ]
    sections["interests"]["items"] = [
        _v5_item(icon="", name=text(i.get("name")),
                 keywords=[text(k) for k in i.get("keywords") or []])
        for i in resume.get("interests") or []
    ]
    sections["publications"]["items"] = [
        _v5_item(title=text(p.get("name")), publisher=text(p.get("publisher")),
                 date=format_date(p.get("releaseDate"), "m"),
                 website=website(p.get("url")),
                 description=md_to_html(p.get("summary")))
        for p in resume.get("publications") or []
    ]
    sections["volunteer"]["items"] = [
        _v5_item(organization=text(v.get("organization")),
                 position=text(v.get("position")),
                 location=location_string(v.get("location")),
                 period=format_period(v.get("startDate"), v.get("endDate")),
                 website=website(v.get("url")),
                 description=html_block(v.get("summary"), v.get("highlights")))
        for v in resume.get("volunteer") or []
    ]
    sections["references"]["items"] = [
        _v5_item(name=text(r.get("name")), position=text(r.get("position")),
                 website=website(r.get("url")), phone=text(r.get("phone")),
                 description=md_to_html(r.get("reference")))
        for r in resume.get("references") or []
    ]

    document: Dict[str, Any] = {
        "picture": {"hidden": False, "url": text(basics.get("image")), "size": 64,
                    "rotation": 0, "aspectRatio": 1, "borderRadius": 0,
                    "borderColor": "rgba(0, 0, 0, 0)", "borderWidth": 0,
                    "shadowColor": "rgba(0, 0, 0, 0.5)", "shadowWidth": 0},
        "basics": {
            "name": text(basics.get("name")),
            "headline": text(basics.get("label")),
            "email": text(basics.get("email")),
            "phone": text(basics.get("phone")),
            "location": location_string(basics.get("location")),
            "website": website(basics.get("url")),
            "customFields": [
                {"id": generate_cuid2(),
                 "icon": PROFILE_ICONS.get(text(p.get("network")).lower(), "link"),
                 "text": text(p.get("username")), "link": text(p.get("url"))}
                for p in basics.get("profiles") or []
            ],
        },
        "summary": {"title": "Summary", "columns": 1, "hidden": False,
                    "content": (f"<p>{md_to_html(basics.get('summary'))}</p>"
                                if basics.get("summary") else "")},
        "sections": sections,
        "customSections": [],
        "metadata": _v5_metadata(template),
    }

    if overflow_work:
        custom_id = generate_cuid2()
        document["customSections"].append({
            "id": custom_id, "title": "Experience Cont.", "type": "experience",
            "columns": 1, "hidden": False,
            "items": [_v5_experience(w) for w in overflow_work],
        })
        document["metadata"]["layout"]["pages"][1]["main"].insert(0, custom_id)

    return document


def _v5_metadata(template: str) -> Dict[str, Any]:
    return {
        "template": template,
        "layout": {
            "sidebarWidth": 35,
            "pages": [
                {"fullWidth": True,
                 "main": ["profiles", "summary", "experience", "volunteer",
                          "references", "interests", "certifications", "awards",
                          "publications", "languages"],
                 "sidebar": []},
                {"fullWidth": False,
                 "main": ["projects", "education", "skills"],
                 "sidebar": []},
            ],
        },
        "css": {"enabled": False, "value": ""},
        "page": {"gapX": 4, "gapY": 6, "marginX": 12, "marginY": 12,
                 "format": "a4", "locale": "en-US", "hideIcons": False},
        "design": {"level": {"icon": "star", "type": "circle"},
                   "colors": {"primary": "rgba(0, 163, 136, 1)",
                              "text": "rgba(0, 0, 0, 1)",
                              "background": "rgba(255, 255, 255, 1)"}},
        "typography": {
            "body": {"fontFamily": "IBM Plex Serif",
                     "fontWeights": ["400", "400", "600"],
                     "fontSize": 8.125, "lineHeight": 1.1},
            "heading": {"fontFamily": "IBM Plex Serif", "fontWeights": ["600"],
                        "fontSize": 10.5, "lineHeight": 1.05},
        },
        "notes": "",
    }


# ---------------------------------------------------------------------------
# v4
# ---------------------------------------------------------------------------

V4_SECTION_DEFAULTS = [
    ("skills", "Skills", 2, True), ("profiles", "Profiles", 3, True),
    ("education", "Education", 2, True), ("experience", "Experience", 1, True),
    ("projects", "Projects", 2, True), ("certifications", "Certifications", 1, True),
    ("awards", "Awards", 1, True), ("interests", "Interests", 1, False),
    ("languages", "Languages", 1, False), ("volunteer", "Volunteering", 1, False),
    ("references", "References", 1, False), ("publications", "Publications", 1, False),
]

V4_DEFAULT_LAYOUT = [[
    ["profiles", "summary", "experience", "education", "projects", "volunteer",
     "references"],
    ["skills", "interests", "certifications", "awards", "publications", "languages"],
]]


def _v4_item(**fields: Any) -> Dict[str, Any]:
    item = {"id": generate_cuid2(), "visible": True}
    item.update(fields)
    return item


def _v4_experience(work: Dict[str, Any]) -> Dict[str, Any]:
    return _v4_item(
        company=text(work.get("name") or work.get("company")),  # see convert_v5
        position=text(work.get("position")),
        date=text(work.get("_period")) or format_period(work.get("startDate"),
                                                        work.get("endDate")),
        location=location_string(work.get("location")),
        summary=html_block(work.get("summary"), work.get("highlights")),
        url=website(work.get("url")),
    )


def convert_v4(resume: Dict[str, Any], template: str = "onyx") -> Dict[str, Any]:
    basics = resume.get("basics") or {}
    work_items = resume.get("work") or []
    page1_work, overflow_work = split_work_items(work_items, SplitConfig())

    sections: Dict[str, Any] = {"custom": {}}
    for key, name, columns, visible in V4_SECTION_DEFAULTS:
        sections[key] = {"id": key, "name": name, "items": [],
                         "columns": columns, "visible": visible}
    sections["projects"]["separateLinks"] = False
    sections["summary"] = {
        "id": "summary", "name": "Summary", "columns": 1, "visible": True,
        "content": (f"<p>{md_to_html(basics.get('summary'))}</p>"
                    if basics.get("summary") else ""),
    }

    sections["profiles"]["items"] = [
        _v4_item(url=website(p.get("url")), icon=text(p.get("network")).lower(),
                 network=text(p.get("network")), username=text(p.get("username")))
        for p in basics.get("profiles") or []
    ]
    sections["experience"]["items"] = [_v4_experience(w) for w in page1_work]
    sections["education"]["items"] = [
        _v4_item(url=website(e.get("url")),
                 date=format_period(e.get("startDate"), e.get("endDate")),
                 area=text(e.get("area")), score=text(e.get("score")),
                 studyType=text(e.get("studyType")),
                 institution=text(e.get("institution")),
                 summary=(f"<p><strong>Courses:</strong></p><ul>" +
                          "".join(f"<li><p>{md_to_html(c)}</p></li>"
                                  for c in e["courses"]) + "</ul>")
                 if e.get("courses") else "")
        for e in resume.get("education") or []
    ]
    sections["projects"]["items"] = [
        _v4_item(name=text(p.get("name")), description="",
                 date=format_period(p.get("startDate"), p.get("endDate")),
                 url=website(p.get("url")),
                 summary=html_block(p.get("description"), p.get("highlights"),
                                    p.get("keywords")))
        for p in resume.get("projects") or []
    ]
    sections["skills"]["items"] = [
        _v4_item(name=text(s.get("name")), description=text(s.get("level")), level=0,
                 keywords=[text(k) for k in s.get("keywords") or []])
        for s in resume.get("skills") or []
    ]
    sections["certifications"]["items"] = [
        _v4_item(name=text(c.get("name")), issuer=text(c.get("issuer")),
                 date=format_date(c.get("date"), "m"), url=website(c.get("url")),
                 summary=md_to_html(c.get("summary") or c.get("description")))
        for c in resume.get("certificates") or []
    ]
    sections["awards"]["items"] = [
        _v4_item(title=text(a.get("title")), awarder=text(a.get("awarder")),
                 date=format_date(a.get("date"), "m"), url=website(a.get("url")),
                 summary=md_to_html(a.get("summary")))
        for a in resume.get("awards") or []
    ]
    sections["languages"]["items"] = [
        _v4_item(name=text(l.get("language")), description=text(l.get("fluency")),
                 level=0)
        for l in resume.get("languages") or []
    ]
    sections["interests"]["items"] = [
        _v4_item(name=text(i.get("name")),
                 keywords=[text(k) for k in i.get("keywords") or []])
        for i in resume.get("interests") or []
    ]
    sections["publications"]["items"] = [
        _v4_item(name=text(p.get("name")), publisher=text(p.get("publisher")),
                 date=format_date(p.get("releaseDate"), "m"),
                 url=website(p.get("url")), summary=md_to_html(p.get("summary")))
        for p in resume.get("publications") or []
    ]
    sections["volunteer"]["items"] = [
        _v4_item(organization=text(v.get("organization")),
                 position=text(v.get("position")),
                 date=format_period(v.get("startDate"), v.get("endDate")),
                 location=location_string(v.get("location")),
                 url=website(v.get("url")),
                 summary=html_block(v.get("summary"), v.get("highlights")))
        for v in resume.get("volunteer") or []
    ]
    sections["references"]["items"] = [
        _v4_item(name=text(r.get("name")), summary=md_to_html(r.get("reference")))
        for r in resume.get("references") or []
    ]

    document: Dict[str, Any] = {
        "basics": {
            "url": website(basics.get("url")),
            "name": text(basics.get("name")),
            "email": text(basics.get("email")),
            "phone": text(basics.get("phone")),
            "headline": text(basics.get("label")),
            "location": location_string(basics.get("location")),
            "picture": {"url": text(basics.get("image")), "size": 64,
                        "aspectRatio": 1, "borderRadius": 0,
                        "effects": {"border": False, "hidden": False,
                                    "grayscale": False}},
            "customFields": [],
        },
        "metadata": _v4_metadata(template),
        "sections": sections,
    }

    if overflow_work:
        custom_id = generate_cuid2()
        sections["custom"][custom_id] = {
            "id": custom_id, "name": "Experience Cont.", "columns": 1,
            "separateLinks": True, "visible": True,
            "items": [
                _v4_item(name=text(w.get("name") or w.get("company")),
                         description=text(w.get("position")),
                         date=text(w.get("_period")) or format_period(
                             w.get("startDate"), w.get("endDate")),
                         location=location_string(w.get("location")),
                         summary=html_block(w.get("summary"), w.get("highlights")),
                         keywords=[], url=website(w.get("url")))
                for w in overflow_work
            ],
        }
        document["metadata"]["layout"] = [
            [["profiles", "summary", "experience", "volunteer", "references"],
             ["skills", "interests", "certifications", "awards", "publications",
              "languages"]],
            [[f"custom.{custom_id}", "education", "projects"], []],
        ]

    return document


def _v4_metadata(template: str) -> Dict[str, Any]:
    return {
        "css": {"value": "", "visible": False},
        "page": {"format": "a4", "margin": 12,
                 "options": {"breakLine": True, "pageNumbers": True}},
        "notes": "",
        "theme": {"text": "#000000", "primary": "#00a388", "background": "#ffffff"},
        "layout": [[list(column) for column in V4_DEFAULT_LAYOUT[0]]],
        "template": template,
        "typography": {
            "font": {"size": 11.5, "family": "IBM Plex Serif", "subset": "latin",
                     "variants": ["regular", "italic", "600"]},
            "hideIcons": False, "lineHeight": 1.05, "underlineLinks": False,
        },
    }


# ---------------------------------------------------------------------------
# Output checks
# ---------------------------------------------------------------------------

V5_REQUIRED = {
    "basics": ["name", "headline", "email", "phone", "location"],
    "experience": ["company", "position", "location", "period", "description"],
    "education": ["school", "degree", "area", "grade", "location", "period"],
    "projects": ["name", "period", "description"],
    "skills": ["name"],
    "profiles": ["network", "username"],
    "certifications": ["title", "issuer", "date"],
    "awards": ["title", "awarder", "date"],
    "languages": ["language"],
}


def check_v5(document: Dict[str, Any]) -> List[str]:
    """Structural check on the generated document.

    Phoenix ran the equivalent check, printed any failure, and returned the broken
    document anyway. Here a failure is fatal, because an export that looks like it
    worked and is not importable is worse than one that stops.
    """
    problems: List[str] = []
    basics = document.get("basics", {})
    for field in V5_REQUIRED["basics"]:
        if not isinstance(basics.get(field), str):
            problems.append(f"basics.{field} must be a string, "
                            f"got {type(basics.get(field)).__name__}")
    if not basics.get("name"):
        problems.append("basics.name is empty — the resume would have no name on it")

    for key, section in document.get("sections", {}).items():
        for attr in ("title", "columns", "hidden", "items"):
            if attr not in section:
                problems.append(f"sections.{key} is missing '{attr}'")
        for index, item in enumerate(section.get("items", [])):
            path = f"sections.{key}.items[{index}]"
            if not item.get("id"):
                problems.append(f"{path} has no id")
            for field in V5_REQUIRED.get(key, []):
                if field not in item:
                    problems.append(f"{path} is missing '{field}'")
                elif not isinstance(item[field], str):
                    problems.append(f"{path}.{field} must be a string, "
                                    f"got {type(item[field]).__name__}")
            for field, value in item.items():
                if value is None:
                    problems.append(f"{path}.{field} is null")

    layout_ids = {i for page in document.get("metadata", {})
                  .get("layout", {}).get("pages", [])
                  for i in page.get("main", []) + page.get("sidebar", [])}
    for custom in document.get("customSections", []):
        if custom["id"] not in layout_ids:
            problems.append(f"custom section {custom['title']!r} is not referenced "
                            f"by any page in metadata.layout, so it would not render")
    return problems


def check_v4(document: Dict[str, Any]) -> List[str]:
    problems: List[str] = []
    basics = document.get("basics", {})
    for field in ("name", "email", "phone", "headline", "location"):
        if not isinstance(basics.get(field), str):
            problems.append(f"basics.{field} must be a string")
    if not basics.get("name"):
        problems.append("basics.name is empty — the resume would have no name on it")

    sections = document.get("sections", {})
    for key, section in sections.items():
        if key == "custom":
            continue
        for attr in ("id", "name", "visible"):
            if attr not in section:
                problems.append(f"sections.{key} is missing '{attr}'")
        for index, item in enumerate(section.get("items", [])):
            for field, value in item.items():
                if value is None:
                    problems.append(f"sections.{key}.items[{index}].{field} is null")

    flat_layout = {entry for page in document.get("metadata", {}).get("layout", [])
                   for column in page for entry in column}
    for custom_id in sections.get("custom", {}):
        if f"custom.{custom_id}" not in flat_layout:
            problems.append(f"custom section {custom_id} is not referenced by "
                            f"metadata.layout, so it would not render")
    return problems


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Convert JSON Resume to Reactive Resume import JSON.")
    parser.add_argument("path", help="the JSON Resume file to convert")
    parser.add_argument("--output", "-o", help="where to write (default: stdout)")
    parser.add_argument("--schema", choices=("v5", "v4"), default="v5",
                        help="Reactive Resume schema version (default: v5)")
    parser.add_argument("--template", default="onyx",
                        help="Reactive Resume template name (default: onyx)")
    parser.add_argument("--seed", type=int,
                        help="seed the id generator so output is reproducible")
    parser.add_argument("--strict", action="store_true",
                        help="refuse to convert a resume with validation errors "
                             "instead of repairing it first")
    args = parser.parse_args(argv)

    try:
        with open(args.path, encoding="utf-8") as fh:
            raw = json.load(fh)
    except FileNotFoundError:
        print(f"{args.path}: no such file", file=sys.stderr)
        return 2
    except json.JSONDecodeError as exc:
        print(f"{args.path}: not valid JSON — {exc}", file=sys.stderr)
        return 2

    if args.seed is not None:
        _rng.seed(args.seed)

    repaired, findings = validate(raw, fix=True)
    errors = [f for f in findings if f.level == "error"]
    if errors:
        if args.strict:
            print(f"{args.path}: {len(errors)} validation error(s); "
                  f"run validate_resume.py --fix first, or drop --strict",
                  file=sys.stderr)
            for finding in errors:
                # Not finding.render(): nothing was written, so a "[fixed]" tag
                # here would claim a repair the user did not get.
                print(f"  {finding.path}: {finding.message}", file=sys.stderr)
            return 1
        print(f"{args.path}: repaired {len(errors)} validation error(s) before "
              f"converting; run validate_resume.py to see them", file=sys.stderr)

    convert = convert_v5 if args.schema == "v5" else convert_v4
    check = check_v5 if args.schema == "v5" else check_v4
    document = convert(repaired, args.template)

    problems = check(document)
    if problems:
        print(f"{args.path}: conversion produced an invalid Reactive Resume "
              f"{args.schema} document and was not written:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    payload = json.dumps(document, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload)
        overflow = len(document.get("customSections", []) or
                       document.get("sections", {}).get("custom", {}))
        note = " (work history split across two pages)" if overflow else ""
        print(f"wrote {args.output} — Reactive Resume {args.schema}{note}",
              file=sys.stderr)
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    sys.exit(main())
