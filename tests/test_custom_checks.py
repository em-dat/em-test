import pytest
import pandas as pd
from emtest.custom_checks import (
    is_valid_json, 
    _is_valid_GAUL_code, 
    check_disno,
    check_yes_no,
    check_disno_vs_start_year
)

def test_is_valid_json():
    assert is_valid_json('{"key": "value"}') is True
    assert is_valid_json('[1, 2, 3]') is True
    assert is_valid_json('invalid json') is False
    assert is_valid_json(None) is False

def test_is_valid_gaul_code():
    # We know from load_GAUL_code example it returns some codes
    # Let's assume some codes exist or just test the logic if we can
    assert _is_valid_GAUL_code(1232, level=1) is True # Based on example in data_loader
    assert _is_valid_GAUL_code(999999, level=1) is False

def test_check_disno():
    s = pd.Series(["2024-0001-BEL", "1900-9999-USA"])
    assert check_disno(s).all() == True
    
    s_invalid = pd.Series(["2024-001-BEL"]) # Missing one digit in sequential
    assert check_disno(s_invalid).all() == False

def test_check_yes_no():
    assert check_yes_no(pd.Series(["Yes", "No"])).all() == True
    assert check_yes_no(pd.Series(["Yes", "Maybe"])).all() == False

def test_check_disno_vs_start_year():
    df = pd.DataFrame({
        "Start Year": [2024, 2023]
    }, index=["2024-0001-BEL", "2024-0002-BEL"])
    df.index.name = "DisNo."
    
    # The check_disno_vs_start_year in custom_checks.py takes start_year Series
    # and accesses its index.
    result = check_disno_vs_start_year(df["Start Year"])
    assert result.iloc[0] == True
    assert result.iloc[1] == False
