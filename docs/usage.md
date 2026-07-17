# EventBroker Lite

This document describes when and how to use EventBroker Lite.

## When to use

- Local Python services needing lightweight decoupling
- Jobs/scripts where full Redis/Kafka is overkill
- Tests that inspect published events in-process

## Limitations

- In-process only; not distributed across processes or hosts
- Topic patterns match single-segment wildcards (`*`) only
- No guaranteed delivery semantics; history is a debugging aid
