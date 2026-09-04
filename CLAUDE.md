# EM-TEST vNext — working notes

Development of EM-TEST **2026.09.0** on branch `dev/v2026.09`. Read
[`AGENTS.md`](AGENTS.md) first — it holds the architecture, domain knowledge and
non-obvious design decisions, and remains authoritative. This file covers only
what is specific to this branch. Planned work is in [`ROADMAP.md`](ROADMAP.md).

This is a full clone of `em-dat/em-test` with `origin` intact, so work here can
go upstream as a PR against `master`, matching how `dev/v2026.05` was merged.

## Commands

```bash
uv sync --all-extras --dev        # or: uv pip install -e ".[dev]"
.venv/Scripts/python.exe -m pytest -q
```

A `.venv` on Python 3.13 is already provisioned. 41 tests currently pass.

## What changed on this branch

Version bumped to `2026.09.0` in `emtest/__init__.py`, `CITATION.cff`
(`date-released: 2026-09-04`) and `pyproject.toml`.

**New: `emtest/adapters.py`** — `api_to_emtest()`, exported from `emtest`.
Converts an EM-DAT GraphQL API response into the layout `emdat_schema`
validates. Before this, EM-TEST could only consume the public Excel download.

Constraints to preserve when touching it:

- **It reshapes, it never repairs.** Nulls in non-nullable columns,
  out-of-range numbers and unknown reference values must reach the validation
  report. Silencing a finding in the adapter defeats the framework.
- **It takes a plain DataFrame**, not a client object. That is what keeps
  EM-TEST's dependency list unchanged — do not add an API client dependency.
- **It reads column order from the schema at runtime**
  (`schema.columns.keys()`), so it survives schema changes. Do not hardcode.
- **Boolean flags are the trap.** `Historic`, `OFDA/BHA Response`, `Appeal` and
  `Declaration` arrive as Booleans; `coerce=True` would cast `True` to `"True"`
  and fail `check_yes_no` on every row. Near-total failure on those four
  columns means the adapter was bypassed, not that the data is bad.

`COLUMN_MAP` is the Excel↔API field mapping, sourced from the `emdat-api`
skill (`em-dat/skills-repo`, `references/excel-workflow.md`).

**Test fixtures**: `tests/conftest.py` gained `to_api_shape()`, `api_df` and
`geocoded_emdat_row`. `to_api_shape` inverts the adapter's own conventions
using `COLUMN_MAP`, so fixtures stay in sync with the mapping instead of
restating 47 column names. `geocoded_emdat_row` covers the admin-units and
earthquake-magnitude paths the plain `valid_emdat_row` leaves null.

Keep the DisNo. year and `Start Year` aligned in fixtures unless testing that
check — otherwise every test using the row emits a `check_disno_vs_start_year`
warning.

## Baseline: EM-DAT 2025 validation, 2026-09-04

582 records (412 natural, 170 technological, 136 countries), pulled from the
API with `start_year == 2025`. **Zero errors.** All EM-TEST non-nullable
columns fully populated. 15 warning cases over 8 events, all benign:

| Warning | Events |
|---|---|
| `TWN` / "Taiwan (Province of China)" not in M49 | 5 |
| `SPI` / "Canary Islands" not in M49 | 1 |
| `AZO` / "Azores Islands" not in M49 | 1 |
| `2024-0962-AGO`: Start Year 2025 under a 2024 DisNo. | 1 |

The last is a bacterial epidemic running 2025-01-07 to 2025-10 — the documented
case of an official start date revised after the DisNo. was assigned.

Use this as the reference point: a *new* warning category in a later run is
worth investigating; recurrence of these four is not. Note that time-relative
checks make runs non-reproducible across dates by construction (ROADMAP item 2).

## Provenance

Originated in `coding/260904_test`, which holds the original API validation
harness (`validate_2025.py`, the pre-promotion adapter, and the raw 2025 pull
plus failure report under `output/`). Nothing there is needed to work here.

Unrelated: `coding/em-test` is a separate working clone on `dev/v2026.05` with
uncommitted local data. Leave it alone.
