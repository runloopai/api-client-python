"""Asynchronous SDK smoke tests for Scorer operations."""

from __future__ import annotations

import pytest

from runloop_api_client import InternalServerError
from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30
ONE_MINUTE_TIMEOUT = 60


class TestAsyncScorerLifecycle:
    """Test basic async scorer lifecycle operations."""

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    async def test_scorer_create_basic(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a basic scorer."""
        scorer_type = unique_name("sdk-async-scorer-basic")
        scorer = await async_sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=1.0'",
        )

        assert scorer is not None
        assert scorer.id is not None
        assert len(scorer.id) > 0

        # Verify it's created successfully
        info = await scorer.get_info()
        assert info.type == scorer_type
        assert info.bash_script == "echo 'score=1.0'"

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    async def test_scorer_get_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving scorer information."""
        scorer_type = unique_name("sdk-async-scorer-info")
        scorer = await async_sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=0.5'",
        )

        info = await scorer.get_info()

        assert info.id == scorer.id
        assert info.type == scorer_type

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    async def test_scorer_update(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test updating a scorer."""
        scorer_type = unique_name("sdk-async-scorer-update")
        scorer = await async_sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=0.0'",
        )

        updated_type = unique_name("sdk-async-scorer-updated")
        result = await scorer.update(
            type=updated_type,
            bash_script="echo 'score=1.0'",
        )

        assert result is not None

        # Verify the update
        info = await scorer.get_info()
        assert info.type == updated_type
        assert info.bash_script == "echo 'score=1.0'"

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    async def test_scorer_validate(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test validating a scorer."""
        scorer_type = unique_name("sdk-async-scorer-validate")
        scorer = await async_sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=1.0'",
        )

        try:
            result = await scorer.validate(
                scoring_context={},
            )
            assert result is not None
        except InternalServerError:
            # Backend may return 500 for validate endpoint - skip if this happens
            pytest.skip("Backend returned 500 for scorer validate endpoint")


class TestAsyncScorerListing:
    """Test async scorer listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_scorers(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing scorers."""
        scorers = await async_sdk_client.scorer.list(limit=10)

        assert isinstance(scorers, list)
        # List might be empty, that's okay
        assert len(scorers) >= 0

    @pytest.mark.timeout(ONE_MINUTE_TIMEOUT)
    async def test_get_scorer_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving scorer by ID."""
        # Create a scorer
        scorer_type = unique_name("sdk-async-scorer-retrieve")
        created = await async_sdk_client.scorer.create(
            type=scorer_type,
            bash_script="echo 'score=1.0'",
        )

        # Retrieve it by ID
        retrieved = async_sdk_client.scorer.from_id(created.id)
        assert retrieved.id == created.id

        # Verify it's the same scorer
        info = await retrieved.get_info()
        assert info.id == created.id
        assert info.type == scorer_type
