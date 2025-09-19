# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.devboxes import (
    computer_create_params,
    computer_mouse_interaction_params,
    computer_screen_interaction_params,
    computer_keyboard_interaction_params,
)
from ...types.devboxes.computer_view import ComputerView
from ...types.devboxes.computer_mouse_interaction_response import ComputerMouseInteractionResponse
from ...types.devboxes.computer_screen_interaction_response import ComputerScreenInteractionResponse
from ...types.devboxes.computer_keyboard_interaction_response import ComputerKeyboardInteractionResponse

__all__ = ["ComputersResource", "AsyncComputersResource"]


class ComputersResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ComputersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return ComputersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ComputersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return ComputersResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        display_dimensions: Optional[computer_create_params.DisplayDimensions] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerView:
        """Create a Computer and begin the boot process.

        The Computer will initially launch
        in the 'provisioning' state while Runloop allocates the necessary
        infrastructure. It will transition to the 'initializing' state while the booted
        Computer runs any Runloop or user defined set up scripts. Finally, the Computer
        will transition to the 'running' state when it is ready for use.

        Args:
          display_dimensions: Customize the dimensions of the computer display.

          name: The name to use for the created computer.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/devboxes/computers",
            body=maybe_transform(
                {
                    "display_dimensions": display_dimensions,
                    "name": name,
                },
                computer_create_params.ComputerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerView,
        )

    def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComputerView:
        """
        Get Computer Details.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/devboxes/computers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ComputerView,
        )

    def keyboard_interaction(
        self,
        id: str,
        *,
        action: Literal["key", "type"],
        text: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerKeyboardInteractionResponse:
        """
        Perform the specified keyboard interaction on the Computer identified by the
        given ID.

        Args:
          action: The keyboard action to perform.

          text: The text to type or the key (with optional modifier) to press.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/computers/{id}/keyboard_interaction",
            body=maybe_transform(
                {
                    "action": action,
                    "text": text,
                },
                computer_keyboard_interaction_params.ComputerKeyboardInteractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerKeyboardInteractionResponse,
        )

    def mouse_interaction(
        self,
        id: str,
        *,
        action: Literal["mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click"],
        coordinate: Optional[computer_mouse_interaction_params.Coordinate] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerMouseInteractionResponse:
        """
        Perform the specified mouse interaction on the Computer identified by the given
        ID.

        Args:
          action: The mouse action to perform.

          coordinate: The x (pixels from the left) and y (pixels from the top) coordinates for the
              mouse to move or click-drag. Required only by `action=mouse_move` or
              `action=left_click_drag`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/computers/{id}/mouse_interaction",
            body=maybe_transform(
                {
                    "action": action,
                    "coordinate": coordinate,
                },
                computer_mouse_interaction_params.ComputerMouseInteractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerMouseInteractionResponse,
        )

    def screen_interaction(
        self,
        id: str,
        *,
        action: Literal["screenshot", "cursor_position"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerScreenInteractionResponse:
        """
        Perform the specified screen interaction on the Computer identified by the given
        ID.

        Args:
          action: The screen action to perform.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/computers/{id}/screen_interaction",
            body=maybe_transform(
                {"action": action}, computer_screen_interaction_params.ComputerScreenInteractionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerScreenInteractionResponse,
        )


class AsyncComputersResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncComputersResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncComputersResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncComputersResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncComputersResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        display_dimensions: Optional[computer_create_params.DisplayDimensions] | Omit = omit,
        name: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerView:
        """Create a Computer and begin the boot process.

        The Computer will initially launch
        in the 'provisioning' state while Runloop allocates the necessary
        infrastructure. It will transition to the 'initializing' state while the booted
        Computer runs any Runloop or user defined set up scripts. Finally, the Computer
        will transition to the 'running' state when it is ready for use.

        Args:
          display_dimensions: Customize the dimensions of the computer display.

          name: The name to use for the created computer.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/devboxes/computers",
            body=await async_maybe_transform(
                {
                    "display_dimensions": display_dimensions,
                    "name": name,
                },
                computer_create_params.ComputerCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerView,
        )

    async def retrieve(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ComputerView:
        """
        Get Computer Details.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/devboxes/computers/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ComputerView,
        )

    async def keyboard_interaction(
        self,
        id: str,
        *,
        action: Literal["key", "type"],
        text: Optional[str] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerKeyboardInteractionResponse:
        """
        Perform the specified keyboard interaction on the Computer identified by the
        given ID.

        Args:
          action: The keyboard action to perform.

          text: The text to type or the key (with optional modifier) to press.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/computers/{id}/keyboard_interaction",
            body=await async_maybe_transform(
                {
                    "action": action,
                    "text": text,
                },
                computer_keyboard_interaction_params.ComputerKeyboardInteractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerKeyboardInteractionResponse,
        )

    async def mouse_interaction(
        self,
        id: str,
        *,
        action: Literal["mouse_move", "left_click", "left_click_drag", "right_click", "middle_click", "double_click"],
        coordinate: Optional[computer_mouse_interaction_params.Coordinate] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerMouseInteractionResponse:
        """
        Perform the specified mouse interaction on the Computer identified by the given
        ID.

        Args:
          action: The mouse action to perform.

          coordinate: The x (pixels from the left) and y (pixels from the top) coordinates for the
              mouse to move or click-drag. Required only by `action=mouse_move` or
              `action=left_click_drag`

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/computers/{id}/mouse_interaction",
            body=await async_maybe_transform(
                {
                    "action": action,
                    "coordinate": coordinate,
                },
                computer_mouse_interaction_params.ComputerMouseInteractionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerMouseInteractionResponse,
        )

    async def screen_interaction(
        self,
        id: str,
        *,
        action: Literal["screenshot", "cursor_position"],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ComputerScreenInteractionResponse:
        """
        Perform the specified screen interaction on the Computer identified by the given
        ID.

        Args:
          action: The screen action to perform.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/computers/{id}/screen_interaction",
            body=await async_maybe_transform(
                {"action": action}, computer_screen_interaction_params.ComputerScreenInteractionParams
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ComputerScreenInteractionResponse,
        )


class ComputersResourceWithRawResponse:
    def __init__(self, computers: ComputersResource) -> None:
        self._computers = computers

        self.create = to_raw_response_wrapper(
            computers.create,
        )
        self.retrieve = to_raw_response_wrapper(
            computers.retrieve,
        )
        self.keyboard_interaction = to_raw_response_wrapper(
            computers.keyboard_interaction,
        )
        self.mouse_interaction = to_raw_response_wrapper(
            computers.mouse_interaction,
        )
        self.screen_interaction = to_raw_response_wrapper(
            computers.screen_interaction,
        )


class AsyncComputersResourceWithRawResponse:
    def __init__(self, computers: AsyncComputersResource) -> None:
        self._computers = computers

        self.create = async_to_raw_response_wrapper(
            computers.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            computers.retrieve,
        )
        self.keyboard_interaction = async_to_raw_response_wrapper(
            computers.keyboard_interaction,
        )
        self.mouse_interaction = async_to_raw_response_wrapper(
            computers.mouse_interaction,
        )
        self.screen_interaction = async_to_raw_response_wrapper(
            computers.screen_interaction,
        )


class ComputersResourceWithStreamingResponse:
    def __init__(self, computers: ComputersResource) -> None:
        self._computers = computers

        self.create = to_streamed_response_wrapper(
            computers.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            computers.retrieve,
        )
        self.keyboard_interaction = to_streamed_response_wrapper(
            computers.keyboard_interaction,
        )
        self.mouse_interaction = to_streamed_response_wrapper(
            computers.mouse_interaction,
        )
        self.screen_interaction = to_streamed_response_wrapper(
            computers.screen_interaction,
        )


class AsyncComputersResourceWithStreamingResponse:
    def __init__(self, computers: AsyncComputersResource) -> None:
        self._computers = computers

        self.create = async_to_streamed_response_wrapper(
            computers.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            computers.retrieve,
        )
        self.keyboard_interaction = async_to_streamed_response_wrapper(
            computers.keyboard_interaction,
        )
        self.mouse_interaction = async_to_streamed_response_wrapper(
            computers.mouse_interaction,
        )
        self.screen_interaction = async_to_streamed_response_wrapper(
            computers.screen_interaction,
        )
