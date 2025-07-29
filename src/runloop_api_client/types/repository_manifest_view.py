# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from .._models import BaseModel

__all__ = [
    "RepositoryManifestView",
    "ContainerConfig",
    "Workspace",
    "WorkspaceDevCommands",
    "ContainerizedService",
    "ContainerizedServiceCredentials",
]


class ContainerConfig(BaseModel):
    base_image_name: str
    """The name of the base image.

    Should be one of the GitHub public images like ubuntu-latest, ubuntu-24.04,
    ubuntu-22.04, windows-latest, windows-2022, macos-latest etc.
    """

    setup_commands: Optional[List[str]] = None
    """
    Commands to run to setup the base container such as installing necessary
    toolchains (e.g. apt install).
    """


class WorkspaceDevCommands(BaseModel):
    build: Optional[List[str]] = None
    """Build command (e.g. npm run build)."""

    install: Optional[List[str]] = None
    """Installation command (e.g. pip install -r requirements.txt)."""

    lint: Optional[List[str]] = None
    """Lint command (e.g. flake8)."""

    test: Optional[List[str]] = None
    """Test command (e.g. pytest)."""


class Workspace(BaseModel):
    package_manager: List[str]
    """Name of the package manager used (e.g. pip, npm)."""

    dev_commands: Optional[WorkspaceDevCommands] = None
    """
    Extracted common commands important to the developer life cycle like linting,
    testing, building, etc.
    """

    name: Optional[str] = None
    """Name of the workspace.

    Can be empty if the workspace is the root of the repository. Only necessary for
    monorepo style repositories.
    """

    path: Optional[str] = None
    """Path to the workspace from the root of the repository.

    Can be empty if the workspace is the root of the repository. Only necessary for
    monorepo style repositories.
    """

    required_env_vars: Optional[List[str]] = None
    """
    Environment variables that are required to be set for this workspace to run
    correctly.
    """

    workspace_refresh_commands: Optional[List[str]] = None
    """
    Commands to run to refresh this workspace after pulling the latest changes to
    the repository via git (e.g. npm install).
    """

    workspace_setup_commands: Optional[List[str]] = None
    """
    Commands to run to setup this workspace after a fresh clone of the repository on
    a new container such as installing necessary toolchains and dependencies (e.g.
    npm install).
    """


class ContainerizedServiceCredentials(BaseModel):
    password: str
    """The password of the container service."""

    username: str
    """The username of the container service."""


class ContainerizedService(BaseModel):
    image: str
    """The image of the container service."""

    name: str
    """The name of the container service."""

    credentials: Optional[ContainerizedServiceCredentials] = None
    """The credentials of the container service."""

    env: Optional[Dict[str, str]] = None
    """The environment variables of the container service."""

    options: Optional[str] = None
    """Additional Docker container create options."""

    port_mappings: Optional[List[str]] = None
    """The port mappings of the container service.

    Port mappings are in the format of <host_port>:<container_port>.
    """


class RepositoryManifestView(BaseModel):
    container_config: ContainerConfig
    """Container configuration specifying the base image and setup commands."""

    workspaces: List[Workspace]
    """List of workspaces within the repository.

    Each workspace represents a buildable unit of code.
    """

    containerized_services: Optional[List[ContainerizedService]] = None
    """List of discovered ContainerizedServices.

    Services can be explicitly started when creating a Devbox.
    """
