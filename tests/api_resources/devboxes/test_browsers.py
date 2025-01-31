# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types.devboxes import BrowserView

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestBrowsers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        browser = client.devboxes.browsers.create()
        assert_matches_type(BrowserView, browser, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.devboxes.browsers.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browser = response.parse()
        assert_matches_type(BrowserView, browser, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.devboxes.browsers.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            browser = response.parse()
            assert_matches_type(BrowserView, browser, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncBrowsers:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        browser = await async_client.devboxes.browsers.create()
        assert_matches_type(BrowserView, browser, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.browsers.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        browser = await response.parse()
        assert_matches_type(BrowserView, browser, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.browsers.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            browser = await response.parse()
            assert_matches_type(BrowserView, browser, path=["response"])

        assert cast(Any, response.is_closed) is True
