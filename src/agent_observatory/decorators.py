import asyncio
import functools
from typing import Any, Callable, TypeVar

# Type variable for the decorated function
F = TypeVar("F", bound=Callable[..., Any])


def trace_agent_step(name: str) -> Callable[[F], F]:
    """
    Decorator to trace a function as an agent step.

    Tries to find an 'obs' or 'session' argument, or 'self.obs'/'self.session'.
    Supports both sync and async functions.
    """

    def decorator(func: F) -> F:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                session = _find_session(args, kwargs)
                if session:
                    with session.agent_step(name):
                        return await func(*args, **kwargs)
                return await func(*args, **kwargs)

            return async_wrapper  # type: ignore
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                session = _find_session(args, kwargs)
                if session:
                    with session.agent_step(name):
                        return func(*args, **kwargs)
                return func(*args, **kwargs)

            return sync_wrapper  # type: ignore

    return decorator


def trace_tool_call(name: str) -> Callable[[F], F]:
    """
    Decorator to trace a function as a tool call.
    Supports both sync and async functions.
    """

    def decorator(func: F) -> F:
        if asyncio.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                session = _find_session(args, kwargs)
                if session:
                    with session.tool_call(name):
                        return await func(*args, **kwargs)
                return await func(*args, **kwargs)

            return async_wrapper  # type: ignore
        else:

            @functools.wraps(func)
            def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
                session = _find_session(args, kwargs)
                if session:
                    with session.tool_call(name):
                        return func(*args, **kwargs)
                return func(*args, **kwargs)

            return sync_wrapper  # type: ignore

    return decorator


def _find_session(args: tuple, kwargs: dict) -> Any | None:
    """
    Heuristic to find an AgentSession in args or kwargs.
    """
    # 1. Check known kwargs
    if "session" in kwargs:
        return kwargs["session"]
    if "obs" in kwargs:
        return kwargs["obs"]

    # 2. Check first arg (self) for .session or .obs
    if args:
        first_arg = args[0]
        if hasattr(first_arg, "session"):
            return getattr(first_arg, "session")
        if hasattr(first_arg, "obs"):
            return getattr(first_arg, "obs")

    return None
