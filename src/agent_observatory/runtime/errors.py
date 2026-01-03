from __future__ import annotations

from typing import Dict, Any, Optional
import traceback


def serialize_error(exc: Exception | None) -> Optional[Dict[str, Any]]:
    if exc is None:
        return None
    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
    }
