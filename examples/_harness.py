from __future__ import annotations

import sys
import json
import asyncio
from typing import Any, TypeVar, Callable, Awaitable
from dataclasses import asdict

from .example_types import (
    ExampleCheck,
    RecipeOutput,
    ExampleResult,
    RecipeContext,
    ExampleCleanupStatus,
    ExampleCleanupFailure,
    empty_cleanup_status,
)

T = TypeVar("T")


class _CleanupTracker:
    """Tracks cleanup actions and executes them in LIFO order."""

    def __init__(self, status: ExampleCleanupStatus) -> None:
        self._status = status
        self._actions: list[tuple[str, Callable[[], Any]]] = []

    def add(self, resource: str, action: Callable[[], Any]) -> None:
        """Register a cleanup action for a resource."""
        self._actions.append((resource, action))

    async def run(self) -> None:
        """Execute all cleanup actions in reverse order."""
        while self._actions:
            resource, action = self._actions.pop()
            self._status.attempted.append(resource)
            try:
                result = action()
                if asyncio.iscoroutine(result):
                    await result
                self._status.succeeded.append(resource)
            except Exception as e:
                self._status.failed.append(ExampleCleanupFailure(resource, str(e)))

        if self._status.attempted:
            if not self._status.failed:
                print("Cleanup completed.")  # noqa: T201
            else:
                print("Cleanup finished with errors.")  # noqa: T201


def _should_fail_process(result: ExampleResult) -> bool:
    """Determine if the process should exit with failure."""
    has_failed_checks = any(not check.passed for check in result.checks)
    return result.skipped or has_failed_checks or len(result.cleanup_status.failed) > 0


def wrap_recipe(
    recipe: Callable[[RecipeContext], RecipeOutput] | Callable[[RecipeContext], Awaitable[RecipeOutput]],
    validate_env: Callable[[], tuple[bool, list[ExampleCheck]]] | None = None,
) -> Callable[[], ExampleResult]:
    """Wrap a recipe function with cleanup tracking and result handling.

    Args:
        recipe: The recipe function to wrap. Can be sync or async.
        validate_env: Optional function to validate environment before running.
                      Returns (skip, checks) tuple.

    Returns:
        A callable that runs the recipe and returns ExampleResult.
    """

    def run() -> ExampleResult:
        cleanup_status = empty_cleanup_status()
        cleanup = _CleanupTracker(cleanup_status)

        if validate_env is not None:
            skip, checks = validate_env()
            if skip:
                return ExampleResult(
                    resources_created=[],
                    checks=checks,
                    cleanup_status=cleanup_status,
                    skipped=True,
                )

        ctx = RecipeContext(cleanup=cleanup)

        async def _run_async() -> RecipeOutput:
            try:
                result = recipe(ctx)
                if asyncio.iscoroutine(result):
                    output: RecipeOutput = await result
                    return output
                return result  # type: ignore[return-value]
            finally:
                await cleanup.run()

        loop = asyncio.new_event_loop()
        try:
            output = loop.run_until_complete(_run_async())
            return ExampleResult(
                resources_created=output.resources_created,
                checks=output.checks,
                cleanup_status=cleanup_status,
            )
        finally:
            loop.close()

    return run


def wrap_recipe_with_options(
    recipe: Callable[[RecipeContext, T], RecipeOutput] | Callable[[RecipeContext, T], Awaitable[RecipeOutput]],
    validate_env: Callable[[T], tuple[bool, list[ExampleCheck]]] | None = None,
) -> Callable[[T], ExampleResult]:
    """Wrap a recipe function that takes options with cleanup tracking.

    Args:
        recipe: The recipe function to wrap. Can be sync or async. Takes options parameter.
        validate_env: Optional function to validate environment before running.
                      Takes options and returns (skip, checks) tuple.

    Returns:
        A callable that runs the recipe with options and returns ExampleResult.
    """

    def run(options: T) -> ExampleResult:
        cleanup_status = empty_cleanup_status()
        cleanup = _CleanupTracker(cleanup_status)

        if validate_env is not None:
            skip, checks = validate_env(options)
            if skip:
                return ExampleResult(
                    resources_created=[],
                    checks=checks,
                    cleanup_status=cleanup_status,
                    skipped=True,
                )

        ctx = RecipeContext(cleanup=cleanup)

        async def _run_async() -> RecipeOutput:
            try:
                result = recipe(ctx, options)
                if asyncio.iscoroutine(result):
                    output: RecipeOutput = await result
                    return output
                return result  # type: ignore[return-value]
            finally:
                await cleanup.run()

        loop = asyncio.new_event_loop()
        try:
            output = loop.run_until_complete(_run_async())
            return ExampleResult(
                resources_created=output.resources_created,
                checks=output.checks,
                cleanup_status=cleanup_status,
            )
        finally:
            loop.close()

    return run


def run_as_cli(run: Callable[[], ExampleResult]) -> None:
    """Run an example and exit with appropriate status code."""
    try:
        result = run()
        print(json.dumps(asdict(result), indent=2))  # noqa: T201
        if _should_fail_process(result):
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")  # noqa: T201
        sys.exit(1)
