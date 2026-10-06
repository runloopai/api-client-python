"""Synchronous SDK smoke tests for Secret operations."""

from __future__ import annotations

import pytest

from runloop_api_client import NotFoundError
from runloop_api_client.sdk import RunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestSecretLifecycle:
    """Test secret lifecycle operations: create, get_info, update, list, delete."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    def test_secret_full_lifecycle(self, sdk_client: RunloopSDK) -> None:
        """Exercise name and ID operations in one lifecycle, including name reuse."""
        name = "sec_" + unique_name("SDK_TEST_SECRET").replace("-", "_")
        secret = sdk_client.secret.create(name=name, value="synthetic-initial")
        assert secret.name == name
        assert secret.id is not None and secret.id.startswith("sec_")
        ids = [secret.id]
        try:
            named = sdk_client.secret.from_name(name)
            assert named.id is None
            info = named.get_info()
            assert info.id == secret.id
            assert info.create_time_ms > 0
            updated = sdk_client.secret.update(secret, "synthetic-ops")
            assert updated.name == name
            assert updated.get_info().update_time_ms >= info.create_time_ms
            assert secret.update("synthetic-name").name == name
            assert any(item.id == secret.id for item in sdk_client.secret.list())

            exact = sdk_client.secret.from_id(secret.id)
            assert exact.get_info().name == name
            assert exact.update("synthetic-id").id == exact.id
            assert exact.delete().id == exact.id
            replacement = sdk_client.secret.create(name=name, value="synthetic-replacement")
            assert replacement.id is not None
            ids.append(replacement.id)
            assert replacement.id != exact.id
            # The original wrapper still follows its name, not its captured ID.
            assert secret.get_info().id == replacement.id
            assert secret.id == exact.id
            with pytest.raises(NotFoundError):
                exact.get_info()
            with pytest.raises(NotFoundError):
                exact.update("must-not-update-replacement")
            with pytest.raises(NotFoundError):
                exact.delete()
            assert secret.delete().id == replacement.id
            assert all(item.name != name for item in sdk_client.secret.list())
        finally:
            for id in ids:
                try:
                    sdk_client.secret.from_id(id).delete()
                except NotFoundError:
                    pass

    @pytest.mark.parametrize("by_name", [False, True])
    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    def test_secret_delete_via_ops(self, sdk_client: RunloopSDK, by_name: bool) -> None:
        """Test deleting a secret via SecretOps.delete()."""
        secret_name = unique_name("SDK_TEST_DEL_SECRET").upper().replace("-", "_")
        secret = sdk_client.secret.create(name=secret_name, value="to-be-deleted")

        try:
            deleted = sdk_client.secret.delete(secret.name if by_name else secret)
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
