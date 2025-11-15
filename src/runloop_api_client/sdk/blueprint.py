"""Blueprint resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ..types import BlueprintView
from ._types import RequestOptions, LongRequestOptions, SDKDevboxExtraCreateParams
from .devbox import Devbox
from .._client import Runloop
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView


class Blueprint:
    """
    High-level wrapper around a blueprint resource.
    """

    def __init__(
        self,
        client: Runloop,
        blueprint_id: str,
    ) -> None:
        self._client = client
        self._id = blueprint_id

    @override
    def __repr__(self) -> str:
        return f"<Blueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintView:
        return self._client.blueprints.retrieve(
            self._id,
            **options,
        )

    def logs(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintBuildLogsListView:
        return self._client.blueprints.logs(
            self._id,
            **options,
        )

    def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        return self._client.blueprints.delete(
            self._id,
            **options,
        )

    def create_devbox(
        self,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> "Devbox":
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_id=self._id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)
