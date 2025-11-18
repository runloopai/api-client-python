"""Snapshot resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    RequestOptions,
    LongRequestOptions,
    PollingRequestOptions,
    SDKDevboxExtraCreateParams,
    SDKDiskSnapshotUpdateParams,
)
from .devbox import Devbox
from .._client import Runloop
from ..types.devbox_snapshot_view import DevboxSnapshotView
from ..types.devboxes.devbox_snapshot_async_status_view import DevboxSnapshotAsyncStatusView


class Snapshot:
    """Wrapper around synchronous snapshot operations."""

    def __init__(
        self,
        client: Runloop,
        snapshot_id: str,
    ) -> None:
        """Initialize the wrapper.

        Args:
            client: Generated Runloop client.
            snapshot_id: Snapshot identifier returned by the API.
        """
        self._client = client
        self._id = snapshot_id

    @override
    def __repr__(self) -> str:
        return f"<Snapshot id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the snapshot identifier.

        Returns:
            str: Unique snapshot ID.
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> DevboxSnapshotAsyncStatusView:
        """Retrieve the latest snapshot status.

        Args:
            **options: Optional request configuration.

        Returns:
            DevboxSnapshotAsyncStatusView: Snapshot state payload.
        """
        return self._client.devboxes.disk_snapshots.query_status(
            self._id,
            **options,
        )

    def update(
        self,
        **params: Unpack[SDKDiskSnapshotUpdateParams],
    ) -> DevboxSnapshotView:
        """Update snapshot metadata.

        Args:
            **params: Fields to update on the snapshot.

        Returns:
            DevboxSnapshotView: Updated snapshot details.
        """
        return self._client.devboxes.disk_snapshots.update(
            self._id,
            **params,
        )

    def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        """Delete the snapshot.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            object: API response acknowledging deletion.
        """
        return self._client.devboxes.disk_snapshots.delete(
            self._id,
            **options,
        )

    def await_completed(
        self,
        **options: Unpack[PollingRequestOptions],
    ) -> DevboxSnapshotAsyncStatusView:
        """Block until the snapshot operation finishes.

        Args:
            **options: Polling configuration (timeouts, intervals).

        Returns:
            DevboxSnapshotAsyncStatusView: Final snapshot status.
        """
        return self._client.devboxes.disk_snapshots.await_completed(
            self._id,
            **options,
        )

    def create_devbox(
        self,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> "Devbox":
        """Create a devbox restored from this snapshot.

        Args:
            **params: Creation parameters to forward to the devbox API.

        Returns:
            Devbox: Wrapper bound to the running devbox.
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            snapshot_id=self._id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)
