from __future__ import annotations

from typing import Any, Callable

Handler = Callable[[Any], Any]


class MiddlewareChain:
    def __init__(self) -> None:
        self._stack: list[Callable[..., Any]] = []

    def add(self, middleware: Callable[..., Any]) -> None:
        if not callable(middleware):
            raise TypeError("Middleware must be callable")
        self._stack.append(middleware)

    def execute(self, handler: Handler, event: Any) -> Any:
        invoke = handler
        for middleware in reversed(self._stack):
            next_invoke = invoke

            def chain(
                event: Any,
                middleware: Callable[..., Any] = middleware,
                nxt: Callable[[Any], Any] = next_invoke,
            ) -> Any:
                return middleware(nxt, event)

            invoke = chain
        return invoke(event)
