"""
In-memory online feature store for low-latency serving.
Production: swap dict for Redis/DynamoDB.
"""
from __future__ import annotations
import json
from datetime import datetime
from typing import Any


class OnlineStore:
    def __init__(self):
        self._store: dict[str, dict] = {}

    def _key(self, feature_view: str, entity_id: str) -> str:
        return f"{feature_view}:{entity_id}"

    def write(self, feature_view: str, entity_id: str, features: dict[str, Any]):
        k = self._key(feature_view, entity_id)
        self._store[k] = {**features, "_written_at": datetime.utcnow().isoformat()}

    def read(self, feature_view: str, entity_id: str) -> dict | None:
        return self._store.get(self._key(feature_view, entity_id))

    def read_batch(self, feature_view: str, entity_ids: list[str]) -> list[dict | None]:
        return [self.read(feature_view, eid) for eid in entity_ids]

    def write_batch(self, feature_view: str, records: list[dict], entity_key: str):
        for rec in records:
            eid = str(rec[entity_key])
            features = {k: v for k, v in rec.items() if k != entity_key}
            self.write(feature_view, eid, features)
        print(f"Wrote {len(records)} records to online store [{feature_view}]")

    @property
    def size(self) -> int:
        return len(self._store)
