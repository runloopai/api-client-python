"""Scorer resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    BaseRequestOptions,
    SDKScorerUpdateParams,
    SDKScorerValidateParams,
)
from .._client import AsyncRunloop
from ..types.scenarios import ScorerUpdateResponse, ScorerRetrieveResponse, ScorerValidateResponse


class AsyncScorer:
    """A custom scorer for evaluating scenario outputs (async).

    Scorers define bash scripts that produce a score in the range [0.0, 1.0] for scenario runs.
    Obtain instances via ``runloop.scorer.create()`` or ``runloop.scorer.from_id()``.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> scorer = await runloop.scorer.create(type="my_scorer", bash_script="echo 'score=1.0'")
        >>> await scorer.validate(scoring_context={"output": "test"})
    """

    def __init__(self, client: AsyncRunloop, scorer_id: str) -> None:
        """Create an AsyncScorer instance.

        :param client: AsyncRunloop client instance
        :type client: AsyncRunloop
        :param scorer_id: ID of the scorer
        :type scorer_id: str
        """
        self._client = client
        self._id = scorer_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncScorer id={self._id!r}>"

    @property
    def id(self) -> str:
        """The scorer's unique identifier.

        :return: Scorer ID
        :rtype: str
        """
        return self._id

    async def get_info(self, **options: Unpack[BaseRequestOptions]) -> ScorerRetrieveResponse:
        """Fetch current scorer details from the API.

        :param options: See :typeddict:`~runloop_api_client.sdk._types.BaseRequestOptions` for available options
        :return: Current scorer details
        :rtype: ScorerRetrieveResponse
        """
        return await self._client.scenarios.scorers.retrieve(self._id, **options)

    async def update(self, **params: Unpack[SDKScorerUpdateParams]) -> ScorerUpdateResponse:
        """Update the scorer's type or bash script.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerUpdateParams` for available parameters
        :return: Updated scorer details
        :rtype: ScorerUpdateResponse
        """
        return await self._client.scenarios.scorers.update(self._id, **params)

    async def validate(self, **params: Unpack[SDKScorerValidateParams]) -> ScorerValidateResponse:
        """Run the scorer against the provided context and return the result.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerValidateParams` for available parameters
        :return: Validation result with score
        :rtype: ScorerValidateResponse
        """
        return await self._client.scenarios.scorers.validate(self._id, **params)
