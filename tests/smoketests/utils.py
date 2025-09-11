import os
import time
import asyncio
import inspect
from typing import Any, Mapping

from runloop_api_client import Runloop, AsyncRunloop


def unique_name(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000)}"


THIRTY_SECOND_TIMEOUT = 30


def make_client(**overrides: Mapping[str, Any]) -> Runloop:
    """Create a Runloop client from local src with sane defaults.

    Read RUNLOOP_BASE_URL and RUNLOOP_API_KEY from environment.
    """

    base_url = os.getenv("RUNLOOP_BASE_URL")
    bearer_token = os.getenv("RUNLOOP_API_KEY")

    # Default values similar to TS smoketests
    kwargs: dict[str, Any] = {
        "base_url": base_url,
        "bearer_token": bearer_token,
    }
    if overrides:
        kwargs.update(dict(overrides))

    return Runloop(**kwargs)


class _AsyncToSyncIterator:
    def __init__(self, async_iterable: Any, loop: asyncio.AbstractEventLoop) -> None:
        self._aiter = async_iterable.__aiter__()
        self._loop = loop

    def __iter__(self) -> "_AsyncToSyncIterator":
        return self

    def __next__(self) -> Any:
        try:
            return self._loop.run_until_complete(self._aiter.__anext__())
        except StopAsyncIteration as exc:
            raise StopIteration from exc


class _SyncFromAsyncProxy:
    def __init__(self, root_client: AsyncRunloop, obj: Any, loop: asyncio.AbstractEventLoop) -> None:
        self._root_client = root_client
        self._obj = obj
        self._loop = loop

    def __iter__(self) -> _AsyncToSyncIterator:
        if hasattr(self._obj, "__aiter__"):
            return _AsyncToSyncIterator(self._obj, self._loop)
        raise TypeError(f"Object of type {type(self._obj)} is not iterable")

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._obj, name)

        if callable(attr):

            def _call(*args: Any, **kwargs: Any) -> Any:
                result = attr(*args, **kwargs)
                if inspect.isawaitable(result):
                    result = self._loop.run_until_complete(result)
                # Prefer wrapping objects so attributes remain accessible (e.g., pages)
                if hasattr(result, "__dict__") or hasattr(result, "__getattr__"):
                    return _SyncFromAsyncProxy(self._root_client, result, self._loop)
                # Convert async iterables returned by methods to sync iterators when not objects
                if hasattr(result, "__aiter__"):
                    return _AsyncToSyncIterator(result, self._loop)
                return result

            return _call

        if hasattr(attr, "__aiter__"):
            return _AsyncToSyncIterator(attr, self._loop)

        # Wrap nested resources/objects so their coroutine methods are syncified
        if hasattr(attr, "__dict__") or hasattr(attr, "__getattr__"):
            return _SyncFromAsyncProxy(self._root_client, attr, self._loop)

        return attr

    def close(self) -> None:
        # Gracefully close the underlying async client and its loop
        async def _close() -> None:
            try:
                await self._root_client.__aexit__(None, None, None)
            finally:
                pass

        self._loop.run_until_complete(_close())
        self._loop.close()


def make_async_client_adapter(**overrides: Mapping[str, Any]) -> Any:
    """Create a sync adapter over the AsyncRunloop so tests can call it synchronously.

    Reads RUNLOOP_BASE_URL and RUNLOOP_API_KEY from environment.
    """

    base_url = os.getenv("RUNLOOP_BASE_URL")
    bearer_token = os.getenv("RUNLOOP_API_KEY")

    kwargs: dict[str, Any] = {
        "base_url": base_url,
        "bearer_token": bearer_token,
    }
    if overrides:
        kwargs.update(dict(overrides))

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def _enter() -> AsyncRunloop:
        client = AsyncRunloop(**kwargs)
        return await client.__aenter__()

    async_client = loop.run_until_complete(_enter())

    return _SyncFromAsyncProxy(async_client, async_client, loop)
