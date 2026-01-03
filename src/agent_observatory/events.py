from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Literal, Dict, Any

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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "timestamp": self.timestamp,
            "type": self.type,
            "trace": {
                "trace_id": self.trace_id,
                "span_id": self.span_id,
                "parent_span_id": self.parent_span_id,
            },
            "payload": self.payload,
        }
