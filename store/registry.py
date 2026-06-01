"""
Feature registry: register feature views, entities, and transformation logic.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Callable, Optional
from datetime import datetime


@dataclass
class Entity:
    name: str
    join_key: str
    description: str = ""


@dataclass
class FeatureView:
    name: str
    entities: list[str]
    features: list[str]
    source: str = ""
    ttl_days: Optional[int] = None
    transform_fn: Optional[Callable] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    version: int = 1


class FeatureRegistry:
    def __init__(self):
        self.entities: dict[str, Entity] = {}
        self.feature_views: dict[str, FeatureView] = {}
        self._history: list[dict] = []

    def register_entity(self, entity: Entity):
        self.entities[entity.name] = entity
        print(f"Registered entity: {entity.name} (join_key={entity.join_key})")
        return self

    def register_feature_view(self, view: FeatureView):
        key = f"{view.name}:v{view.version}"
        self.feature_views[key] = view
        self.feature_views[view.name] = view  # latest alias
        self._history.append({"name": view.name, "version": view.version,
                               "registered_at": view.created_at})
        print(f"Registered feature view: {view.name} v{view.version} ({len(view.features)} features)")
        return self

    def get_view(self, name: str, version: int = None) -> FeatureView:
        key = f"{name}:v{version}" if version else name
        if key not in self.feature_views:
            raise KeyError(f"Feature view '{key}' not found. Available: {list(self.feature_views.keys())}")
        return self.feature_views[key]

    def list_views(self) -> list[dict]:
        return [{"name": v.name, "version": v.version, "features": v.features}
                for k, v in self.feature_views.items() if ":" not in k]
