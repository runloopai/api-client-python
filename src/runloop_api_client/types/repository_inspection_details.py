# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from .._models import BaseModel
from .repository_manifest_view import RepositoryManifestView

__all__ = ["RepositoryInspectionDetails"]


class RepositoryInspectionDetails(BaseModel):
    id: str
    """The ID of the inspection."""

    commit_sha: str
    """The sha of the inspected version of the Repository."""

    inspected_at: int
    """Inspection time of the Repository Version (Unix timestamp milliseconds)."""

    repository_manifest: RepositoryManifestView
    """Repository manifest containing container config and workspace details."""

    status: Literal[
        "invalid",
        "repo_auth_pending",
        "repo_authentication_failure",
        "repo_access_failure",
        "inspection_pending",
        "inspection_failed",
        "inspection_success",
        "image_build_success",
        "image_build_failure",
        "inspection_user_manifest_added",
    ]
    """The status of the repository inspection."""

    blueprint_id: Optional[str] = None
    """The blueprint ID associated with this inspection if successful."""

    blueprint_name: Optional[str] = None
    """The blueprint name associated with this inspection if successful."""

    user_manifest: Optional[RepositoryManifestView] = None
    """
    User uploaded repository manifest containing container config and workspace
    details.
    """
