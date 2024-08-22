"""EM-DAT pandera validation schema

A pandera scheme to validate EM-DAT public table structure, types, and
constraints.

#Authors: Damien Delforge, Valentin Wathelet
#Email: damien.delforge@uclouvain.be
"""
import warnings
from datetime import datetime

from pandera import Check, Column, DataFrameSchema, Index, Timestamp

from .custom_checks import (
    is_valid_json,
    validate_external_id,
    validate_iso3_code
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
from .utils import update_column_checks

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
                    description="Test whether value is either 'Yes' or 'No'"
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
                    description="Test whether value is either 'Yes' or 'No'"
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
                    description="Test whether value is either 'Yes' or 'No'"
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
                    description="Test whether value is either 'Yes' or 'No'"
                )
            ]
        ),
        "AID Contribution ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(
                    0.,
                    description="Test whether value is greater than 0"
                )
            ],
            nullable=True
        ),
        "Magnitude": Column(
            float,
            checks=[
                Check.not_equal_to(
                    0.,
                    description="Test whether value differ from 0"
                )
            ],
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
                    -90., 90.,
                    description="Test whether value is within range -90-90.",
                )
            ],
            nullable=True
        ),
        "Longitude": Column(
            float,
            checks=[
                Check.in_range(-180., 180.)
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
                                f"1900-{CURRENT_YEAR}."
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
                                "(1-12)."
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
                                "(1-31)."
                )
            ],
            nullable=True
        ),
        "End Year": Column(
            int,
            checks=[
                Check.in_range(1900, CURRENT_YEAR)
            ]
        ),
        "End Month": Column(
            float,  # int is not a nullable type
            checks=[
                Check.isin(
                    range(1, 13),
                    name="check_month",
                    description="Test whether value is a valid month number "
                                "(1-31)."
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
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "No. Injured": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "No. Affected": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "No. Homeless": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "Total Affected": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "Reconstruction Costs ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "Reconstruction Costs, Adjusted ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "Insured Damage ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "Insured Damage, Adjusted ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "Total Damage ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "Total Damage, Adjusted ('000 US$)": Column(
            float,
            checks=[
                Check.greater_than(0.)
            ],
            nullable=True
        ),
        "CPI": Column(
            float,
            checks=[
                Check.in_range(0., 100.)
            ],
            nullable=True
        ),
        "Admin Units": Column(
            str,
            checks=[
                # See custom_checks.py
                Check(
                    is_valid_json,
                    name="is_valid_json",
                    description="Test whether value is a json string.",
                    error="Invalid JSON string",
                    element_wise=True
                )
            ],
            nullable=True
        ),
        "Entry Date": Column(
            Timestamp,
            checks=[
                Check.in_range(EMDAT_START_DATE, CURRENT_DATE)
            ]
        ),
        "Last Update": Column(
            Timestamp,
            checks=[
                Check.in_range(EMDAT_START_DATE, CURRENT_DATE)
            ]
        ),
    },
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
    strict=True
)

# Type-specific schema
# --------------------

# Earthquake Magnitude Check

earthquake_schema = update_column_checks(
    schema=emdat_schema,
    col_name='Magnitude',
    new_checks=[
        Check.in_range(
            min_value=3,
            max_value=10,
            description="Test whether value is between 3 and 10",
            name="check_earthquake_magnitude",
            error="Invalid earthquake magnitude"
        )
    ]
)
