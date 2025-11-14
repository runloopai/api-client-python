# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Literal

import httpx

from ..types import object_list_params, object_create_params, object_download_params, object_list_public_params
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
from ..pagination import SyncObjectsCursorIDPage, AsyncObjectsCursorIDPage
from .._base_client import AsyncPaginator, make_request_options
from ..types.object_view import ObjectView
from ..types.object_download_url_view import ObjectDownloadURLView

__all__ = ["ObjectsResource", "AsyncObjectsResource"]


class ObjectsResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> ObjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return ObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> ObjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return ObjectsResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"],
        name: str,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        ttl_ms: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ObjectView:
        """Create a new Object with content and metadata.

        The Object will be assigned a
        unique ID.

        Args:
          content_type: The content type of the Object.

          name: The name of the Object.

          metadata: User defined metadata to attach to the object for organization.

          ttl_ms: Optional lifetime of the object in milliseconds, after which the object is
              automatically deleted. Time starts ticking after the object is created.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return self._post(
            "/v1/objects",
            body=maybe_transform(
                {
                    "content_type": content_type,
                    "name": name,
                    "metadata": metadata,
                    "ttl_ms": ttl_ms,
                },
                object_create_params.ObjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ObjectView,
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
    ) -> ObjectView:
        """
        Retrieve a specific Object by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/objects/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectView,
        )

    def list(
        self,
        *,
        content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"] | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        search: str | Omit = omit,
        starting_after: str | Omit = omit,
        state: Literal["UPLOADING", "READ_ONLY", "DELETED", "ERROR"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncObjectsCursorIDPage[ObjectView]:
        """
        List all Objects for the authenticated account with pagination support.

        Args:
          content_type: Filter storage objects by content type.

          limit: The limit of items to return. Default is 20.

          name: Filter storage objects by name (partial match supported).

          search: Search by object ID or name.

          starting_after: Load the next page of data starting after the item with the given ID.

          state: Filter storage objects by state.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/objects",
            page=SyncObjectsCursorIDPage[ObjectView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "content_type": content_type,
                        "limit": limit,
                        "name": name,
                        "search": search,
                        "starting_after": starting_after,
                        "state": state,
                    },
                    object_list_params.ObjectListParams,
                ),
            ),
            model=ObjectView,
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
    ) -> ObjectView:
        """Delete an existing Object by ID.

        This action is irreversible and will remove the
        Object and all its metadata.

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
            f"/v1/objects/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ObjectView,
        )

    def complete(
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
    ) -> ObjectView:
        """
        Mark an Object's upload as complete, transitioning it from UPLOADING to
        READ-only state.

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
            f"/v1/objects/{id}/complete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ObjectView,
        )

    def download(
        self,
        id: str,
        *,
        duration_seconds: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectDownloadURLView:
        """Generate a presigned download URL for an Object.

        The URL will be valid for the
        specified duration.

        Args:
          duration_seconds: Duration in seconds for the presigned URL validity (default: 3600).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/objects/{id}/download",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {"duration_seconds": duration_seconds}, object_download_params.ObjectDownloadParams
                ),
            ),
            cast_to=ObjectDownloadURLView,
        )

    def list_public(
        self,
        *,
        content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"] | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        search: str | Omit = omit,
        starting_after: str | Omit = omit,
        state: Literal["UPLOADING", "READ_ONLY", "DELETED", "ERROR"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> SyncObjectsCursorIDPage[ObjectView]:
        """
        List all public Objects with pagination support.

        Args:
          content_type: Filter storage objects by content type.

          limit: The limit of items to return. Default is 20.

          name: Filter storage objects by name (partial match supported).

          search: Search by object ID or name.

          starting_after: Load the next page of data starting after the item with the given ID.

          state: Filter storage objects by state.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/objects/list_public",
            page=SyncObjectsCursorIDPage[ObjectView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "content_type": content_type,
                        "limit": limit,
                        "name": name,
                        "search": search,
                        "starting_after": starting_after,
                        "state": state,
                    },
                    object_list_public_params.ObjectListPublicParams,
                ),
            ),
            model=ObjectView,
        )


class AsyncObjectsResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncObjectsResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncObjectsResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncObjectsResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncObjectsResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"],
        name: str,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        ttl_ms: Optional[int] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> ObjectView:
        """Create a new Object with content and metadata.

        The Object will be assigned a
        unique ID.

        Args:
          content_type: The content type of the Object.

          name: The name of the Object.

          metadata: User defined metadata to attach to the object for organization.

          ttl_ms: Optional lifetime of the object in milliseconds, after which the object is
              automatically deleted. Time starts ticking after the object is created.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        return await self._post(
            "/v1/objects",
            body=await async_maybe_transform(
                {
                    "content_type": content_type,
                    "name": name,
                    "metadata": metadata,
                    "ttl_ms": ttl_ms,
                },
                object_create_params.ObjectCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ObjectView,
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
    ) -> ObjectView:
        """
        Retrieve a specific Object by its unique identifier.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/objects/{id}",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=ObjectView,
        )

    def list(
        self,
        *,
        content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"] | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        search: str | Omit = omit,
        starting_after: str | Omit = omit,
        state: Literal["UPLOADING", "READ_ONLY", "DELETED", "ERROR"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ObjectView, AsyncObjectsCursorIDPage[ObjectView]]:
        """
        List all Objects for the authenticated account with pagination support.

        Args:
          content_type: Filter storage objects by content type.

          limit: The limit of items to return. Default is 20.

          name: Filter storage objects by name (partial match supported).

          search: Search by object ID or name.

          starting_after: Load the next page of data starting after the item with the given ID.

          state: Filter storage objects by state.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/objects",
            page=AsyncObjectsCursorIDPage[ObjectView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "content_type": content_type,
                        "limit": limit,
                        "name": name,
                        "search": search,
                        "starting_after": starting_after,
                        "state": state,
                    },
                    object_list_params.ObjectListParams,
                ),
            ),
            model=ObjectView,
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
    ) -> ObjectView:
        """Delete an existing Object by ID.

        This action is irreversible and will remove the
        Object and all its metadata.

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
            f"/v1/objects/{id}/delete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ObjectView,
        )

    async def complete(
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
    ) -> ObjectView:
        """
        Mark an Object's upload as complete, transitioning it from UPLOADING to
        READ-only state.

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
            f"/v1/objects/{id}/complete",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ObjectView,
        )

    async def download(
        self,
        id: str,
        *,
        duration_seconds: int | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> ObjectDownloadURLView:
        """Generate a presigned download URL for an Object.

        The URL will be valid for the
        specified duration.

        Args:
          duration_seconds: Duration in seconds for the presigned URL validity (default: 3600).

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/objects/{id}/download",
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=await async_maybe_transform(
                    {"duration_seconds": duration_seconds}, object_download_params.ObjectDownloadParams
                ),
            ),
            cast_to=ObjectDownloadURLView,
        )

    def list_public(
        self,
        *,
        content_type: Literal["unspecified", "text", "binary", "gzip", "tar", "tgz"] | Omit = omit,
        limit: int | Omit = omit,
        name: str | Omit = omit,
        search: str | Omit = omit,
        starting_after: str | Omit = omit,
        state: Literal["UPLOADING", "READ_ONLY", "DELETED", "ERROR"] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> AsyncPaginator[ObjectView, AsyncObjectsCursorIDPage[ObjectView]]:
        """
        List all public Objects with pagination support.

        Args:
          content_type: Filter storage objects by content type.

          limit: The limit of items to return. Default is 20.

          name: Filter storage objects by name (partial match supported).

          search: Search by object ID or name.

          starting_after: Load the next page of data starting after the item with the given ID.

          state: Filter storage objects by state.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._get_api_list(
            "/v1/objects/list_public",
            page=AsyncObjectsCursorIDPage[ObjectView],
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                query=maybe_transform(
                    {
                        "content_type": content_type,
                        "limit": limit,
                        "name": name,
                        "search": search,
                        "starting_after": starting_after,
                        "state": state,
                    },
                    object_list_public_params.ObjectListPublicParams,
                ),
            ),
            model=ObjectView,
        )


class ObjectsResourceWithRawResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.create = to_raw_response_wrapper(
            objects.create,
        )
        self.retrieve = to_raw_response_wrapper(
            objects.retrieve,
        )
        self.list = to_raw_response_wrapper(
            objects.list,
        )
        self.delete = to_raw_response_wrapper(
            objects.delete,
        )
        self.complete = to_raw_response_wrapper(
            objects.complete,
        )
        self.download = to_raw_response_wrapper(
            objects.download,
        )
        self.list_public = to_raw_response_wrapper(
            objects.list_public,
        )


class AsyncObjectsResourceWithRawResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.create = async_to_raw_response_wrapper(
            objects.create,
        )
        self.retrieve = async_to_raw_response_wrapper(
            objects.retrieve,
        )
        self.list = async_to_raw_response_wrapper(
            objects.list,
        )
        self.delete = async_to_raw_response_wrapper(
            objects.delete,
        )
        self.complete = async_to_raw_response_wrapper(
            objects.complete,
        )
        self.download = async_to_raw_response_wrapper(
            objects.download,
        )
        self.list_public = async_to_raw_response_wrapper(
            objects.list_public,
        )


class ObjectsResourceWithStreamingResponse:
    def __init__(self, objects: ObjectsResource) -> None:
        self._objects = objects

        self.create = to_streamed_response_wrapper(
            objects.create,
        )
        self.retrieve = to_streamed_response_wrapper(
            objects.retrieve,
        )
        self.list = to_streamed_response_wrapper(
            objects.list,
        )
        self.delete = to_streamed_response_wrapper(
            objects.delete,
        )
        self.complete = to_streamed_response_wrapper(
            objects.complete,
        )
        self.download = to_streamed_response_wrapper(
            objects.download,
        )
        self.list_public = to_streamed_response_wrapper(
            objects.list_public,
        )


class AsyncObjectsResourceWithStreamingResponse:
    def __init__(self, objects: AsyncObjectsResource) -> None:
        self._objects = objects

        self.create = async_to_streamed_response_wrapper(
            objects.create,
        )
        self.retrieve = async_to_streamed_response_wrapper(
            objects.retrieve,
        )
        self.list = async_to_streamed_response_wrapper(
            objects.list,
        )
        self.delete = async_to_streamed_response_wrapper(
            objects.delete,
        )
        self.complete = async_to_streamed_response_wrapper(
            objects.complete,
        )
        self.download = async_to_streamed_response_wrapper(
            objects.download,
        )
        self.list_public = async_to_streamed_response_wrapper(
            objects.list_public,
        )
