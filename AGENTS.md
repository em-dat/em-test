# EM-TEST Agent Instructions

EM-TEST is a Python data validation framework for [EM-DAT](https://www.emdat.be/) disaster datasets. It validates disaster event DataFrames against a comprehensive schema of type constraints, business rules, and multi-column consistency checks using `pandera` and `pandas`.

Versioning follows CalVer: `YYYY.MM.N` (e.g., `2026.04.0`). Version is defined in `emtest/__init__.py` and must also be updated in `CITATION.cff` on release.

## Commands

```bash
# Install with all dev dependencies (preferred)
uv sync --all-extras --dev

# Run all tests
uv run pytest

# Run a single test file
uv run pytest tests/test_custom_checks.py

# Run a specific test
uv run pytest tests/test_custom_checks.py::test_check_disno
```

No Makefile or linting config exists — the project relies on `pytest` for correctness checks and manual review.

## Architecture

```
emtest/
├── __init__.py              # Public API: exports emdat_schema and __version__
├── validation_schemas.py    # DataFrameSchema: 50+ columns + multi-column checks
├── custom_checks.py         # Check functions used inside validation_schemas.py
├── utils.py                 # get_validation_report(), update_column_checks(), etc.
└── validation_data/         # Reference data package
    ├── data_loader.py       # Loads TOML/CSV/TXT files via Path(__file__).parent
    ├── classification.py    # Disaster classification tree (loaded from .toml)
    ├── areas.py             # ISO3 codes, country names, regions, GAUL codes
    └── magnitude.py         # Magnitude scale units per disaster type
```

**Data flow**: user loads an Excel/CSV file → passes a DataFrame with `DisNo.` as index to `emdat_schema.validate(df, lazy=True)` → pandera raises `SchemaErrors` → `get_validation_report()` converts errors to a flat DataFrame for export.

## Domain Knowledge

See [`instructions/domain.md`](instructions/domain.md) for the full reference. Key points:

- **ISO3 / geography**: country codes follow ISO-3166-1 alpha-3; latitude −90–90, longitude −180–180; regions follow UNSD M49.
- **DisNo. year**: `Start Year` should generally match the four-digit year embedded in `DisNo.` (a warning, not an error).
- **Date chronology**: `Start Year/Month/Day` ≤ `End Year/Month/Day` at every available resolution.
- **Classification**: Group → Subgroup → Type → Subtype combinations are validated against `classification_tree.toml`.

## Non-Obvious Design Decisions

**Nullable integer columns use `float`**: Fields like `Start Month`, `Start Day`, `End Month`, `End Day` can be null. Pandas `int` dtype is non-nullable, so these are defined as `float` with `NaN` for missing values throughout the schema and checks.

**Wide (multi-column) checks and deduplication**: Multi-column check functions in pandera fail every row they touch, causing duplicated error rows in reports. `deduplicate_errors()` in `utils.py` filters these so each logical failure appears once. When adding new wide checks, define which column should "own" the error in `WIDE_CHECKS_TO_KEEP`.

**Index access inside column checks**: The `check_disno_vs_start_year` check compares the year embedded in `DisNo.` (the DataFrame index) against the `Start Year` column. Since the index isn't a regular column in pandera, this check is attached to the `Start Year` column and accesses `series.index` internally.

**Parameterized date consistency via `partial()`**: `check_start_end_consistency()` in `custom_checks.py` is called three times (year/month/day resolution) using `functools.partial()`. The helper `_convert_to_date` assembles a date string and calls `pd.to_datetime(..., errors='coerce')`. Two subtleties: (1) month/day NaN values map to `'00'`, producing an invalid date string that coerces to `NaT` — the `pd.isna()` guard in the caller then skips the comparison, which is the intended behaviour for incomplete dates; (2) year columns must be converted via `int()` before `str()` because when any row has a null `End Year`, pandas reads the entire column as `float64`, making `.astype(str)` produce `'2024.0'` instead of `'2024'`.

**GAUL code validation is expensive**: `has_valid_GAUL_codes()` parses JSON strings in the `Admin Units` column, then validates codes against two large reference lists (ADM1: ~1k codes, ADM2: ~50k codes). It is only applied to non-null values. If performance is an issue on large datasets, this check is the likely bottleneck.

**Disaster type-specific magnitude rules**: Magnitude validation branches on `Classification Key` (a semicolon-delimited hierarchy like `nat;geo;earthquake`). Earthquake expects 3–10, cold wave ≤10°C, heat wave ≥25°C, everything else >0. The logic lives in `custom_checks.py` functions like `check_earthquake_magnitude`.

**Warnings vs errors**: Some checks (ISO code, country name, start year vs DisNo. year, CPI range) are configured as `raise_warning=True` in `validation_schemas.py`. `get_validation_report(add_warnings=True)` includes them; `set_warnings_to_errors()` in `utils.py` promotes all warnings to hard errors.

## Tests

`tests/conftest.py` provides two fixtures reused across test files:
- `valid_emdat_row` — dict with all 50 columns set to valid values
- `valid_df` — single-row DataFrame with `DisNo.` as index

The typical test pattern mutates one field of `valid_emdat_row`, constructs a DataFrame, and asserts that `emdat_schema.validate()` raises `SchemaError`.

## Detailed Instructions

For specific tasks, refer to the following guides in `instructions/`:

- [**Data Validation**](instructions/validation.md): Writing schemas, custom checks, and handling nullable types.
- [**EM-DAT Domain**](instructions/domain.md): Geospatial, temporal, and classification logic for disaster data.
- [**Reference Data & Metadata**](instructions/data.md): Managing reference files and project metadata (`CITATION.cff`).
