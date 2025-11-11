from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Iterable, Optional
from typing_extensions import override

from ._sync import DevboxClient

if TYPE_CHECKING:
    from .devbox import Devbox
from .._types import NOT_GIVEN, Body, Omit, Query, Headers, Timeout, NotGiven, omit, not_given
from .._client import Runloop
from ..lib.polling import PollingConfig
from ..types.devbox_snapshot_view import DevboxSnapshotView
from ..types.shared_params.launch_parameters import LaunchParameters
from ..types.shared_params.code_mount_parameters import CodeMountParameters
from ..types.devboxes.devbox_snapshot_async_status_view import DevboxSnapshotAsyncStatusView


class Snapshot:
    """
    Wrapper around snapshot operations.
    """

    def __init__(
        self,
        client: Runloop,
        snapshot_id: str,
    ) -> None:
        self._client = client
        self._id = snapshot_id

    @override
    def __repr__(self) -> str:
        return f"<Snapshot id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    def get_info(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> DevboxSnapshotAsyncStatusView:
        return self._client.devboxes.disk_snapshots.query_status(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def update(
        self,
        *,
        commit_message: Optional[str] | Omit = omit,
        metadata: Optional[Dict[str, str]] | Omit = omit,
        name: Optional[str] | Omit = omit,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> DevboxSnapshotView:
        return self._client.devboxes.disk_snapshots.update(
            self._id,
            commit_message=commit_message,
            metadata=metadata,
            name=name,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def delete(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> object:
        return self._client.devboxes.disk_snapshots.delete(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )

    def await_completed(
        self,
        *,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> DevboxSnapshotAsyncStatusView:
        return self._client.devboxes.disk_snapshots.await_completed(
            self._id,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def create_devbox(
        self,
        *,
        code_mounts: Optional[Iterable[CodeMountParameters]] | NotGiven = NOT_GIVEN,
        entrypoint: Optional[str] | NotGiven = NOT_GIVEN,
        environment_variables: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        file_mounts: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        launch_parameters: Optional[LaunchParameters] | NotGiven = NOT_GIVEN,
        metadata: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        name: Optional[str] | NotGiven = NOT_GIVEN,
        repo_connection_id: Optional[str] | NotGiven = NOT_GIVEN,
        secrets: Optional[Dict[str, str]] | NotGiven = NOT_GIVEN,
        polling_config: PollingConfig | None = None,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        idempotency_key: str | None = None,
    ) -> Devbox:
        devbox_client = DevboxClient(self._client)
        return devbox_client.create_from_snapshot(
            self._id,
            code_mounts=code_mounts,
            entrypoint=entrypoint,
            environment_variables=environment_variables,
            file_mounts=file_mounts,
            launch_parameters=launch_parameters,
            metadata=metadata,
            name=name,
            repo_connection_id=repo_connection_id,
            secrets=secrets,
            polling_config=polling_config,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            idempotency_key=idempotency_key,
        )
