"""Smoketests for SDK examples.

These tests run the example scripts against the live API.
Set RUN_EXAMPLE_LIVE_TESTS=1 to enable live tests.
"""

from __future__ import annotations

import os
import sys
from typing import Any
from pathlib import Path

import pytest

# Add the root directory to the path so we can import examples
sys.path.insert(0, str(Path(__file__).parents[3]))

from examples.registry import example_registry  # noqa: E402
from examples.example_types import ExampleResult  # noqa: E402
from examples.mcp_github_tools import McpExampleOptions, run_mcp_github_tools_example  # noqa: E402

LONG_TIMEOUT = 600  # 10 minutes for live tests
SHORT_TIMEOUT = 30  # 30 seconds for skip mode tests


class TestExamples:
    """Tests for SDK examples."""

    @pytest.mark.smoketest
    @pytest.mark.timeout(LONG_TIMEOUT)
    @pytest.mark.parametrize("entry", example_registry, ids=lambda e: e["slug"])
    def test_example_runs_with_successful_checks(self, entry: dict[str, Any]) -> None:
        """Test that examples run successfully with all checks passing."""
        if not os.environ.get("RUN_EXAMPLE_LIVE_TESTS"):
            pytest.skip("RUN_EXAMPLE_LIVE_TESTS not set")

        required_env: list[str] = entry["required_env"]
        missing_env = [e for e in required_env if not os.environ.get(e)]
        if missing_env:
            pytest.skip(f"Missing env vars: {missing_env}")

        # Handle examples that need options
        result: ExampleResult
        if entry["slug"] == "mcp-github-tools":
            result = run_mcp_github_tools_example(McpExampleOptions())
        else:
            result = entry["run"]()

        assert not result.skipped, "Example was unexpectedly skipped"
        assert len(result.resources_created) > 0, "No resources were created"
        assert len(result.checks) > 0, "No checks were performed"

        failed_checks = [c for c in result.checks if not c.passed]
        assert not failed_checks, f"Failed checks: {[c.name for c in failed_checks]}"

        assert len(result.cleanup_status.failed) == 0, (
            f"Cleanup failures: {[f.resource for f in result.cleanup_status.failed]}"
        )

    @pytest.mark.timeout(SHORT_TIMEOUT)
    def test_mcp_skip_mode_for_missing_credentials(self) -> None:
        """Test that mcp-github-tools example skips deterministically when credentials are missing."""
        # Save original env vars
        original_github_token = os.environ.get("GITHUB_TOKEN")
        original_anthropic_key = os.environ.get("ANTHROPIC_API_KEY")

        # Remove credentials
        if "GITHUB_TOKEN" in os.environ:
            del os.environ["GITHUB_TOKEN"]
        if "ANTHROPIC_API_KEY" in os.environ:
            del os.environ["ANTHROPIC_API_KEY"]

        try:
            result = run_mcp_github_tools_example(McpExampleOptions(skip_if_missing_credentials=True))

            assert result.skipped, "Example should be skipped when credentials are missing"
            assert len(result.resources_created) == 0, "No resources should be created when skipped"
            assert len(result.cleanup_status.attempted) == 0, "No cleanup should be attempted when skipped"
        finally:
            # Restore original env vars
            if original_github_token is not None:
                os.environ["GITHUB_TOKEN"] = original_github_token
            elif "GITHUB_TOKEN" in os.environ:
                del os.environ["GITHUB_TOKEN"]

            if original_anthropic_key is not None:
                os.environ["ANTHROPIC_API_KEY"] = original_anthropic_key
            elif "ANTHROPIC_API_KEY" in os.environ:
                del os.environ["ANTHROPIC_API_KEY"]

    @pytest.mark.timeout(SHORT_TIMEOUT)
    def test_example_registry_is_populated(self) -> None:
        """Test that the example registry contains expected entries."""
        assert len(example_registry) >= 2, "Expected at least 2 examples in registry"

        slugs = {e["slug"] for e in example_registry}
        assert "devbox-from-blueprint-lifecycle" in slugs
        assert "mcp-github-tools" in slugs

        for entry in example_registry:
            assert "slug" in entry
            assert "title" in entry
            assert "file_name" in entry
            assert "required_env" in entry
            assert "run" in entry
            assert callable(entry["run"])
