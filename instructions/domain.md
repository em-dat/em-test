# EM-DAT Domain Knowledge

EM-TEST validates data related to international disasters.

## 1. Geospatial Consistency
- **ISO3 Codes**: Country codes should be valid ISO-3166-1 alpha-3 codes.
- **Geography**: Valid latitude (-90 to 90) and longitude (-180 to 180).
- **Standards**: The project follows UNSD M49 standards for country and area codes.

## 2. Temporal Logic
Disaster numbers (`DisNo.`) contain the year the disaster was recorded.
- **Consistency**: `Start Year` should generally match the year in `DisNo.`.
- **Duration**: `Start Year/Month/Day` must be before or equal to `End Year/Month/Day`.

## 3. Classification
Disasters are categorized hierarchically:
- **Disaster Group** (e.g., Natural)
- **Disaster Subgroup** (e.g., Meteorological)
- **Disaster Type** (e.g., Storm)
- **Disaster Subtype** (e.g., Tropical cyclone)

Validation must ensure that combinations of these fields follow the official `classification_tree.toml`.
