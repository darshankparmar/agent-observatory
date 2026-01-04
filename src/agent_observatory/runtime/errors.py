from __future__ import annotations

import traceback
from typing import Any, Dict, Optional


def serialize_error(exc: Exception | None) -> Optional[Dict[str, Any]]:
    if exc is None:
        return None

    return {
        "type": exc.__class__.__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
    }
