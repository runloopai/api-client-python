# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["ProjectListView", "Installation", "Project"]


class Installation(BaseModel):
    status: str
    """Status of the installation (installed | uninstalled | never_installed)."""


class Project(BaseModel):
    id: str
    """Unique id of Project."""

    gh_owner: str
    """Owner of the project in Github"""

    name: str
    """Project display name."""


class ProjectListView(BaseModel):
    installation: Installation

    projects: List[Project]
    """List of projects matching given query."""
