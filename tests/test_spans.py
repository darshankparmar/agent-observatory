from typing import Any
from agent_observatory import Observatory, AgentContext


def test_basic_span_emission(
    observatory: Observatory, agent_ctx: AgentContext, exporter: Any
) -> None:
    with observatory.start_session(agent_ctx) as session:
        with session.span("step1", kind="agent_step"):
            pass

    payload = exporter.payloads[0]
    events = payload["events"]

    assert len(events) == 2
    assert events[0]["type"] == "span_start"
    assert events[0]["payload"]["name"] == "step1"

    assert events[1]["type"] == "span_end"
    assert events[1]["payload"]["status"] == "ok"


def test_nested_spans_parent_child(
    observatory: Observatory, agent_ctx: AgentContext, exporter: Any
) -> None:
    with observatory.start_session(agent_ctx) as session:
        with session.span("parent", kind="agent_step"):
            with session.span("child", kind="agent_step"):
                pass

    events = exporter.payloads[0]["events"]

    parent_start = events[0]
    child_start = events[1]

    assert child_start["trace"]["parent_span_id"] == parent_start["trace"]["span_id"]
