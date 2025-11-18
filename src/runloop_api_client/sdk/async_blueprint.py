"""Blueprint resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ..types import BlueprintView
from ._types import RequestOptions, LongRequestOptions, SDKDevboxExtraCreateParams
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

        Args:
            client: Generated AsyncRunloop client.
            blueprint_id: Blueprint ID returned by the API.
        """
        self._client = client
        self._id = blueprint_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncBlueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the blueprint ID.

        Returns:
            str: Unique blueprint ID.
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintView:
        """Retrieve the latest blueprint details.

        Args:
            **options: Optional request configuration.

        Returns:
            BlueprintView: API response describing the blueprint.
        """
        return await self._client.blueprints.retrieve(
            self._id,
            **options,
        )

    async def logs(
        self,
        **options: Unpack[RequestOptions],
    ) -> BlueprintBuildLogsListView:
        """Retrieve build logs for the blueprint.

        Args:
            **options: Optional request configuration.

        Returns:
            BlueprintBuildLogsListView: Log entries for the most recent build.
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

        Args:
            **options: Optional long-running request configuration.

        Returns:
            object: API response acknowledging deletion.
        """
        return await self._client.blueprints.delete(
            self._id,
            **options,
        )

    async def create_devbox(
        self,
        **params: Unpack[SDKDevboxExtraCreateParams],
    ) -> "AsyncDevbox":
        """Create a devbox derived from the blueprint.

        Args:
            **params: Creation parameters to forward to the devbox API.

        Returns:
            AsyncDevbox: Wrapper bound to the running devbox.
        """
        devbox_view = await self._client.devboxes.create_and_await_running(
            blueprint_id=self._id,
            **params,
        )
        return AsyncDevbox(self._client, devbox_view.id)
