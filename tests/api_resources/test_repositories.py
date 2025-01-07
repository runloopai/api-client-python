# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    RepositoryConnectionView,
    RepositoryVersionListView,
    RepositoryConnectionListView,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestRepositories:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Runloop) -> None:
        repository = client.repositories.create(
            name="name",
            owner="owner",
        )
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    def test_raw_response_create(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.create(
            name="name",
            owner="owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    def test_streaming_response_create(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.create(
            name="name",
            owner="owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(RepositoryConnectionView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        repository = client.repositories.retrieve(
            "id",
        )
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(RepositoryConnectionView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.repositories.with_raw_response.retrieve(
                "",
            )

    @parametrize
    def test_method_list(self, client: Runloop) -> None:
        repository = client.repositories.list()
        assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        repository = client.repositories.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_method_delete(self, client: Runloop) -> None:
        repository = client.repositories.delete(
            "id",
        )
        assert_matches_type(object, repository, path=["response"])

    @parametrize
    def test_raw_response_delete(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(object, repository, path=["response"])

    @parametrize
    def test_streaming_response_delete(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(object, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_delete(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.repositories.with_raw_response.delete(
                "",
            )

    @parametrize
    def test_method_versions(self, client: Runloop) -> None:
        repository = client.repositories.versions(
            "id",
        )
        assert_matches_type(RepositoryVersionListView, repository, path=["response"])

    @parametrize
    def test_raw_response_versions(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.versions(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(RepositoryVersionListView, repository, path=["response"])

    @parametrize
    def test_streaming_response_versions(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.versions(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(RepositoryVersionListView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_versions(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.repositories.with_raw_response.versions(
                "",
            )


class TestAsyncRepositories:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.create(
            name="name",
            owner="owner",
        )
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.create(
            name="name",
            owner="owner",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.create(
            name="name",
            owner="owner",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(RepositoryConnectionView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.retrieve(
            "id",
        )
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.retrieve(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.retrieve(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(RepositoryConnectionView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.repositories.with_raw_response.retrieve(
                "",
            )

    @parametrize
    async def test_method_list(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.list()
        assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.list(
            limit=0,
            starting_after="starting_after",
        )
        assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(RepositoryConnectionListView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_method_delete(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.delete(
            "id",
        )
        assert_matches_type(object, repository, path=["response"])

    @parametrize
    async def test_raw_response_delete(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.delete(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(object, repository, path=["response"])

    @parametrize
    async def test_streaming_response_delete(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.delete(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(object, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_delete(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.repositories.with_raw_response.delete(
                "",
            )

    @parametrize
    async def test_method_versions(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.versions(
            "id",
        )
        assert_matches_type(RepositoryVersionListView, repository, path=["response"])

    @parametrize
    async def test_raw_response_versions(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.versions(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(RepositoryVersionListView, repository, path=["response"])

    @parametrize
    async def test_streaming_response_versions(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.versions(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(RepositoryVersionListView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_versions(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.repositories.with_raw_response.versions(
                "",
            )
