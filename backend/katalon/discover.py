"""Phase-1 connectivity probe: prints keys/shapes, never credentials or full payloads."""
import json, logging
from .client import KatalonClient

def describe(value):
    if isinstance(value, dict): return {k: type(v).__name__ for k, v in value.items()}
    if isinstance(value, list): return {"type": "list", "count": len(value), "first": describe(value[0]) if value else None}
    return type(value).__name__

def probe(paths):
    client = KatalonClient()
    for label, path in paths.items():
        try: print(json.dumps({"resource": label, "path": path, "shape": describe(client.get(path, {"size": 1}))}, indent=2))
        except Exception as exc: logging.exception("probe_failed", extra={"resource": label, "error": str(exc)})
