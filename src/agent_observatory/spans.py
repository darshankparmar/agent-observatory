from __future__ import annotations

from contextvars import Token
from typing import Any, Dict, Literal

from .context import reset_current_span, set_current_span


class SpanContext:
    def __init__(self, span_id: str, session: Any) -> None:
        self.span_id = span_id
        self._session = session
        self._token: Token[str | None] | None = None

    def _emit_event(
        self,
        event: str,
        attributes: Dict[str, Any] | None = None,
    ) -> None:
        self._session._emit_stream_event(
            span_id=self.span_id,
            event=event,
            attributes=attributes or {},
        )

    def event(
        self,
        name: str,
        attributes: Dict[str, Any] | None = None,
    ) -> None:
        """Emit a structured event within this span."""
        self._emit_event(name, attributes)

    def __enter__(self) -> "SpanContext":
        self._token = set_current_span(self.span_id)
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc: Any,
        tb: Any,
    ) -> Literal[False]:
        try:
            self._session._emit_span_end(
                span_id=self.span_id,
                error=exc,
            )
        finally:
            if self._token is not None:
                reset_current_span(self._token)
        return False


class StreamSpan:
    def __init__(self, span_id: str, session: Any) -> None:
        self.span_id = span_id
        self._session = session

    def _emit_event(
        self,
        event: str,
        attributes: Dict[str, Any] | None = None,
    ) -> None:
        self._session._emit_stream_event(
            span_id=self.span_id,
            event=event,
            attributes=attributes or {},
        )

    def event(
        self,
        name: str,
        attributes: Dict[str, Any] | None = None,
    ) -> None:
        """Emit a structured event within this stream."""
        self._emit_event(name, attributes)

    def __enter__(self) -> "StreamSpan":
        return self

    def __exit__(
        self,
        exc_type: Any,
        exc: Any,
        tb: Any,
    ) -> Literal[False]:
        self._session._emit_span_end(
            span_id=self.span_id,
            error=exc,
        )
        return False
