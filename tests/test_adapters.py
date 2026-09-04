import json

import pandas as pd
import pytest

from emtest.adapters import (
    API_ONLY_FIELDS,
    api_to_excel_layout,
    to_json_string,
    to_yes_no,
)
from emtest.validation_schemas import emdat_schema

from conftest import to_api_shape


def test_adapted_api_response_validates(api_df):
    """Test that an adapted API response passes the schema unchanged."""
    emdat_schema.validate(api_to_excel_layout(api_df))


def test_adapted_geocoded_row_validates(geocoded_emdat_row):
    """Test that populated admin units survive the round trip."""
    api_df = to_api_shape([geocoded_emdat_row], ["2024-0042-BEL"])
    emdat_schema.validate(api_to_excel_layout(api_df))


def test_column_order_matches_schema(api_df):
    """Test that the adapter satisfies the ordered=True constraint."""
    out = api_to_excel_layout(api_df)
    assert list(out.columns) == list(emdat_schema.columns.keys())


def test_index_is_disno(api_df):
    """Test that the adapter indexes on 'DisNo.'."""
    out = api_to_excel_layout(api_df)
    assert out.index.name == "DisNo."
    assert out.index.tolist() == ["2024-0001-BEL"]


def test_api_only_fields_are_dropped(api_df):
    """Test that API-only fields are removed for the strict=True constraint."""
    assert all(field in api_df.columns for field in API_ONLY_FIELDS)
    out = api_to_excel_layout(api_df)
    assert not any(field in out.columns for field in API_ONLY_FIELDS)


def test_boolean_flags_become_yes_no(api_df):
    """Test that boolean API flags convert to the Excel 'Yes'/'No' form.

    Without this conversion, coerce=True casts True to the string 'True',
    which fails check_yes_no on every row.
    """
    assert api_df["historic"].dtype == bool
    out = api_to_excel_layout(api_df)
    for column in ["Historic", "OFDA/BHA Response", "Appeal", "Declaration"]:
        assert out[column].tolist() == ["No"]


def test_admin_units_are_serialised(geocoded_emdat_row):
    """Test that parsed admin units are returned to a JSON string."""
    api_df = to_api_shape([geocoded_emdat_row], ["2024-0042-BEL"])
    assert isinstance(api_df["admin_units"].iloc[0], list)
    out = api_to_excel_layout(api_df)
    value = out["Admin Units"].iloc[0]
    assert isinstance(value, str)
    assert json.loads(value)[0]["adm1_code"] == 442


def test_null_admin_units_stay_null(api_df):
    """Test that absent admin units are not serialised to an empty list."""
    out = api_to_excel_layout(api_df)
    assert pd.isna(out["Admin Units"].iloc[0])


def test_dates_are_parsed(api_df):
    """Test that ISO date strings become timestamps."""
    assert isinstance(api_df["entry_date"].iloc[0], str)
    out = api_to_excel_layout(api_df)
    for column in ["Entry Date", "Last Update"]:
        assert pd.api.types.is_datetime64_any_dtype(out[column])


def test_missing_field_raises(api_df):
    """Test that an incomplete API response fails loudly."""
    incomplete = api_df.drop(columns=["total_deaths"])
    with pytest.raises(KeyError, match="Total Deaths"):
        api_to_excel_layout(incomplete)


def test_adapter_does_not_repair_values(api_df):
    """Test that invalid values reach validation rather than being fixed."""
    api_df.loc[0, "total_deaths"] = -5.0
    out = api_to_excel_layout(api_df)
    assert out["Total Deaths"].iloc[0] == -5.0


@pytest.mark.parametrize(
    "value,expected",
    [
        (True, "Yes"),
        (False, "No"),
        ("Yes", "Yes"),
        ("No", "No"),
        ("true", "Yes"),
        (1, "Yes"),
        (0, "No"),
    ],
)
def test_to_yes_no(value, expected):
    """Test boolean-like values map onto the Yes/No convention."""
    assert to_yes_no(value) == expected


def test_to_yes_no_is_idempotent():
    """Test that already-converted values are stable."""
    assert to_yes_no(to_yes_no(True)) == "Yes"


def test_to_yes_no_passes_through_unknown():
    """Test that unrecognised values are left for check_yes_no to report."""
    assert to_yes_no("Maybe") == "Maybe"


def test_to_yes_no_passes_through_other_numbers():
    """Test that only 0 and 1 are read as flags, so 2 stays reportable."""
    assert to_yes_no(2) == 2


def test_to_json_string_empty_list_is_null():
    """Test that an empty list is treated as missing, as in the Excel export."""
    assert pd.isna(to_json_string([]))


def test_to_json_string_passes_through_string():
    """Test that an existing JSON string is not double-encoded."""
    value = json.dumps([{"adm1_code": 442}])
    assert to_json_string(value) == value
