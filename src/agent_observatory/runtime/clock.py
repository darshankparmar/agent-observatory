from __future__ import annotations

import time


def now() -> float:
    return time.monotonic()  # Better for durations
