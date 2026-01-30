"""Asynchronous SDK smoke tests for Devbox operations."""

from __future__ import annotations

import tempfile
from typing import AsyncIterator
from pathlib import Path

import pytest

from runloop_api_client.sdk import AsyncDevbox, AsyncRunloopSDK
from tests.smoketests.utils import unique_name
from runloop_api_client.lib.polling import PollingConfig

pytestmark = [pytest.mark.smoketest, pytest.mark.asyncio]

THIRTY_SECOND_TIMEOUT = 30
TWO_MINUTE_TIMEOUT = 120
FOUR_MINUTE_TIMEOUT = 240


@pytest.fixture(scope="module")
async def shared_devbox(async_sdk_client: AsyncRunloopSDK) -> AsyncIterator[AsyncDevbox]:
    """Create a shared devbox for tests that don't modify state."""
    devbox = await async_sdk_client.devbox.create(
        name=unique_name("sdk-async-devbox-shared"),
        launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 10},
    )
    try:
        yield devbox
    finally:
        try:
            await devbox.shutdown()
        except Exception:
            pass


class TestAsyncDevboxLifecycle:
    """Test basic async devbox lifecycle operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_devbox_create(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a devbox and verify it reaches running state."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-create"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        assert devbox is not None
        assert devbox.id is not None
        assert len(devbox.id) > 0

        # Verify it's running
        info = await devbox.get_info()
        assert info.status == "running"
        assert info.name is not None

        # Cleanup
        await devbox.shutdown()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_devbox_get_info(self, shared_devbox: AsyncDevbox) -> None:
        """Test retrieving devbox information."""
        info = await shared_devbox.get_info()

        assert info.id == shared_devbox.id
        assert info.status == "running"
        assert info.name is not None

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_devbox_shutdown(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test shutting down a devbox."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-shutdown"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        result = await devbox.shutdown()
        assert result.id == devbox.id
        assert result.status == "shutdown"

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_devbox_context_manager(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test devbox async context manager automatically shuts down on exit."""
        devbox_id = None

        async with await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-context"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        ) as devbox:
            devbox_id = devbox.id
            assert devbox.id is not None

            # Verify it's running
            info = await devbox.get_info()
            assert info.status == "running"

        # After exiting context, devbox should be shutdown
        final_info = await async_sdk_client.api.devboxes.retrieve(devbox_id)
        assert final_info.status == "shutdown"


class TestAsyncDevboxCommandExecution:
    """Test async command execution on devboxes."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_simple_command(self, shared_devbox: AsyncDevbox) -> None:
        """Test executing a simple command asynchronously."""
        result = await shared_devbox.cmd.exec("echo 'Hello from async SDK!'")

        assert result is not None
        assert result.exit_code == 0
        assert result.success is True

        stdout = await result.stdout(num_lines=1)
        assert "Hello from async SDK!" in stdout

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_with_exit_code(self, shared_devbox: AsyncDevbox) -> None:
        """Test command execution captures exit codes correctly."""
        result = await shared_devbox.cmd.exec("exit 42")

        assert result.exit_code == 42
        assert result.success is False
        assert await result.stdout(num_lines=1) == ""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_async_command(self, shared_devbox: AsyncDevbox) -> None:
        """Test executing a command asynchronously with exec_async."""
        execution = await shared_devbox.cmd.exec_async("echo 'Async command' && sleep 1")

        assert execution is not None
        assert execution.execution_id is not None

        # Wait for completion
        result = await execution.result()
        assert result.exit_code == 0
        assert result.success is True

        stdout = await result.stdout(num_lines=2)
        assert "Async command" in stdout

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_with_stdout_callback(self, shared_devbox: AsyncDevbox) -> None:
        """Test command execution with stdout streaming callback."""
        stdout_lines: list[str] = []

        def stdout_callback(line: str) -> None:
            stdout_lines.append(line)

        result = await shared_devbox.cmd.exec(
            'echo "line1" && echo "line2" && echo "line3"',
            stdout=stdout_callback,
        )

        assert result.success is True
        assert result.exit_code == 0

        combined_stdout = await result.stdout(num_lines=3)
        assert "line1" in combined_stdout

        # Verify callback received output
        assert len(stdout_lines) > 0
        stdout_combined = "".join(stdout_lines)
        assert "line1" in stdout_combined
        assert "line2" in stdout_combined
        assert "line3" in stdout_combined

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_with_stderr_callback(self, shared_devbox: AsyncDevbox) -> None:
        """Test command execution with stderr streaming callback."""
        stderr_lines: list[str] = []

        def stderr_callback(line: str) -> None:
            stderr_lines.append(line)

        result = await shared_devbox.cmd.exec(
            'echo "error1" >&2 && echo "error2" >&2',
            stderr=stderr_callback,
        )

        assert result.success is True
        assert result.exit_code == 0

        combined_stderr = await result.stderr(num_lines=2)
        assert "error1" in combined_stderr

        # Verify callback received stderr output
        assert len(stderr_lines) > 0
        stderr_combined = "".join(stderr_lines)
        assert "error1" in stderr_combined
        assert "error2" in stderr_combined

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_with_large_stdout(self, shared_devbox: AsyncDevbox) -> None:
        """Ensure we capture all stdout lines (similar to TS last_n coverage)."""
        result = await shared_devbox.cmd.exec(
            "; ".join([f"echo line {i}" for i in range(1, 7)]),
        )

        assert result.exit_code == 0
        lines = (await result.stdout()).strip().split("\n")
        assert lines == [f"line {i}" for i in range(1, 7)]

        tail = (await result.stdout(num_lines=3)).strip().split("\n")
        assert tail == ["line 4", "line 5", "line 6"]

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_with_output_callback(self, shared_devbox: AsyncDevbox) -> None:
        """Test command execution with combined output callback."""
        output_lines: list[str] = []

        def output_callback(line: str) -> None:
            output_lines.append(line)

        result = await shared_devbox.cmd.exec(
            'echo "stdout1" && echo "stderr1" >&2 && echo "stdout2"',
            output=output_callback,
        )

        assert result.success is True
        assert result.exit_code == 0

        stdout_capture = await result.stdout(num_lines=2)
        assert "stdout1" in stdout_capture or "stdout2" in stdout_capture

        # Verify callback received both stdout and stderr
        assert len(output_lines) > 0
        output_combined = "".join(output_lines)
        assert "stdout1" in output_combined or "stdout2" in output_combined

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_exec_async_with_callbacks(self, shared_devbox: AsyncDevbox) -> None:
        """Test async execution with streaming callbacks."""
        stdout_lines: list[str] = []

        def stdout_callback(line: str) -> None:
            stdout_lines.append(line)

        execution = await shared_devbox.cmd.exec_async(
            'echo "async output"',
            stdout=stdout_callback,
        )

        assert execution.execution_id is not None

        # Wait for completion
        result = await execution.result()
        assert result.success is True
        assert result.exit_code == 0

        async_stdout = await result.stdout(num_lines=1)
        assert "async output" in async_stdout

        # Verify streaming captured output
        assert len(stdout_lines) > 0
        stdout_combined = "".join(stdout_lines)
        assert "async output" in stdout_combined


class TestAsyncDevboxFileOperations:
    """Test file operations on async devboxes."""

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_file_write_and_read(self, shared_devbox: AsyncDevbox) -> None:
        """Test writing and reading files."""
        file_path = "/tmp/test_async_sdk_file.txt"
        content = "Hello from async SDK file operations!"

        # Write file
        await shared_devbox.file.write(file_path=file_path, contents=content)

        # Read file
        read_content = await shared_devbox.file.read(file_path=file_path)
        assert read_content == content

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_file_write_bytes(self, shared_devbox: AsyncDevbox) -> None:
        """Test writing bytes to a file."""
        file_path = "/tmp/test_async_sdk_bytes.txt"
        content = b"Binary content from async SDK"

        # Write bytes
        await shared_devbox.file.write(file_path=file_path, contents=content.decode("utf-8"))

        # Read and verify
        read_content = await shared_devbox.file.read(file_path=file_path)
        assert read_content == content.decode("utf-8")

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_file_download(self, shared_devbox: AsyncDevbox) -> None:
        """Test downloading a file."""
        file_path = "/tmp/test_async_download.txt"
        content = "Content to download"

        # Write file first
        await shared_devbox.file.write(file_path=file_path, contents=content)

        # Download file
        downloaded = await shared_devbox.file.download(path=file_path)
        assert isinstance(downloaded, bytes)
        assert downloaded.decode("utf-8") == content

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_file_upload(self, shared_devbox: AsyncDevbox) -> None:
        """Test uploading a file."""
        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as tmp_file:
            tmp_file.write("Uploaded content from async SDK")
            tmp_path = tmp_file.name

        try:
            # Upload file
            remote_path = "~/uploaded_async_test.txt"
            await shared_devbox.file.upload(path=remote_path, file=Path(tmp_path))

            # Verify by reading
            content = await shared_devbox.file.read(file_path=remote_path)
            assert content == "Uploaded content from async SDK"
        finally:
            # Cleanup temp file
            Path(tmp_path).unlink(missing_ok=True)


class TestAsyncDevboxStateManagement:
    """Test async devbox state management operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_suspend_and_resume(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test suspending and resuming a devbox."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-suspend"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Suspend the devbox
            suspended_info = await devbox.suspend()
            if suspended_info.status != "suspended":
                suspended_info = await devbox.await_suspended(
                    polling_config=PollingConfig(timeout_seconds=120.0, interval_seconds=5.0)
                )
            assert suspended_info.status == "suspended"

            # Verify suspended state
            info = await devbox.get_info()
            assert info.status == "suspended"

            # Resume the devbox - resume() automatically waits for running state
            resumed_info = await devbox.resume(
                polling_config=PollingConfig(timeout_seconds=120.0, interval_seconds=5.0)
            )
            assert resumed_info.status == "running"

            # Verify running state
            info = await devbox.get_info()
            assert info.status == "running"
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_resume_async(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test resuming a devbox asynchronously without waiting."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-resume-async"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )
        # wait for devbox to be running
        await devbox.await_running(polling_config=PollingConfig(timeout_seconds=120.0, interval_seconds=5.0))

        try:
            # Suspend the devbox
            suspended_info = await devbox.suspend()
            if suspended_info.status != "suspended":
                suspended_info = await devbox.await_suspended(
                    polling_config=PollingConfig(timeout_seconds=120.0, interval_seconds=5.0)
                )
            assert suspended_info.status == "suspended"

            # Verify suspended state
            info = await devbox.get_info()
            assert info.status == "suspended"

            # Resume the devbox asynchronously - doesn't wait automatically
            resume_response = await devbox.resume_async()
            assert resume_response is not None

            # Status might still be suspended or transitioning
            info_after_resume = await devbox.get_info()
            assert info_after_resume.status in ["suspended", "running", "starting", "provisioning"]

            # Now wait for running state explicitly
            running_info = await devbox.await_running(
                polling_config=PollingConfig(timeout_seconds=120.0, interval_seconds=5.0)
            )
            assert running_info.status == "running"
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_await_running(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test await_running method."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-await"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # It should already be running, but test the await method
            result = await devbox.await_running(polling_config=PollingConfig(timeout_seconds=60, interval_seconds=2))
            assert result.status == "running"
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(THIRTY_SECOND_TIMEOUT)
    async def test_keep_alive(self, shared_devbox: AsyncDevbox) -> None:
        """Test sending keep-alive signal."""
        result = await shared_devbox.keep_alive()
        assert result is not None


class TestAsyncDevboxNetworking:
    """Test async devbox networking operations."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_create_ssh_key(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating SSH key for devbox."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-ssh"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            ssh_key = await devbox.net.create_ssh_key()
            assert ssh_key is not None
            assert ssh_key.ssh_private_key is not None
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_create_and_remove_tunnel(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating and removing a tunnel."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-tunnel"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create tunnel
            tunnel = await devbox.net.create_tunnel(port=8080)
            assert tunnel is not None
            assert tunnel.url is not None
            assert tunnel.port == 8080
            assert tunnel.devbox_id == devbox.id

            # Remove tunnel
            await devbox.net.remove_tunnel(port=8080)
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_create_with_tunnel_param(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a devbox with tunnel configuration in create params."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-tunnel-param"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
            tunnel={"auth_mode": "open"},
        )

        try:
            # Verify devbox is running
            info = await devbox.get_info()
            assert info.status == "running"

            # Verify tunnel was created at launch
            assert info.tunnel is not None
            assert info.tunnel.tunnel_key is not None
            assert info.tunnel.auth_mode is not None
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_enable_tunnel(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test enabling a V2 tunnel on an existing devbox."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-enable-tunnel"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Verify no tunnel exists initially
            info = await devbox.get_info()
            assert info.tunnel is None

            # Enable tunnel using the V2 API via SDK
            tunnel = await devbox.net.enable_tunnel(auth_mode="open")
            assert tunnel is not None
            assert tunnel.tunnel_key is not None
            assert tunnel.auth_mode is not None

            # Verify tunnel is now present in devbox info
            info = await devbox.get_info()
            assert info.tunnel is not None
            assert info.tunnel.tunnel_key == tunnel.tunnel_key
        finally:
            await devbox.shutdown()


class TestAsyncDevboxCreationMethods:
    """Test various async devbox creation methods."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT * 2)
    async def test_create_from_blueprint_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating devbox from blueprint ID."""
        # First create a blueprint
        blueprint = await async_sdk_client.blueprint.create(
            name=unique_name("sdk-async-blueprint-for-devbox"),
            dockerfile="FROM ubuntu:22.04\nRUN apt-get update && apt-get install -y curl",
        )

        try:
            # Create devbox from blueprint
            devbox = await async_sdk_client.devbox.create_from_blueprint_id(
                blueprint_id=blueprint.id,
                name=unique_name("sdk-async-devbox-from-blueprint-id"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
            )

            try:
                assert devbox.id is not None
                info = await devbox.get_info()
                assert info.status == "running"
            finally:
                await devbox.shutdown()
        finally:
            await blueprint.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT * 2)
    async def test_create_from_blueprint_name(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating devbox from blueprint name."""
        blueprint_name = unique_name("sdk-async-blueprint-name")

        # Create blueprint
        blueprint = await async_sdk_client.blueprint.create(
            name=blueprint_name,
            dockerfile="FROM ubuntu:22.04\nRUN apt-get update && apt-get install -y wget",
        )

        try:
            # Create devbox from blueprint name
            devbox = await async_sdk_client.devbox.create_from_blueprint_name(
                blueprint_name=blueprint_name,
                name=unique_name("sdk-async-devbox-from-blueprint-name"),
                launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
            )

            try:
                assert devbox.id is not None
                info = await devbox.get_info()
                assert info.status == "running"
            finally:
                await devbox.shutdown()
        finally:
            await blueprint.delete()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT * 2)
    async def test_create_from_snapshot(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating devbox from snapshot."""
        # Create source devbox
        source_devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-for-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create a file in the devbox
            await source_devbox.file.write(
                file_path="/tmp/test_async_snapshot.txt", contents="Async snapshot test content"
            )

            # Create snapshot
            snapshot = await source_devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot-for-devbox"),
            )

            try:
                # Create devbox from snapshot
                devbox = await async_sdk_client.devbox.create_from_snapshot(
                    snapshot_id=snapshot.id,
                    name=unique_name("sdk-async-devbox-from-snapshot"),
                    launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
                )

                try:
                    assert devbox.id is not None
                    info = await devbox.get_info()
                    assert info.status == "running"

                    # Verify snapshot content is present
                    content = await devbox.file.read(file_path="/tmp/test_async_snapshot.txt")
                    assert content == "Async snapshot test content"
                finally:
                    await devbox.shutdown()
            finally:
                await snapshot.delete()
        finally:
            await source_devbox.shutdown()


class TestAsyncDevboxListing:
    """Test async devbox listing and retrieval."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_list_devboxes(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test listing devboxes."""
        devboxes = await async_sdk_client.devbox.list(limit=10)

        assert isinstance(devboxes, list)
        # We should have at least the shared devbox
        assert len(devboxes) >= 0

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_get_devbox_by_id(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test retrieving devbox by ID."""
        # Create a devbox
        created = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-retrieve"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Retrieve it by ID
            retrieved = async_sdk_client.devbox.from_id(created.id)
            assert retrieved.id == created.id

            # Verify it's the same devbox
            info = await retrieved.get_info()
            assert info.id == created.id
        finally:
            await created.shutdown()


class TestAsyncDevboxSnapshots:
    """Test snapshot operations on async devboxes."""

    @pytest.mark.timeout(FOUR_MINUTE_TIMEOUT)
    async def test_snapshot_disk(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a snapshot from devbox (synchronous wait)."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-snapshot"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create a file to snapshot
            await devbox.file.write(file_path="/tmp/async_snapshot_test.txt", contents="Async snapshot content")

            # Create snapshot (waits for completion)
            snapshot = await devbox.snapshot_disk(
                name=unique_name("sdk-async-snapshot"),
            )

            try:
                assert snapshot.id is not None

                # Verify snapshot info
                info = await snapshot.get_info()
                assert info.status == "complete"
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_snapshot_disk_async(self, async_sdk_client: AsyncRunloopSDK) -> None:
        """Test creating a snapshot asynchronously."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-snapshot-async"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )

        try:
            # Create snapshot asynchronously (returns immediately)
            snapshot = await devbox.snapshot_disk_async(
                name=unique_name("sdk-async-snapshot-async"),
            )

            try:
                assert snapshot.id is not None

                # Wait for completion
                await snapshot.await_completed()

                # Verify it's completed
                info = await snapshot.get_info()
                assert info.status == "complete"
            finally:
                await snapshot.delete()
        finally:
            await devbox.shutdown()


class TestAsyncDevboxExecutionPagination:
    """Test stdout/stderr pagination and streaming functionality."""

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_exec_with_large_stdout_streaming(self, shared_devbox: AsyncDevbox) -> None:
        """Test that large stdout output is fully captured via streaming when truncated."""
        # Generate 1000 lines of output
        result = await shared_devbox.cmd.exec(
            'for i in $(seq 1 1000); do echo "Line $i with some content to make it realistic"; done',
        )

        assert result.exit_code == 0
        stdout = await result.stdout()
        lines = stdout.strip().split("\n")

        # Verify we got all 1000 lines
        assert len(lines) == 1000, f"Expected 1000 lines, got {len(lines)}"

        # Verify first and last lines
        assert "Line 1" in lines[0]
        assert "Line 1000" in lines[-1]

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_exec_with_large_stderr_streaming(self, shared_devbox: AsyncDevbox) -> None:
        """Test that large stderr output is fully captured via streaming when truncated."""
        # Generate 1000 lines of stderr output
        result = await shared_devbox.cmd.exec(
            'for i in $(seq 1 1000); do echo "Error line $i" >&2; done',
        )

        assert result.exit_code == 0
        stderr = await result.stderr()
        lines = stderr.strip().split("\n")

        # Verify we got all 1000 lines
        assert len(lines) == 1000, f"Expected 1000 lines, got {len(lines)}"

        # Verify first and last lines
        assert "Error line 1" in lines[0]
        assert "Error line 1000" in lines[-1]

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_exec_with_truncated_stdout_num_lines(self, shared_devbox: AsyncDevbox) -> None:
        """Test num_lines parameter works correctly with potentially truncated output."""
        # Generate 2000 lines of output
        result = await shared_devbox.cmd.exec(
            'for i in $(seq 1 2000); do echo "Line $i"; done',
        )

        assert result.exit_code == 0

        # Request last 50 lines
        stdout = await result.stdout(num_lines=50)
        lines = stdout.strip().split("\n")

        # Verify we got exactly 50 lines
        assert len(lines) == 50, f"Expected 50 lines, got {len(lines)}"

        # Verify these are the last 50 lines
        assert "Line 1951" in lines[0]
        assert "Line 2000" in lines[-1]

    # TODO: Add test_exec_stdout_line_counting test once empty line logic is fixed.
    # Currently there's an inconsistency where _count_non_empty_lines counts non-empty
    # lines but _get_last_n_lines returns N lines (including empty ones). This affects
    # both Python and TypeScript SDKs and needs to be fixed together.


class TestAsyncDevboxNamedShell:
    """Test named shell functionality for stateful command execution."""

    @pytest.fixture(scope="class")
    async def devbox(self, async_sdk_client: AsyncRunloopSDK) -> AsyncIterator[AsyncDevbox]:
        """Create a devbox for shell tests."""
        devbox = await async_sdk_client.devbox.create(
            name=unique_name("sdk-async-devbox-named-shell"),
            launch_parameters={"resource_size_request": "SMALL", "keep_alive_time_seconds": 60 * 5},
        )
        try:
            yield devbox
        finally:
            try:
                await devbox.shutdown()
            except Exception:
                pass

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_basic(self, devbox: AsyncDevbox) -> None:
        """Test basic shell execution."""
        shell = devbox.shell("test-shell-1")
        result = await shell.exec('echo "Hello from named shell!"')
        assert result.exit_code == 0
        output = await result.stdout()
        assert "Hello from named shell!" in output

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_cwd_persistence(self, devbox: AsyncDevbox) -> None:
        """Test that CWD persists across commands."""
        shell = devbox.shell("test-shell-2")

        # Create a directory and change to it
        await shell.exec("mkdir -p /tmp/test-shell-dir")
        await shell.exec("cd /tmp/test-shell-dir")

        # Verify we're in the new directory
        pwd_result = await shell.exec("pwd")
        pwd = (await pwd_result.stdout()).strip()
        assert pwd == "/tmp/test-shell-dir"

        # Create a file in the current directory
        await shell.exec('echo "test content" > testfile.txt')

        # Verify the file exists and has the correct content in the current directory
        cat_result = await shell.exec("cat testfile.txt")
        assert cat_result.exit_code == 0
        cat_output = await cat_result.stdout()
        assert "test content" in cat_output

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_env_persistence(self, devbox: AsyncDevbox) -> None:
        """Test that environment variables persist across commands."""
        shell = devbox.shell("test-shell-3")

        # Set an environment variable
        await shell.exec('export TEST_VAR="test-value-123"')

        # Verify the variable persists in the next command
        echo_result = await shell.exec("echo $TEST_VAR")
        output = (await echo_result.stdout()).strip()
        assert output == "test-value-123"

        # Set another variable and verify both persist
        await shell.exec('export ANOTHER_VAR="another-value"')
        both_result = await shell.exec('echo "$TEST_VAR:$ANOTHER_VAR"')
        both_output = (await both_result.stdout()).strip()
        assert both_output == "test-value-123:another-value"

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_combined_cwd_and_env(self, devbox: AsyncDevbox) -> None:
        """Test combined CWD and environment persistence."""
        shell = devbox.shell("test-shell-4")

        # Set environment and change directory
        await shell.exec('export PROJECT_DIR="/tmp/my-project"')
        await shell.exec("mkdir -p $PROJECT_DIR")
        await shell.exec("cd $PROJECT_DIR")

        # Verify both persist
        pwd_result = await shell.exec("pwd")
        pwd = (await pwd_result.stdout()).strip()
        assert pwd == "/tmp/my-project"

        # Create a file using the environment variable
        await shell.exec('echo "project file" > $PROJECT_DIR/file.txt')

        # Verify file exists
        ls_result = await shell.exec("ls file.txt")
        assert ls_result.exit_code == 0

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_async_basic(self, devbox: AsyncDevbox) -> None:
        """Test basic async shell execution."""
        shell = devbox.shell("test-shell-5")
        execution = await shell.exec_async('sleep 1 && echo "Async command completed"')
        assert execution is not None
        assert execution.execution_id is not None

        # Wait for completion
        result = await execution.result()
        assert result.exit_code == 0
        output = await result.stdout()
        assert "Async command completed" in output

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_async_stateful(self, devbox: AsyncDevbox) -> None:
        """Test stateful async execution."""
        shell = devbox.shell("test-shell-6")

        # Set state in first command
        await shell.exec('export ASYNC_VAR="async-value"')
        await shell.exec("cd /tmp")

        # Start async command that uses the state
        execution = await shell.exec_async('echo "CWD: $(pwd), VAR: $ASYNC_VAR"')
        result = await execution.result()

        assert result.exit_code == 0
        output = await result.stdout()
        assert "CWD: /tmp" in output
        assert "VAR: async-value" in output

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_sequential(self, devbox: AsyncDevbox) -> None:
        """Test sequential execution (queuing)."""
        shell = devbox.shell("test-shell-7")

        # Start multiple commands - they should execute sequentially
        import time

        start_time = time.time()
        await shell.exec('sleep 1 && echo "first"')
        await shell.exec('sleep 1 && echo "second"')
        await shell.exec('sleep 1 && echo "third"')
        end_time = time.time()

        # Verify they took at least 3 seconds (sequential execution)
        duration = end_time - start_time
        assert duration >= 2.9  # Allow some margin for overhead

        # Verify all commands executed in order
        final_result = await shell.exec('echo "done"')
        output = await final_result.stdout()
        assert "done" in output

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_async_sequential(self, devbox: AsyncDevbox) -> None:
        """Test sequential async execution with queuing."""
        shell = devbox.shell("test-shell-8")

        # Start multiple async commands - they should queue and execute sequentially
        exec1 = shell.exec_async('sleep 1 && echo "async-first"')
        exec2 = shell.exec_async('sleep 1 && echo "async-second"')
        exec3 = shell.exec_async('sleep 1 && echo "async-third"')

        # Wait for all to complete
        result1 = await (await exec1).result()
        result2 = await (await exec2).result()
        result3 = await (await exec3).result()

        # Verify all completed successfully
        assert result1.exit_code == 0
        assert result2.exit_code == 0
        assert result3.exit_code == 0

        # Verify outputs
        assert "async-first" in await result1.stdout()
        assert "async-second" in await result2.stdout()
        assert "async-third" in await result3.stdout()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_with_streaming(self, devbox: AsyncDevbox) -> None:
        """Test shell exec with streaming callbacks."""
        shell = devbox.shell("test-shell-9")
        stdout_lines: list[str] = []

        result = await shell.exec(
            'echo "line1" && echo "line2" && echo "line3"', stdout=lambda line: stdout_lines.append(line)
        )

        assert result.success is True
        assert result.exit_code == 0
        assert len(stdout_lines) > 0
        stdout_combined = "".join(stdout_lines)
        assert "line1" in stdout_combined
        assert "line2" in stdout_combined
        assert "line3" in stdout_combined
        # Verify streaming captured same data as result
        assert stdout_combined == await result.stdout()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_async_with_streaming(self, devbox: AsyncDevbox) -> None:
        """Test shell exec_async with streaming callbacks."""
        shell = devbox.shell("test-shell-10")
        stdout_lines: list[str] = []

        execution = await shell.exec_async(
            'echo "async-line1" && sleep 0.5 && echo "async-line2"', stdout=lambda line: stdout_lines.append(line)
        )

        result = await execution.result()
        assert result.success is True
        assert result.exit_code == 0

        stdout_combined = "".join(stdout_lines)
        assert "async-line1" in stdout_combined
        assert "async-line2" in stdout_combined
        # Verify streaming captured same data as result
        assert stdout_combined == await result.stdout()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_multiple_named_shells_independent(self, devbox: AsyncDevbox) -> None:
        """Test that multiple named shells maintain independent state."""
        shell1 = devbox.shell("independent-shell-1")
        shell2 = devbox.shell("independent-shell-2")

        # Set different state in each shell
        await shell1.exec('export VAR="shell1-value"')
        await shell1.exec("cd /tmp")
        await shell2.exec('export VAR="shell2-value"')
        await shell2.exec("cd /home")

        # Verify each shell maintains its own state
        result1 = await shell1.exec('echo "$VAR:$(pwd)"')
        output1 = (await result1.stdout()).strip()
        assert "shell1-value" in output1
        assert "/tmp" in output1

        result2 = await shell2.exec('echo "$VAR:$(pwd)"')
        output2 = (await result2.stdout()).strip()
        assert "shell2-value" in output2
        assert "/home" in output2

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_auto_generated_name(self, devbox: AsyncDevbox) -> None:
        """Test auto-generated shell name."""
        # Create shell without providing a name - should auto-generate UUID
        shell = devbox.shell()
        assert shell is not None

        result = await shell.exec('echo "test"')
        assert result.exit_code == 0
        output = await result.stdout()
        assert "test" in output

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_with_stderr_streaming(self, devbox: AsyncDevbox) -> None:
        """Test shell exec with stderr streaming callback."""
        shell = devbox.shell("test-shell-stderr")
        stderr_lines: list[str] = []

        result = await shell.exec('echo "error output" >&2', stderr=lambda line: stderr_lines.append(line))

        assert result.success is True
        assert result.exit_code == 0
        assert len(stderr_lines) > 0
        stderr_combined = "".join(stderr_lines)
        assert "error output" in stderr_combined
        # Verify streaming captured same data as result
        assert stderr_combined == await result.stderr()

    @pytest.mark.timeout(TWO_MINUTE_TIMEOUT)
    async def test_shell_exec_async_with_both_streams(self, devbox: AsyncDevbox) -> None:
        """Test shell exec_async with both stdout and stderr streaming callbacks."""
        shell = devbox.shell("test-shell-both-streams")
        stdout_lines: list[str] = []
        stderr_lines: list[str] = []

        execution = await shell.exec_async(
            'echo "to stdout" && echo "to stderr" >&2',
            stdout=lambda line: stdout_lines.append(line),
            stderr=lambda line: stderr_lines.append(line),
        )

        result = await execution.result()
        assert result.success is True
        assert result.exit_code == 0

        stdout_combined = "".join(stdout_lines)
        stderr_combined = "".join(stderr_lines)

        assert "to stdout" in stdout_combined
        assert "to stderr" in stderr_combined

        # Verify streaming captured same data as result
        assert stdout_combined == await result.stdout()
        assert stderr_combined == await result.stderr()
