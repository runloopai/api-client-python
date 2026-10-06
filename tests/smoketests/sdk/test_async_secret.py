"""Asynchronous SDK smoke tests for Secret operations."""

from __future__ import annotations

import pytest

from runloop_api_client import NotFoundError
from runloop_api_client.sdk import AsyncRunloopSDK
from tests.smoketests.utils import unique_name

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120


class TestAsyncSecretLifecycle:
    """Test async secret lifecycle operations: create, get_info, update, list, delete."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_secret_full_lifecycle(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Exercise name and ID operations in one lifecycle, including name reuse."""
        name = "sec_" + unique_name("SDK_TEST_SECRET").replace("-", "_")
        secret = await async_sdk_client.secret.create(name=name, value="synthetic-initial")
        assert secret.name == name
        assert secret.id is not None and secret.id.startswith("sec_")
        ids = [secret.id]
        try:
            named = async_sdk_client.secret.from_name(name)
            assert named.id is None
            info = await named.get_info()
            assert info.id == secret.id
            assert info.create_time_ms > 0
            updated = await async_sdk_client.secret.update(secret, "synthetic-ops")
            assert updated.name == name
            assert (await updated.get_info()).update_time_ms >= info.create_time_ms
            assert (await secret.update("synthetic-name")).name == name
            assert any(item.id == secret.id for item in (await async_sdk_client.secret.list()))

            exact = async_sdk_client.secret.from_id(secret.id)
            assert (await exact.get_info()).name == name
            assert (await exact.update("synthetic-id")).id == exact.id
            assert (await exact.delete()).id == exact.id
            replacement = await async_sdk_client.secret.create(name=name, value="synthetic-replacement")
            assert replacement.id is not None
            ids.append(replacement.id)
            assert replacement.id != exact.id
            # The original wrapper still follows its name, not its captured ID.
            assert (await secret.get_info()).id == replacement.id
            assert secret.id == exact.id
            with pytest.raises(NotFoundError):
                await exact.get_info()
            with pytest.raises(NotFoundError):
                await exact.update("must-not-update-replacement")
            with pytest.raises(NotFoundError):
                await exact.delete()
            assert (await secret.delete()).id == replacement.id
            assert all(item.name != name for item in (await async_sdk_client.secret.list()))
        finally:
            for id in ids:
                try:
                    await async_sdk_client.secret.from_id(id).delete()
                except NotFoundError:
                    pass

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
