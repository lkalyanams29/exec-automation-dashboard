from __future__ import annotations
import logging, os, random, time
from typing import Any, Iterator
import requests

log = logging.getLogger(__name__)

class KatalonClient:
    """Reusable, defensive TestOps HTTP client with pagination and retries.

    Endpoint paths are configuration inputs because TestOps API availability and
    response envelopes can differ by account/version. Run discover.py first and
    adjust paths/envelope keys from observed responses.
    """
    def __init__(self, base_url: str | None = None, timeout: int = 30, retries: int = 5):
        self.base_url = (base_url or os.getenv("KATALON_BASE_URL", "https://testops.katalon.io")).rstrip("/")
        api_key = os.getenv("KATALON_API_KEY")
        if not api_key: raise ValueError("KATALON_API_KEY is required")
        self.account_id, self.org_id = os.getenv("KATALON_ACCOUNT_ID"), os.getenv("KATALON_ORG_ID")
        self.timeout, self.retries = timeout, retries
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {api_key}", "Accept": "application/json"})

    def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}/{path.lstrip('/')}"
        params = {k: v for k, v in (params or {}).items() if v is not None}
        for attempt in range(self.retries + 1):
            response = self.session.get(url, params=params, timeout=self.timeout)
            if response.status_code not in (429, 500, 502, 503, 504):
                response.raise_for_status(); return response.json()
            if attempt == self.retries: response.raise_for_status()
            delay = float(response.headers.get("Retry-After", min(2 ** attempt, 30))) + random.random()
            log.warning("katalon_retry", extra={"status": response.status_code, "attempt": attempt + 1, "delay": delay})
            time.sleep(delay)

    def pages(self, path: str, params: dict[str, Any] | None = None, item_keys=("content", "data", "items")) -> Iterator[dict[str, Any]]:
        page, params = 0, dict(params or {})
        while True:
            payload = self.get(path, {**params, "page": page})
            if isinstance(payload, list): items = payload
            else: items = next((payload[k] for k in item_keys if isinstance(payload.get(k), list)), [])
            for item in items:
                if isinstance(item, dict): yield item
            total_pages = payload.get("totalPages") if isinstance(payload, dict) else None
            if not items or (total_pages is not None and page + 1 >= int(total_pages)) or len(items) < int(params.get("size", 100)): break
            page += 1
