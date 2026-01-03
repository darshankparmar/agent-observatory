from __future__ import annotations

import asyncio
from typing import Optional

from .session import SessionState, AgentSession
from .context import AgentContext, set_current_session
from .exporters.base import Exporter
from .exporters.worker import (
    ExporterWorker,
    InlineExporterWorker,
    ExporterWorkerProtocol,
)


class Observatory:
    def __init__(self, exporter: Exporter, *, inline: bool = False):
        self._exporter = exporter
        self._inline = inline

        self._worker_task: Optional[asyncio.Task] = None

        if inline:
            self._worker: ExporterWorkerProtocol = InlineExporterWorker(exporter)
        else:
            self._worker = ExporterWorker(exporter)

    async def start(self) -> None:
        if not self._inline and self._worker_task is None:
            self._worker_task = asyncio.create_task(self._worker.start())  # type: ignore

    def start_session(self, ctx: AgentContext) -> AgentSession:
        state = SessionState(
            session_id=ctx.session_id,
            agent_id=ctx.agent_id,
            user_id=ctx.user_id,
            metadata=ctx.metadata or {},
        )
        token = set_current_session(state)
        return AgentSession(state, token, self._worker)

    async def shutdown(self) -> None:
        if not self._inline:
            await self._worker.stop()  # type: ignore
            self._worker_task = None
