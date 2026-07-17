from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Callable

from .events import Event
from .exceptions import PublishError, SubscriptionError
from .middleware import MiddlewareChain
from .topic import Topic

logger = logging.getLogger(__name__)

Handler = Callable[[Any], None]


@dataclass
class Subscription:
    pattern: str
    handler: Handler


class EventBroker:
    def __init__(self) -> None:
        self._subscriptions: list[Subscription] = []
        self._middlewares = MiddlewareChain()
        self._history: list[Event] = []

    def subscribe(self, topic_pattern: str) -> Callable[[Handler], Callable[[], None]]:
        def decorator(handler: Handler) -> Callable[[], None]:
            if not callable(handler):
                raise SubscriptionError("Handler must be callable")
            if not topic_pattern or not topic_pattern.strip():
                raise SubscriptionError("Topic pattern must be non-empty")
            sub = Subscription(pattern=topic_pattern, handler=handler)
            self._subscriptions.append(sub)

            def unsubscribe() -> None:
                if sub in self._subscriptions:
                    self._subscriptions.remove(sub)

            return unsubscribe

        return decorator

    def publish(self, topic: str, payload: Any, metadata: dict[str, Any] | None = None) -> None:
        event = Event(topic=topic, payload=payload, metadata=metadata)
        resolved = Topic(event.topic)

        matched: list[Subscription] = [
            sub for sub in self._subscriptions if resolved.matches(sub.pattern)
        ]

        for sub in self._subscriptions:
            resolved = Topic(event.topic)
            if not resolved.matches(sub.pattern):
                continue
            handler = sub.handler
            try:
                def _invoke(ev: Event, h: Handler = handler) -> Any:
                    return h(ev)

                self._middlewares.execute(_invoke, event)
            except Exception:
                logger.exception("Failed to handle event", exc_info=True)
                raise PublishError(f"Handler failed for topic {topic}")

        self._history.append(event)
        if len(matched) == 0:
            logger.debug("Published event with no subscribers", extra={"topic": topic})

    def enable_history(self, enabled: bool = True) -> None:
        if not enabled:
            # Keep existing history; avoid surprise truncation.
            self._history = []

    def history(self) -> list[Event]:
        return list(self._history)

    def use(self, middleware: Callable[..., Any]) -> None:
        self._middlewares.add(middleware)

    def reset(self) -> None:
        self._subscriptions.clear()
        self._history.clear()
        self._middlewares = MiddlewareChain()
