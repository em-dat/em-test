# EM-TEST 2026.09.0 — roadmap

Working branch: `dev/v2026.09`, off `master` at `9cdf047` (the 2026.05 merge).

## Where this came from

A validation run of EM-DAT 2025 data on 2026-09-04 (582 records, sourced from
the GraphQL API) surfaced one framework gap and several smaller observations.
The gap is already addressed on this branch; the rest are candidates.

That run produced **zero errors**. Its 15 warning cases across 8 events were
all in known-benign categories, and they are the evidence behind items 1 and 4
below.

## Delivered on this branch

### API support (`emtest/adapters.py`)

EM-TEST validated only the public Excel download. `emdat_schema` is declared
`strict=True, ordered=True` with a `DisNo.` index, so an API response could not
be passed to it at all — five differences blocked it:

| Difference | API returns | Schema requires |
|---|---|---|
| Field names | `total_deaths`, `disno` | `Total Deaths`, `DisNo.` index |
| Extra fields | 51 fields | 46 + index; 4 API-only fields must go |
| Flags | `historic`, `ofda_response`, `appeal`, `declaration` as Boolean | `"Yes"`/`"No"` strings |
| Admin units | parsed `list[dict]` | JSON string |
| Timestamps | ISO strings | `pd.Timestamp` |

`api_to_emtest()` reconciles all five, exported from `emtest`. It reshapes
only — invalid values are left for validation to report. It takes a plain
DataFrame, so it adds **no dependency** on any API client.

The flag conversion is the subtle one: `coerce=True` will cast `True` to the
string `"True"`, which fails `check_yes_no` on *every* row. A run showing
~100% failure on those four columns means the adapter was bypassed.

17 tests in `tests/test_adapters.py`; suite is 41 passing.

## Candidates for this release

### 1. Distinguish known EM-DAT exceptions from unknown reference values

`check_iso3_code` and `check_country` warn on anything outside the current
UNSD M49 list. In the 2025 run that fired 14 times for three cases that are
permanent, deliberate EM-DAT entries:

- `TWN` / "Taiwan (Province of China)" — 5 events
- `SPI` / "Canary Islands" — 1 event
- `AZO` / "Azores Islands" — 1 event

Every one recurs in every run, so the warning currently carries no signal: a
reader cannot tell a standing exception from a genuinely new bad code. Proposal:
an explicit `KNOWN_AREA_EXCEPTIONS` reference list, with these codes reported
under a separate, quieter category (or suppressed with a summary count), so the
warning again means "look at this".

The README already explains that these exceptions exist. Encoding them makes
the framework act on its own documentation.

### 2. Reproducibility of time-relative checks

`Start Year` / `End Year` are bounded by `CURRENT_YEAR`, and `Entry Date` /
`Last Update` by `CURRENT_DATE`. The same data therefore validates differently
depending on the day. Proposal: an optional `as_of` argument (defaulting to
today) so a historical run can be reproduced exactly. Needed for any use of
EM-TEST as a regression gate.

### 3. `get_validation_report` returns `None` on success

Callers must special-case `None` before touching the result. Returning an empty
DataFrame with the standard `failure_cases` columns would let reports be
concatenated, counted and written without branching. Breaking change — worth
doing on a version boundary if at all.

### 4. Report ergonomics

The report keys events by `index` (the `DisNo.`). Adding the `Country` and
`Start Year` of each failing event would make a report readable without
joining back to the source. Cheap, and it was the first thing wanted when
reading the 2025 output.

### 5. `has_valid_GAUL_codes` performance

Flagged in `AGENTS.md` as the likely bottleneck: it parses JSON per row and
checks against ~50k ADM2 codes. Not a problem at 582 rows; worth measuring on a
full-database run (~26k rows) before optimising.

### 6. Dependency floor vs. current resolutions

`pyproject.toml` floors at `pandera>=0.21`, `pandas>=2.2`. A fresh environment
now resolves `pandera 0.33.1` / `pandas 3.0.5`, well ahead of `uv.lock`. The
suite passes there, but the CI matrix pins only Python versions, not dependency
versions. Consider testing oldest-supported and newest resolutions.

## Release checklist

Version is bumped to `2026.09.0` in `emtest/__init__.py`, `CITATION.cff`
(with `date-released`) and `pyproject.toml`. Per `AGENTS.md`, `__init__.py` and
`CITATION.cff` must agree on release. Update the README schema tables if any
check is added, changed or recategorised between error and warning.
