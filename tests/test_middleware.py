from __future__ import annotations

from typing import Any

from eventbroker import Event, EventBroker


def test_middleware_added_via_broker() -> None:
    broker = EventBroker()
    calls = []

    def log_mw(next, event: Event) -> Any:
        calls.append(event.topic)
        return next(event)

    broker.use(log_mw)
    broker.subscribe("t")(lambda event: None)
    broker.publish("t", None)

    assert len(calls) == 1
    assert calls[0] == "t"
