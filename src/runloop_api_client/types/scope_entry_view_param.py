# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, TypedDict

__all__ = ["ScopeEntryViewParam"]


class ScopeEntryViewParam(TypedDict, total=False):
    access_level: Literal["ACCESS_LEVEL_NONE", "ACCESS_LEVEL_READ", "ACCESS_LEVEL_WRITE"]

    resource_type: Literal[
        "RESOURCE_TYPE_DEVBOXES",
        "RESOURCE_TYPE_BLUEPRINTS",
        "RESOURCE_TYPE_SNAPSHOTS",
        "RESOURCE_TYPE_BENCHMARKS",
        "RESOURCE_TYPE_SCENARIOS",
        "RESOURCE_TYPE_REPO_CONNECTIONS",
        "RESOURCE_TYPE_AGENTS",
        "RESOURCE_TYPE_OBJECTS",
        "RESOURCE_TYPE_ACCOUNT",
    ]
