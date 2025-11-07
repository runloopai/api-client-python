from __future__ import annotations

from typing import Any, List

from .devbox import Devbox, DevboxClient
from .._client import Runloop
from ..lib.polling import PollingConfig
from ..types.blueprint_build_logs_list_view import BlueprintBuildLogsListView


class BlueprintClient:
    """
    Manage :class:`Blueprint` objects through the object-oriented SDK.
    """

    def __init__(self, client: Runloop, devbox_client: DevboxClient) -> None:
        self._client = client
        self._devbox_client = devbox_client

    def create(self, *, polling_config: PollingConfig | None = None, **params: Any) -> "Blueprint":
        """
        Create a blueprint and wait for the build to complete.
        """
        params = dict(params)
        if polling_config is None:
            polling_config = params.pop("polling_config", None)

        blueprint = self._client.blueprints.create_and_await_build_complete(
            polling_config=polling_config,
            **params,
        )
        return Blueprint(self._client, blueprint.id, self._devbox_client)

    def from_id(self, blueprint_id: str) -> "Blueprint":
        """
        Return a :class:`Blueprint` wrapper for an existing blueprint ID.
        """
        return Blueprint(self._client, blueprint_id, self._devbox_client)

    def list(self, **params: Any) -> List["Blueprint"]:
        """
        List blueprints and return lightweight wrappers.
        """
        page = self._client.blueprints.list(**params)
        return [Blueprint(self._client, item.id, self._devbox_client) for item in getattr(page, "blueprints", [])]


class Blueprint:
    """
    High-level wrapper around a blueprint resource.
    """

    def __init__(self, client: Runloop, blueprint_id: str, devbox_client: DevboxClient) -> None:
        self._client = client
        self._id = blueprint_id
        self._devbox_client = devbox_client

    def __repr__(self) -> str:
        return f"<Blueprint id={self._id!r}>"

    @property
    def id(self) -> str:
        return self._id

    def get_info(self, **request_options: Any) -> Any:
        return self._client.blueprints.retrieve(self._id, **request_options)

    def logs(self, **request_options: Any) -> BlueprintBuildLogsListView:
        return self._client.blueprints.logs(self._id, **request_options)

    def delete(self, **request_options: Any) -> Any:
        return self._client.blueprints.delete(self._id, **request_options)

    def create_devbox(self, *, polling_config: PollingConfig | None = None, **params: Any) -> Devbox:
        params = dict(params)
        params["blueprint_id"] = self._id
        return self._devbox_client.create(polling_config=polling_config, **params)
