"""Minimal FastAPI application exposing data quality features."""

from __future__ import annotations

from fastapi import FastAPI, UploadFile, File
import pandas as pd

from data_quality_agent.ingestion.ingestion import read_csv
from data_quality_agent.profiling.profiler import profile_dataframe

app = FastAPI(title="Data Quality Agent")

datasets: dict[str, pd.DataFrame] = {}


@app.post("/upload")
async def upload_dataset(file: UploadFile = File(...)) -> dict[str, str]:
    content = await file.read()
    df = pd.read_csv(pd.io.common.BytesIO(content))
    datasets[file.filename] = df
    return {"status": "uploaded", "name": file.filename}


@app.get("/profile/{name}")
def get_profile(name: str) -> dict:
    df = datasets.get(name)
    if df is None:
        return {"error": "dataset not found"}
    return profile_dataframe(df)
