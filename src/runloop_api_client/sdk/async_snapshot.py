"""Snapshot resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    RequestOptions,
    LongRequestOptions,
    PollingRequestOptions,
    SDKDevboxExtraCreateParams,
    SDKDiskSnapshotUpdateParams,
)
from .._client import AsyncRunloop
from .async_devbox import AsyncDevbox
from ..types.devbox_snapshot_view import DevboxSnapshotView
from ..types.devboxes.devbox_snapshot_async_status_view import DevboxSnapshotAsyncStatusView


class AsyncSnapshot:
    """
    Async wrapper around snapshot operations.
    """

    def __init__(
        self,
        client: AsyncRunloop,
        snapshot_id: str,
    ) -> None:
        self._client = client
        self._id = snapshot_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncSnapshot id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    async def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> DevboxSnapshotAsyncStatusView:
        return await self._client.devboxes.disk_snapshots.query_status(
            self._id,
            **options,
        )

    async def update(
        self,
        **params: Unpack[SDKDiskSnapshotUpdateParams],
    ) -> DevboxSnapshotView:
        return await self._client.devboxes.disk_snapshots.update(
            self._id,
            **params,
        )

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        return await self._client.devboxes.disk_snapshots.delete(
            self._id,
            **options,
        )

    async def await_completed(
        self,
        **options: Unpack[PollingRequestOptions],
    ) -> DevboxSnapshotAsyncStatusView:
        return await self._client.devboxes.disk_snapshots.await_completed(
            self._id,
            **options,
        )

    async def create_devbox(
        self,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> "AsyncDevbox":
        devbox_view = await self._client.devboxes.create_and_await_running(
            snapshot_id=self._id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)
