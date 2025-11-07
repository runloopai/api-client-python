from __future__ import annotations

from typing import Any, List

from .._client import AsyncRunloop
from ..lib.polling import PollingConfig
from .async_devbox import AsyncDevbox, AsyncDevboxClient
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView


class AsyncBlueprintClient:
    """
    Manage :class:`AsyncBlueprint` objects through the async SDK.
    """

    def __init__(self, client: AsyncRunloop, devbox_client: AsyncDevboxClient) -> None:
        self._client = client
        self._devbox_client = devbox_client

    async def create(self, *, polling_config: PollingConfig | None = None, **params: Any) -> "AsyncBlueprint":
        params = dict(params)
        if polling_config is None:
            polling_config = params.pop("polling_config", None)

        blueprint = await self._client.blueprints.create_and_await_build_complete(
            polling_config=polling_config,
            **params,
        )
        return AsyncBlueprint(self._client, blueprint.id, self._devbox_client)

    def from_id(self, blueprint_id: str) -> "AsyncBlueprint":
        return AsyncBlueprint(self._client, blueprint_id, self._devbox_client)

    async def list(self, **params: Any) -> List["AsyncBlueprint"]:
        page = await self._client.blueprints.list(**params)
        return [AsyncBlueprint(self._client, item.id, self._devbox_client) for item in getattr(page, "blueprints", [])]


class AsyncBlueprint:
    """
    Async wrapper around blueprint operations.
    """

    def __init__(self, client: AsyncRunloop, blueprint_id: str, devbox_client: AsyncDevboxClient) -> None:
        self._client = client
        self._id = blueprint_id
        self._devbox_client = devbox_client

    def __repr__(self) -> str:
        return f"<AsyncBlueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    async def get_info(self, **request_options: Any) -> Any:
        return await self._client.blueprints.retrieve(self._id, **request_options)

    async def logs(self, **request_options: Any) -> BlueprintBuildLogsListView:
        return await self._client.blueprints.logs(self._id, **request_options)

    async def delete(self, **request_options: Any) -> Any:
        return await self._client.blueprints.delete(self._id, **request_options)

    async def create_devbox(self, *, polling_config: PollingConfig | None = None, **params: Any) -> AsyncDevbox:
        params = dict(params)
        params["blueprint_id"] = self._id
        return await self._devbox_client.create(polling_config=polling_config, **params)
