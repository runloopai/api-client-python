from __future__ import annotations

from typing import Any, Union, Callable, Protocol, Awaitable
from dataclasses import field, dataclass


@dataclass
class ExampleCheck:
    """Result of a single validation check in an example."""

    name: str
    passed: bool
    details: str | None = None


@dataclass
class ExampleCleanupFailure:
    """Record of a cleanup action that failed."""

    resource: str
    reason: str


@dataclass
class ExampleCleanupStatus:
    """Tracks cleanup operations during example execution."""

    attempted: list[str] = field(default_factory=lambda: [])
    succeeded: list[str] = field(default_factory=lambda: [])
    failed: list[ExampleCleanupFailure] = field(default_factory=lambda: [])


@dataclass
class ExampleResult:
    """Full result of running an example, including checks and cleanup status."""

    resources_created: list[str]
    checks: list[ExampleCheck]
    cleanup_status: ExampleCleanupStatus
    skipped: bool = False


@dataclass
class RecipeOutput:
    """Output from a recipe function before cleanup runs."""

    resources_created: list[str]
    checks: list[ExampleCheck]


CleanupAction = Callable[[], Union[None, Awaitable[None]]]


class CleanupTracker(Protocol):
    """Protocol for tracking cleanup actions."""

    def add(self, resource: str, action: CleanupAction) -> None: ...


@dataclass
class RecipeContext:
    """Context passed to recipe functions."""

    cleanup: Any  # CleanupTracker, but using Any to avoid circular typing issues
