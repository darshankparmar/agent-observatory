from __future__ import annotations

from collections import deque
from typing import Any


class RingBuffer:
    def __init__(self, capacity: int) -> None:
        self._buffer: deque[Any] = deque(maxlen=capacity)

    def append(self, item: Any) -> None:
        self._buffer.append(item)

    def drain(self) -> list[Any]:
        items = list(self._buffer)
        self._buffer.clear()
        return items
