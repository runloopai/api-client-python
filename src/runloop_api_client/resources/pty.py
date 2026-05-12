# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal

import httpx

from ..types import pty_connect_params, pty_control_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import path_template, maybe_transform, async_maybe_transform
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
from ..types.pty_control_result_view import PtyControlResultView

__all__ = ["PtyResource", "AsyncPtyResource"]


class PtyResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> PtyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return PtyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> PtyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return PtyResourceWithStreamingResponse(self)

    def connect(
        self,
        session_name: str,
        *,
        cols: str | Omit = omit,
        rows: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PtyConnectView:
        """
        Looks up the PTY session identified by the path session*name and either
        reconnects to the existing session or creates it if it does not yet exist. The
        session_name is a client-chosen session identifier, not an opaque server-issued
        ID. It must be non-empty (1..=256 chars) and use only ASCII letters, digits, '-'
        and '*'. A newly created PTY session starts an interactive bash shell on the
        Devbox. Optional cols and rows query parameters apply an initial terminal size
        before any I/O; they must both be present and in the range 1..=1000 to take
        effect. The response returns a PtyConnectView containing connect_url (a
        server-relative path to the WebSocket data plane), idle_ttl_seconds (how long
        this session is retained after the last client disconnects), and the resulting
        cols/rows. The interactive byte stream itself is intentionally not modeled in
        OpenAPI; see the controller-level documentation for the WebSocket close-code
        conventions. The single-attach contract is enforced when a client opens the
        WebSocket data plane, not on this bootstrap call: bootstrap always succeeds for
        a valid session_name, even if another client is currently attached. Rejection of
        a second concurrent attach happens at WebSocket upgrade time. If the active
        client disconnects, the session is preserved for the idle TTL so a later connect
        using the same session_name resumes the same shell. After the TTL expires, after
        an explicit close control action, or after the underlying Devbox lifecycle
        replaces the PTY process (such as through suspend/resume), a later request with
        the same session_name creates a fresh PTY session without the previous shell
        state.

        Documentation note: this operation is published from mux strictly as an OpenAPI
        contract stub for the PTY service control plane. It is not evidence that mux
        itself serves the interactive PTY transport.

        Args:
          cols: Optional initial terminal width in character cells (1..=1000). Defaults to 80
              when omitted. Applied only if both cols and rows are provided; otherwise
              ignored.

          rows: Optional initial terminal height in character cells (1..=1000). Defaults to 24
              when omitted. Applied only if both cols and rows are provided; otherwise
              ignored.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_name:
            raise ValueError(f"Expected a non-empty value for `session_name` but received {session_name!r}")
        return self._get(
            path_template("/pty/{session_name}", session_name=session_name),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "cols": cols,
                        "rows": rows,
                    },
                    pty_connect_params.PtyConnectParams,
                ),
            ),
            cast_to=PtyConnectView,
        )

    def control(
        self,
        session_name: str,
        *,
        action: Literal["resize", "signal", "close"] | Omit = omit,
        cols: int | Omit = omit,
        rows: int | Omit = omit,
        signal: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PtyControlResultView:
        """Applies a PTY control operation to an existing session.

        The action field selects
        the operation; the other fields in PtyControlParameters are interpreted only
        when they are relevant to the chosen action.

        resize: cols and rows are required and must each be in 1..=1000. A 0 or
        out-of-range value returns 400. The new winsize is applied to the PTY master and
        the kernel delivers SIGWINCH to the foreground process group.

        signal: signal is the POSIX signal name (for example 'SIGTERM', 'SIGHUP',
        'SIGINT', 'SIGUSR1'). Unknown signal names return 400. The signal is delivered
        to the slave's foreground process group via killpg(2). If the shell has already
        exited and there is no foreground process group, returns 400.

        close: terminates the session. Sends SIGHUP to the foreground process group
        (best-effort; ignored if the shell has already exited) and drops the session
        from the server's session cache. A subsequent connect with the same session_name
        will create a fresh PTY session.

        Documentation note: this operation is published from mux strictly as an OpenAPI
        contract stub for the PTY service control plane. It is not evidence that mux
        itself serves the interactive PTY transport.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not session_name:
            raise ValueError(f"Expected a non-empty value for `session_name` but received {session_name!r}")
        return self._post(
            path_template("/pty/{session_name}/control", session_name=session_name),
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
            cast_to=PtyControlResultView,
        )


class AsyncPtyResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncPtyResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncPtyResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncPtyResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncPtyResourceWithStreamingResponse(self)

    async def connect(
        self,
        session_name: str,
        *,
        cols: str | Omit = omit,
        rows: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> PtyConnectView:
        """
        Looks up the PTY session identified by the path session*name and either
        reconnects to the existing session or creates it if it does not yet exist. The
        session_name is a client-chosen session identifier, not an opaque server-issued
        ID. It must be non-empty (1..=256 chars) and use only ASCII letters, digits, '-'
        and '*'. A newly created PTY session starts an interactive bash shell on the
        Devbox. Optional cols and rows query parameters apply an initial terminal size
        before any I/O; they must both be present and in the range 1..=1000 to take
        effect. The response returns a PtyConnectView containing connect_url (a
        server-relative path to the WebSocket data plane), idle_ttl_seconds (how long
        this session is retained after the last client disconnects), and the resulting
        cols/rows. The interactive byte stream itself is intentionally not modeled in
        OpenAPI; see the controller-level documentation for the WebSocket close-code
        conventions. The single-attach contract is enforced when a client opens the
        WebSocket data plane, not on this bootstrap call: bootstrap always succeeds for
        a valid session_name, even if another client is currently attached. Rejection of
        a second concurrent attach happens at WebSocket upgrade time. If the active
        client disconnects, the session is preserved for the idle TTL so a later connect
        using the same session_name resumes the same shell. After the TTL expires, after
        an explicit close control action, or after the underlying Devbox lifecycle
        replaces the PTY process (such as through suspend/resume), a later request with
        the same session_name creates a fresh PTY session without the previous shell
        state.

        Documentation note: this operation is published from mux strictly as an OpenAPI
        contract stub for the PTY service control plane. It is not evidence that mux
        itself serves the interactive PTY transport.

        Args:
          cols: Optional initial terminal width in character cells (1..=1000). Defaults to 80
              when omitted. Applied only if both cols and rows are provided; otherwise
              ignored.

          rows: Optional initial terminal height in character cells (1..=1000). Defaults to 24
              when omitted. Applied only if both cols and rows are provided; otherwise
              ignored.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not session_name:
            raise ValueError(f"Expected a non-empty value for `session_name` but received {session_name!r}")
        return await self._get(
            path_template("/pty/{session_name}", session_name=session_name),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "cols": cols,
                        "rows": rows,
                    },
                    pty_connect_params.PtyConnectParams,
                ),
            ),
            cast_to=PtyConnectView,
        )

    async def control(
        self,
        session_name: str,
        *,
        action: Literal["resize", "signal", "close"] | Omit = omit,
        cols: int | Omit = omit,
        rows: int | Omit = omit,
        signal: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> PtyControlResultView:
        """Applies a PTY control operation to an existing session.

        The action field selects
        the operation; the other fields in PtyControlParameters are interpreted only
        when they are relevant to the chosen action.

        resize: cols and rows are required and must each be in 1..=1000. A 0 or
        out-of-range value returns 400. The new winsize is applied to the PTY master and
        the kernel delivers SIGWINCH to the foreground process group.

        signal: signal is the POSIX signal name (for example 'SIGTERM', 'SIGHUP',
        'SIGINT', 'SIGUSR1'). Unknown signal names return 400. The signal is delivered
        to the slave's foreground process group via killpg(2). If the shell has already
        exited and there is no foreground process group, returns 400.

        close: terminates the session. Sends SIGHUP to the foreground process group
        (best-effort; ignored if the shell has already exited) and drops the session
        from the server's session cache. A subsequent connect with the same session_name
        will create a fresh PTY session.

        Documentation note: this operation is published from mux strictly as an OpenAPI
        contract stub for the PTY service control plane. It is not evidence that mux
        itself serves the interactive PTY transport.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not session_name:
            raise ValueError(f"Expected a non-empty value for `session_name` but received {session_name!r}")
        return await self._post(
            path_template("/pty/{session_name}/control", session_name=session_name),
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
            cast_to=PtyControlResultView,
        )


class PtyResourceWithRawResponse:
    def __init__(self, pty: PtyResource) -> None:
        self._pty = pty

        self.connect = to_raw_response_wrapper(
            pty.connect,
        )
        self.control = to_raw_response_wrapper(
            pty.control,
        )


class AsyncPtyResourceWithRawResponse:
    def __init__(self, pty: AsyncPtyResource) -> None:
        self._pty = pty

        self.connect = async_to_raw_response_wrapper(
            pty.connect,
        )
        self.control = async_to_raw_response_wrapper(
            pty.control,
        )


class PtyResourceWithStreamingResponse:
    def __init__(self, pty: PtyResource) -> None:
        self._pty = pty

        self.connect = to_streamed_response_wrapper(
            pty.connect,
        )
        self.control = to_streamed_response_wrapper(
            pty.control,
        )


class AsyncPtyResourceWithStreamingResponse:
    def __init__(self, pty: AsyncPtyResource) -> None:
        self._pty = pty

        self.connect = async_to_streamed_response_wrapper(
            pty.connect,
        )
        self.control = async_to_streamed_response_wrapper(
            pty.control,
        )
