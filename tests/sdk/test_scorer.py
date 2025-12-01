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
        scorer = Scorer(mock_client, "scorer_123")
        assert scorer.id == "scorer_123"

    def test_repr(self, mock_client: Mock) -> None:
        """Test Scorer string representation."""
        scorer = Scorer(mock_client, "scorer_123")
        assert repr(scorer) == "<Scorer id='scorer_123'>"

    def test_id_property(self, mock_client: Mock) -> None:
        """Test id property returns the scorer ID."""
        scorer = Scorer(mock_client, "scorer_123")
        assert scorer.id == "scorer_123"

    def test_get_info(self, mock_client: Mock, scorer_view: MockScorerView) -> None:
        """Test get_info method."""
        mock_client.scenarios.scorers.retrieve.return_value = scorer_view

        scorer = Scorer(mock_client, "scorer_123")
        result = scorer.get_info(
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == scorer_view
        mock_client.scenarios.scorers.retrieve.assert_called_once_with(
            "scorer_123",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_update(self, mock_client: Mock) -> None:
        """Test update method."""
        update_response = SimpleNamespace(id="scorer_123", name="updated-scorer")
        mock_client.scenarios.scorers.update.return_value = update_response

        scorer = Scorer(mock_client, "scorer_123")
        result = scorer.update(
            name="updated-scorer",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == update_response
        mock_client.scenarios.scorers.update.assert_called_once_with(
            "scorer_123",
            name="updated-scorer",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

    def test_validate(self, mock_client: Mock) -> None:
        """Test validate method."""
        validate_response = SimpleNamespace(
            is_valid=True,
            score=0.95,
            reasoning="The output matches expected criteria.",
        )
        mock_client.scenarios.scorers.validate.return_value = validate_response

        scorer = Scorer(mock_client, "scorer_123")
        result = scorer.validate(
            bash_command_output="test output",
            expected_output="test output",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )

        assert result == validate_response
        assert result.is_valid is True
        assert result.score == 0.95
        mock_client.scenarios.scorers.validate.assert_called_once_with(
            "scorer_123",
            bash_command_output="test output",
            expected_output="test output",
            extra_headers={"X-Custom": "value"},
            extra_query={"param": "value"},
            extra_body={"key": "value"},
            timeout=30.0,
        )
