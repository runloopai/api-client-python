# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import PtyConnectView, PtyControlResultView

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestPty:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_connect(self, client: Runloop) -> None:
        pty = client.pty.connect(
            session_name="session_name",
        )
        assert_matches_type(PtyConnectView, pty, path=["response"])

    @parametrize
    def test_method_connect_with_all_params(self, client: Runloop) -> None:
        pty = client.pty.connect(
            session_name="session_name",
            cols=0,
            rows=0,
        )
        assert_matches_type(PtyConnectView, pty, path=["response"])

    @parametrize
    def test_raw_response_connect(self, client: Runloop) -> None:
        response = client.pty.with_raw_response.connect(
            session_name="session_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pty = response.parse()
        assert_matches_type(PtyConnectView, pty, path=["response"])

    @parametrize
    def test_streaming_response_connect(self, client: Runloop) -> None:
        with client.pty.with_streaming_response.connect(
            session_name="session_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pty = response.parse()
            assert_matches_type(PtyConnectView, pty, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_connect(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_name` but received ''"):
            client.pty.with_raw_response.connect(
                session_name="",
            )

    @parametrize
    def test_method_control(self, client: Runloop) -> None:
        pty = client.pty.control(
            session_name="session_name",
        )
        assert_matches_type(PtyControlResultView, pty, path=["response"])

    @parametrize
    def test_method_control_with_all_params(self, client: Runloop) -> None:
        pty = client.pty.control(
            session_name="session_name",
            action="resize",
            cols=0,
            rows=0,
            signal="signal",
        )
        assert_matches_type(PtyControlResultView, pty, path=["response"])

    @parametrize
    def test_raw_response_control(self, client: Runloop) -> None:
        response = client.pty.with_raw_response.control(
            session_name="session_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pty = response.parse()
        assert_matches_type(PtyControlResultView, pty, path=["response"])

    @parametrize
    def test_streaming_response_control(self, client: Runloop) -> None:
        with client.pty.with_streaming_response.control(
            session_name="session_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pty = response.parse()
            assert_matches_type(PtyControlResultView, pty, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_control(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_name` but received ''"):
            client.pty.with_raw_response.control(
                session_name="",
            )


class TestAsyncPty:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_connect(self, async_client: AsyncRunloop) -> None:
        pty = await async_client.pty.connect(
            session_name="session_name",
        )
        assert_matches_type(PtyConnectView, pty, path=["response"])

    @parametrize
    async def test_method_connect_with_all_params(self, async_client: AsyncRunloop) -> None:
        pty = await async_client.pty.connect(
            session_name="session_name",
            cols=0,
            rows=0,
        )
        assert_matches_type(PtyConnectView, pty, path=["response"])

    @parametrize
    async def test_raw_response_connect(self, async_client: AsyncRunloop) -> None:
        response = await async_client.pty.with_raw_response.connect(
            session_name="session_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pty = await response.parse()
        assert_matches_type(PtyConnectView, pty, path=["response"])

    @parametrize
    async def test_streaming_response_connect(self, async_client: AsyncRunloop) -> None:
        async with async_client.pty.with_streaming_response.connect(
            session_name="session_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pty = await response.parse()
            assert_matches_type(PtyConnectView, pty, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_connect(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_name` but received ''"):
            await async_client.pty.with_raw_response.connect(
                session_name="",
            )

    @parametrize
    async def test_method_control(self, async_client: AsyncRunloop) -> None:
        pty = await async_client.pty.control(
            session_name="session_name",
        )
        assert_matches_type(PtyControlResultView, pty, path=["response"])

    @parametrize
    async def test_method_control_with_all_params(self, async_client: AsyncRunloop) -> None:
        pty = await async_client.pty.control(
            session_name="session_name",
            action="resize",
            cols=0,
            rows=0,
            signal="signal",
        )
        assert_matches_type(PtyControlResultView, pty, path=["response"])

    @parametrize
    async def test_raw_response_control(self, async_client: AsyncRunloop) -> None:
        response = await async_client.pty.with_raw_response.control(
            session_name="session_name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        pty = await response.parse()
        assert_matches_type(PtyControlResultView, pty, path=["response"])

    @parametrize
    async def test_streaming_response_control(self, async_client: AsyncRunloop) -> None:
        async with async_client.pty.with_streaming_response.control(
            session_name="session_name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            pty = await response.parse()
            assert_matches_type(PtyControlResultView, pty, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_control(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `session_name` but received ''"):
            await async_client.pty.with_raw_response.control(
                session_name="",
            )
