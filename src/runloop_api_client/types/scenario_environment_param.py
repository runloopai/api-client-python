# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["ScenarioEnvironmentParam"]


class ScenarioEnvironmentParam(TypedDict, total=False):
    blueprint_id: Optional[str]
    """Use the blueprint with matching ID."""

    prebuilt_id: Optional[str]
    """Use the prebuilt with matching ID."""

    snapshot_id: Optional[str]
    """Use the snapshot with matching ID."""
