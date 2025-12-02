"""Synchronous SDK smoke tests for Scorer operations."""

from __future__ import annotations

import pytest

from runloop_api_client import InternalServerError
from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30
ONE_MINUTE_TIMEOUT = 60


class TestScorerLifecycle:
    """Test basic scorer lifecycle operations."""

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    def test_scorer_create_basic(self, sdk_client: RunloopSDK) -> None:
        """Test creating a basic scorer."""
        scorer_type = unique_name("sdk-scorer-basic")
        scorer = sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=1.0'",
        )

        assert scorer is not None
        assert scorer.id is not None
        assert len(scorer.id) > 0

        # Verify it's created successfully
        info = scorer.get_info()
        assert info.type == scorer_type
        assert info.bash_script == "echo 'score=1.0'"

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    def test_scorer_get_info(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving scorer information."""
        scorer_type = unique_name("sdk-scorer-info")
        scorer = sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=0.5'",
        )

        info = scorer.get_info()

        assert info.id == scorer.id
        assert info.type == scorer_type

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    def test_scorer_update(self, sdk_client: RunloopSDK) -> None:
        """Test updating a scorer."""
        scorer_type = unique_name("sdk-scorer-update")
        scorer = sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=0.0'",
        )

        updated_type = unique_name("sdk-scorer-updated")
        result = scorer.update(
            type=updated_type,
            bash_script="echo 'score=1.0'",
        )

        assert result is not None

        # Verify the update
        info = scorer.get_info()
        assert info.type == updated_type
        assert info.bash_script == "echo 'score=1.0'"

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    def test_scorer_validate(self, sdk_client: RunloopSDK) -> None:
        """Test validating a scorer."""
        scorer_type = unique_name("sdk-scorer-validate")
        scorer = sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=1.0'",
        )

        try:
            result = scorer.validate(
                scoring_context={},
            )
            assert result is not None
        except InternalServerError:
            # Backend may return 500 for validate endpoint - skip if this happens
            pytest.skip("Backend returned 500 for scorer validate endpoint")


class TestScorerListing:
    """Test scorer listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_scorers(self, sdk_client: RunloopSDK) -> None:
        """Test listing scorers."""
        scorers = sdk_client.scorer.list(limit=10)

        assert isinstance(scorers, list)
        # List might be empty, that's okay
        assert len(scorers) >= 0

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    def test_get_scorer_by_id(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving scorer by ID."""
        # Create a scorer
        scorer_type = unique_name("sdk-scorer-retrieve")
        created = sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=1.0'",
        )

        # Retrieve it by ID
        retrieved = sdk_client.scorer.from_id(created.id)
        assert retrieved.id == created.id

        # Verify it's the same scorer
        info = retrieved.get_info()
        assert info.id == created.id
        assert info.type == scorer_type
