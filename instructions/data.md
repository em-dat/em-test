# Reference Data & Metadata Management

EM-TEST relies on reference data to validate EM-DAT content.

## 1. Reference Files
Reference data is stored in `emtest/validation_data/`.
- **`classification_tree.toml`**: The source of truth for disaster types and subgroups.
- **`UNSD_M49_standards.csv`**: Reference for country and region names.
- **`gaul_adm1_code.txt`**: GAUL administrative level 1 codes.

## 2. Loading Data
Reference data is loaded by `emtest/validation_data/data_loader.py`.
When adding new reference files, update `data_loader.py` and ensure they are included in `pyproject.toml` under `tool.setuptools.package-data`.

## 3. Metadata and Citations
- **`CITATION.cff`**: Project citation info for scientific researchers.
- **`LICENSE`**: MIT License.
- **Versioning**: Follow CalVer (`YYYY.MM.N`), reflected in `emtest/__init__.py`, `pyproject.toml`, and `CITATION.cff`.
- **README Updates**: If you add new validation checks, update the corresponding tables in `README.md`.
