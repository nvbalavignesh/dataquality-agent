"""Simple anomaly detection utilities."""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd
from sklearn.ensemble import IsolationForest


class AnomalyDetector:
    """Detect numeric anomalies using Isolation Forest."""

    def __init__(self, contamination: float = 0.05) -> None:
        self.model = IsolationForest(contamination=contamination, random_state=42)

    def fit(self, df: pd.DataFrame) -> None:
        numeric_df = df.select_dtypes(include="number")
        if numeric_df.empty:
            raise ValueError("No numeric columns to fit anomaly detector")
        self.model.fit(numeric_df)

    def score(self, df: pd.DataFrame) -> pd.Series:
        numeric_df = df.select_dtypes(include="number")
        scores = -self.model.decision_function(numeric_df)
        return pd.Series(scores, index=df.index, name="anomaly_score")

    def detect(self, df: pd.DataFrame, threshold: float = 0.5) -> pd.DataFrame:
        scores = self.score(df)
        anomalies = df[scores > threshold].copy()
        anomalies["anomaly_score"] = scores[scores > threshold]
        return anomalies


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect anomalies in a dataset")
    parser.add_argument("file", help="CSV file containing numeric columns")
    args = parser.parse_args()

    data = pd.read_csv(args.file)
    detector = AnomalyDetector()
    detector.fit(data)
    result = detector.detect(data)
    print(result.head())
