from __future__ import annotations

import logging

logger = logging.getLogger("agent_observatory")
logger.setLevel(logging.ERROR)  # Default; configurable


def log_internal_error(msg: str) -> None:
    logger.error(msg)
