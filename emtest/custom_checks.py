"""Contains custom checks used in the validation schema.
"""

import json
import re
from typing import Any, Literal

import pandas as pd
from pandera.typing import Series

from .validation_data.areas import ADM1_GAUL_LIST, ADM2_GAUL_LIST


# Single Checks
# -------------

def check_disno_vs_start_year(start_year: Series[int]) -> Series[bool]:
    """Check that disno year is the same as start year."""

    def disno_to_year(disno: str) -> int:
        try:
            disno_year = int(disno[:4])
        except ValueError:
            disno_year = 0
        return disno_year

    disno = pd.Series(start_year.index)
    disno_year = disno.apply(lambda x: disno_to_year(x))
    disno_year.index = disno
    return disno_year == start_year


def validate_external_id(external_id: str | None) -> bool:
    """Validates external ID regex patterns.
    """
    glide_pattern = r"GLIDE:[A-Z]{2}-\d{4}-\d{6}"
    usgs_pattern = r"USGS:[0-9a-zA-Z]{10}"
    dfo_pattern = r"DFO:\d{4}"
    if external_id != external_id:  # Skip NaN
        return True
    ids = external_id.split("|")
    valid = False
    for id_ in ids:
        if (
                re.match(glide_pattern, id_) or
                re.match(usgs_pattern, id_) or
                re.match(dfo_pattern, id_)
        ):
            valid |= bool(
                re.match(glide_pattern, id_) or
                re.match(usgs_pattern, id_) or
                re.match(dfo_pattern, id_)
            )
    return valid


def is_valid_json(json_data: Any) -> bool:
    """Check if the provided string is a valid JSON.

    Parameters
    ----------
    json_data : Any
        The JSON string to be validated.

    Returns
    -------
    bool
        True if json_data is a valid JSON string, False otherwise.
    """
    if isinstance(json_data, float) and pd.isna(json_data):
        return False
    elif not isinstance(json_data, (str, bytes, bytearray)):
        return False

    try:
        json.loads(json_data)
        return True
    except json.JSONDecodeError:
        return False


def has_valid_GAUL_codes(json_data: Any) -> bool:
    """Check if GAUL codes are valid."""
    if isinstance(json_data, float) and pd.isna(json_data):
        return False
    elif not isinstance(json_data, (str, bytes, bytearray)):
        return False
    try:
        admin_units = json.loads(json_data)
        code_list: list[tuple[int, int]] = [_extract_GAUL_code(d) for d in
                                            admin_units]
        all_code_valid = all(
            [_is_valid_GAUL_code(code, level) for level, code in code_list]
        )
        return all_code_valid
    except json.JSONDecodeError:
        return False


def validate_iso3_code(iso3_country_code: Series[str]) -> Series[bool]:
    """Validate ISO3 code using regular expression.
    """
    return iso3_country_code.str.match(r'^[A-Z]{3}$')


# Wide Checks
# -----------

def check_both_lat_lon_coordinates(df: pd.DataFrame) -> Series[bool]:
    """Check that latitude and longitude are both defined or undefined"""
    lat_defined = df['Latitude'].notnull()
    lon_defined = df['Longitude'].notnull()
    return lat_defined == lon_defined


def check_coldwave_magnitude(df: pd.DataFrame) -> Series[bool]:
    """Check that cold wave is in realistic range"""
    is_coldwave = df['Disaster Subtype'] == 'Cold wave'
    in_mag_range = df['Magnitude'].le(10)
    return ~is_coldwave | in_mag_range


def check_earthquake_magnitude(df: pd.DataFrame) -> Series[bool]:
    """Check that earthquake is in realistic range"""
    is_earthquake = df['Disaster Type'] == 'Earthquake'
    in_mag_range = df['Magnitude'].between(3, 10)
    return ~is_earthquake | in_mag_range


def check_heatwave_magnitude(df: pd.DataFrame) -> Series[bool]:
    """Check that heat wave is in realistic range"""
    is_heatwave = df['Disaster Subtype'] == 'Heat wave'
    in_mag_range = df['Magnitude'].ge(25)
    return ~is_heatwave | in_mag_range


def check_other_magnitude(df: pd.DataFrame) -> Series[bool]:
    """Check that heat wave is in realistic range"""
    is_other = ~((df['Classification Key'].str.startswith('nat-geo-ear')) |
                (df['Classification Key'].str.startswith('nat-met-ext')))
    return ~is_other | df['Magnitude'] > 0


def check_no_day_if_no_month(
        df: pd.DataFrame,
        start_or_end: Literal['Start', 'End'],
) -> Series[bool]:
    """Check that day are null if month is null"""
    day_defined = df[f'{start_or_end} Day'].notnull()
    month_defined = df[f'{start_or_end} Month'].notnull()
    day_if_month = (~day_defined | month_defined)

    return day_if_month


def check_start_end_consistency(
        df: pd.DataFrame,
        resolution: Literal['year', 'month', 'day'],
) -> Series[bool]:
    """Check start and end dates correct chronology"""
    date_start = _convert_to_date(df, 'Start', resolution)
    date_end = _convert_to_date(df, 'End', resolution)
    return (date_start <= date_end) | pd.isna(date_start) | pd.isna(date_end)


def _convert_to_date(
        df: pd.DataFrame,
        start_or_end: Literal['Start', 'End'],
        resolution: Literal['year', 'month', 'day']
) -> Series:
    def float_to_string(x):
        if x != x:
            return '00'
        else:
            return str(int(x)).zfill(2)

    if resolution == 'day':
        return pd.to_datetime(
            df[f'{start_or_end} Year'].astype(str) +
            df[f'{start_or_end} Month'].apply(float_to_string) +
            df[f'{start_or_end} Day'].apply(float_to_string),
            format='%Y%m%d',
            errors='coerce'
        )
    elif resolution == 'month':
        return pd.to_datetime(
            df[f'{start_or_end} Year'].astype(str) +
            df[f'{start_or_end} Month'].apply(float_to_string),
            format='%Y%m',
            errors='coerce'
        )
    elif resolution == 'year':
        return pd.to_datetime(df[f'{start_or_end} Year'], format='%Y')


def _extract_GAUL_code(d: dict) -> tuple[int, int]:
    """Extract GAUL code from dictionary."""
    level: int = int(list(d.keys())[0][3])
    code_key: str = f"adm{level}_code"
    code_value: int = int(d[code_key])
    return level, code_value


def _is_valid_GAUL_code(code: int, level=Literal[1, 2]) -> bool:
    """Check if code is a valid GAUL code."""
    if level == 1:
        return code in ADM1_GAUL_LIST
    elif level == 2:
        return code in ADM2_GAUL_LIST
