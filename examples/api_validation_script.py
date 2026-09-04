"""Example API Validation Script

Validates a year of EM-DAT data pulled from the GraphQL API, as a counterpart
to validation_script.py which reads the public Excel download.

Records are selected on the Start Year field, not on the year embedded in the
DisNo. The two legitimately differ when an official start date is revised after
the identifier is assigned; EM-TEST reports that divergence as a warning.

Fetching is left to the caller so that EM-TEST itself stays free of any API
client dependency. The fetch below uses empy (https://github.com/dadelforge/empy)
and expects EMDAT_API_KEY in the environment; any client returning one row per
event with API field names will do.

Author: Damien Delforge
Email: damien.delforge@uclouvain.be
License: MIT
"""

import pandas as pd

YEAR: int = 2025
CSV_OUTPUT_NAME: str = 'emdat_api_test_failure.csv'


def fetch_emdat(year: int = YEAR) -> pd.DataFrame:
    """Fetch every record whose start year equals the given year.

    include_historical=True disables a server-side filter; it does not add
    pre-2000 data to a recent-year query. Leaving it off would silently drop
    any record carrying a wrongly set Historic flag, hiding the very defect
    validation is meant to surface.
    """
    import empy

    client = empy.EMDATClient()
    return client.get_disasters(
        from_year=year,
        to_year=year,
        fields='all',
        include_historical=True,
    )


def main() -> None:
    from emtest import (
        emdat_schema,
        api_to_emtest
    )
    from emtest.utils import get_validation_report

    emdat = api_to_emtest(fetch_emdat())
    emdat_report = get_validation_report(emdat, emdat_schema, add_warnings=True)

    if emdat_report is not None:
        emdat_report.to_csv(CSV_OUTPUT_NAME)
        print(f'{len(emdat_report)} failure case(s) written to '
              f'{CSV_OUTPUT_NAME}')
    else:
        print(f'All {len(emdat)} records passed validation.')


if __name__ == '__main__':
    main()
