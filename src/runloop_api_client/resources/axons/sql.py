# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable

import httpx

from ..._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from ..._utils import path_template, maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ...types.axons import sql_batch_params, sql_query_params
from ..._base_client import make_request_options
from ...types.axons.sql_statement_params import SqlStatementParams
from ...types.axons.sql_batch_result_view import SqlBatchResultView
from ...types.axons.sql_query_result_view import SqlQueryResultView

__all__ = ["SqlResource", "AsyncSqlResource"]


class SqlResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> SqlResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return SqlResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> SqlResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return SqlResourceWithStreamingResponse(self)

    def batch(
        self,
        id: str,
        *,
        statements: Iterable[SqlStatementParams],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SqlBatchResultView:
        """
        [Beta] Execute multiple SQL statements atomically within a single transaction
        against an axon's SQLite database.

        Args:
          statements: The SQL statements to execute atomically within a transaction.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/axons/{id}/sql/batch", id=id),
            body=maybe_transform({"statements": statements}, sql_batch_params.SqlBatchParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SqlBatchResultView,
        )

    def query(
        self,
        id: str,
        *,
        sql: str,
        params: Iterable[object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SqlQueryResultView:
        """
        [Beta] Execute a single parameterized SQL statement against an axon's SQLite
        database.

        Args:
          sql: SQL query with ?-style positional placeholders.

          params: Positional parameter bindings for ? placeholders.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            path_template("/v1/axons/{id}/sql/query", id=id),
            body=maybe_transform(
                {
                    "sql": sql,
                    "params": params,
                },
                sql_query_params.SqlQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SqlQueryResultView,
        )


class AsyncSqlResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncSqlResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncSqlResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncSqlResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncSqlResourceWithStreamingResponse(self)

    async def batch(
        self,
        id: str,
        *,
        statements: Iterable[SqlStatementParams],
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SqlBatchResultView:
        """
        [Beta] Execute multiple SQL statements atomically within a single transaction
        against an axon's SQLite database.

        Args:
          statements: The SQL statements to execute atomically within a transaction.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/axons/{id}/sql/batch", id=id),
            body=await async_maybe_transform({"statements": statements}, sql_batch_params.SqlBatchParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SqlBatchResultView,
        )

    async def query(
        self,
        id: str,
        *,
        sql: str,
        params: Iterable[object] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> SqlQueryResultView:
        """
        [Beta] Execute a single parameterized SQL statement against an axon's SQLite
        database.

        Args:
          sql: SQL query with ?-style positional placeholders.

          params: Positional parameter bindings for ? placeholders.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            path_template("/v1/axons/{id}/sql/query", id=id),
            body=await async_maybe_transform(
                {
                    "sql": sql,
                    "params": params,
                },
                sql_query_params.SqlQueryParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SqlQueryResultView,
        )


class SqlResourceWithRawResponse:
    def __init__(self, sql: SqlResource) -> None:
        self._sql = sql

        self.batch = to_raw_response_wrapper(
            sql.batch,
        )
        self.query = to_raw_response_wrapper(
            sql.query,
        )


class AsyncSqlResourceWithRawResponse:
    def __init__(self, sql: AsyncSqlResource) -> None:
        self._sql = sql

        self.batch = async_to_raw_response_wrapper(
            sql.batch,
        )
        self.query = async_to_raw_response_wrapper(
            sql.query,
        )


class SqlResourceWithStreamingResponse:
    def __init__(self, sql: SqlResource) -> None:
        self._sql = sql

        self.batch = to_streamed_response_wrapper(
            sql.batch,
        )
        self.query = to_streamed_response_wrapper(
            sql.query,
        )


class AsyncSqlResourceWithStreamingResponse:
    def __init__(self, sql: AsyncSqlResource) -> None:
        self._sql = sql

        self.batch = async_to_streamed_response_wrapper(
            sql.batch,
        )
        self.query = async_to_streamed_response_wrapper(
            sql.query,
        )
