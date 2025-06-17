# Data Quality Agent

This project contains a scaffold for an **AI-driven Data Quality Agent**. The
system is organized into modular components that can be extended to provide full
data ingestion, profiling, anomaly detection, rule generation, feedback capture,
and continuous learning.

## Project Structure

```
data_quality_agent/
├── ingestion/               # dataset loading utilities
├── profiling/               # dataframe profiling
├── anomalies/               # anomaly detection
├── rule_generation/         # LLM-based rule suggestion
├── feedback/                # store user feedback
├── continuous_learning/     # use feedback to improve rules
├── api/                     # FastAPI app exposing features
├── ui/                      # Streamlit or Gradio interface
├── models/                  # embeddings and vector store helpers
├── utils/                   # shared helpers
└── tests/                   # basic tests
```

Each folder contains a Python module with minimal working code and example
usage. See the individual modules for details.

## Quick Start

Install dependencies and run the example profiling flow:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python data_quality_agent/ingestion/ingestion.py sample_data.csv
python data_quality_agent/profiling/profiler.py sample_data.csv
```

The other modules provide placeholders for anomaly detection, rule generation,
feedback handling, continuous learning, and API/UI layers.
