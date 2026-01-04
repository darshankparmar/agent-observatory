from __future__ import annotations

import time


def now() -> float:
    """
    Return a monotonic timestamp in seconds.

    Used for:
    - event ordering
    - duration calculations
    - span lifetimes

    Not intended for wall-clock correlation.
    """
    return time.monotonic()
