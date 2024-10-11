# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Iterable
from typing_extensions import TypedDict

from .code_mount_parameters_param import CodeMountParametersParam
from .shared_params.launch_parameters import LaunchParameters

__all__ = ["DevboxCreateParams"]


class DevboxCreateParams(TypedDict, total=False):
    blueprint_id: str
    """(Optional) Blueprint to use for the Devbox.

    If none set, the Devbox will be created with the default Runloop Devbox image.
    """

    blueprint_name: str
    """(Optional) Name of Blueprint to use for the Devbox.

    When set, this will load the latest successfully built Blueprint with the given
    name.
    """

    code_mounts: Iterable[CodeMountParametersParam]
    """A list of code mounts to be included in the Devbox."""

    entrypoint: str
    """
    (Optional) When specified, the Devbox will run this script as its main
    executable. The devbox lifecycle will be bound to entrypoint, shutting down when
    the process is complete.
    """

    environment_variables: Dict[str, str]
    """(Optional) Environment variables used to configure your Devbox."""

    file_mounts: Dict[str, str]
    """(Optional) Map of paths and file contents to write before setup.."""

    launch_parameters: LaunchParameters
    """Parameters to configure the resources and launch time behavior of the Devbox."""

    metadata: Dict[str, str]
    """User defined metadata to attach to the devbox for organization."""

    name: str
    """(Optional) A user specified name to give the Devbox."""

    prebuilt: str
    """Reference to prebuilt Blueprint."""

    setup_commands: List[str]
    """(Optional) List of commands needed to set up your Devbox.

    Examples might include fetching a tool or building your dependencies. Runloop
    will look optimize these steps for you.
    """

    snapshot_id: str
    """Snapshot ID to use for the Devbox."""
