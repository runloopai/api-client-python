# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Any, List, Generic, TypeVar, Optional, cast
from typing_extensions import Protocol, override, runtime_checkable

from ._base_client import BasePage, PageInfo, BaseSyncPage, BaseAsyncPage

__all__ = [
    "SyncBlueprintsCursorIDPage",
    "AsyncBlueprintsCursorIDPage",
    "SyncDevboxesCursorIDPage",
    "AsyncDevboxesCursorIDPage",
    "SyncRepositoriesCursorIDPage",
    "AsyncRepositoriesCursorIDPage",
    "SyncDiskSnapshotsCursorIDPage",
    "AsyncDiskSnapshotsCursorIDPage",
    "SyncBenchmarksCursorIDPage",
    "AsyncBenchmarksCursorIDPage",
    "SyncAgentsCursorIDPage",
    "AsyncAgentsCursorIDPage",
    "SyncBenchmarkRunsCursorIDPage",
    "AsyncBenchmarkRunsCursorIDPage",
    "SyncScenariosCursorIDPage",
    "AsyncScenariosCursorIDPage",
    "SyncScenarioRunsCursorIDPage",
    "AsyncScenarioRunsCursorIDPage",
    "SyncScenarioScorersCursorIDPage",
    "AsyncScenarioScorersCursorIDPage",
    "SyncObjectsCursorIDPage",
    "AsyncObjectsCursorIDPage",
]

_T = TypeVar("_T")


@runtime_checkable
class BlueprintsCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class DevboxesCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class RepositoriesCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class DiskSnapshotsCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class BenchmarksCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class AgentsCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class BenchmarkRunsCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class ScenariosCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class ScenarioRunsCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class ScenarioScorersCursorIDPageItem(Protocol):
    id: str


@runtime_checkable
class ObjectsCursorIDPageItem(Protocol):
    id: str


class SyncBlueprintsCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    blueprints: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        blueprints = self.blueprints
        if not blueprints:
            return []
        return blueprints

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        blueprints = self.blueprints
        if not blueprints:
            return None

        item = cast(Any, blueprints[-1])
        if not isinstance(item, BlueprintsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncBlueprintsCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    blueprints: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        blueprints = self.blueprints
        if not blueprints:
            return []
        return blueprints

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        blueprints = self.blueprints
        if not blueprints:
            return None

        item = cast(Any, blueprints[-1])
        if not isinstance(item, BlueprintsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncDevboxesCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    devboxes: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        devboxes = self.devboxes
        if not devboxes:
            return []
        return devboxes

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        devboxes = self.devboxes
        if not devboxes:
            return None

        item = cast(Any, devboxes[-1])
        if not isinstance(item, DevboxesCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncDevboxesCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    devboxes: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        devboxes = self.devboxes
        if not devboxes:
            return []
        return devboxes

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        devboxes = self.devboxes
        if not devboxes:
            return None

        item = cast(Any, devboxes[-1])
        if not isinstance(item, DevboxesCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncRepositoriesCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    repositories: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        repositories = self.repositories
        if not repositories:
            return []
        return repositories

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        repositories = self.repositories
        if not repositories:
            return None

        item = cast(Any, repositories[-1])
        if not isinstance(item, RepositoriesCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncRepositoriesCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    repositories: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        repositories = self.repositories
        if not repositories:
            return []
        return repositories

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        repositories = self.repositories
        if not repositories:
            return None

        item = cast(Any, repositories[-1])
        if not isinstance(item, RepositoriesCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncDiskSnapshotsCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    snapshots: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        snapshots = self.snapshots
        if not snapshots:
            return []
        return snapshots

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        snapshots = self.snapshots
        if not snapshots:
            return None

        item = cast(Any, snapshots[-1])
        if not isinstance(item, DiskSnapshotsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncDiskSnapshotsCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    snapshots: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        snapshots = self.snapshots
        if not snapshots:
            return []
        return snapshots

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        snapshots = self.snapshots
        if not snapshots:
            return None

        item = cast(Any, snapshots[-1])
        if not isinstance(item, DiskSnapshotsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncBenchmarksCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    benchmarks: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        benchmarks = self.benchmarks
        if not benchmarks:
            return []
        return benchmarks

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        benchmarks = self.benchmarks
        if not benchmarks:
            return None

        item = cast(Any, benchmarks[-1])
        if not isinstance(item, BenchmarksCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncBenchmarksCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    benchmarks: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        benchmarks = self.benchmarks
        if not benchmarks:
            return []
        return benchmarks

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        benchmarks = self.benchmarks
        if not benchmarks:
            return None

        item = cast(Any, benchmarks[-1])
        if not isinstance(item, BenchmarksCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncAgentsCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    agents: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        agents = self.agents
        if not agents:
            return []
        return agents

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        agents = self.agents
        if not agents:
            return None

        item = cast(Any, agents[-1])
        if not isinstance(item, AgentsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncAgentsCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    agents: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        agents = self.agents
        if not agents:
            return []
        return agents

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        agents = self.agents
        if not agents:
            return None

        item = cast(Any, agents[-1])
        if not isinstance(item, AgentsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncBenchmarkRunsCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    runs: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        runs = self.runs
        if not runs:
            return []
        return runs

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        runs = self.runs
        if not runs:
            return None

        item = cast(Any, runs[-1])
        if not isinstance(item, BenchmarkRunsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncBenchmarkRunsCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    runs: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        runs = self.runs
        if not runs:
            return []
        return runs

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        runs = self.runs
        if not runs:
            return None

        item = cast(Any, runs[-1])
        if not isinstance(item, BenchmarkRunsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncScenariosCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    scenarios: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        scenarios = self.scenarios
        if not scenarios:
            return []
        return scenarios

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        scenarios = self.scenarios
        if not scenarios:
            return None

        item = cast(Any, scenarios[-1])
        if not isinstance(item, ScenariosCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncScenariosCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    scenarios: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        scenarios = self.scenarios
        if not scenarios:
            return []
        return scenarios

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        scenarios = self.scenarios
        if not scenarios:
            return None

        item = cast(Any, scenarios[-1])
        if not isinstance(item, ScenariosCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncScenarioRunsCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    runs: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        runs = self.runs
        if not runs:
            return []
        return runs

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        runs = self.runs
        if not runs:
            return None

        item = cast(Any, runs[-1])
        if not isinstance(item, ScenarioRunsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncScenarioRunsCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    runs: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        runs = self.runs
        if not runs:
            return []
        return runs

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        runs = self.runs
        if not runs:
            return None

        item = cast(Any, runs[-1])
        if not isinstance(item, ScenarioRunsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncScenarioScorersCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    scorers: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        scorers = self.scorers
        if not scorers:
            return []
        return scorers

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        scorers = self.scorers
        if not scorers:
            return None

        item = cast(Any, scorers[-1])
        if not isinstance(item, ScenarioScorersCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncScenarioScorersCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    scorers: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        scorers = self.scorers
        if not scorers:
            return []
        return scorers

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        scorers = self.scorers
        if not scorers:
            return None

        item = cast(Any, scorers[-1])
        if not isinstance(item, ScenarioScorersCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class SyncObjectsCursorIDPage(BaseSyncPage[_T], BasePage[_T], Generic[_T]):
    objects: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        objects = self.objects
        if not objects:
            return []
        return objects

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        objects = self.objects
        if not objects:
            return None

        item = cast(Any, objects[-1])
        if not isinstance(item, ObjectsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})


class AsyncObjectsCursorIDPage(BaseAsyncPage[_T], BasePage[_T], Generic[_T]):
    objects: List[_T]
    has_more: Optional[bool] = None
    total_count: Optional[int] = None

    @override
    def _get_page_items(self) -> List[_T]:
        objects = self.objects
        if not objects:
            return []
        return objects

    @override
    def has_next_page(self) -> bool:
        has_more = self.has_more
        if has_more is not None and has_more is False:
            return False

        return super().has_next_page()

    @override
    def next_page_info(self) -> Optional[PageInfo]:
        objects = self.objects
        if not objects:
            return None

        item = cast(Any, objects[-1])
        if not isinstance(item, ObjectsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})
