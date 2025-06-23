# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types.devboxes import (
    ComputerView,
    ComputerMouseInteractionResponse,
    ComputerScreenInteractionResponse,
    ComputerKeyboardInteractionResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestComputers:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        computer = client.devboxes.computers.create()
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        computer = client.devboxes.computers.create(
            display_dimensions={
                "display_height_px": 0,
                "display_width_px": 0,
            },
            name="name",
        )
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.devboxes.computers.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = response.parse()
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.devboxes.computers.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = response.parse()
            assert_matches_type(ComputerView, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        computer = client.devboxes.computers.retrieve(
            "id",
        )
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.devboxes.computers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = response.parse()
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.devboxes.computers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = response.parse()
            assert_matches_type(ComputerView, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.computers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_keyboard_interaction(self, client: Runloop) -> None:
        computer = client.devboxes.computers.keyboard_interaction(
            id="id",
            action="key",
        )
        assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

    @parametrize
    def test_method_keyboard_interaction_with_all_params(self, client: Runloop) -> None:
        computer = client.devboxes.computers.keyboard_interaction(
            id="id",
            action="key",
            text="text",
        )
        assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

    @parametrize
    def test_raw_response_keyboard_interaction(self, client: Runloop) -> None:
        response = client.devboxes.computers.with_raw_response.keyboard_interaction(
            id="id",
            action="key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = response.parse()
        assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

    @parametrize
    def test_streaming_response_keyboard_interaction(self, client: Runloop) -> None:
        with client.devboxes.computers.with_streaming_response.keyboard_interaction(
            id="id",
            action="key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = response.parse()
            assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_keyboard_interaction(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.computers.with_raw_response.keyboard_interaction(
                id="",
                action="key",
            )

    @parametrize
    def test_method_mouse_interaction(self, client: Runloop) -> None:
        computer = client.devboxes.computers.mouse_interaction(
            id="id",
            action="mouse_move",
        )
        assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

    @parametrize
    def test_method_mouse_interaction_with_all_params(self, client: Runloop) -> None:
        computer = client.devboxes.computers.mouse_interaction(
            id="id",
            action="mouse_move",
            coordinate={
                "x": 0,
                "y": 0,
            },
        )
        assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

    @parametrize
    def test_raw_response_mouse_interaction(self, client: Runloop) -> None:
        response = client.devboxes.computers.with_raw_response.mouse_interaction(
            id="id",
            action="mouse_move",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = response.parse()
        assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

    @parametrize
    def test_streaming_response_mouse_interaction(self, client: Runloop) -> None:
        with client.devboxes.computers.with_streaming_response.mouse_interaction(
            id="id",
            action="mouse_move",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = response.parse()
            assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_mouse_interaction(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.computers.with_raw_response.mouse_interaction(
                id="",
                action="mouse_move",
            )

    @parametrize
    def test_method_screen_interaction(self, client: Runloop) -> None:
        computer = client.devboxes.computers.screen_interaction(
            id="id",
            action="screenshot",
        )
        assert_matches_type(ComputerScreenInteractionResponse, computer, path=["response"])

    @parametrize
    def test_raw_response_screen_interaction(self, client: Runloop) -> None:
        response = client.devboxes.computers.with_raw_response.screen_interaction(
            id="id",
            action="screenshot",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = response.parse()
        assert_matches_type(ComputerScreenInteractionResponse, computer, path=["response"])

    @parametrize
    def test_streaming_response_screen_interaction(self, client: Runloop) -> None:
        with client.devboxes.computers.with_streaming_response.screen_interaction(
            id="id",
            action="screenshot",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = response.parse()
            assert_matches_type(ComputerScreenInteractionResponse, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_screen_interaction(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.computers.with_raw_response.screen_interaction(
                id="",
                action="screenshot",
            )


class TestAsyncComputers:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.create()
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.create(
            display_dimensions={
                "display_height_px": 0,
                "display_width_px": 0,
            },
            name="name",
        )
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.computers.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = await response.parse()
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.computers.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = await response.parse()
            assert_matches_type(ComputerView, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.retrieve(
            "id",
        )
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.computers.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = await response.parse()
        assert_matches_type(ComputerView, computer, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.computers.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = await response.parse()
            assert_matches_type(ComputerView, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.computers.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_keyboard_interaction(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.keyboard_interaction(
            id="id",
            action="key",
        )
        assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_method_keyboard_interaction_with_all_params(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.keyboard_interaction(
            id="id",
            action="key",
            text="text",
        )
        assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_raw_response_keyboard_interaction(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.computers.with_raw_response.keyboard_interaction(
            id="id",
            action="key",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = await response.parse()
        assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_streaming_response_keyboard_interaction(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.computers.with_streaming_response.keyboard_interaction(
            id="id",
            action="key",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = await response.parse()
            assert_matches_type(ComputerKeyboardInteractionResponse, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_keyboard_interaction(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.computers.with_raw_response.keyboard_interaction(
                id="",
                action="key",
            )

    @parametrize
    async def test_method_mouse_interaction(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.mouse_interaction(
            id="id",
            action="mouse_move",
        )
        assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_method_mouse_interaction_with_all_params(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.mouse_interaction(
            id="id",
            action="mouse_move",
            coordinate={
                "x": 0,
                "y": 0,
            },
        )
        assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_raw_response_mouse_interaction(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.computers.with_raw_response.mouse_interaction(
            id="id",
            action="mouse_move",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = await response.parse()
        assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_streaming_response_mouse_interaction(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.computers.with_streaming_response.mouse_interaction(
            id="id",
            action="mouse_move",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = await response.parse()
            assert_matches_type(ComputerMouseInteractionResponse, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_mouse_interaction(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.computers.with_raw_response.mouse_interaction(
                id="",
                action="mouse_move",
            )

    @parametrize
    async def test_method_screen_interaction(self, async_client: AsyncRunloop) -> None:
        computer = await async_client.devboxes.computers.screen_interaction(
            id="id",
            action="screenshot",
        )
        assert_matches_type(ComputerScreenInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_raw_response_screen_interaction(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.computers.with_raw_response.screen_interaction(
            id="id",
            action="screenshot",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        computer = await response.parse()
        assert_matches_type(ComputerScreenInteractionResponse, computer, path=["response"])

    @parametrize
    async def test_streaming_response_screen_interaction(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.computers.with_streaming_response.screen_interaction(
            id="id",
            action="screenshot",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            computer = await response.parse()
            assert_matches_type(ComputerScreenInteractionResponse, computer, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_screen_interaction(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.computers.with_raw_response.screen_interaction(
                id="",
                action="screenshot",
            )
