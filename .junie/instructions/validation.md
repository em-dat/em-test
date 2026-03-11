# Data Validation with Pandera and Pandas

The core of EM-TEST is built on `pandera` and `pandas`.

## 1. Schema Definition
Schemas are defined in `emtest\validation_schemas.py`.
- **`DataFrameSchema`**: Use this to define per-column constraints.
- **Nullability**: In Pandas, the standard `int` type is not nullable. Use `float` for columns that contain integers but may have null values (e.g., `Start Month`, `Start Day`).

## 2. Custom Checks
Complex validation logic should be implemented in `emtest\custom_checks.py`.
- **Single-Column Checks**: Implement logic for a specific field (e.g., `check_disno`, `check_month`).
- **Multi-Column ("Wide") Checks**: Use these for consistency between fields (e.g., `check_start_end_year_consistency`).

## 3. Regular Expression Engineering
Identifiers are often validated via Regex:
- **DisNo format**: `^\d{4}-\d{4}-[A-Z]{3}$` (Year-Sequence-CountryISO).
- **External IDs**: GLIDE numbers and other identifiers rely on specific patterns.

## 4. Testing Pattern
Since there are no traditional automated tests, verify changes using the example script:
- `python examples\validation_script.py`
This script uses the schema to validate a sample dataset.
