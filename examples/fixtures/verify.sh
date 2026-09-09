#!/usr/bin/env bash
# Check the job-search-workspace scripts against the fixtures.
# No network, no API key. Run from anywhere.
set -uo pipefail

here="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo="$(cd "$here/../.." && pwd)"
scripts="$repo/skills/job-search-workspace/scripts"
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

pass=0 fail=0
check() {  # check <description> <expected-exit> <command...>
    local description="$1" expected="$2"; shift 2
    "$@" >"$tmp/out" 2>&1
    local actual=$?
    if [ "$actual" -eq "$expected" ]; then
        printf '  ok    %s\n' "$description"; pass=$((pass + 1))
    else
        printf '  FAIL  %s (exit %d, wanted %d)\n' "$description" "$actual" "$expected"
        sed 's/^/          /' "$tmp/out" | head -5
        fail=$((fail + 1))
    fi
}

assert() {  # assert <description> <python expression over `d`> <json file>
    local description="$1" expression="$2" file="$3"
    if python3 -c "
import json,sys
d=json.load(open('$file'))
sys.exit(0 if ($expression) else 1)
" 2>"$tmp/err"; then
        printf '  ok    %s\n' "$description"; pass=$((pass + 1))
    else
        printf '  FAIL  %s\n' "$description"; sed 's/^/          /' "$tmp/err"
        fail=$((fail + 1))
    fi
}

echo "validate_resume.py"
check "a valid résumé passes" 0 \
    python3 "$scripts/validate_resume.py" "$repo/examples/workspace/profile/resume.json" -q
check "a tailored résumé passes" 0 \
    python3 "$scripts/validate_resume.py" \
    "$repo/examples/workspace/applications/kestrel-labs-senior-data-engineer/resume.json" -q
check "the long résumé passes" 0 \
    python3 "$scripts/validate_resume.py" "$here/long-resume.json" -q
check "the malformed résumé fails" 1 \
    python3 "$scripts/validate_resume.py" "$here/malformed-resume.json" -q
check "--fix repairs it" 0 \
    python3 "$scripts/validate_resume.py" "$here/malformed-resume.json" --fix -o "$tmp/fixed.json" -q
check "the repaired file then passes" 0 \
    python3 "$scripts/validate_resume.py" "$tmp/fixed.json" -q
assert "repair moves experience -> work" "'work' in d and 'experience' not in d" "$tmp/fixed.json"
assert "repair maps company -> name" "d['work'][0]['name'] == 'Halcyon Retail Group'" "$tmp/fixed.json"
assert "repair maps role -> position" "d['work'][0]['position'] == 'Senior Data Engineer'" "$tmp/fixed.json"
assert "repair maps list description -> highlights" "len(d['work'][0]['highlights']) == 3" "$tmp/fixed.json"
assert "repair splits 'Apr 2023 - Present'" \
    "d['work'][0]['startDate'] == '2023-04' and 'endDate' not in d['work'][0]" "$tmp/fixed.json"

echo
echo "to_rxresume.py"
check "converts a valid résumé (v5)" 0 \
    python3 "$scripts/to_rxresume.py" "$repo/examples/workspace/profile/resume.json" --seed 1 -o "$tmp/good.v5.json"
check "converts a valid résumé (v4)" 0 \
    python3 "$scripts/to_rxresume.py" "$repo/examples/workspace/profile/resume.json" --schema v4 --seed 1 -o "$tmp/good.v4.json"
check "converts the malformed résumé by repairing it" 0 \
    python3 "$scripts/to_rxresume.py" "$here/malformed-resume.json" --seed 1 -o "$tmp/bad.v5.json"
check "--strict refuses the malformed résumé" 1 \
    python3 "$scripts/to_rxresume.py" "$here/malformed-resume.json" --strict -o "$tmp/never.json"
[ -f "$tmp/never.json" ] && { echo "  FAIL  --strict wrote a file anyway"; fail=$((fail + 1)); } \
                         || { echo "  ok    --strict wrote nothing"; pass=$((pass + 1)); }

assert "company is the employer, not the job title" \
    "d['sections']['experience']['items'][0]['company'] == 'Halcyon Retail Group'" "$tmp/good.v5.json"
assert "position is the job title, not the employer" \
    "d['sections']['experience']['items'][0]['position'] == 'Senior Data Engineer'" "$tmp/good.v5.json"
assert "company/position survive the repair path too" \
    "d['sections']['experience']['items'][0]['company'] == 'Halcyon Retail Group' and d['sections']['experience']['items'][0]['position'] == 'Senior Data Engineer'" "$tmp/bad.v5.json"
assert "YYYY-MM dates are formatted, not passed through" \
    "d['sections']['experience']['items'][0]['period'] == 'Apr 2023 - Present'" "$tmp/good.v5.json"
assert "v4 maps company/position the same way" \
    "d['sections']['experience']['items'][0]['company'] == 'Halcyon Retail Group'" "$tmp/good.v4.json"
assert "location keeps region and country" \
    "d['basics']['location'] == 'Manchester, England, GB'" "$tmp/good.v5.json"
assert "no custom section for a résumé that fits" "d['customSections'] == []" "$tmp/good.v5.json"

echo
echo "Experience Cont. overflow split"
check "converts the long résumé (v5)" 0 \
    python3 "$scripts/to_rxresume.py" "$here/long-resume.json" --seed 1 -o "$tmp/long.v5.json"
check "converts the long résumé (v4)" 0 \
    python3 "$scripts/to_rxresume.py" "$here/long-resume.json" --schema v4 --seed 1 -o "$tmp/long.v4.json"
assert "v5 splits the work history" \
    "len(d['customSections']) == 1 and d['customSections'][0]['title'] == 'Experience Cont.'" "$tmp/long.v5.json"
assert "v5 puts the overflow section on page two" \
    "d['customSections'][0]['id'] == d['metadata']['layout']['pages'][1]['main'][0]" "$tmp/long.v5.json"
assert "v5 preserves chronological order across the break" \
    "[i['position'] for i in d['sections']['experience']['items']] + [i['position'] for i in d['customSections'][0]['items']] == [w['position'] for w in json.load(open('$here/long-resume.json'))['work']]" "$tmp/long.v5.json"
assert "v4 splits the work history" \
    "len(d['sections']['custom']) == 1" "$tmp/long.v4.json"
assert "v4 references the overflow section in its layout" \
    "('custom.' + next(iter(d['sections']['custom']))) in d['metadata']['layout'][1][0]" "$tmp/long.v4.json"

echo
echo "invalid output is refused, not written"
printf '{"basics":{"label":"Engineer"},"work":[{"name":"Acme","position":"Engineer","startDate":"2020"}]}' > "$tmp/nameless.json"
check "a résumé with no name does not convert" 1 \
    python3 "$scripts/to_rxresume.py" "$tmp/nameless.json" -o "$tmp/nameless.v5.json"
[ -f "$tmp/nameless.v5.json" ] && { echo "  FAIL  invalid output was written"; fail=$((fail + 1)); } \
                               || { echo "  ok    invalid output was not written"; pass=$((pass + 1)); }

echo
echo "reproducibility"
python3 "$scripts/to_rxresume.py" "$repo/examples/workspace/profile/resume.json" --seed 7 -o "$tmp/s7a.json" 2>/dev/null
python3 "$scripts/to_rxresume.py" "$repo/examples/workspace/profile/resume.json" --seed 7 -o "$tmp/s7b.json" 2>/dev/null
cmp -s "$tmp/s7a.json" "$tmp/s7b.json" && { echo "  ok    --seed makes output reproducible"; pass=$((pass + 1)); } \
                                       || { echo "  FAIL  --seed did not make output reproducible"; fail=$((fail + 1)); }

echo
echo "cross-artifact figure consistency"
if python3 "$repo/examples/fixtures/check_consistency.py" \
        "$repo/examples/workspace/applications/kestrel-labs-senior-data-engineer" \
        >"$tmp/cons" 2>&1; then
    printf '  ok    every figure in the example letter and answers is supported\n'
    pass=$((pass + 1))
else
    printf '  FAIL  an artifact claims a figure nothing supports\n'
    sed 's/^/          /' "$tmp/cons"; fail=$((fail + 1))
fi
# The check must actually fail on an invented figure, or it proves nothing.
rm -rf "$tmp/inject"; cp -R "$repo/examples/workspace" "$tmp/inject"
python3 - "$tmp/inject" <<'INNER'
import pathlib, sys
p = pathlib.Path(sys.argv[1]) / "applications/kestrel-labs-senior-data-engineer/cover-letter.md"
p.write_text(p.read_text().replace("three internal consumers", "forty-one internal consumers"))
INNER
if python3 "$repo/examples/fixtures/check_consistency.py" \
        "$tmp/inject/applications/kestrel-labs-senior-data-engineer" >/dev/null 2>&1; then
    printf '  FAIL  an invented figure was not detected\n'; fail=$((fail + 1))
else
    printf '  ok    an invented figure is detected\n'; pass=$((pass + 1))
fi

echo
echo "uk_visa_sponsor_lookup.py name matching (offline)"
if python3 "$repo/skills/researching-companies/scripts/matcher_cases.py" >"$tmp/match" 2>&1; then
    n=$(tail -1 "$tmp/match")
    printf '  ok    %s\n' "$n"; pass=$((pass + 1))
else
    printf '  FAIL  name matching regressed\n'; sed 's/^/          /' "$tmp/match"
    fail=$((fail + 1))
fi

echo
printf '%d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ]
