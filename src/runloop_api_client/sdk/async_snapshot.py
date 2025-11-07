from __future__ import annotations

from typing import Any, List

from .._client import AsyncRunloop
from ..lib.polling import PollingConfig
from .async_devbox import AsyncDevbox, AsyncDevboxClient
from ..types.devbox_snapshot_view import DevboxSnapshotView
from ..types.devboxes.devbox_snapshot_async_status_view import DevboxSnapshotAsyncStatusView


class AsyncSnapshotClient:
    """
    Manage :class:`AsyncSnapshot` instances.
    """

    def __init__(self, client: AsyncRunloop, devbox_client: AsyncDevboxClient) -> None:
        self._client = client
        self._devbox_client = devbox_client

    async def list(self, **params: Any) -> List["AsyncSnapshot"]:
        page = await self._client.devboxes.disk_snapshots.list(**params)
        return [
            AsyncSnapshot(self._client, item.id, self._devbox_client) for item in getattr(page, "disk_snapshots", [])
        ]

    def from_id(self, snapshot_id: str) -> "AsyncSnapshot":
        return AsyncSnapshot(self._client, snapshot_id, self._devbox_client)


class AsyncSnapshot:
    """
    Async wrapper around snapshot operations.
    """

    def __init__(self, client: AsyncRunloop, snapshot_id: str, devbox_client: AsyncDevboxClient) -> None:
        self._client = client
        self._id = snapshot_id
        self._devbox_client = devbox_client

    def __repr__(self) -> str:
        return f"<AsyncSnapshot id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    async def get_info(self, **request_options: Any) -> DevboxSnapshotAsyncStatusView:
        return await self._client.devboxes.disk_snapshots.query_status(self._id, **request_options)

    async def update(self, **params: Any) -> DevboxSnapshotView:
        return await self._client.devboxes.disk_snapshots.update(self._id, **params)

    async def delete(self, **request_options: Any) -> Any:
        return await self._client.devboxes.disk_snapshots.delete(self._id, **request_options)

    async def await_completed(
        self,
        *,
        polling_config: PollingConfig | None = None,
        **request_options: Any,
    ) -> DevboxSnapshotAsyncStatusView:
        return await self._client.devboxes.disk_snapshots.await_completed(
            self._id,
            polling_config=polling_config,
            **request_options,
        )

    async def create_devbox(self, *, polling_config: PollingConfig | None = None, **params: Any) -> AsyncDevbox:
        params = dict(params)
        params["snapshot_id"] = self._id
        return await self._devbox_client.create(polling_config=polling_config, **params)
