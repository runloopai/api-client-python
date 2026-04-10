# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["ScopeEntryView"]


class ScopeEntryView(BaseModel):
    access_level: Optional[Literal["ACCESS_LEVEL_NONE", "ACCESS_LEVEL_READ", "ACCESS_LEVEL_WRITE"]] = None

    resource_type: Optional[
        Literal[
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
    ] = None
