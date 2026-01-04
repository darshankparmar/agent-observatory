from __future__ import annotations

from typing import Any, Dict


class Exporter:
    """
    Exporter contract.

    DESIGN:
    - Exporters are synchronous.
    - Must fail open (never raise).
    - Must be safe to call from any thread / event loop.
    """

    def export(self, payload: Dict[str, Any]) -> None:
        raise NotImplementedError
