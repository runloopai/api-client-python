# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .repository_manifest_view import RepositoryManifestView

__all__ = ["RepositoryInspectionDetails", "WorkflowContexts", "WorkflowContextsActionsContext"]


class WorkflowContextsActionsContext(BaseModel):
    actions_skipped_unnecessary: List[str]
    """
    Actions that were skipped because they were unnecessary (e.g., upload
    artifacts).
    """

    actions_taken: List[str]
    """Actions that were translated into commands and executed."""

    actions_unknown: List[str]
    """
    Actions that were not understood and skipped because we did not know what to do.
    """


class WorkflowContexts(BaseModel):
    actions_context: WorkflowContextsActionsContext
    """Details about actions processing for this workflow."""

    file_name: str
    """The file name of the workflow."""


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
        "inspection_user_manifest_added",
    ]
    """The status of the repository inspection."""

    blueprint_id: Optional[str] = None
    """The blueprint ID associated with this inspection if successful."""

    blueprint_name: Optional[str] = None
    """The blueprint name associated with this inspection if successful."""

    build_status: Optional[Literal["image_building", "image_build_success", "image_build_failure"]] = None
    """The status of the linked Blueprint build."""

    user_manifest: Optional[RepositoryManifestView] = None
    """
    User uploaded repository manifest containing container config and workspace
    details.
    """

    workflow_contexts: Optional[Dict[str, WorkflowContexts]] = None
    """Workflow contexts mapping workflow names to their processing details."""
