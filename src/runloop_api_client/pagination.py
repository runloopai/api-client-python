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
    def next_page_info(self) -> Optional[PageInfo]:
        snapshots = self.snapshots
        if not snapshots:
            return None

        item = cast(Any, snapshots[-1])
        if not isinstance(item, DiskSnapshotsCursorIDPageItem) or item.id is None:  # pyright: ignore[reportUnnecessaryComparison]
            # TODO emit warning log
            return None

        return PageInfo(params={"starting_after": item.id})
