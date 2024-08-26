"""Example Validation Script

Author: Damien Delforge
Email: damien.delforge@uclouvain.be
Date: 24-08-22
License: MIT

"""
import pandas as pd


EMDAT_PATH: str = 'data/fake_emdat_test.xlsx' #
CSV_OUTPUT_NAME: str = 'emdat_test_failure.csv'


def load_emdat(emdat_path: str = EMDAT_PATH) -> pd.DataFrame:
    df = pd.read_excel(
        emdat_path,
        index_col='DisNo.',
        parse_dates=['Entry Date', 'Last Update']
    )
    return df


def main() -> None:

    from emtest import (
        emdat_schema
    )
    from emtest.utils import get_validation_report

    emdat = load_emdat()
    emdat_report = get_validation_report(emdat, emdat_schema, add_warnings=True)

    if emdat_report is not None:
        emdat_report.to_csv(CSV_OUTPUT_NAME)


if __name__ == '__main__':
    main()
