# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import AgentView
from runloop_api_client.pagination import SyncAgentsCursorIDPage, AsyncAgentsCursorIDPage

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAgents:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        agent = client.agents.create(
            name="name",
        )
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        agent = client.agents.create(
            name="name",
            source={
                "type": "type",
                "git": {
                    "repository": "repository",
                    "agent_setup": ["string"],
                    "ref": "ref",
                },
                "npm": {
                    "package_name": "package_name",
                    "agent_setup": ["string"],
                    "npm_version": "npm_version",
                    "registry_url": "registry_url",
                },
                "object": {
                    "object_id": "object_id",
                    "agent_setup": ["string"],
                },
                "pip": {
                    "package_name": "package_name",
                    "agent_setup": ["string"],
                    "pip_version": "pip_version",
                    "registry_url": "registry_url",
                },
            },
        )
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.agents.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.agents.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(AgentView, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        agent = client.agents.retrieve(
            "id",
        )
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.agents.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.agents.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(AgentView, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.agents.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        agent = client.agents.list()
        assert_matches_type(SyncAgentsCursorIDPage[AgentView], agent, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        agent = client.agents.list(
            is_public=True,
            limit=0,
            name="name",
            search="search",
            starting_after="starting_after",
        )
        assert_matches_type(SyncAgentsCursorIDPage[AgentView], agent, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.agents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = response.parse()
        assert_matches_type(SyncAgentsCursorIDPage[AgentView], agent, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.agents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = response.parse()
            assert_matches_type(SyncAgentsCursorIDPage[AgentView], agent, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncAgents:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        agent = await async_client.agents.create(
            name="name",
        )
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        agent = await async_client.agents.create(
            name="name",
            source={
                "type": "type",
                "git": {
                    "repository": "repository",
                    "agent_setup": ["string"],
                    "ref": "ref",
                },
                "npm": {
                    "package_name": "package_name",
                    "agent_setup": ["string"],
                    "npm_version": "npm_version",
                    "registry_url": "registry_url",
                },
                "object": {
                    "object_id": "object_id",
                    "agent_setup": ["string"],
                },
                "pip": {
                    "package_name": "package_name",
                    "agent_setup": ["string"],
                    "pip_version": "pip_version",
                    "registry_url": "registry_url",
                },
            },
        )
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.agents.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.agents.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AgentView, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        agent = await async_client.agents.retrieve(
            "id",
        )
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.agents.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AgentView, agent, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.agents.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AgentView, agent, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.agents.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        agent = await async_client.agents.list()
        assert_matches_type(AsyncAgentsCursorIDPage[AgentView], agent, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        agent = await async_client.agents.list(
            is_public=True,
            limit=0,
            name="name",
            search="search",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncAgentsCursorIDPage[AgentView], agent, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.agents.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        agent = await response.parse()
        assert_matches_type(AsyncAgentsCursorIDPage[AgentView], agent, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.agents.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            agent = await response.parse()
            assert_matches_type(AsyncAgentsCursorIDPage[AgentView], agent, path=["response"])

        assert cast(Any, response.is_closed) is True
