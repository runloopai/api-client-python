"""Synchronous SDK smoke tests for Axon operations."""

from __future__ import annotations

import json
import uuid

import pytest

from runloop_api_client.sdk import RunloopSDK


def _unique_table() -> str:
    return f"t_{uuid.uuid4().hex[:12]}"

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30


class TestAxonLifecycle:
    """Test basic axon lifecycle operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_axon_create(self, sdk_client: RunloopSDK) -> None:
        """Test creating an axon."""
        axon = sdk_client.axon.create()

        try:
            assert axon is not None
            assert axon.id is not None
            assert len(axon.id) > 0

            info = axon.get_info()
            assert info.id == axon.id
            assert info.created_at_ms > 0
        finally:
            # TODO: Add axon cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_axon_from_id(self, sdk_client: RunloopSDK) -> None:
        """Test retrieving axon by ID."""
        created = sdk_client.axon.create()

        try:
            retrieved = sdk_client.axon.from_id(created.id)
            assert retrieved.id == created.id

            info = retrieved.get_info()
            assert info.id == created.id
        finally:
            # TODO: Add axon cleanup once delete endpoint is implemented
            pass

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_axon_publish(self, sdk_client: RunloopSDK) -> None:
        """Test publishing events to an axon."""
        axon = sdk_client.axon.create()

        try:
            result = axon.publish(
                event_type="test_event",
                origin="USER_EVENT",
                payload=json.dumps({"message": "hello"}),
                source="sdk-smoke-test",
            )

            assert result is not None
            assert result.sequence >= 0
            assert result.timestamp_ms > 0
        finally:
            # TODO: Add axon cleanup once delete endpoint is implemented
            pass


class TestAxonSql:
    """Test axon SQL operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_sql_query_create_and_select(self, sdk_client: RunloopSDK) -> None:
        """Test creating a table and querying it via sql.query."""
        axon = sdk_client.axon.create()
        table = _unique_table()

        axon.sql.query(sql=f"CREATE TABLE {table} (id INTEGER PRIMARY KEY, value TEXT)")

        axon.sql.query(sql=f"INSERT INTO {table} (id, value) VALUES (?, ?)", params=[1, "hello"])

        result = axon.sql.query(sql=f"SELECT * FROM {table} WHERE id = ?", params=[1])

        assert result.columns is not None
        assert len(result.columns) > 0
        assert len(result.rows) == 1
        assert result.meta.duration_ms >= 0

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_sql_batch(self, sdk_client: RunloopSDK) -> None:
        """Test executing multiple statements atomically via sql.batch."""
        axon = sdk_client.axon.create()

        result = axon.sql.batch(
            statements=[
                {"sql": "CREATE TABLE IF NOT EXISTS batch_test (id INTEGER PRIMARY KEY, name TEXT)"},
                {"sql": "INSERT INTO batch_test (id, name) VALUES (?, ?)", "params": [1, "alice"]},
                {"sql": "INSERT INTO batch_test (id, name) VALUES (?, ?)", "params": [2, "bob"]},
                {"sql": "SELECT * FROM batch_test ORDER BY id"},
            ],
        )

        assert result.results is not None
        assert len(result.results) == 4
        select_result = result.results[3]
        assert select_result.success is not None
        assert len(select_result.success.rows) == 2


class TestAxonListing:
    """Test axon listing operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_list_axons(self, sdk_client: RunloopSDK) -> None:
        """Test listing axons."""
        axons = sdk_client.axon.list()

        assert isinstance(axons, list)
        assert len(axons) >= 0
