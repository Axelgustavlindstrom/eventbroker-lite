from eventbroker import Event, EventBroker


class Counter:
    def __init__(self) -> None:
        self.value: int = 0

    def handle(self, event: Event) -> None:
        self.value += 1


def test_subscribe_and_publish() -> None:
    broker = EventBroker()
    counter = Counter()
    broker.subscribe("demo.clicked")(counter.handle)

    broker.publish("demo.clicked", {"button": "ok"})

    assert counter.value == 1


def test_no_match_subscription_does_not_invoke() -> None:
    broker = EventBroker()
    counter = Counter()
    broker.subscribe("demo.clicked")(counter.handle)

    broker.publish("demo.pressed", {"button": "ok"})

    assert counter.value == 0


def test_unsubscribe_removes_handler() -> None:
    broker = EventBroker()
    counter = Counter()
    unsub = broker.subscribe("demo.clicked")(counter.handle)

    broker.publish("demo.clicked", {})
    assert counter.value == 1

    unsub()
    broker.publish("demo.clicked", {})
    assert counter.value == 1


def test_wildcard_subscription() -> None:
    broker = EventBroker()
    counter = Counter()
    broker.subscribe("orders.*")(counter.handle)

    broker.publish("orders.created", {"id": 1})
    broker.publish("orders.updated", {"id": 1})

    assert counter.value == 2


def test_multiple_handlers_receive_same_event() -> None:
    broker = EventBroker()
    c1 = Counter()
    c2 = Counter()
    broker.subscribe("notify")(c1.handle)
    broker.subscribe("notify")(c2.handle)

    broker.publish("notify", {})

    assert c1.value == 1
    assert c2.value == 1


def test_history_records_events() -> None:
    broker = EventBroker()
    broker.publish("x.y", 1)
    broker.publish("x.z", 2)

    history = broker.history()
    assert len(history) == 2
    assert history[0].topic == "x.y"
    assert history[0].payload == 1


def test_non_singleton_handler_matches_do_not_share_state() -> None:
    broker = EventBroker()
    counter = Counter()

    broker.subscribe("orders.created")(counter.handle)
    broker.subscribe("orders.updated")(counter.handle)

    broker.publish("orders.created", {})
    broker.publish("orders.updated", {})

    assert counter.value == 2
