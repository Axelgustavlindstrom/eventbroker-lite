from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Topic:
    raw: str
    _segments: tuple[str, ...] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if not self.raw:
            raise ValueError("Topic must be non-empty")
        object.__setattr__(self, "_segments", tuple(self.raw.split(".")))

    def __str__(self) -> str:
        return self.raw

    def __hash__(self) -> int:
        return hash(self.raw)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Topic) and self.raw == other.raw

    @property
    def segments(self) -> tuple[str, ...]:
        return self._segments

    def matches(self, pattern: str) -> bool:
        if pattern == "#":
            return True
        target_segments = tuple(pattern.split("."))
        if len(self._segments) != len(target_segments):
            return False
        for t, p in zip(self._segments, target_segments):
            if p == "*":
                continue
            if p != t:
                return False
        return True
