# Note: initially copied from https://github.com/florimondmanca/httpx-sse/blob/master/src/httpx_sse/_decoders.py
from __future__ import annotations

import json
import inspect
from types import TracebackType
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    Callable,
    Iterator,
    Optional,
    Awaitable,
    AsyncIterator,
    cast,
)
from typing_extensions import (
    Self,
    Protocol,
    TypeGuard,
    override,
    get_origin,
    runtime_checkable,
)

import httpx

from ._utils import extract_type_var_from_base
from ._exceptions import APIStatusError, APITimeoutError

if TYPE_CHECKING:
    from ._client import Runloop, AsyncRunloop


_T = TypeVar("_T")


class Stream(Generic[_T]):
    """Provides the core interface to iterate over a synchronous stream response."""

    response: httpx.Response

    _decoder: SSEBytesDecoder

    def __init__(
        self,
        *,
        cast_to: type[_T],
        response: httpx.Response,
        client: Runloop,
    ) -> None:
        self.response = response
        self._cast_to = cast_to
        self._client = client
        self._decoder = client._make_sse_decoder()
        self._iterator = self.__stream__()

    def __next__(self) -> _T:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[_T]:
        for item in self._iterator:
            yield item

    def _iter_events(self) -> Iterator[ServerSentEvent]:
        yield from self._decoder.iter_bytes(self.response.iter_bytes())

    def __stream__(self) -> Iterator[_T]:
        cast_to = cast(Any, self._cast_to)
        response = self.response
        process_data = self._client._process_response_data
        iterator = self._iter_events()

        for sse in iterator:
            # Surface server-sent error events as API errors to allow callers to handle/retry
            if sse.event == "error":
                try:
                    error_obj = json.loads(sse.data)
                    status_code = int(error_obj.get("code", 500))
                    # Build a synthetic response to mirror normal error handling
                    fake_resp = httpx.Response(status_code, request=response.request, content=sse.data)
                except Exception:
                    fake_resp = httpx.Response(500, request=response.request, content=sse.data)
                raise self._client._make_status_error_from_response(fake_resp)

            yield process_data(data=sse.json(), cast_to=cast_to, response=response)

        # Ensure the entire stream is consumed
        for _sse in iterator:
            ...

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        """
        Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        self.response.close()


class AsyncStream(Generic[_T]):
    """Provides the core interface to iterate over an asynchronous stream response."""

    response: httpx.Response

    _decoder: SSEDecoder | SSEBytesDecoder

    def __init__(
        self,
        *,
        cast_to: type[_T],
        response: httpx.Response,
        client: AsyncRunloop,
    ) -> None:
        self.response = response
        self._cast_to = cast_to
        self._client = client
        self._decoder = client._make_sse_decoder()
        self._iterator = self.__stream__()

    async def __anext__(self) -> _T:
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[_T]:
        async for item in self._iterator:
            yield item

    async def _iter_events(self) -> AsyncIterator[ServerSentEvent]:
        async for sse in self._decoder.aiter_bytes(self.response.aiter_bytes()):
            yield sse

    async def __stream__(self) -> AsyncIterator[_T]:
        cast_to = cast(Any, self._cast_to)
        response = self.response
        process_data = self._client._process_response_data
        iterator = self._iter_events()

        async for sse in iterator:
            # Surface server-sent error events as API errors to allow callers to handle/retry
            if sse.event == "error":
                try:
                    error_obj = json.loads(sse.data)
                    status_code = int(error_obj.get("code", 500))
                    # Build a synthetic response to mirror normal error handling
                    fake_resp = httpx.Response(status_code, request=response.request, content=sse.data)
                except Exception:
                    fake_resp = httpx.Response(500, request=response.request, content=sse.data)
                raise self._client._make_status_error_from_response(fake_resp)

            yield process_data(data=sse.json(), cast_to=cast_to, response=response)

        # Ensure the entire stream is consumed
        async for _sse in iterator:
            ...

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """
        Close the response and release the connection.

        Automatically called if the response body is read to completion.
        """
        await self.response.aclose()


class ServerSentEvent:
    def __init__(
        self,
        *,
        event: str | None = None,
        data: str | None = None,
        id: str | None = None,
        retry: int | None = None,
    ) -> None:
        if data is None:
            data = ""

        self._id = id
        self._data = data
        self._event = event or None
        self._retry = retry

    @property
    def event(self) -> str | None:
        return self._event

    @property
    def id(self) -> str | None:
        return self._id

    @property
    def retry(self) -> int | None:
        return self._retry

    @property
    def data(self) -> str:
        return self._data

    def json(self) -> Any:
        return json.loads(self.data)

    @override
    def __repr__(self) -> str:
        return f"ServerSentEvent(event={self.event}, data={self.data}, id={self.id}, retry={self.retry})"


class SSEDecoder:
    _data: list[str]
    _event: str | None
    _retry: int | None
    _last_event_id: str | None

    def __init__(self) -> None:
        self._event = None
        self._data = []
        self._last_event_id = None
        self._retry = None

    def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields raw binary data, iterate over it & yield every event encountered"""
        for chunk in self._iter_chunks(iterator):
            # Split before decoding so splitlines() only uses \r and \n
            for raw_line in chunk.splitlines():
                line = raw_line.decode("utf-8")
                sse = self.decode(line)
                if sse:
                    yield sse

    def _iter_chunks(self, iterator: Iterator[bytes]) -> Iterator[bytes]:
        """Given an iterator that yields raw binary data, iterate over it and yield individual SSE chunks"""
        data = b""
        for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    async def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an iterator that yields raw binary data, iterate over it & yield every event encountered"""
        async for chunk in self._aiter_chunks(iterator):
            # Split before decoding so splitlines() only uses \r and \n
            for raw_line in chunk.splitlines():
                line = raw_line.decode("utf-8")
                sse = self.decode(line)
                if sse:
                    yield sse

    async def _aiter_chunks(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[bytes]:
        """Given an iterator that yields raw binary data, iterate over it and yield individual SSE chunks"""
        data = b""
        async for chunk in iterator:
            for line in chunk.splitlines(keepends=True):
                data += line
                if data.endswith((b"\r\r", b"\n\n", b"\r\n\r\n")):
                    yield data
                    data = b""
        if data:
            yield data

    def decode(self, line: str) -> ServerSentEvent | None:
        # See: https://html.spec.whatwg.org/multipage/server-sent-events.html#event-stream-interpretation  # noqa: E501

        if not line:
            if not self._event and not self._data and not self._last_event_id and self._retry is None:
                return None

            sse = ServerSentEvent(
                event=self._event,
                data="\n".join(self._data),
                id=self._last_event_id,
                retry=self._retry,
            )

            # NOTE: as per the SSE spec, do not reset last_event_id.
            self._event = None
            self._data = []
            self._retry = None

            return sse

        if line.startswith(":"):
            return None

        fieldname, _, value = line.partition(":")

        if value.startswith(" "):
            value = value[1:]

        if fieldname == "event":
            self._event = value
        elif fieldname == "data":
            self._data.append(value)
        elif fieldname == "id":
            if "\0" in value:
                pass
            else:
                self._last_event_id = value
        elif fieldname == "retry":
            try:
                self._retry = int(value)
            except (TypeError, ValueError):
                pass
        else:
            pass  # Field is ignored.

        return None


@runtime_checkable
class SSEBytesDecoder(Protocol):
    def iter_bytes(self, iterator: Iterator[bytes]) -> Iterator[ServerSentEvent]:
        """Given an iterator that yields raw binary data, iterate over it & yield every event encountered"""
        ...

    def aiter_bytes(self, iterator: AsyncIterator[bytes]) -> AsyncIterator[ServerSentEvent]:
        """Given an async iterator that yields raw binary data, iterate over it & yield every event encountered"""
        ...


def is_stream_class_type(typ: type) -> TypeGuard[type[Stream[object]] | type[AsyncStream[object]]]:
    """TypeGuard for determining whether or not the given type is a subclass of `Stream` / `AsyncStream`"""
    origin = get_origin(typ) or typ
    return inspect.isclass(origin) and issubclass(origin, (Stream, AsyncStream))


def extract_stream_chunk_type(
    stream_cls: type,
    *,
    failure_message: str | None = None,
) -> type:
    """Given a type like `Stream[T]`, returns the generic type variable `T`.

    This also handles the case where a concrete subclass is given, e.g.
    ```py
    class MyStream(Stream[bytes]):
        ...

    extract_stream_chunk_type(MyStream) -> bytes
    ```
    """
    from ._base_client import Stream, AsyncStream

    return extract_type_var_from_base(
        stream_cls,
        index=0,
        generic_bases=cast("tuple[type, ...]", (Stream, AsyncStream)),
        failure_message=failure_message,
    )


class ReconnectingStream(Generic[_T]):
    """Wraps a Stream with automatic reconnection on timeout (HTTP 408) or read timeouts.

    The reconnection uses the last observed offset from each item, as provided by
    the given `get_offset` callback. The `stream_creator` will be called with the
    last known offset to resume the stream.
    """

    def __init__(
        self,
        *,
        current_stream: Stream[_T],
        stream_creator: Callable[[Optional[str]], Stream[_T]],
        get_offset: Callable[[_T], Optional[str]],
    ) -> None:
        self._current_stream = current_stream
        self._stream_creator = stream_creator
        self._get_offset = get_offset
        self._last_offset: Optional[str] = None
        self._iterator = self.__stream__()

    @property
    def response(self) -> httpx.Response:
        return self._current_stream.response

    def __next__(self) -> _T:
        return self._iterator.__next__()

    def __iter__(self) -> Iterator[_T]:
        for item in self._iterator:
            yield item

    def __enter__(self) -> "ReconnectingStream[_T]":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self._current_stream.close()

    def __stream__(self) -> Iterator[_T]:
        while True:
            try:
                for item in self._current_stream:
                    offset = self._get_offset(item)
                    if offset is not None:
                        self._last_offset = offset
                    yield item
                return
            except Exception as e:
                # Reconnect on timeouts
                should_reconnect = False
                if isinstance(e, APITimeoutError):
                    should_reconnect = True
                elif isinstance(e, APIStatusError) and getattr(e, "status_code", None) == 408:
                    should_reconnect = True
                elif isinstance(e, httpx.TimeoutException):
                    should_reconnect = True

                if should_reconnect:
                    # Close existing response before reconnecting
                    try:
                        self._current_stream.close()
                    except Exception:
                        pass
                    self._current_stream = self._stream_creator(self._last_offset)
                    continue
                raise


class AsyncReconnectingStream(Generic[_T]):
    """Async variant of ReconnectingStream supporting auto-reconnect on timeouts."""

    def __init__(
        self,
        *,
        current_stream: AsyncStream[_T],
        stream_creator: Callable[[Optional[str]], Awaitable[AsyncStream[_T]]],
        get_offset: Callable[[_T], Optional[str]],
    ) -> None:
        self._current_stream = current_stream
        self._stream_creator = stream_creator
        self._get_offset = get_offset
        self._last_offset: Optional[str] = None
        self._iterator = self.__stream__()

    @property
    def response(self) -> httpx.Response:
        return self._current_stream.response

    async def __anext__(self) -> _T:
        return await self._iterator.__anext__()

    async def __aiter__(self) -> AsyncIterator[_T]:
        async for item in self._iterator:
            yield item

    async def __aenter__(self) -> "AsyncReconnectingStream[_T]":
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        await self._current_stream.close()

    async def __stream__(self) -> AsyncIterator[_T]:
        while True:
            try:
                async for item in self._current_stream:
                    offset = self._get_offset(item)
                    if offset is not None:
                        self._last_offset = offset
                    yield item
                return
            except Exception as e:
                # Reconnect on timeouts
                should_reconnect = False
                if isinstance(e, APITimeoutError):
                    should_reconnect = True
                elif isinstance(e, APIStatusError) and getattr(e, "status_code", None) == 408:
                    should_reconnect = True
                elif isinstance(e, httpx.TimeoutException):
                    should_reconnect = True

                if should_reconnect:
                    try:
                        await self._current_stream.close()
                    except Exception:
                        pass
                    self._current_stream = await self._stream_creator(self._last_offset)
                    continue
                raise
