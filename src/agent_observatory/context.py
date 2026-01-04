from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class AgentContext:
    session_id: str
    agent_id: str
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


_current_session: ContextVar[object | None] = ContextVar(
    "current_session",
    default=None,
)
_current_span: ContextVar[str | None] = ContextVar(
    "current_span",
    default=None,
)


def get_current_session() -> object | None:
    return _current_session.get()


def set_current_session(session: object) -> Token[object | None]:
    return _current_session.set(session)


def reset_current_session(token: Token[object | None]) -> None:
    _current_session.reset(token)


def get_current_span() -> str | None:
    return _current_span.get()


def set_current_span(span_id: str) -> Token[str | None]:
    return _current_span.set(span_id)


def reset_current_span(token: Token[str | None]) -> None:
    _current_span.reset(token)
