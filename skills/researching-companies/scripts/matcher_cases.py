#!/usr/bin/env python3
"""Regression cases for the sponsor-register name matcher.

Run directly: exits 0 and prints a summary, or exits 1 listing what changed.

The first case is the one that matters. Phoenix scored candidate names with rapidfuzz
`partial_ratio`, and its own shipped fixture records a search for OpenAI matching a
London company called Morena at 66.7 — after which the summariser recorded
`is_visa_sponsor: True`. Loose character-level overlap is why. Every case below exists
to keep that class of match out.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uk_visa_sponsor_lookup import score  # noqa: E402

SHOWN, STRONG = 62, 74

# (query, register name, should be shown, should be strong)
CASES = [
    ("OpenAI",          "Morena",                        False, False),
    ("Kestrel Labs",    "Kestrel Labs Ltd",              True,  True),
    ("Kestrel Labs",    "Kestrel Labs Limited",          True,  True),
    ("Kestrel Labs",    "Kestrel Laboratories Ltd",      True,  True),
    ("Kestrel Labs",    "Kestrel Insurance Brokers",     True,  False),
    ("Kestrel Labs",    "Kestrel Facilities Management", True,  False),
    ("Kestrel Labs",    "Peregrine Labs Ltd",            False, False),
    ("Google",          "Google UK Limited",             True,  True),
    ("Google",          "Googlemail Ltd",                False, False),
    ("Expedia",         "Expedia.com Ltd",               True,  True),
    ("Monzo",           "Monzo Bank Ltd",                True,  True),
    ("Monzo Bank",      "GB Bank Limited",               False, False),
    ("Monzo",           "Mondo Ltd",                     False, False),
    ("Deliveroo",       "Roofoods Ltd",                  False, False),
    ("Deliveroo",       "Roofoods Ltd t/a Deliveroo",    True,  True),
    ("Acme",            "Acme",                          True,  True),
    ("Acme Systems",    "Systems Acme Ltd",              True,  True),
    ("Acme Systems",    "Acme",                          True,  True),
    ("BT",              "BT Group PLC",                  True,  True),
    ("Ocado",           "Ocado Group plc",               True,  True),
    ("Ocado",           "Ocado Central Services Limited", True, True),
    ("Ocado",           "Avocado Consulting Ltd",        False, False),
    ("Meta",            "Metabolic Health Ltd",          False, False),
    ("Revolut",         "Revolut Ltd",                   True,  True),
    ("Stripe",          "Stripe Payments UK Ltd",        True,  True),
    ("Stripe",          "Pinstripe Recruitment",         False, False),
    ("Trellis Bio",     "Trellis Bioscience Ltd",        True,  True),
    ("Trellis Bio",     "Lattice Bio Ltd",               False, False),
    ("Northwind",       "Northwind Logistics Ltd",       True,  True),
    ("Apple",           "Pineapple Studios Ltd",         False, False),
    ("Oracle",          "Oracle Corporation UK Ltd",     True,  True),
    ("Sage",            "Sage Group",                    True,  True),
    ("Sage",            "Message Labs Ltd",              False, False),
    ("Orbital Freight", "Orbital Freight Ltd",           True,  True),
    # The register stores names unaccented. Without accent folding a user typing the
    # company's real name gets "No plausible match", which this script frames as strong
    # evidence they cannot sponsor — a confident wrong answer about right to work.
    ("Nestlé",          "Nestle UK Limited",             True,  True),
    ("NESTLÉ",          "Nestle UK Limited",             True,  True),
    ("Ørsted",          "Orsted Power (UK) Limited",     True,  True),
    ("Société Générale","Societe Generale",              True,  True),
    ("Nestlé",          "Kestrel Grove Limited",         False, False),
]


def main() -> int:
    wrong = []
    for query, name, want_shown, want_strong in CASES:
        points, why = score(query, name)
        shown, strong = points >= SHOWN, points >= STRONG
        if (shown, strong) != (want_shown, want_strong):
            wrong.append(f"{query!r} vs {name!r} -> {points} ({why or 'no match'}); "
                         f"wanted shown={want_shown} strong={want_strong}, "
                         f"got shown={shown} strong={strong}")
    for line in wrong:
        print("  " + line, file=sys.stderr)
    print(f"name matching: {len(CASES) - len(wrong)}/{len(CASES)} cases correct")
    return 1 if wrong else 0


if __name__ == "__main__":
    sys.exit(main())
