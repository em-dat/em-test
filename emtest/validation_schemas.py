"""EM-DAT pandera validation schema

A pandera scheme to validate EM-DAT public table structure, types, and
constraints.

#Authors: Damien Delforge, Valentin Wathelet
#Email: damien.delforge@uclouvain.be
"""
from datetime import datetime
from functools import partial

from pandera import Check, Column, DataFrameSchema, Index, Timestamp

from .custom_checks import (
    is_valid_json,
    has_valid_GAUL_codes,
    validate_external_id,
    validate_iso3_code,
    check_both_lat_lon_coordinates,
    check_disno_vs_start_year,
    check_start_end_consistency,
    check_coldwave_magnitude,
    check_earthquake_magnitude,
    check_heatwave_magnitude,
    check_other_magnitude,
    check_no_day_if_no_month
)
from .validation_data.areas import (
    COUNTRY_LIST,
    ISO3_LIST,
    REGION_LIST,
    SUBREGION_LIST
)
from .validation_data.classification import (
    KEY_LIST,
    GROUP_LIST,
    SUBGROUP_LIST,
    TYPE_LIST,
    SUBTYPE_LIST
)
from .validation_data.magnitude import MAG_UNIT_LIST

CURRENT_DATE = datetime.now()
CURRENT_YEAR = datetime.now().year
EMDAT_START_DATE = datetime(1988, 1, 1)

emdat_schema = DataFrameSchema(
    {
        "Historic": Column(
            str,
            checks=[
                # Should be either "Yes" or "No"
                Check.isin(
                    allowed_values=["Yes", "No"],
                    name='check_yes_no',
                    description="Test whether value is either 'Yes' or 'No'",
                    error="Invalid Historic value"
                )
            ]
        ),
        "Classification Key": Column(
            str,
            checks=[
                # Should belong to KEY_LIST
                Check.isin(
                    KEY_LIST,
                    name='check_classification_key',
                    description="Test whether value is in the reference list",
                    error="Invalid classification key"
                )
            ]
        ),
        "Disaster Group": Column(
            str,
            checks=[
                # Should belong to GROUP_LIST
                Check.isin(
                    GROUP_LIST,
                    name='check_goup',
                    description="Test whether value is in the reference list",
                    error="Invalid group name"
                )
            ]
        ),
        "Disaster Subgroup": Column(
            str,
            checks=[
                # Should belong to SUBGROUP_LIST
                Check.isin(
                    SUBGROUP_LIST,
                    name='check_subgroup',
                    description="Test whether value is in the reference list",
                    error="Invalid subgroup name"
                )
            ]
        ),
        "Disaster Type": Column(
            str,
            checks=[
                # Should belong to TYPE_LIST
                Check.isin(
                    TYPE_LIST,
                    name='check_type',
                    description="Test whether value is in the reference list",
                    error="Invalid type name"
                )
            ]
        ),
        "Disaster Subtype": Column(
            str,
            checks=[
                # Should belong to SUBTYPE_LIST
                Check.isin(
                    SUBTYPE_LIST,
                    name='check_subtype',
                    description="Test whether value is in the reference list",
                    error="Invalid subtype name"
                )
            ]
        ),
        "External IDs": Column(
            str,
            checks=[
                Check(
                    # See custom_checks.py
                    validate_external_id,
                    element_wise=True,
                    error="Invalid external ID",
                    description="Validate values using regular expressions"
                )
            ],
            nullable=True,
        ),
        "Event Name": Column(str, nullable=True),
        "ISO": Column(
            str,
            checks=[
                Check(
                    validate_iso3_code,
                    name='validate_iso3_code',
                    error="Invalid ISO3 code",
                    description="Validate values using regular expressions"
                ),
                Check.isin(
                    ISO3_LIST,
                    raise_warning=True,
                    name="check_iso3_code",
                    description="Test whether value is in the reference list",
                    error="ISO3 code not in reference list"
                )
            ]
        ),
        "Country": Column(
            str,
            checks=[
                # Should belong to COUNTRY_LIST
                Check.isin(
                    COUNTRY_LIST,
                    raise_warning=True,
                    name="check_country",
                    description="Test whether value is in the reference list",
                    error="Countries not in reference list"
                )
            ]
        ),
        "Subregion": Column(
            str,
            checks=[
                # Should belong to SUBREGION_LIST
                Check.isin(
                    SUBREGION_LIST,
                    name="check_subregion",
                    description="Test whether value is in the reference list",
                    error="Subregions not in reference list"
                )
            ]
        ),
        "Region": Column(
            str,
            checks=[
                # Should belong to REGION_LIST
                Check.isin(
                    REGION_LIST,
                    name="check_region",
                    description="Test whether value is in the reference list",
                    error="Regions not in reference list"
                )
            ]
        ),
        "Location": Column(str, nullable=True),
        "Origin": Column(str, nullable=True),
        "Associated Types": Column(str, nullable=True),
        "OFDA/BHA Response": Column(
            str,
            checks=[
                # Should be either "Yes" or "No"
                Check.isin(
                    ["Yes", "No"],
                    name="check_yes_no",
                    description="Test whether value is either 'Yes' or 'No'",
                    error="Invalid OFDA/BHA Response value"
                )
            ]
        ),
        "Appeal": Column(
            str,
            checks=[
                # Should be either "Yes" or "No"
                Check.isin(
                    ["Yes", "No"],
                    name="check_yes_no",
                    description="Test whether value is either 'Yes' or 'No'",
                    error="Invalid Appeal value"
                )
            ]
        ),
        "Declaration": Column(
            str,
            checks=[
                # Should be either "Yes" or "No"
                Check.isin(
                    ["Yes", "No"],
                    name="check_yes_no",
                    description="Test whether value is either 'Yes' or 'No'",
                    error="Invalid Declaration value"
                )
            ]
        ),
        "AID Contribution ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid AID Contribution value"
                )
            ],
            nullable=True
        ),
        "Magnitude": Column(
            float,
            nullable=True
        ),
        "Magnitude Scale": Column(
            str,
            checks=[
                Check.isin(
                    MAG_UNIT_LIST,
                    name="check_magnitude_unit",
                    description="Test whether value is in the reference list",
                    error="Magnitude unit not in reference list"
                )
            ],
            nullable=True
        ),
        "Latitude": Column(
            float,
            checks=[
                Check.in_range(
                    -90.,
                    90.,
                    description="Test whether value is within range -90-90",
                    error="Invalid Latitude value"
                )
            ],
            nullable=True
        ),
        "Longitude": Column(
            float,
            checks=[
                Check.in_range(
                    -180.,
                    180.,
                    description="Test whether value is within range -180-180",
                    error="Invalid Longitude value"
                )
            ],
            nullable=True
        ),
        "River Basin": Column(str, nullable=True),
        "Start Year": Column(
            int,
            checks=[
                Check.in_range(
                    1900,
                    CURRENT_YEAR,
                    description=f"Test whether value is within range "
                                f"1900-{CURRENT_YEAR}.",
                    error="Invalid Start Year value"
                ),
                Check(
                    check_disno_vs_start_year,
                    description=f"Test that start year is the same as disno "
                                f"year.",
                    error="Start year differs from DisNo year",
                    raise_warning=True
                )

            ]
        ),
        "Start Month": Column(
            float,  # int is not a nullable type
            nullable=True,
            checks=[
                Check.isin(
                    range(1, 13),
                    name="check_month",
                    description="Test whether value is a valid month number "
                                "(1-12).",
                    error="Invalid Start Month value"
                )
            ]
        ),
        "Start Day": Column(
            float,  # int is not a nullable type
            checks=[
                Check.isin(
                    range(1, 32),
                    name="check_day",
                    description="Test whether value is a valid day number "
                                "(1-31).",
                    error="Invalid Start Day value"
                )
            ],
            nullable=True
        ),
        "End Year": Column(
            int,
            checks=[
                Check.in_range(
                    1900,
                    CURRENT_YEAR,
                    description=f"Test whether value is within range "
                                f"1900-{CURRENT_YEAR}.",
                    error="Invalid End Year value"
                )
            ]
        ),
        "End Month": Column(
            float,  # int is not a nullable type
            checks=[
                Check.isin(
                    range(1, 13),
                    name="check_month",
                    description="Test whether value is a valid month number "
                                "(1-31).",
                    error="Invalid End Month value"
                )
            ],
            nullable=True
        ),
        "End Day": Column(
            float,  # int is not a nullable type
            checks=[
                Check.isin(
                    range(1, 32),
                    name="check_day",
                    description="Test whether value is a valid day number "
                                "(1-31)."
                )
            ],
            nullable=True
        ),
        "Total Deaths": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Total Deaths value"
                )
            ],
            nullable=True
        ),
        "No. Injured": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid No. Injured value"
                )
            ],
            nullable=True
        ),
        "No. Affected": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid No. Affected value"
                )
            ],
            nullable=True
        ),
        "No. Homeless": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid No. Homeless value"
                )
            ],
            nullable=True
        ),
        "Total Affected": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Total Affected value"
                )
            ],
            nullable=True
        ),
        "Reconstruction Costs ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Reconstruction Costs value"
                )
            ],
            nullable=True
        ),
        "Reconstruction Costs, Adjusted ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Reconstruction Costs, Adjusted value"
                )
            ],
            nullable=True
        ),
        "Insured Damage ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Insured Damage value"
                )
            ],
            nullable=True
        ),
        "Insured Damage, Adjusted ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Insured Damage, Adjusted value"
                )
            ],
            nullable=True
        ),
        "Total Damage ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Total Damage value"
                )
            ],
            nullable=True
        ),
        "Total Damage, Adjusted ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0",
                    error="Invalid Total Damage, Adjusted value"
                )
            ],
            nullable=True
        ),
        "CPI": Column(
            float,
            checks=[
                # CPI is rescaled to 100 each year. Above-100 values are
                # unlikely but possible in case of deflation.
                Check.in_range(
                    0.,
                    110.,
                    description="Test whether value is within range (1-110)",
                    error="Invalid CPI value",
                    raise_warning=True
                )
            ],
            nullable=True
        ),
        "Admin Units": Column(
            str,
            checks=[
                # See custom_checks.py
                Check(
                    is_valid_json,
                    description="Test whether value is a json string",
                    error="Invalid JSON string",
                    element_wise=True
                ),
                Check(
                    has_valid_GAUL_codes,
                    description="Test whether value contains valid GAUL codes",
                    error="Invalid GAUL codes",
                    element_wise=True
                )
            ],
            nullable=True
        ),
        "Entry Date": Column(
            Timestamp,
            checks=[
                Check.in_range(
                    EMDAT_START_DATE,
                    CURRENT_DATE,
                    description=f"Test whether value is within range "
                                f"1988-present",
                    error="Invalid Entry Date value",
                )
            ]
        ),
        "Last Update": Column(
            Timestamp,
            checks=[
                Check.in_range(
                    EMDAT_START_DATE,
                    CURRENT_DATE,
                    description=f"Test whether value is within range "
                                f"1988-present",
                    error="Invalid Last Update value",
                )
            ]
        ),
    },
    # Define checks at the DataFrameSchema-level
    # Note: error message should be unique to post-filter reports
    checks=[
        Check(
            check_both_lat_lon_coordinates,
            description="Test whether latitude and longitude coordinates are "
                        "either both defined or undefined",
            error="Missing latitude or longitude coordinates"
        ),
        Check(
            partial(check_no_day_if_no_month, start_or_end='Start'),
            name="check_no_start_day_if_no_month",
            description="Test whether Start Day is set if Start Month is not",
            error="Missing start month value"
        ),
        Check(
            partial(check_no_day_if_no_month, start_or_end='End'),
            name="check_no_end_day_if_no_month",
            description="Test whether End Day is set if End Month is not",
            error="Missing end month value"
        ),
        Check(
            partial(check_start_end_consistency, resolution='year'),
            name="check_start_end_year_consistency",
            description="Test whether start year is prior or equal to end year",
            error="Start date inconsistency at the year resolution"
        ),
        Check(
            partial(check_start_end_consistency, resolution='month'),
            description="Test whether start date is prior or equal to end date "
                        "at the month resolution",
            error="Start date inconsistency at the month resolution"
        ),
        Check(
            partial(check_start_end_consistency, resolution='day'),
            description="Test whether start date is prior or equal to end date "
                        "at the day resolution",
            error="Start date inconsistency at the day resolution"
        ),
        Check(
            check_coldwave_magnitude,
            description="Test whether coldwave magnitude is in realistic "
                        "range (<= 10°C)",
            error="Invalid coldwave magnitude"
        ),
        Check(
            check_earthquake_magnitude,
            description="Test whether earthquake magnitude is in realistic "
                        "range (3 to 10)",
            error="Invalid earthquake magnitude"
        ),
        Check(
            check_heatwave_magnitude,
            description="Test whether heatwave magnitude is in realistic "
                        "range (>= 25°C)",
            error="Invalid heatwave magnitude"
        ),
        Check(
            check_other_magnitude,
            description="Test whether disaster different from earthquake, cold "
                        " and heat waves have magnitude above zero",
            error="Invalid magnitude"
        ),

    ],
    # Check the index
    index=Index(
        str,
        name="DisNo.",
        checks=[
            # Check DisNo. pattern, e.g., "2004-0659-USA"
            Check.str_matches(
                r"^\d{4}-\d{4}-[A-Z]{3}$",
                name="check_disno",
                description="Validate value using regular expression.",
                error="Invalid DisNo. Pattern"
            )
        ],
        unique=True
    ),
    coerce=True,
    ordered=True,
    strict=True,
)
