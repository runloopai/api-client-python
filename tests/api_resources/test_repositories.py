# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import (
    RepositoryConnectionView,
    RepositoryInspectionDetails,
    RepositoryInspectionListView,
)
from runloop_api_client.pagination import SyncRepositoriesCursorIDPage, AsyncRepositoriesCursorIDPage

# pyright: reportDeprecated=false

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
    def test_method_create_with_all_params(self, client: Runloop) -> None:
        repository = client.repositories.create(
            name="name",
            owner="owner",
            blueprint_id="blueprint_id",
            github_auth_token="github_auth_token",
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
        assert_matches_type(SyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

    @parametrize
    def test_method_list_with_all_params(self, client: Runloop) -> None:
        repository = client.repositories.list(
            limit=0,
            name="name",
            owner="owner",
            starting_after="starting_after",
        )
        assert_matches_type(SyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

    @parametrize
    def test_raw_response_list(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(SyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

    @parametrize
    def test_streaming_response_list(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(SyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

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
    def test_method_inspect(self, client: Runloop) -> None:
        repository = client.repositories.inspect(
            id="id",
        )
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    def test_method_inspect_with_all_params(self, client: Runloop) -> None:
        repository = client.repositories.inspect(
            id="id",
            github_auth_token="github_auth_token",
        )
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    def test_raw_response_inspect(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.inspect(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    def test_streaming_response_inspect(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.inspect(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_inspect(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.repositories.with_raw_response.inspect(
                id="",
            )

    @parametrize
    def test_method_list_inspections(self, client: Runloop) -> None:
        repository = client.repositories.list_inspections(
            "id",
        )
        assert_matches_type(RepositoryInspectionListView, repository, path=["response"])

    @parametrize
    def test_raw_response_list_inspections(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.list_inspections(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(RepositoryInspectionListView, repository, path=["response"])

    @parametrize
    def test_streaming_response_list_inspections(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.list_inspections(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(RepositoryInspectionListView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_list_inspections(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.repositories.with_raw_response.list_inspections(
                "",
            )

    @parametrize
    def test_method_refresh(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            repository = client.repositories.refresh(
                id="id",
            )

        assert_matches_type(object, repository, path=["response"])

    @parametrize
    def test_method_refresh_with_all_params(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            repository = client.repositories.refresh(
                id="id",
                blueprint_id="blueprint_id",
                github_auth_token="github_auth_token",
            )

        assert_matches_type(object, repository, path=["response"])

    @parametrize
    def test_raw_response_refresh(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.repositories.with_raw_response.refresh(
                id="id",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(object, repository, path=["response"])

    @parametrize
    def test_streaming_response_refresh(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            with client.repositories.with_streaming_response.refresh(
                id="id",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                repository = response.parse()
                assert_matches_type(object, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_refresh(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                client.repositories.with_raw_response.refresh(
                    id="",
                )

    @parametrize
    def test_method_retrieve_inspection(self, client: Runloop) -> None:
        repository = client.repositories.retrieve_inspection(
            "id",
        )
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    def test_raw_response_retrieve_inspection(self, client: Runloop) -> None:
        response = client.repositories.with_raw_response.retrieve_inspection(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = response.parse()
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    def test_streaming_response_retrieve_inspection(self, client: Runloop) -> None:
        with client.repositories.with_streaming_response.retrieve_inspection(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = response.parse()
            assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve_inspection(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.repositories.with_raw_response.retrieve_inspection(
                "",
            )


class TestAsyncRepositories:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_create(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.create(
            name="name",
            owner="owner",
        )
        assert_matches_type(RepositoryConnectionView, repository, path=["response"])

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.create(
            name="name",
            owner="owner",
            blueprint_id="blueprint_id",
            github_auth_token="github_auth_token",
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
        assert_matches_type(AsyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

    @parametrize
    async def test_method_list_with_all_params(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.list(
            limit=0,
            name="name",
            owner="owner",
            starting_after="starting_after",
        )
        assert_matches_type(AsyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

    @parametrize
    async def test_raw_response_list(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.list()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(AsyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

    @parametrize
    async def test_streaming_response_list(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.list() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(AsyncRepositoriesCursorIDPage[RepositoryConnectionView], repository, path=["response"])

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
    async def test_method_inspect(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.inspect(
            id="id",
        )
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    async def test_method_inspect_with_all_params(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.inspect(
            id="id",
            github_auth_token="github_auth_token",
        )
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    async def test_raw_response_inspect(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.inspect(
            id="id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    async def test_streaming_response_inspect(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.inspect(
            id="id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_inspect(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.repositories.with_raw_response.inspect(
                id="",
            )

    @parametrize
    async def test_method_list_inspections(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.list_inspections(
            "id",
        )
        assert_matches_type(RepositoryInspectionListView, repository, path=["response"])

    @parametrize
    async def test_raw_response_list_inspections(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.list_inspections(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(RepositoryInspectionListView, repository, path=["response"])

    @parametrize
    async def test_streaming_response_list_inspections(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.list_inspections(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(RepositoryInspectionListView, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_list_inspections(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.repositories.with_raw_response.list_inspections(
                "",
            )

    @parametrize
    async def test_method_refresh(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            repository = await async_client.repositories.refresh(
                id="id",
            )

        assert_matches_type(object, repository, path=["response"])

    @parametrize
    async def test_method_refresh_with_all_params(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            repository = await async_client.repositories.refresh(
                id="id",
                blueprint_id="blueprint_id",
                github_auth_token="github_auth_token",
            )

        assert_matches_type(object, repository, path=["response"])

    @parametrize
    async def test_raw_response_refresh(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.repositories.with_raw_response.refresh(
                id="id",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(object, repository, path=["response"])

    @parametrize
    async def test_streaming_response_refresh(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.repositories.with_streaming_response.refresh(
                id="id",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                repository = await response.parse()
                assert_matches_type(object, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_refresh(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                await async_client.repositories.with_raw_response.refresh(
                    id="",
                )

    @parametrize
    async def test_method_retrieve_inspection(self, async_client: AsyncRunloop) -> None:
        repository = await async_client.repositories.retrieve_inspection(
            "id",
        )
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    async def test_raw_response_retrieve_inspection(self, async_client: AsyncRunloop) -> None:
        response = await async_client.repositories.with_raw_response.retrieve_inspection(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        repository = await response.parse()
        assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve_inspection(self, async_client: AsyncRunloop) -> None:
        async with async_client.repositories.with_streaming_response.retrieve_inspection(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            repository = await response.parse()
            assert_matches_type(RepositoryInspectionDetails, repository, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve_inspection(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.repositories.with_raw_response.retrieve_inspection(
                "",
            )
