import pytest
import pandas as pd
import pandera as pa
from emtest.validation_schemas import emdat_schema

def test_valid_df_passes(valid_df):
    """Test that the default valid fixture passes the schema."""
    emdat_schema.validate(valid_df)

def test_invalid_historic(valid_df):
    """Test that an invalid 'Historic' value fails."""
    valid_df.loc[valid_df.index[0], "Historic"] = "Maybe"
    with pytest.raises(pa.errors.SchemaError, match="Invalid Historic value"):
        emdat_schema.validate(valid_df)

def test_invalid_classification_key(valid_df):
    """Test that an invalid 'Classification Key' value fails."""
    valid_df.loc[valid_df.index[0], "Classification Key"] = "InvalidKey"
    with pytest.raises(pa.errors.SchemaError, match="Invalid classification key"):
        emdat_schema.validate(valid_df)

def test_invalid_iso_code(valid_df):
    """Test that an invalid 'ISO' code fails (regex check)."""
    valid_df.loc[valid_df.index[0], "ISO"] = "BXX" # Invalid 3-letter code if we strictly check against reference, but let's see if regex fails it first
    # The schema has two checks on ISO: validate_iso3_code (regex) and check_iso3_code (list check, warning only)
    # Let's try one that fails regex:
    valid_df.loc[valid_df.index[0], "ISO"] = "123"
    # We expect a SchemaError for regex AND a SchemaWarning for the list check
    with pytest.warns(pa.errors.SchemaWarning, match="ISO3 code not in reference list"):
        with pytest.raises(pa.errors.SchemaError, match="Invalid ISO3 code"):
            emdat_schema.validate(valid_df)

def test_invalid_disno_index(valid_df):
    """Test that an invalid 'DisNo.' index pattern fails."""
    valid_df.index = ["INVALID-DISNO"]
    valid_df.index.name = "DisNo."
    # We expect a SchemaError for the index pattern AND a SchemaWarning for the Start Year vs DisNo. check
    with pytest.warns(pa.errors.SchemaWarning, match="Start year differs from DisNo year"):
        with pytest.raises(pa.errors.SchemaError, match="Invalid DisNo. Pattern"):
            emdat_schema.validate(valid_df)

def test_magnitude_range_checks(valid_df):
    """Test magnitude range checks for specific disaster types."""
    # Earthquake magnitude should be between 3 and 10
    valid_df.loc[valid_df.index[0], "Disaster Type"] = "Earthquake"
    valid_df.loc[valid_df.index[0], "Magnitude"] = 1.0
    with pytest.raises(pa.errors.SchemaError, match="Invalid earthquake magnitude"):
        emdat_schema.validate(valid_df)

def test_date_consistency(valid_df):
    """Test that start date after end date fails."""
    valid_df.loc[valid_df.index[0], "Start Year"] = 2024
    valid_df.loc[valid_df.index[0], "Start Month"] = 12
    valid_df.loc[valid_df.index[0], "End Year"] = 2024
    valid_df.loc[valid_df.index[0], "End Month"] = 1
    with pytest.raises(pa.errors.SchemaError, match="Start date inconsistency at the month resolution"):
        emdat_schema.validate(valid_df)

def test_lat_lon_consistency(valid_df):
    """Test that having only one of Latitude/Longitude fails."""
    valid_df.loc[valid_df.index[0], "Latitude"] = 50.0
    valid_df.loc[valid_df.index[0], "Longitude"] = None
    with pytest.raises(pa.errors.SchemaError, match="Missing latitude or longitude coordinates"):
        emdat_schema.validate(valid_df)

def test_json_admin_units(valid_df):
    """Test that invalid JSON in Admin Units fails."""
    valid_df.loc[valid_df.index[0], "Admin Units"] = "Not a JSON"
    with pytest.raises(pa.errors.SchemaError, match="Invalid JSON string"):
        emdat_schema.validate(valid_df)
