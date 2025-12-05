"""ScenarioRun resource class for synchronous operations."""

from __future__ import annotations

import os
from typing import Union, Optional
from functools import cached_property
from typing_extensions import Unpack, override

from ..types import ScenarioRunView
from ._types import BaseRequestOptions, LongRequestOptions, PollingRequestOptions
from .devbox import Devbox
from .._client import Runloop
from ._helpers import filter_params
from ..types.scoring_contract_result_view import ScoringContractResultView


class ScenarioRun:
    """A running scenario with devbox access.

    Provides methods for managing the scenario run lifecycle, accessing
    the devbox, and retrieving scoring results. Obtain instances via
    ``scenario.run()`` or ``scenario.run_async()``.

    Example:
        >>> scenario = runloop.scenario.from_id("scn-xxx")
        >>> run = scenario.run_async()
        >>> run.await_env_ready()
        >>> devbox = run.devbox
        >>> # ... agent does work on the devbox ...
        >>> run.score_and_await()
        >>> score = run.get_score()
    """

    def __init__(self, client: Runloop, run_id: str, devbox_id: str) -> None:
        """Create a ScenarioRun instance.

        :param client: Runloop client instance
        :type client: Runloop
        :param run_id: Scenario run ID
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

    @cached_property
    def devbox(self) -> Devbox:
        """The devbox instance for this scenario run.

        Use this to interact with the devbox environment during the scenario run.

        :return: Devbox instance
        :rtype: Devbox
        """
        return Devbox(self._client, self._devbox_id)

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> ScenarioRunView:
        """Retrieve current scenario run status and metadata.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.BaseRequestOptions` for available options
        :return: Current scenario run state info
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.retrieve(
            self._id,
            **options,
        )

    def await_env_ready(
        self,
        **options: Unpack[PollingRequestOptions],
    ) -> ScenarioRunView:
        """Wait for the scenario environment (devbox) to be ready.

        Blocks until the devbox reaches running state.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.PollingRequestOptions` for available options
        :return: Scenario run state after environment is ready
        :rtype: ScenarioRunView
        """
        self._client.devboxes.await_running(self._devbox_id, polling_config=options.get("polling_config"))
        return self.get_info(**filter_params(options, BaseRequestOptions))

    def score(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ScenarioRunView:
        """Submit the scenario run for scoring.

        This triggers the scoring process using the scenario's scoring contract.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Updated scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.score(
            self._id,
            **options,
        )

    def await_scored(
        self,
        **options: Unpack[PollingRequestOptions],
    ) -> ScenarioRunView:
        """Wait for the scenario run to be scored.

        Blocks until scoring is complete.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.PollingRequestOptions` for available options
        :return: Scored scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.await_scored(
            self._id,
            **options,
        )

    def score_and_await(
        self,
        **options: Unpack[PollingRequestOptions],
    ) -> ScenarioRunView:
        """Submit for scoring and wait for completion.

        Convenience method that calls score() then await_scored().

        :param options: See :typeddict:`~runloop_api_client.sdk._types.PollingRequestOptions` for available options
        :return: Scored scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.score_and_await(
            self._id,
            **options,
        )

    def score_and_complete(
        self,
        **options: Unpack[PollingRequestOptions],
    ) -> ScenarioRunView:
        """Score the run, wait for scoring, then complete and shutdown.

        Convenience method that scores the scenario run, waits for scoring to
        finish, then completes the run and shuts down the devbox.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.PollingRequestOptions` for available options
        :return: Completed scenario run state with scoring results
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.score_and_complete(
            self._id,
            **options,
        )

    def complete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> ScenarioRunView:
        """Complete the scenario run and shutdown the devbox.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
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

        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        :return: Cancelled scenario run state
        :rtype: ScenarioRunView
        """
        return self._client.scenarios.runs.cancel(
            self._id,
            **options,
        )

    def download_logs(
        self,
        file: Union[str, os.PathLike[str]],
        **options: Unpack[LongRequestOptions],
    ) -> None:
        """Download all logs for this scenario run to a zip file.

        Downloads a zip archive containing all logs from the scenario run's
        associated devbox.

        :param file: Path where the zip file will be written
        :type file: str | os.PathLike[str]
        :param options: See :typeddict:`~runloop_api_client.sdk._types.LongRequestOptions` for available options
        """
        response = self._client.scenarios.runs.download_logs(self._id, **options)
        response.write_to_file(file)

    def get_score(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> Optional[ScoringContractResultView]:
        """Get the scoring result for this run.

        Returns None if the run has not been scored yet. Always makes an API
        call to retrieve the current scoring result.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.BaseRequestOptions` for available options
        :return: Scoring result or None if not yet scored
        :rtype: Optional[ScoringContractResultView]
        """
        info = self.get_info(**options)
        return info.scoring_contract_result
