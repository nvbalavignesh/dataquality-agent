"""Utility helpers for the Data Quality Agent."""

from __future__ import annotations

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dq_agent")


def log(message: str) -> None:
    logger.info(message)
