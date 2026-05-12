# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal

import httpx

from ..types import pty_connect_params, pty_control_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.pty_connect_view import PtyConnectView

__all__ = [
    "PtyResource",
    "AsyncPtyResource",
    "PtyResourceWithRawResponse",
    "AsyncPtyResourceWithRawResponse",
    "PtyResourceWithStreamingResponse",
    "AsyncPtyResourceWithStreamingResponse",
]


class PtyResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PtyResourceWithRawResponse:
        return PtyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PtyResourceWithStreamingResponse:
        return PtyResourceWithStreamingResponse(self)

    def connect(
        self,
        *,
        command: Optional[str] | Omit = omit,
        cwd: Optional[str] | Omit = omit,
        env: Optional[Dict[str, str]] | Omit = omit,
        cols: Optional[int] | Omit = omit,
        rows: Optional[int] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PtyConnectView:
        return self._post(
            "/pty/connect",
            body=maybe_transform(
                {
                    "command": command,
                    "cwd": cwd,
                    "env": env,
                    "cols": cols,
                    "rows": rows,
                },
                pty_connect_params.PtyConnectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PtyConnectView,
        )

    def control(
        self,
        *,
        action: Literal["resize", "signal", "close"],
        cols: Optional[int] | Omit = omit,
        rows: Optional[int] | Omit = omit,
        signal: Optional[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return self._post(
            "/pty/control",
            body=maybe_transform(
                {
                    "action": action,
                    "cols": cols,
                    "rows": rows,
                    "signal": signal,
                },
                pty_control_params.PtyControlParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )


class AsyncPtyResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPtyResourceWithRawResponse:
        return AsyncPtyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPtyResourceWithStreamingResponse:
        return AsyncPtyResourceWithStreamingResponse(self)

    async def connect(
        self,
        *,
        command: Optional[str] | Omit = omit,
        cwd: Optional[str] | Omit = omit,
        env: Optional[Dict[str, str]] | Omit = omit,
        cols: Optional[int] | Omit = omit,
        rows: Optional[int] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PtyConnectView:
        return await self._post(
            "/pty/connect",
            body=await async_maybe_transform(
                {
                    "command": command,
                    "cwd": cwd,
                    "env": env,
                    "cols": cols,
                    "rows": rows,
                },
                pty_connect_params.PtyConnectParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=PtyConnectView,
        )

    async def control(
        self,
        *,
        action: Literal["resize", "signal", "close"],
        cols: Optional[int] | Omit = omit,
        rows: Optional[int] | Omit = omit,
        signal: Optional[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return await self._post(
            "/pty/control",
            body=await async_maybe_transform(
                {
                    "action": action,
                    "cols": cols,
                    "rows": rows,
                    "signal": signal,
                },
                pty_control_params.PtyControlParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )


class PtyResourceWithRawResponse:
    def __init__(self, pty: PtyResource) -> None:
        self._pty = pty
        self.connect = to_raw_response_wrapper(pty.connect)
        self.control = to_raw_response_wrapper(pty.control)


class AsyncPtyResourceWithRawResponse:
    def __init__(self, pty: AsyncPtyResource) -> None:
        self._pty = pty
        self.connect = async_to_raw_response_wrapper(pty.connect)
        self.control = async_to_raw_response_wrapper(pty.control)


class PtyResourceWithStreamingResponse:
    def __init__(self, pty: PtyResource) -> None:
        self._pty = pty
        self.connect = to_streamed_response_wrapper(pty.connect)
        self.control = to_streamed_response_wrapper(pty.control)


class AsyncPtyResourceWithStreamingResponse:
    def __init__(self, pty: AsyncPtyResource) -> None:
        self._pty = pty
        self.connect = async_to_streamed_response_wrapper(pty.connect)
        self.control = async_to_streamed_response_wrapper(pty.control)
