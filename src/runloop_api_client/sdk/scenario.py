"""Scenario resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ..types import ScenarioView
from ._types import BaseRequestOptions, SDKScenarioRunParams, SDKScenarioUpdateParams, SDKScenarioRunAsyncParams
from .._client import Runloop
from .scenario_run import ScenarioRun


class Scenario:
    """A scenario for evaluating agent performance.

    Provides methods for retrieving scenario details, updating the scenario,
    and starting scenario runs. Obtain instances via ``runloop.scenario.from_id()``
    or ``runloop.scenario.list()``.

    Example:
        >>> scenario = runloop.scenario.from_id("scn-xxx")
        >>> info = scenario.get_info()
        >>> run = scenario.run(run_name="test-run")
    """

    def __init__(self, client: Runloop, scenario_id: str) -> None:
        """Create a Scenario instance.

        :param client: Runloop client instance
        :type client: Runloop
        :param scenario_id: Scenario ID
        :type scenario_id: str
        """
        self._client = client
        self._id = scenario_id

    @override
    def __repr__(self) -> str:
        return f"<Scenario id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the scenario ID.

        :return: Unique scenario ID
        :rtype: str
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> ScenarioView:
        """Retrieve current scenario details.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.BaseRequestOptions` for available options
        :return: Current scenario info
        :rtype: ScenarioView
        """
        return self._client.scenarios.retrieve(
            self._id,
            **options,
        )

    def update(
        self,
        **params: Unpack[SDKScenarioUpdateParams],
    ) -> ScenarioView:
        """Update the scenario.

        Only provided fields will be updated.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScenarioUpdateParams` for available parameters
        :return: Updated scenario info
        :rtype: ScenarioView
        """
        return self._client.scenarios.update(
            self._id,
            **params,
        )

    def run_async(
        self,
        **params: Unpack[SDKScenarioRunAsyncParams],
    ) -> ScenarioRun:
        """Start a new scenario run without waiting for the devbox.

        Creates a new scenario run and returns immediately. The devbox may still
        be starting; call ``await_env_ready()`` on the returned ScenarioRun to
        wait for it to be ready.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScenarioRunAsyncParams` for available parameters
        :return: ScenarioRun instance for managing the run
        :rtype: ScenarioRun
        """
        run_view = self._client.scenarios.start_run(
            scenario_id=self._id,
            **params,
        )
        return ScenarioRun(self._client, run_view.id, run_view.devbox_id)

    def run(
        self,
        **params: Unpack[SDKScenarioRunParams],
    ) -> ScenarioRun:
        """Start a new scenario run and wait for the devbox to be ready.

        Convenience method that starts a run and waits for the devbox to be ready.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScenarioRunParams` for available parameters
        :return: ScenarioRun instance with ready devbox
        :rtype: ScenarioRun
        """
        run_view = self._client.scenarios.start_run_and_await_env_ready(
            scenario_id=self._id,
            **params,
        )
        return ScenarioRun(self._client, run_view.id, run_view.devbox_id)
