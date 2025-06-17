"""Dataset profiling utilities."""

from __future__ import annotations

import re
from collections import Counter
from typing import Any, Dict

import numpy as np
import pandas as pd


def _detect_regex_pattern(series: pd.Series) -> str | None:
    """Attempt to infer a simple regex pattern for a column."""
    if series.empty:
        return None

    non_null = series.dropna().astype(str)
    if non_null.empty:
        return None

    patterns = [
        (r"^\d+$", "numeric"),
        (r"^[a-zA-Z]+$", "alpha"),
        (r"^[a-zA-Z0-9]+$", "alphanumeric"),
        (r"^[0-9a-fA-F]+$", "hex"),
    ]
    for regex, _ in patterns:
        if non_null.str.match(regex).all():
            return regex
    return None


def profile_dataframe(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Compute basic profiling metrics for a DataFrame."""
    results: Dict[str, Dict[str, Any]] = {}
    row_count = len(df)

    for col in df.columns:
        series = df[col]
        metrics: Dict[str, Any] = {}
        metrics["null_count"] = int(series.isna().sum())
        metrics["null_percentage"] = float(series.isna().mean() * 100)
        metrics["unique_count"] = int(series.nunique(dropna=True))

        if pd.api.types.is_numeric_dtype(series):
            metrics["min"] = series.min()
            metrics["max"] = series.max()
            metrics["distribution"] = (
                series.value_counts(dropna=True).head(10).to_dict()
            )
        else:
            metrics["distribution"] = (
                series.astype(str).value_counts(dropna=True).head(10).to_dict()
            )
            regex = _detect_regex_pattern(series)
            if regex:
                metrics["regex_pattern"] = regex

        results[col] = metrics

    results["__row_count__"] = row_count
    return results


if __name__ == "__main__":
    # Example usage
    import argparse

    parser = argparse.ArgumentParser(description="Dataset profiling example")
    parser.add_argument("file", help="Path to a CSV or Parquet file to profile")
    args = parser.parse_args()

    df = pd.read_csv(args.file) if args.file.endswith(".csv") else pd.read_parquet(args.file)
    profile = profile_dataframe(df)
    for col, metrics in profile.items():
        if col == "__row_count__":
            continue
        print(f"Column: {col}")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
        print()

