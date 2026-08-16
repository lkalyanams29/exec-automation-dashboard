from __future__ import annotations
import json, sqlite3
from pathlib import Path
from typing import Any

class Repository:
    def __init__(self, path="data/katalon_dashboard.db"):
        Path(path).parent.mkdir(parents=True, exist_ok=True); self.db=sqlite3.connect(path); self.db.row_factory=sqlite3.Row
    def initialize(self): self.db.executescript(Path(__file__).with_name("schema.sql").read_text()); self.db.execute("PRAGMA optimize"); self.db.commit()
    def upsert(self, table: str, row: dict[str, Any], conflict: str):
        allowed={"projects","test_cases","test_executions","test_results","daily_project_metrics"}
        if table not in allowed: raise ValueError("Unsupported table")
        keys=list(row); cols=",".join(keys); marks=",".join("?" for _ in keys); updates=",".join(f"{k}=excluded.{k}" for k in keys if k not in conflict.split(","))
        self.db.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks}) ON CONFLICT({conflict}) DO UPDATE SET {updates}",[json.dumps(v) if isinstance(v,(dict,list)) else v for v in row.values()])
    def commit(self): self.db.commit()
