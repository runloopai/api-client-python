"""Blueprint resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ..types import BlueprintView
from ._types import RequestOptions, LongRequestOptions, SDKDevboxExtraCreateParams
from .devbox import Devbox
from .._client import Runloop
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView


class Blueprint:
    """Synchronous wrapper around a blueprint resource."""

    def __init__(
        self,
        client: Runloop,
        blueprint_id: str,
    ) -> None:
        """Initialize the wrapper.

        Args:
            client: Generated Runloop client.
            blueprint_id: Blueprint ID returned by the API.
        """
        self._client = client
        self._id = blueprint_id

    @override
    def __repr__(self) -> str:
        return f"<Blueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the blueprint ID.

        Returns:
            str: Unique blueprint ID.
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintView:
        """Retrieve the latest blueprint details.

        Args:
            **options: Optional request configuration.

        Returns:
            BlueprintView: API response describing the blueprint.
        """
        return self._client.blueprints.retrieve(
            self._id,
            **options,
        )

    def logs(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintBuildLogsListView:
        """Retrieve build logs for the blueprint.

        Args:
            **options: Optional request configuration.

        Returns:
            BlueprintBuildLogsListView: Log entries for the most recent build.
        """
        return self._client.blueprints.logs(
            self._id,
            **options,
        )

    def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        """Delete the blueprint.

        Args:
            **options: Optional long-running request configuration.

        Returns:
            object: API response acknowledging deletion.
        """
        return self._client.blueprints.delete(
            self._id,
            **options,
        )

    def create_devbox(
        self,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> "Devbox":
        """Create a devbox derived from the blueprint.

        Args:
            **params: Creation parameters to forward to the devbox API.

        Returns:
            Devbox: Wrapper bound to the running devbox.
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_id=self._id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)
