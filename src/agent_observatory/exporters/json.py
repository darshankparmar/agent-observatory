from __future__ import annotations

import json
from typing import Any, Dict

from .base import Exporter


class JSONExporter(Exporter):
    def export(self, payload: Dict[str, Any]) -> None:
        print(json.dumps(payload, indent=2))
