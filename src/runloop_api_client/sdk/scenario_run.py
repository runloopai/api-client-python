"""ScenarioRun resource class for synchronous operations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from typing_extensions import Unpack, override

from ..types import ScenarioRunView
from ._types import BaseRequestOptions, LongRequestOptions
from .._client import Runloop
from ..lib.polling import PollingConfig
from ..types.scoring_contract_result_view import ScoringContractResultView

if TYPE_CHECKING:
    from .devbox import Devbox


class ScenarioRun:
    """Wrapper around a running scenario with devbox access.

    Provides methods for managing the scenario run lifecycle, accessing
    the underlying devbox, and retrieving scoring results.

    Example:
        >>> scenario = sdk.scenario.from_id("scn-xxx")
        >>> run = scenario.run()
        >>> run.await_env_ready()
        >>> devbox = run.devbox
        >>> # ... agent does work on the devbox ...
        >>> run.score()
        >>> run.await_scored()
        >>> result = run.get_score()
    """

    def __init__(self, client: Runloop, run_id: str, devbox_id: str) -> None:
        """Initialize the wrapper.

        :param client: Generated Runloop client
        :type client: Runloop
        :param run_id: ScenarioRun ID returned by the API
        :type run_id: str
        :param devbox_id: Devbox ID associated with this run
        :type devbox_id: str
        """
        self._client = client
        self._id = run_id
        self._devbox_id = devbox_id

    @override
    def __repr__(self) -> str:
        return f"<ScenarioRun id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the scenario run ID.

        :return: Unique scenario run ID
        :rtype: str
        """
        return self._id

    @property
    def devbox_id(self) -> str:
        """Return the devbox ID associated with this run.

        :return: Devbox ID
        :rtype: str
        """
        return self._devbox_id

    @property
    def devbox(self) -> "Devbox":
        """Return a Devbox wrapper for the underlying devbox.

        Use this to interact with the devbox environment during the scenario run.

        :return: Devbox wrapper instance
        :rtype: Devbox
        """
        from .devbox import Devbox

        return Devbox(self._client, self._devbox_id)

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> ScenarioRunView:
        """Retrieve current scenario run status and metadata.

        :param options: Optional request configuration
        :return: Current scenario run state info
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.retrieve(
            self._id,
            **options,
        )

    def await_env_ready(
        self,
        *,
        polling_config: PollingConfig | None = None,
        **options: Unpack[BaseRequestOptions],
    ) -> ScenarioRunView:
        """Wait for the scenario environment (devbox) to be ready.

        Blocks until the devbox reaches running state.

        :param polling_config: Optional polling configuration
        :type polling_config: PollingConfig | None
        :param options: Optional request configuration
        :return: Scenario run state after environment is ready
        :rtype: ScenarioRunView
        """
        self._client.devboxes.await_running(self._devbox_id, polling_config=polling_config)
        return self.get_info(**options)

    def score(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ScenarioRunView:
        """Submit the scenario run for scoring.

        This triggers the scoring process using the scenario's scoring contract.

        :param options: Optional long-running request configuration
        :return: Updated scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.score(
            self._id,
            **options,
        )

    def await_scored(
        self,
        *,
        polling_config: PollingConfig | None = None,
        **options: Unpack[BaseRequestOptions],
    ) -> ScenarioRunView:
        """Wait for the scenario run to be scored.

        Blocks until scoring is complete.

        :param polling_config: Optional polling configuration
        :type polling_config: PollingConfig | None
        :param options: Optional request configuration
        :return: Scored scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.await_scored(
            self._id,
            polling_config=polling_config,
            **options,
        )

    def score_and_await(
        self,
        *,
        polling_config: PollingConfig | None = None,
        **options: Unpack[BaseRequestOptions],
    ) -> ScenarioRunView:
        """Submit for scoring and wait for completion.

        Convenience method that calls score() then await_scored().

        :param polling_config: Optional polling configuration
        :type polling_config: PollingConfig | None
        :param options: Optional request configuration
        :return: Scored scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.score_and_await(
            self._id,
            polling_config=polling_config,
            **options,
        )

    def complete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ScenarioRunView:
        """Complete the scenario run and shutdown the devbox.

        :param options: Optional long-running request configuration
        :return: Final scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.complete(
            self._id,
            **options,
        )

    def cancel(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ScenarioRunView:
        """Cancel the scenario run and shutdown the devbox.

        :param options: Optional long-running request configuration
        :return: Cancelled scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.cancel(
            self._id,
            **options,
        )

    def get_score(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> Optional[ScoringContractResultView]:
        """Get the scoring result for this run.

        Returns None if the run has not been scored yet.

        :param options: Optional request configuration
        :return: Scoring result or None
        :rtype: Optional[ScoringContractResultView]
        """
        info = self.get_info(**options)
        return info.scoring_contract_result
