import pytest
import pandas as pd

@pytest.fixture
def valid_emdat_row():
    """Provides a single valid EM-DAT row as a dictionary."""
    return {
        "Historic": "No",
        "Classification Key": "nat-bio-epi-vir",
        "Disaster Group": "Natural",
        "Disaster Subgroup": "Biological",
        "Disaster Type": "Epidemic",
        "Disaster Subtype": "Viral disease",
        "External IDs": None,
        "Event Name": "Test Event",
        "ISO": "BEL",
        "Country": "Belgium",
        "Subregion": "Western Europe",
        "Region": "Europe",
        "Location": "Brussels",
        "Origin": None,
        "Associated Types": None,
        "OFDA/BHA Response": "No",
        "Appeal": "No",
        "Declaration": "No",
        "AID Contribution ('000 US$)": None,
        "Magnitude": 7.0,
        "Magnitude Scale": "Moment Magnitude",
        "Latitude": 50.85,
        "Longitude": 4.35,
        "River Basin": None,
        "Start Year": 2024,
        "Start Month": 1.0,
        "Start Day": 1.0,
        "End Year": 2024,
        "End Month": 1.0,
        "End Day": 2.0,
        "Total Deaths": 1.0,
        "No. Injured": None,
        "No. Affected": None,
        "No. Homeless": None,
        "Total Affected": 1.0,
        "Reconstruction Costs ('000 US$)": None,
        "Reconstruction Costs, Adjusted ('000 US$)": None,
        "Insured Damage ('000 US$)": None,
        "Insured Damage, Adjusted ('000 US$)": None,
        "Total Damage ('000 US$)": None,
        "Total Damage, Adjusted ('000 US$)": None,
        "CPI": 100.0,
        "Admin Units": None,
        "GADM Admin Units": None,
        "Entry Date": pd.Timestamp("2024-01-01"),
        "Last Update": pd.Timestamp("2024-01-01")
    }

@pytest.fixture
def valid_df(valid_emdat_row):
    """Provides a valid EM-DAT DataFrame."""
    df = pd.DataFrame([valid_emdat_row])
    df.index = ["2024-0001-BEL"]
    df.index.name = "DisNo."
    return df
