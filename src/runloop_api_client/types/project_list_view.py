# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["ProjectListView", "Installation", "Project"]


class Installation(BaseModel):
    status: Optional[str] = None
    """Status of the installation (installed | uninstalled | never_installed)."""


class Project(BaseModel):
    id: Optional[str] = None
    """Unique id of Project."""

    gh_owner: Optional[str] = None
    """Owner of the project in Github"""

    name: Optional[str] = None
    """Project display name."""


class ProjectListView(BaseModel):
    installation: Optional[Installation] = None

    projects: Optional[List[Project]] = None
    """List of projects matching given query."""
