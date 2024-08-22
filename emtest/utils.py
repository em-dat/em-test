import copy
import pandas as pd
from pandera import DataFrameSchema, Check
from pandera.errors import SchemaErrors


def get_validation_report(
        df: pd.DataFrame,
        schema: DataFrameSchema,
        add_warnings: bool = False,
) -> pd.DataFrame | None:
    """Return schema errors as a dataframe report"""
    if add_warnings:
        schema = set_warnings_to_errors(schema)
    try:
        schema.validate(df, lazy=True)
    except SchemaErrors as e:
        return e.failure_cases


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
