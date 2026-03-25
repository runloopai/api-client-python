# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types.axons import SqlBatchResultView, SqlQueryResultView

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestSql:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_batch(self, client: Runloop) -> None:
        sql = client.axons.sql.batch(
            id="id",
            statements=[{"sql": "sql"}],
        )
        assert_matches_type(SqlBatchResultView, sql, path=["response"])

    @parametrize
    def test_raw_response_batch(self, client: Runloop) -> None:
        response = client.axons.sql.with_raw_response.batch(
            id="id",
            statements=[{"sql": "sql"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sql = response.parse()
        assert_matches_type(SqlBatchResultView, sql, path=["response"])

    @parametrize
    def test_streaming_response_batch(self, client: Runloop) -> None:
        with client.axons.sql.with_streaming_response.batch(
            id="id",
            statements=[{"sql": "sql"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sql = response.parse()
            assert_matches_type(SqlBatchResultView, sql, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_batch(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.axons.sql.with_raw_response.batch(
                id="",
                statements=[{"sql": "sql"}],
            )

    @parametrize
    def test_method_query(self, client: Runloop) -> None:
        sql = client.axons.sql.query(
            id="id",
            sql="sql",
        )
        assert_matches_type(SqlQueryResultView, sql, path=["response"])

    @parametrize
    def test_method_query_with_all_params(self, client: Runloop) -> None:
        sql = client.axons.sql.query(
            id="id",
            sql="sql",
            params=[{}],
        )
        assert_matches_type(SqlQueryResultView, sql, path=["response"])

    @parametrize
    def test_raw_response_query(self, client: Runloop) -> None:
        response = client.axons.sql.with_raw_response.query(
            id="id",
            sql="sql",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sql = response.parse()
        assert_matches_type(SqlQueryResultView, sql, path=["response"])

    @parametrize
    def test_streaming_response_query(self, client: Runloop) -> None:
        with client.axons.sql.with_streaming_response.query(
            id="id",
            sql="sql",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sql = response.parse()
            assert_matches_type(SqlQueryResultView, sql, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_query(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.axons.sql.with_raw_response.query(
                id="",
                sql="sql",
            )


class TestAsyncSql:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_batch(self, async_client: AsyncRunloop) -> None:
        sql = await async_client.axons.sql.batch(
            id="id",
            statements=[{"sql": "sql"}],
        )
        assert_matches_type(SqlBatchResultView, sql, path=["response"])

    @parametrize
    async def test_raw_response_batch(self, async_client: AsyncRunloop) -> None:
        response = await async_client.axons.sql.with_raw_response.batch(
            id="id",
            statements=[{"sql": "sql"}],
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sql = await response.parse()
        assert_matches_type(SqlBatchResultView, sql, path=["response"])

    @parametrize
    async def test_streaming_response_batch(self, async_client: AsyncRunloop) -> None:
        async with async_client.axons.sql.with_streaming_response.batch(
            id="id",
            statements=[{"sql": "sql"}],
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sql = await response.parse()
            assert_matches_type(SqlBatchResultView, sql, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_batch(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.axons.sql.with_raw_response.batch(
                id="",
                statements=[{"sql": "sql"}],
            )

    @parametrize
    async def test_method_query(self, async_client: AsyncRunloop) -> None:
        sql = await async_client.axons.sql.query(
            id="id",
            sql="sql",
        )
        assert_matches_type(SqlQueryResultView, sql, path=["response"])

    @parametrize
    async def test_method_query_with_all_params(self, async_client: AsyncRunloop) -> None:
        sql = await async_client.axons.sql.query(
            id="id",
            sql="sql",
            params=[{}],
        )
        assert_matches_type(SqlQueryResultView, sql, path=["response"])

    @parametrize
    async def test_raw_response_query(self, async_client: AsyncRunloop) -> None:
        response = await async_client.axons.sql.with_raw_response.query(
            id="id",
            sql="sql",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        sql = await response.parse()
        assert_matches_type(SqlQueryResultView, sql, path=["response"])

    @parametrize
    async def test_streaming_response_query(self, async_client: AsyncRunloop) -> None:
        async with async_client.axons.sql.with_streaming_response.query(
            id="id",
            sql="sql",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            sql = await response.parse()
            assert_matches_type(SqlQueryResultView, sql, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_query(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.axons.sql.with_raw_response.query(
                id="",
                sql="sql",
            )
