"""Basic Streamlit UI for the Data Quality Agent."""

from __future__ import annotations

import streamlit as st
import pandas as pd

from data_quality_agent.profiling.profiler import profile_dataframe

st.title("Data Quality Agent")

uploaded = st.file_uploader("Upload CSV", type="csv")
if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.write(df.head())
    profile = profile_dataframe(df)
    st.json(profile)
