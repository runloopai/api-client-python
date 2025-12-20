"""Comprehensive tests for sync Scorer class."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import MockScorerView
from runloop_api_client.sdk import Scorer


class TestScorer:
    """Tests for Scorer class."""

    def test_init(self, mock_client: Mock) -> None:
        """Test Scorer initialization."""
        scorer = Scorer(mock_client, "sco_123")
        assert scorer.id == "sco_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Scorer string representation."""
        scorer = Scorer(mock_client, "sco_123")
        assert repr(scorer) == "<Scorer id='sco_123'>"

    def test_get_info(self, mock_client: Mock, scorer_view: MockScorerView) -> None:
        """Test get_info method."""
        mock_client.scenarios.scorers.retrieve.return_value = scorer_view

        scorer = Scorer(mock_client, "sco_123")
        result = scorer.get_info()

        assert result == scorer_view
        mock_client.scenarios.scorers.retrieve.assert_called_once_with("sco_123")

    def test_update(self, mock_client: Mock) -> None:
        """Test update method."""
        update_response = SimpleNamespace(id="sco_123", type="updated_scorer", bash_script="echo 'score=1.0'")
        mock_client.scenarios.scorers.update.return_value = update_response

        scorer = Scorer(mock_client, "sco_123")
        result = scorer.update(
            type="updated_scorer",
            bash_script="echo 'score=1.0'",
        )

        assert result == update_response
        mock_client.scenarios.scorers.update.assert_called_once_with(
            "sco_123",
            type="updated_scorer",
            bash_script="echo 'score=1.0'",
        )

    def test_validate(self, mock_client: Mock) -> None:
        """Test validate method."""
        validate_response = SimpleNamespace(
            name="test_scorer",
            scoring_context={},
            scoring_result=SimpleNamespace(score=0.95),
        )
        mock_client.scenarios.scorers.validate.return_value = validate_response

        scorer = Scorer(mock_client, "sco_123")
        result = scorer.validate(
            scoring_context={"test": "context"},
        )

        assert result == validate_response
        mock_client.scenarios.scorers.validate.assert_called_once_with(
            "sco_123",
            scoring_context={"test": "context"},
        )
