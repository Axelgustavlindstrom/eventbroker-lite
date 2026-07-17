# EventBroker Lite

![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-stable-green)

**EventBroker Lite** is a lightweight, typed, in-process event broker designed for small services, local development, and serverless workflows. It gives you topic-based pub/sub, basic schema validation, middleware hooks, and an optional SQLite-backed event log—without the operational overhead of Kafka, Redis, or RabbitMQ.

## About

Most local or lightweight services don't need a full distributed message broker, but they do need clean decoupling. EventBroker Lite fills that gap: a single dependency, deterministic behavior, and developer-friendly APIs. It's built to drop into existing Python projects with minimal ceremony, and it's friendly for tests because events can be inspected in-memory.

## Features

- Topic-based publish/subscribe with wildcard support (`orders.*`, `billing.created`)
- Type-safe payloads via `@dataclass` and runtime validation
- Event middleware / interceptors for logging, validation, or tracing
- Optional SQLite-backed "event bus" persistence for replay or debugging
- Dead-letter / failed handler support
- Synchronous and asynchronous handlers
- Full type annotations and small API surface

## Installation

### From source

```bash
git clone https://github.com/<owner>/eventbroker-lite.git
cd eventbroker-lite
pip install -e .
```

### Requirements

- Python 3.11 or newer
- No mandatory external services. Optional SQLite persistence uses the Python standard library.

## Quick Start

```python
from dataclasses import dataclass
from eventbroker import EventBroker

@dataclass
class OrderCreated:
    order_id: str
    amount: float

broker = EventBroker()

@broker.subscribe("orders.created")
def handle_order(event: OrderCreated):
    print(f"Processing order {event.order_id}: ${event.amount}")

broker.publish("orders.created", OrderCreated(order_id="ORD-1", amount=29.9))
```

### Wildcard subscriptions

```python
@broker.subscribe("billing.*")
def on_any_billing(event):
    print(f"Billing event: {event}")
```

### Middleware

```python
def logging_middleware(next, event):
    print(f"[out] {event.topic}")
    return next(event)

broker.use(logging_middleware)
```

## Project Structure

```text
eventbroker-lite/
├── README.md
├── pyproject.toml
├── src/
│   └── eventbroker/
│   ├── __init__.py
│   ├── broker.py
│   ├── topic.py
│   ├── events.py
│   ├── exceptions.py
│   └── middleware.py
├── tests/
│   ├── test_broker.py
│   ├── test_topics.py
│   └── test_middleware.py
└── docs/
└── usage.md
```

## Configuration

EventBroker Lite is configured programmatically. Recommended defaults:

- Use in-memory broker for tests and short-lived processes.
- Enable `sqlite_history=True` when you need ordered persistence or replay.
- Wildcard matching is substring glob-style on segments.

## Verification

This project includes a test suite and optional linting.

```bash
# Run tests
pytest

# Lint
ruff check src tests
```

## License

MIT
