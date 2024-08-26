import copy

import pandas as pd
from pandera import DataFrameSchema, Check
from pandera.errors import SchemaErrors

WIDE_CHECKS_TO_KEEP: dict[str, list[str]] = {
    'Missing latitude or longitude coordinates': ['Latitude', 'Longitude'],
    'Start date and end date inconsistency': ['Start Year'],
    'Invalid coldwave magnitude': ['Magnitude'],
    'Invalid earthquake magnitude': ['Magnitude'],
    'Invalid heatwave magnitude': ['Magnitude'],
    'Invalid magnitude': ['Magnitude'],
    'Missing start month value': ['Start Month', 'Start Day'],
    'Missing end month value': ['End Month', 'End Day'],
    'Start date inconsistency at the year resolution': ['Start Year'],
    'Start date inconsistency at the month resolution': ['Start Month'],
    'Start date inconsistency at the day resolution': ['Start Day']
}



def get_validation_report(
        df: pd.DataFrame,
        schema: DataFrameSchema,
        add_warnings: bool = False,
        deduplicate_wide: bool = True,
) -> pd.DataFrame | None:
    """Return schema errors as a dataframe report"""
    if add_warnings:
        schema = set_warnings_to_errors(schema)
    try:
        schema.validate(df, lazy=True)
    except SchemaErrors as e:
        report = e.failure_cases
        if deduplicate_wide:
            for error, column_to_keep in WIDE_CHECKS_TO_KEEP.items():
                report = deduplicate_errors(
                    report,
                    error_message=error,
                    keep_columns=column_to_keep
                )
        return report


def update_column_checks(
        schema: DataFrameSchema,
        col_name: str,
        new_checks: list[Check]
) -> DataFrameSchema:
    """Simplifies checks updates for a specific column"""
    new_schema = schema.update_columns({col_name: {"checks": new_checks}})
    return new_schema


def set_warnings_to_errors(schema: DataFrameSchema) -> DataFrameSchema:
    schema_copy = copy.deepcopy(schema)
    for col_name, col in schema.columns.items():
        for ix, check in enumerate(col.checks):
            if check.raise_warning is True:
                schema_copy.columns[col_name].checks[ix].raise_warning = False
    return schema_copy


def deduplicate_errors(
        report: pd.DataFrame,
        error_message: str,
        keep_columns: list[str]
) -> pd.DataFrame:
    index_to_drop = report[
        (report['check'] == error_message) &
        (~report['column'].isin(keep_columns))
        ].index
    return report.drop(index_to_drop)

