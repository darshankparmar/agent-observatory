from typing import Any

from ..internal.logging import log_internal_error
from .base import Exporter


class MultiExporter(Exporter):
    """Exporter that forwards to multiple exporters."""

    def __init__(self, exporters: list[Exporter]) -> None:
        self.exporters = exporters

    def export(self, payload: dict[str, Any]) -> None:
        for i, exporter in enumerate(self.exporters):
            try:
                exporter.export(payload)
            except Exception as e:
                log_internal_error(f"multi_exporter[{i}] failed: {e}")
