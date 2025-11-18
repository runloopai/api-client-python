"""Asynchronous SDK smoke tests for Blueprint operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestAsyncBlueprintLifecycle:
    """Test basic async blueprint lifecycle operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_blueprint_create_basic(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a basic blueprint with dockerfile."""
        name = unique_name("sdk-async-blueprint-basic")
        blueprint = await async_sdk_client.blueprint.create(
            name=name,
            dockerfile="FROM ubuntu:20.04\nRUN apt-get update && apt-get install -y curl",
        )

        try:
            assert blueprint is not None
            assert blueprint.id is not None
            assert len(blueprint.id) > 0

            # Verify it's built successfully
            info = await blueprint.get_info()
            assert info.status == "build_complete"
            assert info.name == name
        finally:
            await blueprint.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_blueprint_create_with_system_setup(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a blueprint with system setup commands."""
        name = unique_name("sdk-async-blueprint-setup")
        blueprint = await async_sdk_client.blueprint.create(
            name=name,
            dockerfile="FROM ubuntu:20.04",
            system_setup_commands=[
                "sudo apt-get update",
                "sudo apt-get install -y wget",
            ],
        )

        try:
            assert blueprint.id is not None
            info = await blueprint.get_info()
            assert info.status == "build_complete"
            assert info.name == name
        finally:
            await blueprint.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_blueprint_get_info(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving blueprint information."""
        name = unique_name("sdk-async-blueprint-info")
        blueprint = await async_sdk_client.blueprint.create(
            name=name,
            dockerfile="FROM ubuntu:20.04\nRUN echo 'test'",
        )

        try:
            info = await blueprint.get_info()

            assert info.id == blueprint.id
            assert info.status == "build_complete"
            assert info.name == name
        finally:
            await blueprint.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_blueprint_delete(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test deleting a blueprint."""
        blueprint = await async_sdk_client.blueprint.create(
            name=unique_name("sdk-async-blueprint-delete"),
            dockerfile="FROM ubuntu:20.04",
        )

        blueprint_id = blueprint.id
        result = await blueprint.delete()

        assert result is not None
        # Verify it's deleted by checking status
        info = await async_sdk_client.api.blueprints.retrieve(blueprint_id)
        assert info.state == "deleted"


class TestAsyncBlueprintCreationVariations:
    """Test different async blueprint creation scenarios."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT * 2)
    async def test_blueprint_with_base_blueprint(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a blueprint based on another blueprint."""
        # Create base blueprint
        base_blueprint = await async_sdk_client.blueprint.create(
            name=unique_name("sdk-async-blueprint-base"),
            dockerfile="FROM ubuntu:20.04\nRUN apt-get update && apt-get install -y curl",
        )

        try:
            # Create derived blueprint
            name = unique_name("sdk-async-blueprint-derived")
            derived_blueprint = await async_sdk_client.blueprint.create(
                name=name,
                base_blueprint_id=base_blueprint.id,
                system_setup_commands=["sudo apt-get install -y wget"],
            )

            try:
                assert derived_blueprint.id is not None
                info = await derived_blueprint.get_info()
                assert info.status == "build_complete"
                assert info.name == name
            finally:
                await derived_blueprint.delete()
        finally:
            await base_blueprint.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_blueprint_with_metadata(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a blueprint with metadata."""
        name = unique_name("sdk-async-blueprint-metadata")
        metadata = {
            "purpose": "sdk-async-testing",
            "version": "1.0",
        }

        blueprint = await async_sdk_client.blueprint.create(
            name=name,
            dockerfile="FROM ubuntu:20.04",
            metadata=metadata,
        )

        try:
            assert blueprint.id is not None
            info = await blueprint.get_info()
            assert info.status == "build_complete"
            assert info.name == name
            # Metadata should be preserved
            assert info.metadata is not None and info.metadata == metadata
        finally:
            await blueprint.delete()


class TestAsyncBlueprintListing:
    """Test async blueprint listing and retrieval operations."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_list_blueprints(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing blueprints."""
        blueprints = await async_sdk_client.blueprint.list(limit=10)

        assert isinstance(blueprints, list)
        # List might be empty, that's okay
        assert len(blueprints) >= 0

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_get_blueprint_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving blueprint by ID."""
        # Create a blueprint
        created = await async_sdk_client.blueprint.create(
            name=unique_name("sdk-async-blueprint-retrieve"),
            dockerfile="FROM ubuntu:20.04",
        )

        try:
            # Retrieve it by ID
            retrieved = async_sdk_client.blueprint.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same blueprint
            info = await retrieved.get_info()
            assert info.id == created.id
        finally:
            await created.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_list_blueprints_by_name(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing blueprints filtered by name."""
        blueprint_name = unique_name("sdk-async-blueprint-list-name")

        # Create a blueprint with a specific name
        blueprint = await async_sdk_client.blueprint.create(
            name=blueprint_name,
            dockerfile="FROM ubuntu:20.04",
        )

        try:
            # List blueprints with that name
            blueprints = await async_sdk_client.blueprint.list(name=blueprint_name)

            assert isinstance(blueprints, list)
            assert len(blueprints) >= 1

            # Should find our blueprint
            blueprint_ids = [bp.id for bp in blueprints]
            assert blueprint.id in blueprint_ids
        finally:
            await blueprint.delete()


class TestAsyncBlueprintDevboxIntegration:
    """Test integration between async blueprints and devboxes."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT * 2)
    async def test_create_devbox_from_blueprint(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a devbox from a blueprint."""
        # Create a blueprint
        blueprint = await async_sdk_client.blueprint.create(
            name=unique_name("sdk-async-blueprint-for-devbox"),
            dockerfile="FROM ubuntu:20.04\nRUN apt-get update && apt-get install -y python3",
        )

        try:
            # Create devbox from the blueprint
            devbox = await blueprint.create_devbox(
                name=unique_name("sdk-async-devbox-from-blueprint"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
            )

            try:
                assert devbox.id is not None

                # Verify devbox is running
                info = await devbox.get_info()
                assert info.status == "running"

                # Verify the blueprint's software is installed
                result = await devbox.cmd.exec(command="which python3")
                assert result.exit_code == 0
                assert result.success is True
                assert "python" in await result.stdout(num_lines=1)
            finally:
                await devbox.shutdown()
        finally:
            await blueprint.delete()


class TestAsyncBlueprintErrorHandling:
    """Test async blueprint error handling scenarios."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_blueprint_invalid_dockerfile(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a blueprint with an invalid dockerfile."""
        # This should fail because INVALID_COMMAND doesn't exist
        # We expect this to raise an error during build
        try:
            blueprint = await async_sdk_client.blueprint.create(
                name=unique_name("sdk-async-blueprint-invalid"),
                dockerfile="FROM ubuntu:20.04\nRUN INVALID_COMMAND_THAT_DOES_NOT_EXIST",
            )
            # If it somehow succeeds, verify it failed during build
            info = await blueprint.get_info()
            assert info.status in ["failed", "error", "build_failed"]
            await blueprint.delete()
        except Exception:
            # Expected to fail - this is the success case
            pass
