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
    """Test that a non-alphabetic ISO code fails the regex check and raises a warning."""
    valid_df.loc[valid_df.index[0], "ISO"] = "123"
    with pytest.warns(pa.errors.SchemaWarning, match="ISO3 code not in reference list"):
        with pytest.raises(pa.errors.SchemaError, match="Invalid ISO3 code"):
            emdat_schema.validate(valid_df)

def test_invalid_disno_index(valid_df):
    """Test that an invalid 'DisNo.' index pattern fails."""
    valid_df.index = ["INVALID-DISNO"]
    valid_df.index.name = "DisNo."
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
    """Test that start month after end month within the same year fails."""
    valid_df.loc[valid_df.index[0], "Start Year"] = 2024
    valid_df.loc[valid_df.index[0], "Start Month"] = 12
    valid_df.loc[valid_df.index[0], "End Year"] = 2024
    valid_df.loc[valid_df.index[0], "End Month"] = 1
    with pytest.raises(pa.errors.SchemaError, match="Start date inconsistency at the month resolution"):
        emdat_schema.validate(valid_df)

def test_start_year_after_end_year(valid_df):
    """Test that start year after end year fails."""
    valid_df.index = ["2025-0001-BEL"]
    valid_df.index.name = "DisNo."
    valid_df.loc[valid_df.index[0], "Start Year"] = 2025
    valid_df.loc[valid_df.index[0], "End Year"] = 2024
    with pytest.raises(pa.errors.SchemaError, match="Start date inconsistency at the year resolution"):
        emdat_schema.validate(valid_df)

def test_start_day_after_end_day(valid_df):
    """Test that start day after end day within the same year and month fails."""
    valid_df.loc[valid_df.index[0], "Start Month"] = 3.0
    valid_df.loc[valid_df.index[0], "Start Day"] = 20.0
    valid_df.loc[valid_df.index[0], "End Month"] = 3.0
    valid_df.loc[valid_df.index[0], "End Day"] = 10.0
    with pytest.raises(pa.errors.SchemaError, match="Start date inconsistency at the day resolution"):
        emdat_schema.validate(valid_df)

def test_date_consistency_skips_month_when_absent(valid_df):
    """Test that missing months do not cause a false positive on the month check."""
    valid_df.loc[valid_df.index[0], "Start Month"] = None
    valid_df.loc[valid_df.index[0], "Start Day"] = None
    valid_df.loc[valid_df.index[0], "End Month"] = None
    valid_df.loc[valid_df.index[0], "End Day"] = None
    emdat_schema.validate(valid_df)

def test_date_consistency_skips_day_when_absent(valid_df):
    """Test that missing days do not cause a false positive on the day check."""
    valid_df.loc[valid_df.index[0], "Start Day"] = None
    valid_df.loc[valid_df.index[0], "End Day"] = None
    emdat_schema.validate(valid_df)

def test_date_consistency_cross_year_no_false_positive(valid_df):
    """Test that a cross-year event passes even when start month > end month."""
    valid_df.index = ["2025-0001-BEL"]
    valid_df.index.name = "DisNo."
    valid_df.loc[valid_df.index[0], "Start Year"] = 2025
    valid_df.loc[valid_df.index[0], "Start Month"] = 6.0
    valid_df.loc[valid_df.index[0], "End Year"] = 2026
    valid_df.loc[valid_df.index[0], "End Month"] = 3.0
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
