"""Placeholder for continuous learning from feedback."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

RULES_FILE = Path("validated_rules.txt")


def store_rule(rule: str) -> None:
    """Append a validated rule to the local rules file."""
    if RULES_FILE.exists():
        existing = RULES_FILE.read_text()
        RULES_FILE.write_text(existing + rule + "\n")
    else:
        RULES_FILE.write_text(rule + "\n")


def load_rules() -> Iterable[str]:
    if not RULES_FILE.exists():
        return []
    return [line.strip() for line in RULES_FILE.read_text().splitlines() if line.strip()]


if __name__ == "__main__":
    store_rule("col_A > 0")
    print(list(load_rules()))
