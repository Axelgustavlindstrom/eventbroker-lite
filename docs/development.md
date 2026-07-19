# Development Guide

This guide covers local development workflows for EventBroker Lite.

## Setup

Clone the repository and install the package in editable mode with development
dependencies:

```bash
git clone https://github.com/Axelgustavlindstrom/eventbroker-lite.git
cd eventbroker-lite
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running tests

```bash
pytest
```

## Lint and type checks

```bash
ruff check src tests
mypy src
```

If `mypy` is unavailable, `ruff check src tests` provides fast static linting
without additional setup.

## Make a change

1. Create a focused branch for the work.
2. Keep changes small and behavior-driven.
3. Add or update tests alongside code changes.
4. Run the test suite before opening a pull request.

```bash
git checkout -b fix/topic-matching-edge-case
```

## Commit conventions

This project uses conventional commit prefixes where helpful:

- `docs:` for README and documentation changes
- `fix:` for bug fixes
- `feat:` for backward-compatible additions
- `refactor:` for code changes that do not affect behavior
- `test:` for test-only changes

Aim for truthful, descriptive messages.
