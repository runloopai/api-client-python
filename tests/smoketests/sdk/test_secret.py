"""Synchronous SDK smoke tests for Secret operations."""

from __future__ import annotations

import pytest

from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestSecretLifecycle:
    """Test secret lifecycle operations: create, get_info, update, list, delete."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_secret_full_lifecycle(self, sdk_client: RunloopSDK) -> None:
        """Test complete secret lifecycle: create, get_info, update (both ways), list, from_name, delete."""
        secret_name = unique_name("SDK_TEST_SECRET").upper().replace("-", "_")

        # Create
        secret = sdk_client.secret.create(name=secret_name, value="initial-value")
        assert secret is not None
        assert secret.name == secret_name

        try:
            # get_info uses GET /v1/secrets/{name}
            info = secret.get_info()
            assert info.id.startswith("sec_")
            assert info.name == secret_name
            assert info.create_time_ms > 0
            create_time_ms = info.create_time_ms

            # Update via SecretOps
            updated = sdk_client.secret.update(secret, "updated-via-ops")
            assert updated.name == secret_name
            updated_info = updated.get_info()
            assert updated_info.update_time_ms >= create_time_ms

            # Update via instance method
            instance_updated_info = secret.update("updated-via-instance")
            assert instance_updated_info.name == secret_name

            # List
            secrets = sdk_client.secret.list()
            assert isinstance(secrets, list)
            assert len(secrets) > 0
            found = next((s for s in secrets if s.name == secret_name), None)
            assert found is not None
            assert found.name == secret_name

            # from_name (no API call)
            by_name = sdk_client.secret.from_name(secret_name)
            assert by_name.name == secret_name
            by_name_info = by_name.get_info()
            assert by_name_info.id == info.id

        finally:
            # Delete
            deleted = secret.delete()
            assert deleted is not None
            assert deleted.name == secret_name

            # Verify deleted
            remaining = sdk_client.secret.list()
            assert all(s.name != secret_name for s in remaining)

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_secret_delete_via_ops(self, sdk_client: RunloopSDK) -> None:
        """Test deleting a secret via SecretOps.delete()."""
        secret_name = unique_name("SDK_TEST_DEL_SECRET").upper().replace("-", "_")
        secret = sdk_client.secret.create(name=secret_name, value="to-be-deleted")

        try:
            deleted = sdk_client.secret.delete(secret)
            assert deleted.name == secret_name

            remaining = sdk_client.secret.list()
            assert all(s.name != secret_name for s in remaining)
        except Exception:
            # Cleanup if delete failed
            try:
                secret.delete()
            except Exception:
                pass
            raise

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_secret_delete_by_name_string(self, sdk_client: RunloopSDK) -> None:
        """Test deleting a secret by passing a name string to SecretOps.delete()."""
        secret_name = unique_name("SDK_TEST_STR_SECRET").upper().replace("-", "_")
        sdk_client.secret.create(name=secret_name, value="to-be-deleted-by-name")

        try:
            deleted = sdk_client.secret.delete(secret_name)
            assert deleted.name == secret_name
        except Exception:
            try:
                sdk_client.secret.delete(secret_name)
            except Exception:
                pass
            raise


class TestSecretWithDevbox:
    """Test secret injection into devboxes."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_devbox_can_access_injected_secret(self, sdk_client: RunloopSDK) -> None:
        """Test that a secret injected into a devbox is accessible as an env var."""
        secret_name = unique_name("SDK_DEVBOX_SECRET").upper().replace("-", "_")
        secret_value = "secret-for-devbox-test"

        secret = sdk_client.secret.create(name=secret_name, value=secret_value)

        devbox = None
        try:
            devbox = sdk_client.devbox.create(
                name=unique_name("secret-test-devbox"),
                secrets={
                    "MY_SECRET_VAR": secret.name,
                },
                launch_parameters={
                    "resource_size_request": "X_SMALL",
                    "keep_alive_time_seconds": 60,
                },
            )

            result = devbox.cmd.exec("echo $MY_SECRET_VAR")
            assert result.exit_code == 0
            assert result.stdout().strip() == secret_value

        finally:
            if devbox is not None:
                try:
                    devbox.shutdown()
                except Exception:
                    pass
            try:
                secret.delete()
            except Exception:
                pass
