from __future__ import annotations

from typing import Any, List

from .devbox import Devbox, DevboxClient
from .._client import Runloop
from ..lib.polling import PollingConfig
from ..types.devbox_snapshot_view import DevboxSnapshotView
from ..types.devboxes.devbox_snapshot_async_status_view import DevboxSnapshotAsyncStatusView


class SnapshotClient:
    """
    Manage :class:`Snapshot` objects through the SDK.
    """

    def __init__(self, client: Runloop, devbox_client: DevboxClient) -> None:
        self._client = client
        self._devbox_client = devbox_client

    def list(self, **params: Any) -> List["Snapshot"]:
        page = self._client.devboxes.disk_snapshots.list(**params)
        return [Snapshot(self._client, item.id, self._devbox_client) for item in getattr(page, "disk_snapshots", [])]

    def from_id(self, snapshot_id: str) -> "Snapshot":
        return Snapshot(self._client, snapshot_id, self._devbox_client)


class Snapshot:
    """
    Wrapper around snapshot operations.
    """

    def __init__(self, client: Runloop, snapshot_id: str, devbox_client: DevboxClient) -> None:
        self._client = client
        self._id = snapshot_id
        self._devbox_client = devbox_client

    def __repr__(self) -> str:
        return f"<Snapshot id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    def get_info(self, **request_options: Any) -> DevboxSnapshotAsyncStatusView:
        return self._client.devboxes.disk_snapshots.query_status(self._id, **request_options)

    def update(self, **params: Any) -> DevboxSnapshotView:
        return self._client.devboxes.disk_snapshots.update(self._id, **params)

    def delete(self, **request_options: Any) -> Any:
        return self._client.devboxes.disk_snapshots.delete(self._id, **request_options)

    def await_completed(
        self, *, polling_config: PollingConfig | None = None, **request_options: Any
    ) -> DevboxSnapshotAsyncStatusView:
        return self._client.devboxes.disk_snapshots.await_completed(
            self._id,
            polling_config=polling_config,
            **request_options,
        )

    def create_devbox(self, *, polling_config: PollingConfig | None = None, **params: Any) -> Devbox:
        params = dict(params)
        params["snapshot_id"] = self._id
        return self._devbox_client.create(polling_config=polling_config, **params)
