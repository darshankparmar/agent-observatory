from __future__ import annotations

import asyncio
from typing import Optional

from .context import AgentContext, set_current_session
from .exporters.base import Exporter
from .exporters.worker import (
    ExporterWorker,
    ExporterWorkerProtocol,
    InlineExporterWorker,
)
from .session import AgentSession, SessionState


class Observatory:
    def __init__(self, exporter: Exporter, *, inline: bool = False) -> None:
        self._exporter = exporter
        self._inline = inline

        self._worker: ExporterWorkerProtocol
        self._worker_task: Optional[asyncio.Task[None]] = None

        if inline:
            self._worker = InlineExporterWorker(exporter)
        else:
            self._worker = ExporterWorker(exporter)

    async def start(self) -> None:
        if self._inline:
            return

        worker = self._worker
        assert isinstance(worker, ExporterWorker)

        if self._worker_task is None:
            self._worker_task = asyncio.create_task(worker.start())

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
        if self._inline:
            return

        worker = self._worker
        assert isinstance(worker, ExporterWorker)

        await worker.stop()
        self._worker_task = None
