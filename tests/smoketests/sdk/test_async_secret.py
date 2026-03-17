"""Asynchronous SDK smoke tests for Secret operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestAsyncSecretLifecycle:
    """Test async secret lifecycle operations: create, get_info, update, list, delete."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_secret_full_lifecycle(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test complete async secret lifecycle: create, get_info, update (both ways), list, from_name, delete."""
        secret_name = unique_name("SDK_ASYNC_TEST_SECRET").upper().replace("-", "_")

        # Create
        secret = await async_sdk_client.secret.create(name=secret_name, value="initial-value")
        assert secret is not None
        assert secret.name == secret_name

        try:
            # get_info uses GET /v1/secrets/{name}
            info = await secret.get_info()
            assert info.id.startswith("sec_")
            assert info.name == secret_name
            assert info.create_time_ms > 0
            create_time_ms = info.create_time_ms

            # Update via AsyncSecretOps
            updated = await async_sdk_client.secret.update(secret, "updated-via-ops")
            assert updated.name == secret_name
            updated_info = await updated.get_info()
            assert updated_info.update_time_ms >= create_time_ms

            # Update via instance method
            instance_updated_info = await secret.update("updated-via-instance")
            assert instance_updated_info.name == secret_name

            # List
            secrets = await async_sdk_client.secret.list()
            assert isinstance(secrets, list)
            assert len(secrets) > 0
            found = next((s for s in secrets if s.name == secret_name), None)
            assert found is not None
            assert found.name == secret_name

            # from_name (no API call)
            by_name = async_sdk_client.secret.from_name(secret_name)
            assert by_name.name == secret_name
            by_name_info = await by_name.get_info()
            assert by_name_info.id == info.id

        finally:
            # Delete
            deleted = await secret.delete()
            assert deleted is not None
            assert deleted.name == secret_name

            # Verify deleted
            remaining = await async_sdk_client.secret.list()
            assert all(s.name != secret_name for s in remaining)

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_secret_delete_via_ops(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test deleting a secret via AsyncSecretOps.delete()."""
        secret_name = unique_name("SDK_ASYNC_DEL_SECRET").upper().replace("-", "_")
        secret = await async_sdk_client.secret.create(name=secret_name, value="to-be-deleted")

        try:
            deleted = await async_sdk_client.secret.delete(secret)
            assert deleted.name == secret_name

            remaining = await async_sdk_client.secret.list()
            assert all(s.name != secret_name for s in remaining)
        except Exception:
            try:
                await secret.delete()
            except Exception:
                pass
            raise


class TestAsyncSecretWithDevbox:
    """Test async secret injection into devboxes."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_devbox_can_access_injected_secret(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test that a secret injected into a devbox is accessible as an env var."""
        secret_name = unique_name("SDK_ASYNC_DEVBOX_SECRET").upper().replace("-", "_")
        secret_value = "async-secret-for-devbox-test"

        secret = await async_sdk_client.secret.create(name=secret_name, value=secret_value)

        devbox = None
        try:
            devbox = await async_sdk_client.devbox.create(
                name=unique_name("async-secret-test-devbox"),
                secrets={
                    "MY_SECRET_VAR": secret.name,
                },
                launch_parameters={
                    "resource_size_request": "X_SMALL",
                    "keep_alive_time_seconds": 60,
                },
            )

            result = await devbox.cmd.exec("echo $MY_SECRET_VAR")
            assert result.exit_code == 0
            assert (await result.stdout()).strip() == secret_value

        finally:
            if devbox is not None:
                try:
                    await devbox.shutdown()
                except Exception:
                    pass
            try:
                await secret.delete()
            except Exception:
                pass
