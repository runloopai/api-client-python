# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from .._models import BaseModel

__all__ = ["DeploymentGetResponse", "Deployment"]


class Deployment(BaseModel):
    id: Optional[str] = None
    """ID of the deployment."""

    deploy_commit_message: Optional[str] = None
    """Associated Commit Message"""

    deploy_commit_sha: Optional[str] = None
    """Associated Commit Sha"""

    deploy_commit_time_ms: Optional[int] = None
    """Associated Commit Time"""

    deploy_end_time_ms: Optional[int] = None
    """Time the Deploy completed (Unix timestamp milliseconds)."""

    deploy_start_time_ms: Optional[int] = None
    """Time the Deploy was started (Unix timestamp milliseconds)."""

    deployed_functions: Optional[List[str]] = None
    """The list of deployed functions."""

    failure_code: Optional[str] = None
    """
    Failure code (generic_failure | git_clone_failure | not_runloop_repo |
    secrets_failure | provision_failure | runtime_failure). Only set on
    deploy_failed.
    """

    failure_message: Optional[str] = None
    """Failure message"""

    project_name: Optional[str] = None
    """Project name associated with the deployment."""

    redeploy_of: Optional[str] = None
    """ID of original deployment this is redeployment for."""

    status: Optional[Literal["scheduled", "skipped", "in_progress", "failed", "deployed"]] = None
    """Status of the deploy."""


class DeploymentGetResponse(BaseModel):
    deployments: Optional[List[Deployment]] = None
    """List of projects matching given query."""

    has_more: Optional[bool] = None

    total_count: Optional[int] = None
