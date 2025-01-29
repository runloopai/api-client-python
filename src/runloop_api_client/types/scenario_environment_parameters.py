# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["ScenarioEnvironmentParameters"]


class ScenarioEnvironmentParameters(BaseModel):
    blueprint_id: Optional[str] = None
    """Use the blueprint with matching ID."""

    prebuilt_id: Optional[str] = None
    """Use the prebuilt with matching ID."""

    snapshot_id: Optional[str] = None
    """Use the snapshot with matching ID."""
