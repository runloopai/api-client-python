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
    """Async wrapper around snapshot operations."""

    def __init__(
        self,
        client: AsyncRunloop,
        snapshot_id: str,
    ) -> None:
        """Initialize the wrapper.

        Args:
            client: Generated AsyncRunloop client.
            snapshot_id: Snapshot identifier returned by the API.
        """
        self._client = client
        self._id = snapshot_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncSnapshot id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the snapshot identifier.

        Returns:
            str: Unique snapshot ID.
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> DevboxSnapshotAsyncStatusView:
        """Retrieve the latest snapshot status.

        Args:
            **options: Optional request configuration.

        Returns:
            DevboxSnapshotAsyncStatusView: Snapshot state payload.
        """
        return await self._client.devboxes.disk_snapshots.query_status(
            self._id,
            **options,
        )

    async def update(
        self,
        **params: Unpack[SDKDiskSnapshotUpdateParams],
    ) -> DevboxSnapshotView:
        """Update snapshot metadata.

        Args:
            **params: Fields to update on the snapshot.

        Returns:
            DevboxSnapshotView: Updated snapshot details.
        """
        return await self._client.devboxes.disk_snapshots.update(
            self._id,
            **params,
        )

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        """Delete the snapshot.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            object: API response acknowledging deletion.
        """
        return await self._client.devboxes.disk_snapshots.delete(
            self._id,
            **options,
        )

    async def await_completed(
        self,
        **options: Unpack[PollingRequestOptions],
    ) -> DevboxSnapshotAsyncStatusView:
        """Block until the snapshot operation finishes.

        Args:
            **options: Polling configuration (timeouts, intervals).

        Returns:
            DevboxSnapshotAsyncStatusView: Final snapshot status.
        """
        return await self._client.devboxes.disk_snapshots.await_completed(
            self._id,
            **options,
        )

    async def create_devbox(
        self,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> "AsyncDevbox":
        """Create a devbox restored from this snapshot.

        Args:
            **params: Creation parameters forwarded to the devbox API.

        Returns:
            AsyncDevbox: Wrapper bound to the running devbox.
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            snapshot_id=self._id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)
