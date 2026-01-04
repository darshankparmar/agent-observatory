from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Literal, Optional

SCHEMA_VERSION = "0.1"


@dataclass(slots=True)
class TraceEvent:
    event_id: str
    timestamp: float
    type: Literal["span_start", "span_end", "stream_event"]
    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    payload: Dict[str, Any]
