"""Contains custom checks used in the validation schema.
"""

import json
import re
from typing import Any

import pandas as pd
from pandera.typing import Series


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


def validate_iso3_code(iso3_country_code: Series[str]) -> Series[bool]:
    """Validate ISO3 code using regular expression.
    """
    return iso3_country_code.str.match(r'^[A-Z]{3}$')


# def validate_earthquake_magnitude_(df: pd.DataFrame) -> Series[bool]:
#     valid = pd.Series([True] * len(df), index=df.index)
#     is_earthquake = df['Disaster Type'] == 'Earthquake'
#     magnitude_check = (df[is_earthquake]['Magnitude'].between(3, 10) &
#                        (~df[is_earthquake]['Magnitude'].isna()))
#     valid.loc[is_earthquake] = magnitude_check
#     return valid


def validate_earthquake_magnitude(data: pd.DataFrame) -> bool:
    earthquake_data = data[data['Disaster Type'] == 'Earthquake']
    # Check if all Magnitude values for Earthquakes are within specified range
    if not earthquake_data['Magnitude'].between(3, 10).all():
        return False
    return True
