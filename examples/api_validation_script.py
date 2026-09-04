"""Example API Validation Script

Validates a year of EM-DAT data pulled from the GraphQL API, as a counterpart
to validation_script.py which reads the public Excel download.

Records are selected on the Start Year field, not on the year embedded in the
DisNo. The two legitimately differ when an official start date is revised after
the identifier is assigned; EM-TEST reports that divergence as a warning.

Fetching is left to the caller so that EM-TEST itself stays free of any API
client dependency. The fetch below is a minimal, self-contained client built on
the standard library: it issues one GraphQL query and returns one row per
event, keyed by API field name. Any client returning that shape will do.

Requires an EM-DAT API key in the EMDAT_API_KEY environment variable. The API
is not public: access is reserved to authorized users and requests for access
are currently closed.

Author: Damien Delforge
Email: damien.delforge@uclouvain.be
License: MIT
"""

import json
import os
import urllib.error
import urllib.request

import pandas as pd

YEAR: int = 2025
CSV_OUTPUT_NAME: str = 'emdat_api_test_failure.csv'

API_URL: str = 'https://api.emdat.be/v1'
API_KEY_ENV: str = 'EMDAT_API_KEY'
TIMEOUT: int = 300

#: include_hist disables a server-side filter; it does not add pre-2000 data to
#: a recent-year query. Leaving it off would silently drop any record carrying a
#: wrongly set Historic flag, hiding the very defect validation is meant to
#: surface. cursor limit -1 disables the default pagination.
QUERY_TEMPLATE: str = """query emtest_validation {{
  public_emdat(
    filters: {{ from: {year}, to: {year}, include_hist: true }}
    cursor: {{ limit: -1 }}
  ) {{
    total_available
    data {{
      {fields}
    }}
  }}
}}"""


def run_query(query: str) -> dict:
    """Send one GraphQL query to the EM-DAT API and return its payload.

    Parameters
    ----------
    query : str
        GraphQL query string.

    Returns
    -------
    dict
        The `public_emdat` object of the response.

    Raises
    ------
    RuntimeError
        If the API key is missing, the request fails, or the API reports
        GraphQL errors.
    """
    api_key = os.environ.get(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(
            f'{API_KEY_ENV} is not set. The EM-DAT API is restricted to '
            f'authorized users; validate the public Excel download with '
            f'validation_script.py instead.'
        )

    request = urllib.request.Request(
        API_URL,
        data=json.dumps({'query': query}).encode('utf-8'),
        headers={
            'Authorization': api_key,
            'Content-Type': 'application/json',
        },
        method='GET',
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        detail = 'check your API key' if exc.code == 401 else exc.reason
        raise RuntimeError(
            f'EM-DAT API returned HTTP {exc.code}: {detail}'
        ) from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f'Could not reach {API_URL}: {exc.reason}') from exc

    if payload.get('errors'):
        raise RuntimeError(f'EM-DAT API returned errors: {payload["errors"]}')

    return payload['data']['public_emdat']


def fetch_emdat(year: int = YEAR) -> pd.DataFrame:
    """Fetch every record whose start year equals the given year.

    The requested fields are read from the adapter's COLUMN_MAP, so the query
    asks for exactly what api_to_excel_layout needs and stays correct if the
    mapping changes. API-only fields are not requested: the adapter drops them
    anyway.

    Parameters
    ----------
    year : int, optional
        Start year to select on. Defaults to YEAR.

    Returns
    -------
    pandas.DataFrame
        One row per event, using API field names.
    """
    from emtest.adapters import COLUMN_MAP

    query = QUERY_TEMPLATE.format(
        year=year,
        fields='\n      '.join(COLUMN_MAP.values()),
    )
    result = run_query(query)

    # Passing columns keeps the frame well shaped when a year returns no
    # record; GraphQL returns every requested field, null included, so it
    # never hides a field the response actually carried.
    df = pd.DataFrame(result['data'], columns=list(COLUMN_MAP.values()))

    available = result.get('total_available')
    if available is not None and len(df) != available:
        raise RuntimeError(
            f'Incomplete pull: {len(df)} of {available} records returned. '
            f'Validating a truncated dataset would misreport coverage.'
        )

    return df


def main() -> None:
    from emtest import (
        emdat_schema,
        api_to_excel_layout
    )
    from emtest.utils import get_validation_report

    emdat = api_to_excel_layout(fetch_emdat())
    emdat_report = get_validation_report(emdat, emdat_schema, add_warnings=True)

    if emdat_report is not None:
        emdat_report.to_csv(CSV_OUTPUT_NAME)
        print(f'{len(emdat_report)} failure case(s) written to '
              f'{CSV_OUTPUT_NAME}')
    else:
        print(f'All {len(emdat)} records passed validation.')


if __name__ == '__main__':
    main()
