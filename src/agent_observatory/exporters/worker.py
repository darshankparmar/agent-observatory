from __future__ import annotations

import asyncio
from typing import Optional, Protocol

from .base import Exporter
from agent_observatory.internal.logging import log_internal_error


class ExporterWorkerProtocol(Protocol):
    def enqueue(self, payload: dict) -> None: ...


class ExporterWorker:
    """
    Async, background exporter worker (production).

    Intended for:
    - long-running services
    - agents
    - servers
    """

    def __init__(self, exporter: Exporter, max_queue_size: int = 100):
        self._exporter = exporter
        self._queue: asyncio.Queue[dict] = asyncio.Queue(maxsize=max_queue_size)
        self._task: Optional[asyncio.Task] = None
        self._running = False

    async def start(self) -> None:
        if self._running:
            return
        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self) -> None:
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
            self._task = None

    async def _run(self) -> None:
        while self._running:
            try:
                payload = await self._queue.get()
                self._exporter.export(payload)
            except asyncio.CancelledError:
                break
            except Exception as e:
                log_internal_error(f"export failed: {e}")

    def enqueue(self, payload: dict) -> None:
        try:
            self._queue.put_nowait(payload)
        except asyncio.QueueFull:
            log_internal_error("export queue full — dropping trace")


class InlineExporterWorker:
    """
    Synchronous exporter worker (tests, scripts, CLIs).

    GUARANTEE:
    - export() is executed immediately and deterministically.
    """

    def __init__(self, exporter: Exporter):
        self._exporter = exporter

    def enqueue(self, payload: dict) -> None:
        try:
            self._exporter.export(payload)
        except Exception as e:
            log_internal_error(f"inline export failed: {e}")
