from __future__ import annotations

from eventbroker import EventBroker


def main() -> int:
    broker = EventBroker()

    @broker.subscribe("demo.greeting")
    def handle_greeting(event: object) -> None:
        print(f"Received event: {event}")

    broker.publish("demo.greeting", {"message": "hello from EventBroker Lite"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
