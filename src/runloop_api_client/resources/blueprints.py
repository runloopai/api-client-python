# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable, Optional

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
from ..pagination import SyncBlueprintsCursorIDPage, AsyncBlueprintsCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.blueprint_view import BlueprintView
from ..types.blueprint_preview_view import BlueprintPreviewView
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView
from ..types.shared_params.launch_parameters import LaunchParameters
from ..types.shared_params.code_mount_parameters import CodeMountParameters

__all__ = ["BlueprintsResource", "AsyncBlueprintsResource"]


class BlueprintsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> BlueprintsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return BlueprintsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> BlueprintsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return BlueprintsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        name: str,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        dockerfile: Optional[str] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        system_setup_commands: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BlueprintView:
        """Starts build of custom defined container Blueprint.

        The Blueprint will begin in
        the 'provisioning' step and transition to the 'building' step once it is
        selected off the build queue., Upon build complete it will transition to
        'building_complete' if the build is successful.

        Args:
          name: Name of the Blueprint.

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure your Devbox at launch time.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/blueprints",
            body=maybe_transform(
                {
                    "name": name,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_create_params.BlueprintCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
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
        Get the details of a previously created Blueprint including the build status.

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
        limit: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncBlueprintsCursorIDPage[BlueprintView]:
        """
        List all Blueprints or filter by name.

        Args:
          limit: The limit of items to return. Default is 20.

          name: Filter by name

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/blueprints",
            page=SyncBlueprintsCursorIDPage[BlueprintView],
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
            model=BlueprintView,
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
        Get all logs from the building of a Blueprint.

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
        name: str,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        dockerfile: Optional[str] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        system_setup_commands: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BlueprintPreviewView:
        """Preview building a Blueprint with the specified configuration.

        You can take the
        resulting Dockerfile and test out your build using any local docker tooling.

        Args:
          name: Name of the Blueprint.

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure your Devbox at launch time.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/blueprints/preview",
            body=maybe_transform(
                {
                    "name": name,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_preview_params.BlueprintPreviewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=BlueprintPreviewView,
        )


class AsyncBlueprintsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncBlueprintsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncBlueprintsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncBlueprintsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncBlueprintsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        name: str,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        dockerfile: Optional[str] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        system_setup_commands: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BlueprintView:
        """Starts build of custom defined container Blueprint.

        The Blueprint will begin in
        the 'provisioning' step and transition to the 'building' step once it is
        selected off the build queue., Upon build complete it will transition to
        'building_complete' if the build is successful.

        Args:
          name: Name of the Blueprint.

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure your Devbox at launch time.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/blueprints",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_create_params.BlueprintCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
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
        Get the details of a previously created Blueprint including the build status.

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

    def list(
        self,
        *,
        limit: int | NotGiven = NOT_GIVEN,
        name: str | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[BlueprintView, AsyncBlueprintsCursorIDPage[BlueprintView]]:
        """
        List all Blueprints or filter by name.

        Args:
          limit: The limit of items to return. Default is 20.

          name: Filter by name

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/blueprints",
            page=AsyncBlueprintsCursorIDPage[BlueprintView],
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
            model=BlueprintView,
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
        Get all logs from the building of a Blueprint.

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
        name: str,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        dockerfile: Optional[str] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        system_setup_commands: Optional[List[str]] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> BlueprintPreviewView:
        """Preview building a Blueprint with the specified configuration.

        You can take the
        resulting Dockerfile and test out your build using any local docker tooling.

        Args:
          name: Name of the Blueprint.

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup..

          launch_parameters: Parameters to configure your Devbox at launch time.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/blueprints/preview",
            body=await async_maybe_transform(
                {
                    "name": name,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_preview_params.BlueprintPreviewParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
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
