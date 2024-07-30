# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Iterable

import httpx

from ..types import blueprint_list_params, blueprint_create_params, blueprint_preview_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.blueprint_view import BlueprintView
from ..types.blueprint_list_view import BlueprintListView
from ..types.blueprint_preview_view import BlueprintPreviewView
from ..types.code_mount_parameters_param import CodeMountParametersParam
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView

__all__ = ["BlueprintsResource", "AsyncBlueprintsResource"]


class BlueprintsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BlueprintsResourceWithRawResponse:
        return BlueprintsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BlueprintsResourceWithStreamingResponse:
        return BlueprintsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        code_mounts: Iterable[CodeMountParametersParam] | NotGiven = NOT_GIVEN,
        dockerfile: str | NotGiven = NOT_GIVEN,
        launch_parameters: blueprint_create_params.LaunchParameters | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        system_setup_commands: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintView:
        """Build a Blueprint with the specified configuration.

        The Blueprint will begin
        building upon create, ' and will transition to 'building_complete' once it is
        ready.

        Args:
          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          launch_parameters: Parameters to configure your Devbox at launch time.

          name: Name of the Blueprint.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/blueprints",
            body=maybe_transform(
                {
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "launch_parameters": launch_parameters,
                    "name": name,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_create_params.BlueprintCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintView:
        """
        Get a previously built Blueprint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/blueprints/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintView,
        )

    def list(
        self,
        *,
        limit: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintListView:
        """List all blueprints or filter by name.

        If no status is provided, all blueprints
        are returned.

        Args:
          limit: Page Limit

          name: Filter by name

          starting_after: Load the next page starting after the given token.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get(
            "/v1/blueprints",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    blueprint_list_params.BlueprintListParams,
                ),
            ),
            cast_to=BlueprintListView,
        )

    def logs(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintBuildLogsListView:
        """
        Get Blueprint build logs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/blueprints/{id}/logs",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintBuildLogsListView,
        )

    def preview(
        self,
        *,
        code_mounts: Iterable[CodeMountParametersParam] | NotGiven = NOT_GIVEN,
        dockerfile: str | NotGiven = NOT_GIVEN,
        launch_parameters: blueprint_preview_params.LaunchParameters | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        system_setup_commands: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintPreviewView:
        """Preview building a Blueprint with the specified configuration.

        You can take the
        resulting Dockerfile and test out your build.

        Args:
          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          launch_parameters: Parameters to configure your Devbox at launch time.

          name: Name of the Blueprint.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/blueprints/preview",
            body=maybe_transform(
                {
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "launch_parameters": launch_parameters,
                    "name": name,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_preview_params.BlueprintPreviewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintPreviewView,
        )


class AsyncBlueprintsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBlueprintsResourceWithRawResponse:
        return AsyncBlueprintsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBlueprintsResourceWithStreamingResponse:
        return AsyncBlueprintsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        code_mounts: Iterable[CodeMountParametersParam] | NotGiven = NOT_GIVEN,
        dockerfile: str | NotGiven = NOT_GIVEN,
        launch_parameters: blueprint_create_params.LaunchParameters | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        system_setup_commands: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintView:
        """Build a Blueprint with the specified configuration.

        The Blueprint will begin
        building upon create, ' and will transition to 'building_complete' once it is
        ready.

        Args:
          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          launch_parameters: Parameters to configure your Devbox at launch time.

          name: Name of the Blueprint.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/blueprints",
            body=await async_maybe_transform(
                {
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "launch_parameters": launch_parameters,
                    "name": name,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_create_params.BlueprintCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintView:
        """
        Get a previously built Blueprint.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/blueprints/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintView,
        )

    async def list(
        self,
        *,
        limit: str | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintListView:
        """List all blueprints or filter by name.

        If no status is provided, all blueprints
        are returned.

        Args:
          limit: Page Limit

          name: Filter by name

          starting_after: Load the next page starting after the given token.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._get(
            "/v1/blueprints",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {
                        "limit": limit,
                        "name": name,
                        "starting_after": starting_after,
                    },
                    blueprint_list_params.BlueprintListParams,
                ),
            ),
            cast_to=BlueprintListView,
        )

    async def logs(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintBuildLogsListView:
        """
        Get Blueprint build logs.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/blueprints/{id}/logs",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintBuildLogsListView,
        )

    async def preview(
        self,
        *,
        code_mounts: Iterable[CodeMountParametersParam] | NotGiven = NOT_GIVEN,
        dockerfile: str | NotGiven = NOT_GIVEN,
        launch_parameters: blueprint_preview_params.LaunchParameters | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        system_setup_commands: List[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> BlueprintPreviewView:
        """Preview building a Blueprint with the specified configuration.

        You can take the
        resulting Dockerfile and test out your build.

        Args:
          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          launch_parameters: Parameters to configure your Devbox at launch time.

          name: Name of the Blueprint.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/blueprints/preview",
            body=await async_maybe_transform(
                {
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "launch_parameters": launch_parameters,
                    "name": name,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_preview_params.BlueprintPreviewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=BlueprintPreviewView,
        )


class BlueprintsResourceWithRawResponse:
    def __init__(self, blueprints: BlueprintsResource) -> None:
        self._blueprints = blueprints

        self.create = to_raw_response_wrapper(
            blueprints.create,
        )
        self.retrieve = to_raw_response_wrapper(
            blueprints.retrieve,
        )
        self.list = to_raw_response_wrapper(
            blueprints.list,
        )
        self.logs = to_raw_response_wrapper(
            blueprints.logs,
        )
        self.preview = to_raw_response_wrapper(
            blueprints.preview,
        )


class AsyncBlueprintsResourceWithRawResponse:
    def __init__(self, blueprints: AsyncBlueprintsResource) -> None:
        self._blueprints = blueprints

        self.create = async_to_raw_response_wrapper(
            blueprints.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            blueprints.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            blueprints.list,
        )
        self.logs = async_to_raw_response_wrapper(
            blueprints.logs,
        )
        self.preview = async_to_raw_response_wrapper(
            blueprints.preview,
        )


class BlueprintsResourceWithStreamingResponse:
    def __init__(self, blueprints: BlueprintsResource) -> None:
        self._blueprints = blueprints

        self.create = to_streamed_response_wrapper(
            blueprints.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            blueprints.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            blueprints.list,
        )
        self.logs = to_streamed_response_wrapper(
            blueprints.logs,
        )
        self.preview = to_streamed_response_wrapper(
            blueprints.preview,
        )


class AsyncBlueprintsResourceWithStreamingResponse:
    def __init__(self, blueprints: AsyncBlueprintsResource) -> None:
        self._blueprints = blueprints

        self.create = async_to_streamed_response_wrapper(
            blueprints.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            blueprints.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            blueprints.list,
        )
        self.logs = async_to_streamed_response_wrapper(
            blueprints.logs,
        )
        self.preview = async_to_streamed_response_wrapper(
            blueprints.preview,
        )
