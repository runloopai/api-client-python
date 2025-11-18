# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional

import httpx

from ..types import (
    blueprint_list_params,
    blueprint_create_params,
    blueprint_preview_params,
    blueprint_list_public_params,
    blueprint_create_from_inspection_params,
)
from .._types import Body, Omit, Query, Headers, NotGiven, SequenceNotStr, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
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
from ..types.inspection_source_param import InspectionSourceParam
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
        base_blueprint_id: Optional[str] | Omit = omit,
        base_blueprint_name: Optional[str] | Omit = omit,
        build_args: Optional[Dict[str, str]] | Omit = omit,
        build_contexts: Optional[Dict[str, blueprint_create_params.BuildContexts]] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        dockerfile: Optional[str] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        local_build_context: Optional[blueprint_create_params.LocalBuildContext] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        services: Optional[Iterable[blueprint_create_params.Service]] | Omit = omit,
        system_setup_commands: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BlueprintView:
        """Starts build of custom defined container Blueprint.

        The Blueprint will begin in
        the 'provisioning' step and transition to the 'building' step once it is
        selected off the build queue., Upon build complete it will transition to
        'building_complete' if the build is successful.

        Args:
          name: Name of the Blueprint.

          base_blueprint_id: (Optional) ID of previously built blueprint to use as a base blueprint for this
              build.

          base_blueprint_name: (Optional) Name of previously built blueprint to use as a base blueprint for
              this build. When set, this will load the latest successfully built Blueprint
              with the given name. Only one of (base_blueprint_id, base_blueprint_name) should
              be specified.

          build_args: (Optional) Arbitrary Docker build args to pass during build.

          build_contexts: (Optional) Map of named Docker build contexts. Keys are context names, values
              are typed context definitions (object or http). See Docker buildx additional
              contexts for details:
              https://docs.docker.com/reference/cli/docker/buildx/build/#build-context

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup.

          launch_parameters: Parameters to configure your Devbox at launch time.

          local_build_context: (Optional) Local build context stored in object-storage.

          metadata: (Optional) User defined metadata for the Blueprint.

          secrets: (Optional) Map of mount IDs/environment variable names to secret names. Secrets
              will be available to commands during the build. Secrets are NOT stored in the
              blueprint image. Example: {"DB_PASS": "DATABASE_PASSWORD"} makes the secret
              'DATABASE_PASSWORD' available as environment variable 'DB_PASS'.

          services: (Optional) List of containerized services to include in the Blueprint. These
              services will be pre-pulled during the build phase for optimized startup
              performance.

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
                    "base_blueprint_id": base_blueprint_id,
                    "base_blueprint_name": base_blueprint_name,
                    "build_args": build_args,
                    "build_contexts": build_contexts,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "local_build_context": local_build_context,
                    "metadata": metadata,
                    "secrets": secrets,
                    "services": services,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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

    def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """Delete a previously created Blueprint.

        If a blueprint has dependent snapshots,
        it cannot be deleted. You can find them by querying: GET
        /v1/devboxes/disk_snapshots?source_blueprint_id={blueprint_id}.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/blueprints/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    def create_from_inspection(
        self,
        *,
        inspection_source: InspectionSourceParam,
        name: str,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        system_setup_commands: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BlueprintView:
        """
        Starts build of custom defined container Blueprint using a RepositoryConnection
        Inspection as a source container specification.

        Args:
          inspection_source: (Optional) Use a RepositoryInspection a source of a Blueprint build. The
              Dockerfile will be automatically created based on the RepositoryInspection
              contents.

          name: Name of the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup.

          launch_parameters: Parameters to configure your Devbox at launch time.

          metadata: (Optional) User defined metadata for the Blueprint.

          secrets: (Optional) Map of mount IDs/environment variable names to secret names. Secrets
              can be used as environment variables in system_setup_commands. Example:
              {"GITHUB_TOKEN": "gh_secret"} makes 'gh_secret' available as GITHUB_TOKEN.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/blueprints/create_from_inspection",
            body=maybe_transform(
                {
                    "inspection_source": inspection_source,
                    "name": name,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "metadata": metadata,
                    "secrets": secrets,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_create_from_inspection_params.BlueprintCreateFromInspectionParams,
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

    def list_public(
        self,
        *,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncBlueprintsCursorIDPage[BlueprintView]:
        """
        List all public Blueprints that are available to all users.

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
            "/v1/blueprints/list_public",
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
                    blueprint_list_public_params.BlueprintListPublicParams,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
        base_blueprint_id: Optional[str] | Omit = omit,
        base_blueprint_name: Optional[str] | Omit = omit,
        build_args: Optional[Dict[str, str]] | Omit = omit,
        build_contexts: Optional[Dict[str, blueprint_preview_params.BuildContexts]] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        dockerfile: Optional[str] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        local_build_context: Optional[blueprint_preview_params.LocalBuildContext] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        services: Optional[Iterable[blueprint_preview_params.Service]] | Omit = omit,
        system_setup_commands: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BlueprintPreviewView:
        """Preview building a Blueprint with the specified configuration.

        You can take the
        resulting Dockerfile and test out your build using any local docker tooling.

        Args:
          name: Name of the Blueprint.

          base_blueprint_id: (Optional) ID of previously built blueprint to use as a base blueprint for this
              build.

          base_blueprint_name: (Optional) Name of previously built blueprint to use as a base blueprint for
              this build. When set, this will load the latest successfully built Blueprint
              with the given name. Only one of (base_blueprint_id, base_blueprint_name) should
              be specified.

          build_args: (Optional) Arbitrary Docker build args to pass during build.

          build_contexts: (Optional) Map of named Docker build contexts. Keys are context names, values
              are typed context definitions (object or http). See Docker buildx additional
              contexts for details:
              https://docs.docker.com/reference/cli/docker/buildx/build/#build-context

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup.

          launch_parameters: Parameters to configure your Devbox at launch time.

          local_build_context: (Optional) Local build context stored in object-storage.

          metadata: (Optional) User defined metadata for the Blueprint.

          secrets: (Optional) Map of mount IDs/environment variable names to secret names. Secrets
              will be available to commands during the build. Secrets are NOT stored in the
              blueprint image. Example: {"DB_PASS": "DATABASE_PASSWORD"} makes the secret
              'DATABASE_PASSWORD' available as environment variable 'DB_PASS'.

          services: (Optional) List of containerized services to include in the Blueprint. These
              services will be pre-pulled during the build phase for optimized startup
              performance.

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
                    "base_blueprint_id": base_blueprint_id,
                    "base_blueprint_name": base_blueprint_name,
                    "build_args": build_args,
                    "build_contexts": build_contexts,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "local_build_context": local_build_context,
                    "metadata": metadata,
                    "secrets": secrets,
                    "services": services,
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
        base_blueprint_id: Optional[str] | Omit = omit,
        base_blueprint_name: Optional[str] | Omit = omit,
        build_args: Optional[Dict[str, str]] | Omit = omit,
        build_contexts: Optional[Dict[str, blueprint_create_params.BuildContexts]] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        dockerfile: Optional[str] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        local_build_context: Optional[blueprint_create_params.LocalBuildContext] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        services: Optional[Iterable[blueprint_create_params.Service]] | Omit = omit,
        system_setup_commands: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BlueprintView:
        """Starts build of custom defined container Blueprint.

        The Blueprint will begin in
        the 'provisioning' step and transition to the 'building' step once it is
        selected off the build queue., Upon build complete it will transition to
        'building_complete' if the build is successful.

        Args:
          name: Name of the Blueprint.

          base_blueprint_id: (Optional) ID of previously built blueprint to use as a base blueprint for this
              build.

          base_blueprint_name: (Optional) Name of previously built blueprint to use as a base blueprint for
              this build. When set, this will load the latest successfully built Blueprint
              with the given name. Only one of (base_blueprint_id, base_blueprint_name) should
              be specified.

          build_args: (Optional) Arbitrary Docker build args to pass during build.

          build_contexts: (Optional) Map of named Docker build contexts. Keys are context names, values
              are typed context definitions (object or http). See Docker buildx additional
              contexts for details:
              https://docs.docker.com/reference/cli/docker/buildx/build/#build-context

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup.

          launch_parameters: Parameters to configure your Devbox at launch time.

          local_build_context: (Optional) Local build context stored in object-storage.

          metadata: (Optional) User defined metadata for the Blueprint.

          secrets: (Optional) Map of mount IDs/environment variable names to secret names. Secrets
              will be available to commands during the build. Secrets are NOT stored in the
              blueprint image. Example: {"DB_PASS": "DATABASE_PASSWORD"} makes the secret
              'DATABASE_PASSWORD' available as environment variable 'DB_PASS'.

          services: (Optional) List of containerized services to include in the Blueprint. These
              services will be pre-pulled during the build phase for optimized startup
              performance.

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
                    "base_blueprint_id": base_blueprint_id,
                    "base_blueprint_name": base_blueprint_name,
                    "build_args": build_args,
                    "build_contexts": build_contexts,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "local_build_context": local_build_context,
                    "metadata": metadata,
                    "secrets": secrets,
                    "services": services,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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

    async def delete(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        """Delete a previously created Blueprint.

        If a blueprint has dependent snapshots,
        it cannot be deleted. You can find them by querying: GET
        /v1/devboxes/disk_snapshots?source_blueprint_id={blueprint_id}.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/blueprints/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )

    async def create_from_inspection(
        self,
        *,
        inspection_source: InspectionSourceParam,
        name: str,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        system_setup_commands: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BlueprintView:
        """
        Starts build of custom defined container Blueprint using a RepositoryConnection
        Inspection as a source container specification.

        Args:
          inspection_source: (Optional) Use a RepositoryInspection a source of a Blueprint build. The
              Dockerfile will be automatically created based on the RepositoryInspection
              contents.

          name: Name of the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup.

          launch_parameters: Parameters to configure your Devbox at launch time.

          metadata: (Optional) User defined metadata for the Blueprint.

          secrets: (Optional) Map of mount IDs/environment variable names to secret names. Secrets
              can be used as environment variables in system_setup_commands. Example:
              {"GITHUB_TOKEN": "gh_secret"} makes 'gh_secret' available as GITHUB_TOKEN.

          system_setup_commands: A list of commands to run to set up your system.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/blueprints/create_from_inspection",
            body=await async_maybe_transform(
                {
                    "inspection_source": inspection_source,
                    "name": name,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "metadata": metadata,
                    "secrets": secrets,
                    "system_setup_commands": system_setup_commands,
                },
                blueprint_create_from_inspection_params.BlueprintCreateFromInspectionParams,
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

    def list_public(
        self,
        *,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        starting_after: str | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[BlueprintView, AsyncBlueprintsCursorIDPage[BlueprintView]]:
        """
        List all public Blueprints that are available to all users.

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
            "/v1/blueprints/list_public",
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
                    blueprint_list_public_params.BlueprintListPublicParams,
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
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
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
        base_blueprint_id: Optional[str] | Omit = omit,
        base_blueprint_name: Optional[str] | Omit = omit,
        build_args: Optional[Dict[str, str]] | Omit = omit,
        build_contexts: Optional[Dict[str, blueprint_preview_params.BuildContexts]] | Omit = omit,
        code_mounts: Optional[Iterable[CodeMountParameters]] | Omit = omit,
        dockerfile: Optional[str] | Omit = omit,
        file_mounts: Optional[Dict[str, str]] | Omit = omit,
        launch_parameters: Optional[LaunchParameters] | Omit = omit,
        local_build_context: Optional[blueprint_preview_params.LocalBuildContext] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        secrets: Optional[Dict[str, str]] | Omit = omit,
        services: Optional[Iterable[blueprint_preview_params.Service]] | Omit = omit,
        system_setup_commands: Optional[SequenceNotStr[str]] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> BlueprintPreviewView:
        """Preview building a Blueprint with the specified configuration.

        You can take the
        resulting Dockerfile and test out your build using any local docker tooling.

        Args:
          name: Name of the Blueprint.

          base_blueprint_id: (Optional) ID of previously built blueprint to use as a base blueprint for this
              build.

          base_blueprint_name: (Optional) Name of previously built blueprint to use as a base blueprint for
              this build. When set, this will load the latest successfully built Blueprint
              with the given name. Only one of (base_blueprint_id, base_blueprint_name) should
              be specified.

          build_args: (Optional) Arbitrary Docker build args to pass during build.

          build_contexts: (Optional) Map of named Docker build contexts. Keys are context names, values
              are typed context definitions (object or http). See Docker buildx additional
              contexts for details:
              https://docs.docker.com/reference/cli/docker/buildx/build/#build-context

          code_mounts: A list of code mounts to be included in the Blueprint.

          dockerfile: Dockerfile contents to be used to build the Blueprint.

          file_mounts: (Optional) Map of paths and file contents to write before setup.

          launch_parameters: Parameters to configure your Devbox at launch time.

          local_build_context: (Optional) Local build context stored in object-storage.

          metadata: (Optional) User defined metadata for the Blueprint.

          secrets: (Optional) Map of mount IDs/environment variable names to secret names. Secrets
              will be available to commands during the build. Secrets are NOT stored in the
              blueprint image. Example: {"DB_PASS": "DATABASE_PASSWORD"} makes the secret
              'DATABASE_PASSWORD' available as environment variable 'DB_PASS'.

          services: (Optional) List of containerized services to include in the Blueprint. These
              services will be pre-pulled during the build phase for optimized startup
              performance.

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
                    "base_blueprint_id": base_blueprint_id,
                    "base_blueprint_name": base_blueprint_name,
                    "build_args": build_args,
                    "build_contexts": build_contexts,
                    "code_mounts": code_mounts,
                    "dockerfile": dockerfile,
                    "file_mounts": file_mounts,
                    "launch_parameters": launch_parameters,
                    "local_build_context": local_build_context,
                    "metadata": metadata,
                    "secrets": secrets,
                    "services": services,
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
        self.delete = to_raw_response_wrapper(
            blueprints.delete,
        )
        self.create_from_inspection = to_raw_response_wrapper(
            blueprints.create_from_inspection,
        )
        self.list_public = to_raw_response_wrapper(
            blueprints.list_public,
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
        self.delete = async_to_raw_response_wrapper(
            blueprints.delete,
        )
        self.create_from_inspection = async_to_raw_response_wrapper(
            blueprints.create_from_inspection,
        )
        self.list_public = async_to_raw_response_wrapper(
            blueprints.list_public,
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
        self.delete = to_streamed_response_wrapper(
            blueprints.delete,
        )
        self.create_from_inspection = to_streamed_response_wrapper(
            blueprints.create_from_inspection,
        )
        self.list_public = to_streamed_response_wrapper(
            blueprints.list_public,
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
        self.delete = async_to_streamed_response_wrapper(
            blueprints.delete,
        )
        self.create_from_inspection = async_to_streamed_response_wrapper(
            blueprints.create_from_inspection,
        )
        self.list_public = async_to_streamed_response_wrapper(
            blueprints.list_public,
        )
        self.logs = async_to_streamed_response_wrapper(
            blueprints.logs,
        )
        self.preview = async_to_streamed_response_wrapper(
            blueprints.preview,
        )
