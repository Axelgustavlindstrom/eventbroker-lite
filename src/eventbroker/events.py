from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .topic import Topic


@dataclass(frozen=True)
class Event:
    topic: str
    payload: Any
    metadata: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.topic:
            raise ValueError("Event topic must be non-empty")
        object.__setattr__(self, "metadata", self.metadata or {})

    def resolved_topic(self) -> Topic:
        return Topic(self.topic)
