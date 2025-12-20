"""Comprehensive tests for async AsyncScorer class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from tests.sdk.conftest import MockScorerView
from runloop_api_client.sdk import AsyncScorer


class TestAsyncScorer:
    """Tests for AsyncScorer class."""

    def test_init(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncScorer initialization."""
        scorer = AsyncScorer(mock_async_client, "sco_123")
        assert scorer.id == "sco_123"

    def test_repr(self, mock_async_client: AsyncMock) -> None:
        """Test AsyncScorer string representation."""
        scorer = AsyncScorer(mock_async_client, "sco_123")
        assert repr(scorer) == "<AsyncScorer id='sco_123'>"

    @pytest.mark.asyncio
    async def test_get_info(self, mock_async_client: AsyncMock, scorer_view: MockScorerView) -> None:
        """Test get_info method."""
        mock_async_client.scenarios.scorers.retrieve = AsyncMock(return_value=scorer_view)

        scorer = AsyncScorer(mock_async_client, "sco_123")
        result = await scorer.get_info()

        assert result == scorer_view
        mock_async_client.scenarios.scorers.retrieve.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_update(self, mock_async_client: AsyncMock) -> None:
        """Test update method."""
        update_response = SimpleNamespace(id="sco_123", type="updated_scorer", bash_script="echo 'score=1.0'")
        mock_async_client.scenarios.scorers.update = AsyncMock(return_value=update_response)

        scorer = AsyncScorer(mock_async_client, "sco_123")
        result = await scorer.update(
            type="updated_scorer",
            bash_script="echo 'score=1.0'",
        )

        assert result == update_response
        mock_async_client.scenarios.scorers.update.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_validate(self, mock_async_client: AsyncMock) -> None:
        """Test validate method."""
        validate_response = SimpleNamespace(
            name="test_scorer",
            scoring_context={},
            scoring_result=SimpleNamespace(score=0.95),
        )
        mock_async_client.scenarios.scorers.validate = AsyncMock(return_value=validate_response)

        scorer = AsyncScorer(mock_async_client, "sco_123")
        result = await scorer.validate(
            scoring_context={"test": "context"},
        )

        assert result == validate_response
        mock_async_client.scenarios.scorers.validate.assert_awaited_once()
