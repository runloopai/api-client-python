# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = [
    "ProjectListView",
    "Installation",
    "Project",
    "ProjectActiveDeploy",
    "ProjectInProgressDeploy",
    "ProjectRecentDeployment",
]


class Installation(BaseModel):
    status: Optional[str] = None
    """Status of the installation (installed | uninstalled | never_installed)."""


class ProjectActiveDeploy(BaseModel):
    deploy_start_time_ms: int
    """Time the Deploy was started (Unix timestamp milliseconds)."""

    id: Optional[str] = None
    """ID of the deployment."""

    deploy_commit_sha: Optional[str] = None
    """Associated Commit Sha"""

    deploy_commit_time_ms: Optional[int] = None
    """Associated Commit Time"""

    deploy_end_time_ms: Optional[int] = None
    """Time the Deploy completed (Unix timestamp milliseconds)."""

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

    status: Optional[str] = None
    """
    Status of the deploy (deploy_in_progress | deployed | deploy_failed |
    not_started).
    """


class ProjectInProgressDeploy(BaseModel):
    deploy_start_time_ms: int
    """Time the Deploy was started (Unix timestamp milliseconds)."""

    id: Optional[str] = None
    """ID of the deployment."""

    deploy_commit_sha: Optional[str] = None
    """Associated Commit Sha"""

    deploy_commit_time_ms: Optional[int] = None
    """Associated Commit Time"""

    deploy_end_time_ms: Optional[int] = None
    """Time the Deploy completed (Unix timestamp milliseconds)."""

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

    status: Optional[str] = None
    """
    Status of the deploy (deploy_in_progress | deployed | deploy_failed |
    not_started).
    """


class ProjectRecentDeployment(BaseModel):
    deploy_start_time_ms: int
    """Time the Deploy was started (Unix timestamp milliseconds)."""

    id: Optional[str] = None
    """ID of the deployment."""

    deploy_commit_sha: Optional[str] = None
    """Associated Commit Sha"""

    deploy_commit_time_ms: Optional[int] = None
    """Associated Commit Time"""

    deploy_end_time_ms: Optional[int] = None
    """Time the Deploy completed (Unix timestamp milliseconds)."""

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

    status: Optional[str] = None
    """
    Status of the deploy (deploy_in_progress | deployed | deploy_failed |
    not_started).
    """


class Project(BaseModel):
    id: Optional[str] = None
    """Unique id of Project."""

    active_deploy: Optional[ProjectActiveDeploy] = None

    in_progress_deploy: Optional[ProjectInProgressDeploy] = None

    name: Optional[str] = None
    """Project display name."""

    recent_deployments: Optional[List[ProjectRecentDeployment]] = None
    """Last deployment attempts (up to 10)"""


class ProjectListView(BaseModel):
    installation: Optional[Installation] = None

    projects: Optional[List[Project]] = None
    """List of projects matching given query."""
