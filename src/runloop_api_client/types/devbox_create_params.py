# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable, Optional
from typing_extensions import TypedDict

from .shared_params.launch_parameters import LaunchParameters
from .shared_params.code_mount_parameters import CodeMountParameters

__all__ = ["DevboxCreateParams"]


class DevboxCreateParams(TypedDict, total=False):
    blueprint_id: Optional[str]
    """Blueprint ID to use for the Devbox.

    If none set, the Devbox will be created with the default Runloop Devbox image.
    Only one of (Snapshot ID, Blueprint ID, Blueprint name) should be specified.
    """

    blueprint_name: Optional[str]
    """Name of Blueprint to use for the Devbox.

    When set, this will load the latest successfully built Blueprint with the given
    name. Only one of (Snapshot ID, Blueprint ID, Blueprint name) should be
    specified.
    """

    code_mounts: Optional[Iterable[CodeMountParameters]]
    """A list of code mounts to be included in the Devbox."""

    entrypoint: Optional[str]
    """
    (Optional) When specified, the Devbox will run this script as its main
    executable. The devbox lifecycle will be bound to entrypoint, shutting down when
    the process is complete.
    """

    environment_variables: Optional[Dict[str, str]]
    """(Optional) Environment variables used to configure your Devbox."""

    file_mounts: Optional[Dict[str, str]]
    """(Optional) Map of paths and file contents to write before setup.."""

    launch_parameters: Optional[LaunchParameters]
    """Parameters to configure the resources and launch time behavior of the Devbox."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the devbox for organization."""

    name: Optional[str]
    """(Optional) A user specified name to give the Devbox."""

    prebuilt: Optional[str]
    """Reference to prebuilt Blueprint to create the Devbox from.

    Should not be used together with (Snapshot ID, Blueprint ID, or Blueprint name).
    """

    snapshot_id: Optional[str]
    """Snapshot ID to use for the Devbox.

    Only one of (Snapshot ID, Blueprint ID, Blueprint name) should be specified.
    """
