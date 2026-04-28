# Data Validation with Pandera and Pandas

The core of EM-TEST is built on `pandera` and `pandas`.

## 1. Schema Definition
Schemas are defined in `emtest/validation_schemas.py`.
- **`DataFrameSchema`**: Use this to define per-column constraints.
- **Nullability**: In Pandas, the standard `int` type is not nullable. Use `float` for columns that contain integers but may have null values (e.g., `Start Month`, `Start Day`).

## 2. Custom Checks
Complex validation logic should be implemented in `emtest/custom_checks.py`.
- **Single-Column Checks**: Implement logic for a specific field (e.g., `check_disno`, `check_month`).
- **Multi-Column ("Wide") Checks**: Use these for consistency between fields (e.g., `check_start_end_year_consistency`).

## 3. Regular Expression Engineering
Identifiers are often validated via Regex:
- **DisNo format**: `^\d{4}-\d{4}-[A-Z]{3}$` (Year-Sequence-CountryISO).
- **External IDs**: GLIDE numbers and other identifiers rely on specific patterns.

## 4. Testing Pattern
Changes must be verified with the pytest test suite:
- `uv run pytest` — runs all tests in `tests/`
- `uv run pytest tests/test_validation.py::test_date_consistency` — run a single test

The suite tests both individual check functions (`tests/test_custom_checks.py`) and the full schema (`tests/test_validation.py`). The fixture in `tests/conftest.py` provides a valid single-row DataFrame; tests mutate one field at a time and assert the expected `SchemaError`.

The example scripts in `examples/` validate real datasets and can be used for end-to-end verification after schema changes.
