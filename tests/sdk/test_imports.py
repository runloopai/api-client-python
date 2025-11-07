from __future__ import annotations

import pytest

from runloop_api_client import Runloop, RunloopSDK, AsyncRunloop, AsyncRunloopSDK


def test_runloop_sdk_exposes_api() -> None:
    sdk = RunloopSDK(bearer_token="test-token")
    try:
        assert isinstance(sdk.api, Runloop)
        from runloop_api_client.sdk import DevboxClient

        assert isinstance(sdk.devbox, DevboxClient)
    finally:
        sdk.close()


@pytest.mark.asyncio
async def test_async_runloop_sdk_exposes_api() -> None:
    sdk = AsyncRunloopSDK(bearer_token="test-token")
    try:
        assert isinstance(sdk.api, AsyncRunloop)
        from runloop_api_client.sdk import AsyncDevboxClient

        assert isinstance(sdk.devbox, AsyncDevboxClient)
    finally:
        await sdk.aclose()
