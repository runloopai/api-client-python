"""Blueprint resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ..types import BlueprintView
from ._types import BaseRequestOptions, LongRequestOptions, SDKDevboxCreateFromImageParams
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

        :param client: Generated Runloop client
        :type client: Runloop
        :param blueprint_id: Blueprint ID returned by the API
        :type blueprint_id: str
        """
        self._client = client
        self._id = blueprint_id

    @override
    def __repr__(self) -> str:
        return f"<Blueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the blueprint ID.

        :return: Unique blueprint ID
        :rtype: str
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> BlueprintView:
        """Retrieve the latest blueprint details.

        :param options: Optional request configuration
        :return: API response describing the blueprint
        :rtype: BlueprintView
        """
        return self._client.blueprints.retrieve(
            self._id,
            **options,
        )

    def logs(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> BlueprintBuildLogsListView:
        """Retrieve build logs for the blueprint.

        :param options: Optional request configuration
        :return: Log entries for the most recent build
        :rtype: BlueprintBuildLogsListView
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

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: object
        """
        return self._client.blueprints.delete(
            self._id,
            **options,
        )

    def create_devbox(
        self,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> "Devbox":
        """Create a devbox derived from the blueprint.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the running devbox
        :rtype: Devbox
        """
        devbox_view = self._client.devboxes.create_and_await_running(
            blueprint_id=self._id,
            **params,
        )
        return Devbox(self._client, devbox_view.id)
