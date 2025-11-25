"""Scorer resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    BaseRequestOptions,
    SDKScorerListParams,
    SDKScorerCreateParams,
    SDKScorerUpdateParams,
    SDKScorerValidateParams,
)
from .._client import AsyncRunloop
from ..types.scenarios import ScorerUpdateResponse, ScorerRetrieveResponse, ScorerValidateResponse


class AsyncScorer:
    """Asynchronous wrapper around a scenario scorer resource."""

    def __init__(
        self,
        client: AsyncRunloop,
        scorer_id: str,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param scorer_id: Scorer ID returned by the API
        :type scorer_id: str
        """
        self._client = client
        self._id = scorer_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncScorer id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the scorer ID.

        :return: Unique scorer ID
        :rtype: str
        """
        return self._id

    # TODO: replace static method once we have a proper client
    @staticmethod
    async def create(
        client: AsyncRunloop,
        **params: Unpack[SDKScorerCreateParams],
    ) -> "AsyncScorer":
        """Create a new scenario scorer.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerCreateParams` for available parameters
        :return: Wrapper bound to the newly created scorer
        :rtype: AsyncScorer
        """
        response = await client.scenarios.scorers.create(
            **params,
        )
        return AsyncScorer(client, response.id)

    # TODO: replace static method once we have a proper client
    @staticmethod
    async def list(
        client: AsyncRunloop,
        **params: Unpack[SDKScorerListParams],
    ) -> list["AsyncScorer"]:
        """List all scenario scorers.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerListParams` for available parameters
        :return: List of scorer wrappers
        :rtype: list[AsyncScorer]
        """
        page = await client.scenarios.scorers.list(
            **params,
        )
        return [AsyncScorer(client, item.id) async for item in page]

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> ScorerRetrieveResponse:
        """Retrieve the latest scorer details.

        :param options: Optional request configuration
        :return: API response describing the scorer
        :rtype: ScorerRetrieveResponse
        """
        return await self._client.scenarios.scorers.retrieve(
            self._id,
            **options,
        )

    async def update(
        self,
        **params: Unpack[SDKScorerUpdateParams],
    ) -> ScorerUpdateResponse:
        """Update the scorer.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerUpdateParams` for available parameters
        :return: API response with updated scorer details
        :rtype: ScorerUpdateResponse
        """
        return await self._client.scenarios.scorers.update(
            self._id,
            **params,
        )

    async def validate(
        self,
        **params: Unpack[SDKScorerValidateParams],
    ) -> ScorerValidateResponse:
        """Validate the scorer with a given context.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKScorerValidateParams` for available parameters
        :return: API response with validation results
        :rtype: ScorerValidateResponse
        """
        return await self._client.scenarios.scorers.validate(
            self._id,
            **params,
        )
