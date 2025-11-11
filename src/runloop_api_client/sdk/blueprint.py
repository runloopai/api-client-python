from __future__ import annotations

from typing import Any, Dict, Iterable, Optional

from typing_extensions import override

from .devbox import Devbox
from .._client import Runloop
from ..lib.polling import PollingConfig
from .._types import Body, Headers, NotGiven, NOT_GIVEN, Query, Timeout, not_given
from ..types.shared_params.code_mount_parameters import CodeMountParameters
from ..types.shared_params.launch_parameters import LaunchParameters
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
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> Any:
        return self._client.blueprints.retrieve(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def logs(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> BlueprintBuildLogsListView:
        return self._client.blueprints.logs(
            self._id,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
        )

    def delete(
        self,
        *,
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
    ) -> Any:
        return self._client.blueprints.delete(
            self._id,
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
        from ._sync import DevboxClient

        devbox_client = DevboxClient(self._client)
        return devbox_client.create_from_blueprint_id(
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
