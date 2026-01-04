from datetime import datetime, timezone
from typing import Any, Dict, Optional

from .buffering.ring_buffer import RingBuffer
from .context import get_current_span, reset_current_session
from .events import SCHEMA_VERSION, TraceEvent
from .internal.logging import log_internal_error
from .runtime.clock import now
from .runtime.errors import serialize_error
from .runtime.ids import new_event_id, new_span_id, new_trace_id
from .spans import SpanContext, StreamSpan

DEFAULT_EVENT_BUFFER_SIZE = 10_000


def _iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


class SessionState:
    def __init__(
        self,
        session_id: str,
        agent_id: str,
        user_id: Optional[str],
        metadata: Dict[str, Any],
    ) -> None:
        self.session_id = session_id
        self.agent_id = agent_id
        self.user_id = user_id
        self.metadata = metadata

        self.trace_id: str = new_trace_id()
        self.start_time: float = now()
        self.event_buffer = RingBuffer(capacity=DEFAULT_EVENT_BUFFER_SIZE)

        self._span_meta: dict[str, dict[str, str]] = {}


class AgentSession:
    def __init__(self, state: SessionState, token, exporter_worker) -> None:
        self._state = state
        self._token = token
        self._exporter_worker = exporter_worker

    def __enter__(self) -> "AgentSession":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        reset_current_session(self._token)
        try:
            envelope = self._build_envelope()
            self._exporter_worker.enqueue(envelope)
        except Exception as e:
            log_internal_error(f"session flush failed: {e}")

    # ---------------- Public API ----------------

    def span(
        self,
        name: str,
        kind: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> SpanContext:
        span_id = new_span_id()
        parent_span_id = get_current_span()

        self._emit_span_start(
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            kind=kind,
            attributes=attributes or {},
        )

        return SpanContext(span_id=span_id, session=self)

    def stream(
        self,
        name: str,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> StreamSpan:
        span_id = new_span_id()
        parent_span_id = get_current_span()

        self._emit_span_start(
            span_id=span_id,
            parent_span_id=parent_span_id,
            name=name,
            kind="stream",
            attributes=attributes or {},
        )

        return StreamSpan(span_id=span_id, session=self)

    # ---------------- Internal ----------------

    def _build_envelope(self) -> Dict[str, Any]:
        events = self._state.event_buffer.drain()

        return {
            "schema_version": SCHEMA_VERSION,
            "session": {
                "session_id": self._state.session_id,
                "agent_id": self._state.agent_id,
                "user_id": self._state.user_id,
                "metadata": self._state.metadata,
                "trace_id": self._state.trace_id,
                "start_time": _iso(self._state.start_time),
                "end_time": _iso(now()),
            },
            "events": [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp,
                    "type": e.type,
                    "trace": {
                        "trace_id": e.trace_id,
                        "span_id": e.span_id,
                        "parent_span_id": e.parent_span_id,
                    },
                    "payload": e.payload,
                }
                for e in events
            ],
        }

    def _emit_span_start(
        self,
        span_id: str,
        parent_span_id: Optional[str],
        name: str,
        kind: str,
        attributes: Dict[str, Any],
    ) -> None:
        try:
            self._state.event_buffer.append(
                TraceEvent(
                    event_id=new_event_id(),
                    timestamp=now(),
                    type="span_start",
                    trace_id=self._state.trace_id,
                    span_id=span_id,
                    parent_span_id=parent_span_id,
                    payload={
                        "kind": kind,
                        "name": name,
                        "attributes": attributes,
                    },
                )
            )
            self._state._span_meta[span_id] = {"name": name, "kind": kind}
        except Exception as e:
            log_internal_error(f"span_start failed: {e}")

    def _emit_span_end(
        self,
        span_id: str,
        error: Optional[Exception],
    ) -> None:
        try:
            meta = self._state._span_meta.get(span_id, {})

            self._state.event_buffer.append(
                TraceEvent(
                    event_id=new_event_id(),
                    timestamp=now(),
                    type="span_end",
                    trace_id=self._state.trace_id,
                    span_id=span_id,
                    parent_span_id=None,
                    payload={
                        "name": meta.get("name"),
                        "kind": meta.get("kind"),
                        "status": "error" if error else "ok",
                        "error": serialize_error(error),
                    },
                )
            )

            self._state._span_meta.pop(span_id, None)

        except Exception as e:
            log_internal_error(f"span_end failed: {e}")

    def _emit_stream_event(
        self,
        span_id: str,
        event: str,
        attributes: Dict[str, Any],
    ) -> None:
        try:
            self._state.event_buffer.append(
                TraceEvent(
                    event_id=new_event_id(),
                    timestamp=now(),
                    type="stream_event",
                    trace_id=self._state.trace_id,
                    span_id=span_id,
                    parent_span_id=None,
                    payload={
                        "event": event,
                        "attributes": attributes,
                    },
                )
            )
        except Exception as e:
            log_internal_error(f"stream_event failed: {e}")
