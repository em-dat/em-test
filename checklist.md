# Release Checklist

This checklist outlines the items to check, modify, and do before finalizing the release of EM-TEST.

## 1. Versioning and Metadata
- [ ] Synchronize version number in `pyproject.toml`.
- [ ] Synchronize version number in `emtest/__init__.py`.
- [ ] Update version and release date in `CITATION.cff` and within the How to Cite section of `README.md`.
- [ ] Check if `README.md` requires any version-specific updates (e.g., supported Python versions, installation steps).
- [ ] Ensure the license year is up to date if necessary.

## 2. Code and Logic
- [ ] Review all `TODO` and `FIXME` comments in the codebase.
- [ ] Verify that all custom checks in `emtest/custom_checks.py` are properly tested.
- [ ] Ensure `emtest/validation_schemas.py` reflects the latest EM-DAT public data structure.
- [ ] Check for any hardcoded paths in scripts and examples (e.g., `examples/validation_script.py`).

## 3. Data Files
- [ ] Update `emtest/validation_data/UNSD_M49_standards.csv` if new standards are available.
- [ ] Verify GAUL codes in `gaul_adm1_code.txt` and `gaul_adm2_code.txt`.
- [ ] Review classification lists in `classification_tree.toml` and associated Python files.

## 4. Documentation and Examples
- [ ] Verify that `examples/example_notebook.ipynb` runs without errors.
- [ ] Ensure `examples/validation_script.py` and other example scripts work with the provided test data.
- [ ] Update `README.md` with any new features or changes in usage.
- [ ] Check that links in documentation are not broken.

## 5. Testing and CI/CD
- [ ] Run the full test suite using `pytest`.
- [ ] Expand CI workflow to include version branch testing.
- [ ] Ensure all GitHub Actions workflows are passing.
- [ ] Add regression tests for any bugs fixed in this release cycle.
- [ ] Verify that the package can be built successfully (`python -m build`).

## 6. Final Steps
- [ ] Create a git tag for the version (e.g., `v2026.03.0`).
- [ ] Draft release notes summarizing key changes, bug fixes, and improvements.
