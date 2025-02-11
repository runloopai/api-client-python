# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import (
    maybe_transform,
    async_maybe_transform,
)
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...pagination import SyncDiskSnapshotsCursorIDPage, AsyncDiskSnapshotsCursorIDPage
from ..._base_client import AsyncPaginator, make_request_options
from ...types.devboxes import disk_snapshot_list_params, disk_snapshot_update_params
from ...types.devbox_snapshot_view import DevboxSnapshotView

__all__ = ["DiskSnapshotsResource", "AsyncDiskSnapshotsResource"]


class DiskSnapshotsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> DiskSnapshotsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return DiskSnapshotsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> DiskSnapshotsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return DiskSnapshotsResourceWithStreamingResponse(self)

    def update(
        self,
        id: str,
        *,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DevboxSnapshotView:
        """Updates disk snapshot metadata via update vs patch.

        The entire metadata will be
        replaced.

        Args:
          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/disk_snapshots/{id}",
            body=maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                disk_snapshot_update_params.DiskSnapshotUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSnapshotView,
        )

    def list(
        self,
        *,
        devbox_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]:
        """
        List all snapshots of a Devbox while optionally filtering by Devbox ID.

        Args:
          devbox_id: Devbox ID to filter by.

          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/devboxes/disk_snapshots",
            page=SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "devbox_id": devbox_id,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    disk_snapshot_list_params.DiskSnapshotListParams,
                ),
            ),
            model=DevboxSnapshotView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Delete a previously taken disk snapshot of a Devbox.

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
            f"/v1/devboxes/disk_snapshots/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )


class AsyncDiskSnapshotsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncDiskSnapshotsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncDiskSnapshotsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncDiskSnapshotsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncDiskSnapshotsResourceWithStreamingResponse(self)

    async def update(
        self,
        id: str,
        *,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DevboxSnapshotView:
        """Updates disk snapshot metadata via update vs patch.

        The entire metadata will be
        replaced.

        Args:
          metadata: (Optional) Metadata used to describe the snapshot

          name: (Optional) A user specified name to give the snapshot

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/disk_snapshots/{id}",
            body=await async_maybe_transform(
                {
                    "metadata": metadata,
                    "name": name,
                },
                disk_snapshot_update_params.DiskSnapshotUpdateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DevboxSnapshotView,
        )

    def list(
        self,
        *,
        devbox_id: str | NotGiven = NOT_GIVEN,
        limit: int | NotGiven = NOT_GIVEN,
        starting_after: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> AsyncPaginator[DevboxSnapshotView, AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]]:
        """
        List all snapshots of a Devbox while optionally filtering by Devbox ID.

        Args:
          devbox_id: Devbox ID to filter by.

          limit: The limit of items to return. Default is 20.

          starting_after: Load the next page of data starting after the item with the given ID.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/devboxes/disk_snapshots",
            page=AsyncDiskSnapshotsCursorIDPage[DevboxSnapshotView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "devbox_id": devbox_id,
                        "limit": limit,
                        "starting_after": starting_after,
                    },
                    disk_snapshot_list_params.DiskSnapshotListParams,
                ),
            ),
            model=DevboxSnapshotView,
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
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> object:
        """
        Delete a previously taken disk snapshot of a Devbox.

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
            f"/v1/devboxes/disk_snapshots/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=object,
        )


class DiskSnapshotsResourceWithRawResponse:
    def __init__(self, disk_snapshots: DiskSnapshotsResource) -> None:
        self._disk_snapshots = disk_snapshots

        self.update = to_raw_response_wrapper(
            disk_snapshots.update,
        )
        self.list = to_raw_response_wrapper(
            disk_snapshots.list,
        )
        self.delete = to_raw_response_wrapper(
            disk_snapshots.delete,
        )


class AsyncDiskSnapshotsResourceWithRawResponse:
    def __init__(self, disk_snapshots: AsyncDiskSnapshotsResource) -> None:
        self._disk_snapshots = disk_snapshots

        self.update = async_to_raw_response_wrapper(
            disk_snapshots.update,
        )
        self.list = async_to_raw_response_wrapper(
            disk_snapshots.list,
        )
        self.delete = async_to_raw_response_wrapper(
            disk_snapshots.delete,
        )


class DiskSnapshotsResourceWithStreamingResponse:
    def __init__(self, disk_snapshots: DiskSnapshotsResource) -> None:
        self._disk_snapshots = disk_snapshots

        self.update = to_streamed_response_wrapper(
            disk_snapshots.update,
        )
        self.list = to_streamed_response_wrapper(
            disk_snapshots.list,
        )
        self.delete = to_streamed_response_wrapper(
            disk_snapshots.delete,
        )


class AsyncDiskSnapshotsResourceWithStreamingResponse:
    def __init__(self, disk_snapshots: AsyncDiskSnapshotsResource) -> None:
        self._disk_snapshots = disk_snapshots

        self.update = async_to_streamed_response_wrapper(
            disk_snapshots.update,
        )
        self.list = async_to_streamed_response_wrapper(
            disk_snapshots.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            disk_snapshots.delete,
        )
