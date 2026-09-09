#!/usr/bin/env python3
"""Search the UK register of licensed sponsors for a company.

For anyone who needs a Skilled Worker visa, this is the single highest-value check in
the whole research process, and it is binary: an employer that does not hold a licence
cannot hire them, however good the role is. The register is a public CSV published by
the Home Office and needs no credential of any kind.

This is a port of Phoenix's UK visa sponsorship extractor, minus its matching. That
version scored candidate names with rapidfuzz `partial_ratio` and accepted anything at
82 or above. Its own shipped test fixture records what that approach does: a search for
**OpenAI** matched a London company called **Morena** at 66.7, and the summariser then
built a record asserting `is_visa_sponsor: True` — the score never gated the conclusion,
only the shortlist. It also carried a hardcoded table mapping google to alphabet, meta to
facebook and so on, which is a maintenance burden and a poor substitute for knowing what
a company is called.

So this script does not decide. It finds register rows that plausibly correspond to the
name you gave it, shows you what the register actually says about each, and leaves the
identification to you. Matching is on whole tokens, never on loose substrings, because
loose substring matching is precisely what turned OpenAI into Morena.

Standard library only. One HTTP request to gov.uk, then a local cache for seven days.

Usage:
    python3 uk_visa_sponsor_lookup.py "Kestrel Labs"
    python3 uk_visa_sponsor_lookup.py "Acme" --town London
    python3 uk_visa_sponsor_lookup.py "Acme" --json
    python3 uk_visa_sponsor_lookup.py "Acme" --refresh      # ignore the cached CSV

Exit codes:
    0  at least one candidate row was found
    1  the register was searched and nothing plausible matched
    2  the lookup could not be completed (network, layout change, bad arguments)
"""

from __future__ import annotations

import argparse
import csv
import difflib
import io
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Tuple

LANDING_PAGE = ("https://www.gov.uk/government/publications/"
                "register-of-licensed-sponsors-workers")
CSV_HREF = re.compile(
    r'href="(https://assets\.publishing\.service\.gov\.uk/media/[^"]+\.csv)"')
CSV_HREF_ALT = re.compile(r'href="([^"]*Worker_and_Temporary_Worker[^"]*\.csv[^"]*)"')
CACHE_TTL_SECONDS = 7 * 24 * 60 * 60
USER_AGENT = "phoenix-skills-visa-lookup/1.0 (+https://github.com/arashbehmand/phoenix-skills)"

# Legal-form suffixes. Stripped for comparison only; the register's own spelling is
# always what gets displayed.
SUFFIXES = re.compile(
    r"\b(ltd|limited|plc|llp|llc|inc|incorporated|corporation|corp|co|company|"
    r"group|holdings|holding|uk|gb|europe|international|global|services|"
    r"solutions|technologies|technology|systems)\b", re.IGNORECASE)
PUNCTUATION = re.compile(r"[^\w\s]", re.UNICODE)
# Tokens too generic to identify anything on their own.
STOPWORDS = {"the", "and", "of", "for", "a", "an"}


def normalise(name: str) -> str:
    name = PUNCTUATION.sub(" ", name.lower())
    name = SUFFIXES.sub(" ", name)
    return " ".join(name.split())


def tokens(name: str) -> List[str]:
    return [t for t in normalise(name).split() if t not in STOPWORDS]


def akin(a: str, b: str) -> bool:
    """Is one word plausibly an abbreviation or expansion of the other?

    "labs" and "laboratories"; "bio" and "bioscience". Not "labs" and "insurance".
    """
    if a == b:
        return True
    shorter, longer = sorted((a, b), key=len)
    if len(shorter) >= 3 and longer.startswith(shorter[:3]):
        return True
    return difflib.SequenceMatcher(None, a, b).ratio() >= 0.75


def score(query: str, candidate: str) -> Tuple[int, str]:
    """Rate how well a register row's name matches the query.

    Returns (0-100, why). Deliberately conservative: a score here means "worth your
    eyes", never "this is them".
    """
    q_norm, c_norm = normalise(query), normalise(candidate)
    q_tokens, c_tokens = tokens(query), tokens(candidate)
    if not q_tokens or not c_tokens:
        return 0, ""

    if q_norm == c_norm:
        return 100, "exact match on name, ignoring legal suffix"

    q_set, c_set = set(q_tokens), set(c_tokens)

    # Every word of the query appears in the register name, in order and adjacent.
    if len(q_tokens) <= len(c_tokens):
        for start in range(len(c_tokens) - len(q_tokens) + 1):
            if c_tokens[start:start + len(q_tokens)] == q_tokens:
                extra = len(c_tokens) - len(q_tokens)
                return max(96 - extra * 4, 80), "register name contains the full name"

    if q_set == c_set:
        return 92, "same words in a different order"

    if q_set <= c_set:
        return max(88 - (len(c_set) - len(q_set)) * 5, 70), "register name adds words"

    if c_set <= q_set and q_tokens[0] in c_set:
        # The first-token requirement matters here: without it "Monzo Bank" matches
        # "GB Bank Limited", which strips to the single word "bank".
        return max(82 - (len(q_set) - len(c_set)) * 8, 62), "register name is shorter"

    shared = q_set & c_set

    # Partial overlap only counts when the *distinctive* word is shared. The first
    # token of a company name usually carries the identity ("Kestrel" in "Kestrel
    # Labs"); the rest is category ("Labs", "Group", "Partners"). Without this,
    # "Kestrel Labs" matches "Peregrine Labs" on the word they have in common — and
    # loose character-level overlap of the kind Phoenix used matched OpenAI to a
    # company called Morena.
    if shared and q_tokens[0] in c_set:
        rest_q, rest_c = q_set - shared, c_set - shared
        if any(akin(a, b) for a in rest_q for b in rest_c):
            # The words that differ are the same word abbreviated or expanded:
            # "Kestrel Labs" against "Kestrel Laboratories".
            return 74, f"shares {', '.join(sorted(shared))}, rest reads as a variant"
        # Only the leading word agrees, and the rest is a different business:
        # "Kestrel Labs" against "Kestrel Insurance Brokers". Shown deliberately,
        # scored low — usually unrelated, occasionally a rebrand. A flat score, not
        # a similarity ratio, so the cutoff does not depend on how long the other
        # name happens to be.
        return 64, f"shares only the leading word '{q_tokens[0]}' — likely unrelated"

    # Near-identical spelling: a typo or a genuine variant, not a coincidence.
    ratio = difflib.SequenceMatcher(None, q_norm, c_norm).ratio()
    if ratio >= 0.87 and abs(len(q_norm) - len(c_norm)) <= 4:
        return int(ratio * 70), "very similar spelling"

    return 0, ""


# ---------------------------------------------------------------------------
# Fetching
# ---------------------------------------------------------------------------

def cache_path(cache_dir: str) -> str:
    return os.path.join(cache_dir, "uk-licensed-sponsors.csv")


def fetch(url: str, timeout: int = 120) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read().decode("utf-8-sig", errors="replace")


def find_csv_url(html: str) -> str | None:
    match = CSV_HREF.search(html) or CSV_HREF_ALT.search(html)
    if not match:
        return None
    url = match.group(1)
    if not url.startswith("http"):
        url = "https://assets.publishing.service.gov.uk" + url
    return url


def load_register(cache_dir: str, refresh: bool,
                  use_cache: bool = True) -> Tuple[List[Dict[str, str]], str]:
    """Return (rows, provenance). Uses a local cache for seven days."""
    path = cache_path(cache_dir)

    if use_cache and not refresh and os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        if age < CACHE_TTL_SECONDS:
            with open(path, encoding="utf-8") as fh:
                content = fh.read()
            stamp = time.strftime("%Y-%m-%d", time.localtime(os.path.getmtime(path)))
            return parse(content), f"local cache, downloaded {stamp}"

    html = fetch(LANDING_PAGE)
    csv_url = find_csv_url(html)
    if not csv_url:
        raise RuntimeError(
            "could not find the CSV download link on\n  " + LANDING_PAGE +
            "\nThe page layout has probably changed. Open it in a browser, download the "
            "'Worker and Temporary Worker' CSV by hand, and pass it with --csv.")
    content = fetch(csv_url)

    if use_cache:
        os.makedirs(cache_dir, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)

    return parse(content), f"downloaded {time.strftime('%Y-%m-%d')} from gov.uk"


def parse(content: str) -> List[Dict[str, str]]:
    """Parse the register CSV, normalising the column names."""
    rows: List[Dict[str, str]] = []
    for row in csv.DictReader(io.StringIO(content)):
        normalised = {}
        for key, value in row.items():
            if key:
                normalised[key.strip().lower().replace(" ", "_")] = (value or "").strip()
        if normalised:
            rows.append(normalised)
    return rows


def field(row: Dict[str, str], *names: str) -> str:
    """Read the first present column. The register's headers change between editions."""
    for name in names:
        if row.get(name):
            return row[name]
    return ""


def search(rows: List[Dict[str, str]], query: str, town: str | None,
           threshold: int, limit: int) -> List[Dict[str, Any]]:
    hits: List[Dict[str, Any]] = []
    seen: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
    for row in rows:
        name = field(row, "organisation_name", "name", "organisation")
        if not name:
            continue
        points, reason = score(query, name)
        if points < threshold:
            continue
        row_town = field(row, "town/city", "town", "city")
        if town and town.lower() not in row_town.lower():
            continue
        route = field(row, "route", "tier_&_rating", "type_&_rating")
        rating = field(row, "type_&_rating", "tier_&_rating", "rating")
        county = field(row, "county")
        key = (name, row_town, county)
        if key in seen:
            entry = seen[key]
            if route and route not in entry["routes"]:
                entry["routes"].append(route)
            if rating and rating not in entry["ratings"]:
                entry["ratings"].append(rating)
            continue
        seen[key] = {
            "organisation_name": name,
            "town_city": row_town,
            "county": county,
            "routes": [route] if route else [],
            "ratings": [rating] if rating else [],
            "score": points,
            "why": reason,
        }
        hits.append(seen[key])
    hits.sort(key=lambda h: (-h["score"], h["organisation_name"]))
    return hits[:limit]


# ---------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------

CAVEAT = """
What this does and does not tell you:

  * Appearing on the register means the organisation HOLDS a sponsor licence. It does
    not mean it will sponsor this role, or you.
  * Company names collide, and the register lists trading names, subsidiaries and
    unrelated organisations that happen to share a word. Confirm the town, and confirm
    it against the employer's own registered name, before relying on any row above.
  * Not appearing is strong evidence, not proof. Check obvious variants of the name and
    the parent company before concluding they cannot sponsor.
  * The route matters. A 'Temporary Worker' or 'Student' licence is not a Skilled
    Worker licence.
  * The register is a snapshot. Licences are granted and revoked continuously.
"""


def render(query: str, hits: List[Dict[str, Any]], total: int,
           provenance: str) -> str:
    out = [
        "Register of Licensed Sponsors (Workers and Temporary Workers)",
        f"{total:,} organisations · {provenance}",
        "",
        f'Searching for: "{query}"',
        "",
    ]
    if not hits:
        out += [
            "  No plausible match.",
            "",
            "  Before concluding they cannot sponsor, try: the full registered name",
            "  (Companies House has it), the parent or group company, the UK",
            "  subsidiary, and any former name.",
        ]
        return "\n".join(out) + "\n" + CAVEAT

    strong = [h for h in hits if h["score"] >= 74]
    if strong:
        out.append(f"  {len(hits)} row(s) worth checking — none of them is confirmed to")
        out.append("  be the employer you mean. That judgement is yours:")
    else:
        out.append(f"  {len(hits)} weak row(s) only. Nothing here looks like the same")
        out.append("  organisation — most likely this employer is not on the register")
        out.append("  under this name. Try the registered name or the parent company:")
    out.append("")
    width = max(len(h["organisation_name"]) for h in hits)
    width = min(max(width, 20), 54)
    header = f"  {'ORGANISATION'.ljust(width)}  {'TOWN/CITY'.ljust(16)}  ROUTE"
    out += [header, "  " + "-" * (len(header) - 2)]
    for hit in hits:
        name = hit["organisation_name"]
        if len(name) > width:
            name = name[:width - 1] + "…"
        routes = "; ".join(hit["routes"]) or "—"
        out.append(f"  {name.ljust(width)}  {hit['town_city'][:16].ljust(16)}  {routes}")
    out.append("")
    for hit in hits:
        detail = f"  {hit['organisation_name']}"
        if hit["county"]:
            detail += f" · {hit['county']}"
        ratings = [r for r in hit["ratings"] if r not in hit["routes"]]
        if ratings:
            detail += " · " + "; ".join(ratings)
        out.append(detail + f"  ({hit['why']})")
    return "\n".join(out) + "\n" + CAVEAT


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Search the UK register of licensed sponsors for a company.")
    parser.add_argument("company", help="the employer's name")
    parser.add_argument("--town", help="only show rows in this town or city")
    parser.add_argument("--json", action="store_true", dest="as_json",
                        help="emit JSON instead of a table")
    parser.add_argument("--limit", type=int, default=12,
                        help="maximum rows to show (default: 12)")
    parser.add_argument("--threshold", type=int, default=62,
                        help="minimum match score, 0-100 (default: 62)")
    parser.add_argument("--refresh", action="store_true",
                        help="re-download the register instead of using the cache")
    parser.add_argument("--csv", help="read the register from a local CSV file")
    parser.add_argument("--cache-dir",
                        default=os.path.join(
                            os.environ.get("XDG_CACHE_HOME",
                                           os.path.expanduser("~/.cache")),
                            "phoenix-skills"),
                        help="where the downloaded register is cached")
    args = parser.parse_args(argv)

    try:
        if args.csv:
            with open(args.csv, encoding="utf-8-sig") as fh:
                rows = parse(fh.read())
            provenance = f"local file {args.csv}"
        else:
            rows, provenance = load_register(args.cache_dir, args.refresh)
    except (urllib.error.URLError, OSError, RuntimeError) as exc:
        print(f"could not load the register: {exc}", file=sys.stderr)
        return 2

    if not rows:
        print("the register parsed as empty — the CSV format has probably changed",
              file=sys.stderr)
        return 2

    hits = search(rows, args.company, args.town, args.threshold, args.limit)

    if args.as_json:
        print(json.dumps({
            "query": args.company,
            "register_rows": len(rows),
            "provenance": provenance,
            "matches": hits,
            "confirmed": False,
            "note": ("Presence means the organisation holds a licence, not that it "
                     "will sponsor this role. Identity is not confirmed — check the "
                     "town and the registered name."),
        }, indent=2, ensure_ascii=False))
    else:
        print(render(args.company, hits, len(rows), provenance))

    return 0 if hits else 1


if __name__ == "__main__":
    sys.exit(main())
