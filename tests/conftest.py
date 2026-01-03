import pytest
from typing import Dict, Any

from agent_observatory import Observatory, AgentContext
from agent_observatory.exporters.base import Exporter


class InMemoryExporter(Exporter):
    def __init__(self) -> None:
        self.payloads: list[Dict[str, Any]] = []

    def export(self, payload: Dict[str, Any]) -> None:
        self.payloads.append(payload)


@pytest.fixture
def exporter() -> InMemoryExporter:
    return InMemoryExporter()


@pytest.fixture
def observatory(exporter: InMemoryExporter) -> Observatory:
    return Observatory(exporter=exporter, inline=True)


@pytest.fixture
def agent_ctx() -> AgentContext:
    return AgentContext(
        session_id="test_session",
        agent_id="test_agent",
        user_id="user_1",
    )
