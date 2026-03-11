# EM-TEST Agent Instructions

EM-TEST is a Python-based testing framework for [EM-DAT](https://www.emdat.be/) disaster datasets using `pandas` and `pandera`.

## Quick Start
- **Environment**: Python 3.11+, managed with `uv`.
- **Install**: `uv sync`
- **Core Logic**: `emtest/` module.
- **Validation**: `emtest/validation_schemas.py` and `emtest/custom_checks.py`.

## Progressive Disclosure Instructions
For specific tasks, refer to the following guides:

- [**Data Validation**](.junie/instructions/validation.md): Writing schemas, custom checks, and handling nullable types.
- [**EM-DAT Domain**](.junie/instructions/domain.md): Geospatial, temporal, and classification logic for disaster data.
- [**Reference Data & Metadata**](.junie/instructions/data.md): Managing reference files and project metadata (`CITATION.cff`).

## General Principles
- **Transparency**: Every check must be well-documented.
- **Reproducibility**: Use `uv` for consistent environments.
- **Consistency**: Maintain the existing `pandera` schema structure.
