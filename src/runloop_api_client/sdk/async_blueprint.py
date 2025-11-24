"""Blueprint resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ..types import BlueprintView
from ._types import BaseRequestOptions, LongRequestOptions, SDKDevboxCreateFromImageParams
from .._client import AsyncRunloop
from .async_devbox import AsyncDevbox
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView


class AsyncBlueprint:
    """Asynchronous wrapper around a blueprint resource."""

    def __init__(
        self,
        client: AsyncRunloop,
        blueprint_id: str,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param blueprint_id: Blueprint ID returned by the API
        :type blueprint_id: str
        """
        self._client = client
        self._id = blueprint_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncBlueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the blueprint ID.

        :return: Unique blueprint ID
        :rtype: str
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> BlueprintView:
        """Retrieve the latest blueprint details.

        :param options: Optional request configuration
        :return: API response describing the blueprint
        :rtype: BlueprintView
        """
        return await self._client.blueprints.retrieve(
            self._id,
            **options,
        )

    async def logs(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> BlueprintBuildLogsListView:
        """Retrieve build logs for the blueprint.

        :param options: Optional request configuration
        :return: Log entries for the most recent build
        :rtype: BlueprintBuildLogsListView
        """
        return await self._client.blueprints.logs(
            self._id,
            **options,
        )

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> object:
        """Delete the blueprint.

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: object
        """
        return await self._client.blueprints.delete(
            self._id,
            **options,
        )

    async def create_devbox(
        self,
        **params: Unpack[SDKDevboxCreateFromImageParams],
    ) -> "AsyncDevbox":
        """Create a devbox derived from the blueprint.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams` for available parameters
        :return: Wrapper bound to the running devbox
        :rtype: AsyncDevbox
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_id=self._id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)
