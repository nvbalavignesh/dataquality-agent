"""Generate data quality rules using an LLM."""

from __future__ import annotations

from typing import Dict

import pandas as pd

try:
    import openai
except ImportError:  # pragma: no cover - openai is optional for tests
    openai = None


class RuleGenerator:
    """Call an LLM to suggest data quality rules."""

    def __init__(self, model: str = "gpt-3.5-turbo") -> None:
        self.model = model

    def suggest(self, df: pd.DataFrame) -> Dict[str, str]:
        if openai is None:
            raise ImportError("openai package is required for rule generation")

        prompt = (
            "Suggest simple data quality checks for the following dataframe columns: "
            + ", ".join(df.columns)
        )
        response = openai.ChatCompletion.create(model=self.model, messages=[{"role": "user", "content": prompt}])
        message = response["choices"][0]["message"]["content"]
        return {"rules": message}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate rules for a dataset")
    parser.add_argument("file", help="CSV file to analyse")
    args = parser.parse_args()

    data = pd.read_csv(args.file)
    generator = RuleGenerator()
    print(generator.suggest(data))
