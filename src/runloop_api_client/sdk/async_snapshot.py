"""Snapshot resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    BaseRequestOptions,
    LongRequestOptions,
    PollingRequestOptions,
    SDKDiskSnapshotUpdateParams,
    SDKDevboxCreateFromImageParams,
)
from .._client import AsyncRunloop
from .async_devbox import AsyncDevbox
from ..types.devboxes import DevboxSnapshotAsyncStatusView
from ..types.devbox_snapshot_view import DevboxSnapshotView


class AsyncSnapshot:
    """Async wrapper around snapshot operations."""

    def __init__(
        self,
        client: AsyncRunloop,
        snapshot_id: str,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param snapshot_id: Snapshot identifier returned by the API
        :type snapshot_id: str
        """
        self._client = client
        self._id = snapshot_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncSnapshot id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the snapshot identifier.

        :return: Unique snapshot ID
        :rtype: str
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> DevboxSnapshotAsyncStatusView:
        """Retrieve the latest snapshot status.

        :param options: Optional request configuration
        :return: Snapshot state payload
        :rtype: DevboxSnapshotAsyncStatusView
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

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDiskSnapshotUpdateParams` for available parameters
        :return: Updated snapshot details
        :rtype: DevboxSnapshotView
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

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: object
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

        :param options: Polling configuration (timeouts, intervals)
        :return: Final snapshot status
        :rtype: DevboxSnapshotAsyncStatusView
        """
        return await self._client.devboxes.disk_snapshots.await_completed(
            self._id,
            **options,
        )

    async def create_devbox(
        self,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> "AsyncDevbox":
        """Create a devbox restored from this snapshot.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the running devbox
        :rtype: AsyncDevbox
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            snapshot_id=self._id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)
