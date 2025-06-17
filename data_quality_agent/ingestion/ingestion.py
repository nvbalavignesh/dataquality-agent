"""Dataset ingestion utilities.

This module provides functions to read datasets from various
sources including CSV files, Parquet files and SQL tables.
"""

from __future__ import annotations

import pandas as pd
from sqlalchemy import create_engine


def read_csv(path: str, **kwargs) -> pd.DataFrame:
    """Load a dataset from a CSV file."""
    return pd.read_csv(path, **kwargs)


def read_parquet(path: str, **kwargs) -> pd.DataFrame:
    """Load a dataset from a Parquet file."""
    return pd.read_parquet(path, **kwargs)


def read_sql_table(connection_string: str, table_name: str, **kwargs) -> pd.DataFrame:
    """Load a dataset from a SQL table.

    Parameters
    ----------
    connection_string:
        SQLAlchemy-compatible database connection string.
    table_name:
        Name of the table to read.
    """
    engine = create_engine(connection_string)
    with engine.begin() as connection:
        df = pd.read_sql_table(table_name, connection, **kwargs)
    return df


def read_dataset(source: str, fmt: str | None = None, **kwargs) -> pd.DataFrame:
    """Generic dataset reader.

    Parameters
    ----------
    source:
        File path or identifier for the dataset.
    fmt:
        Format of the dataset. If not provided, it will be inferred
        from the source file extension when possible. Supported values
        are ``csv``, ``parquet`` and ``sql``.

    Returns
    -------
    :class:`pandas.DataFrame`
    """
    if fmt is None:
        if source.endswith(".csv"):
            fmt = "csv"
        elif source.endswith(".parquet"):
            fmt = "parquet"

    if fmt == "csv":
        return read_csv(source, **kwargs)
    if fmt == "parquet":
        return read_parquet(source, **kwargs)
    if fmt == "sql":
        connection_string = kwargs.get("connection_string")
        table_name = kwargs.get("table_name")
        if not connection_string or not table_name:
            raise ValueError(
                "For SQL sources, `connection_string` and `table_name` must be provided"
            )
        return read_sql_table(connection_string, table_name, **kwargs)

    raise ValueError(f"Unsupported format: {fmt}")


if __name__ == "__main__":
    # Sample usage
    import argparse

    parser = argparse.ArgumentParser(description="Dataset ingestion example")
    parser.add_argument("source", help="Path to dataset or SQL identifier")
    parser.add_argument(
        "--fmt",
        choices=["csv", "parquet", "sql"],
        help="Format of the dataset if it cannot be inferred",
    )
    parser.add_argument("--table", help="SQL table name, if reading from a database")
    parser.add_argument(
        "--conn", help="SQLAlchemy connection string, if reading from a database"
    )
    args = parser.parse_args()

    df = read_dataset(
        args.source,
        fmt=args.fmt,
        connection_string=args.conn,
        table_name=args.table,
    )
    print(df.head())

