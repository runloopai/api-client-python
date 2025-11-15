"""Blueprint resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ..types import BlueprintView
from ._types import RequestOptions, LongRequestOptions, SDKDevboxExtraCreateParams
from .._client import AsyncRunloop
from .async_devbox import AsyncDevbox
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView


class AsyncBlueprint:
    """
    Async wrapper around blueprint operations.
    """

    def __init__(
        self,
        client: AsyncRunloop,
        blueprint_id: str,
    ) -> None:
        self._client = client
        self._id = blueprint_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncBlueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    async def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintView:
        return await self._client.blueprints.retrieve(
            self._id,
            **options,
        )

    async def logs(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintBuildLogsListView:
        return await self._client.blueprints.logs(
            self._id,
            **options,
        )

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        return await self._client.blueprints.delete(
            self._id,
            **options,
        )

    async def create_devbox(
        self,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> "AsyncDevbox":
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_id=self._id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)
