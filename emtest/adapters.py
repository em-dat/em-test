"""Adapters converting external EM-DAT representations to the schema layout.

The `emdat_schema` is defined with `strict=True`, `ordered=True` and a
`DisNo.` index, i.e. it validates the layout of the EM-DAT public Excel
download. Data obtained from the EM-DAT GraphQL API describes the same records
in a different shape and cannot be validated as returned.

The `api_to_emtest` function performs that conversion. It reshapes only:
values that violate the schema are left intact so that validation reports
them.

#Authors: Damien Delforge, Valentin Wathelet
#Email: damien.delforge@uclouvain.be
"""
from __future__ import annotations

import json
from typing import Any, Optional

import pandas as pd

__all__ = [
    "COLUMN_MAP",
    "API_TO_EXCEL",
    "API_ONLY_FIELDS",
    "api_to_emtest",
    "to_yes_no",
    "to_json_string",
]

#: Excel column name to API field name, for the 47 shared fields.
COLUMN_MAP: dict = {
    "DisNo.": "disno",
    "Historic": "historic",
    "Classification Key": "classif_key",
    "Disaster Group": "group",
    "Disaster Subgroup": "subgroup",
    "Disaster Type": "type",
    "Disaster Subtype": "subtype",
    "External IDs": "external_ids",
    "Event Name": "name",
    "ISO": "iso",
    "Country": "country",
    "Subregion": "subregion",
    "Region": "region",
    "Location": "location",
    "Origin": "origin",
    "Associated Types": "associated_types",
    "OFDA/BHA Response": "ofda_response",
    "Appeal": "appeal",
    "Declaration": "declaration",
    "AID Contribution ('000 US$)": "aid_contribution",
    "Magnitude": "magnitude",
    "Magnitude Scale": "magnitude_scale",
    "Latitude": "latitude",
    "Longitude": "longitude",
    "River Basin": "river_basin",
    "Start Year": "start_year",
    "Start Month": "start_month",
    "Start Day": "start_day",
    "End Year": "end_year",
    "End Month": "end_month",
    "End Day": "end_day",
    "Total Deaths": "total_deaths",
    "No. Injured": "no_injured",
    "No. Affected": "no_affected",
    "No. Homeless": "no_homeless",
    "Total Affected": "total_affected",
    "Reconstruction Costs ('000 US$)": "reconstr_dam",
    "Reconstruction Costs, Adjusted ('000 US$)": "reconstr_dam_adj",
    "Insured Damage ('000 US$)": "insur_dam",
    "Insured Damage, Adjusted ('000 US$)": "insur_dam_adj",
    "Total Damage ('000 US$)": "total_dam",
    "Total Damage, Adjusted ('000 US$)": "total_dam_adj",
    "CPI": "cpi",
    "Admin Units": "admin_units",
    "GADM Admin Units": "gadm_admin_units",
    "Entry Date": "entry_date",
    "Last Update": "last_update",
}

#: API field name to Excel column name.
API_TO_EXCEL: dict = {v: k for k, v in COLUMN_MAP.items()}

#: API fields with no Excel counterpart; strict=True rejects them.
API_ONLY_FIELDS: tuple = (
    "external_ids_dict",
    "associated_types_list",
    "region_code",
    "subregion_code",
)

#: Columns stored as Yes/No strings in Excel but returned as booleans.
YES_NO_COLUMNS: tuple = (
    "Historic",
    "OFDA/BHA Response",
    "Appeal",
    "Declaration",
)

#: Columns holding a JSON string in Excel but returned parsed by the API.
JSON_COLUMNS: tuple = ("Admin Units", "GADM Admin Units")

#: Columns parsed as timestamps when reading the Excel file.
DATE_COLUMNS: tuple = ("Entry Date", "Last Update")

#: Name of the schema index.
INDEX_NAME: str = "DisNo."


def to_yes_no(value: Any) -> Any:
    """Map a boolean-like API value onto the Excel Yes/No convention.

    Idempotent: values already reading Yes or No pass through unchanged, so
    the conversion is safe to apply to data of either origin. Values that are
    neither boolean-like nor recognised are returned untouched, leaving
    `check_yes_no` to report them.

    Parameters
    ----------
    value : Any
        Value to convert.

    Returns
    -------
    Any
        Yes, No, pd.NA for nulls, or the input unchanged.
    """
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return pd.NA
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, str):
        lowered = value.strip().lower()
        if lowered in {"yes", "true", "1"}:
            return "Yes"
        if lowered in {"no", "false", "0"}:
            return "No"
        return value
    if isinstance(value, (int, float)):
        return "Yes" if value else "No"
    return value


def to_json_string(value: Any) -> Any:
    """Serialise a parsed admin-units value to the Excel JSON string form.

    An empty collection is treated as missing, matching the Excel export where
    an event with no geocoded admin unit leaves the cell blank.

    Parameters
    ----------
    value : Any
        Parsed admin units, a JSON string, or a null.

    Returns
    -------
    Any
        A JSON string, pd.NA, or the input unchanged.
    """
    if value is None:
        return pd.NA
    if isinstance(value, float) and pd.isna(value):
        return pd.NA
    if isinstance(value, str):
        return value if value.strip() else pd.NA
    if isinstance(value, (list, tuple)):
        return json.dumps(list(value)) if len(value) else pd.NA
    if isinstance(value, dict):
        return json.dumps(value) if value else pd.NA
    return value


def api_to_emtest(
        df: pd.DataFrame,
        schema: Optional[Any] = None
) -> pd.DataFrame:
    """Convert an EM-DAT API response to the layout the schema expects.

    Six differences are reconciled: API-only fields are dropped, fields are
    renamed to the Excel headers, boolean flags become Yes/No, parsed admin
    units are re-serialised to JSON strings, date strings become timestamps,
    and the frame is indexed on DisNo. and ordered to match the schema.

    Values are never repaired. Nulls in non-nullable columns, out-of-range
    numbers and unknown reference values reach the validation report as
    genuine findings.

    Parameters
    ----------
    df : pandas.DataFrame
        Records as returned by the EM-DAT GraphQL API, one row per event,
        using API field names. Every field in API_TO_EXCEL must be present;
        querying the API for all fields guarantees this.
    schema : pandera.DataFrameSchema, optional
        Schema whose column order to target. Defaults to `emdat_schema`.
        Reading the order from the schema keeps the adapter correct as the
        schema evolves.

    Returns
    -------
    pandas.DataFrame
        Indexed by DisNo., carrying exactly the schema columns in schema
        order.

    Raises
    ------
    KeyError
        If the response lacks fields the schema requires.
    """
    if schema is None:
        from emtest.validation_schemas import emdat_schema as schema

    out = df.copy()

    # API-only fields have no Excel counterpart and strict=True rejects them.
    out = out.drop(columns=[c for c in API_ONLY_FIELDS if c in out.columns])

    out = out.rename(columns=API_TO_EXCEL)

    expected = [INDEX_NAME] + list(schema.columns.keys())
    missing = [c for c in expected if c not in out.columns]
    if missing:
        raise KeyError(
            "API response is missing fields required by the EM-TEST schema: "
            "{}. Query the API for all fields.".format(missing)
        )

    for col in YES_NO_COLUMNS:
        out[col] = out[col].map(to_yes_no)

    for col in JSON_COLUMNS:
        out[col] = out[col].map(to_json_string)

    for col in DATE_COLUMNS:
        out[col] = pd.to_datetime(out[col], errors="coerce")

    out = out.set_index(INDEX_NAME)
    out = out[list(schema.columns.keys())]

    return out
