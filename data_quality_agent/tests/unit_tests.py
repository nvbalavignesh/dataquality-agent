"""Basic unit tests for the scaffolding."""

import pytest

pytest.importorskip("pandas")

from data_quality_agent.ingestion import ingestion
from data_quality_agent.profiling import profiler


def test_ingestion_csv(tmp_path):
    pytest.importorskip("pandas")

    csv = tmp_path / "sample.csv"
    csv.write_text("a,b\n1,2\n3,4")
    df = ingestion.read_csv(str(csv))
    assert len(df) == 2


def test_profile():
    pd = pytest.importorskip("pandas")

    df = pd.DataFrame({"a": [1, 2, 3]})
    profile = profiler.profile_dataframe(df)
    assert profile["a"]["null_count"] == 0
