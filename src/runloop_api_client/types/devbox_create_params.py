# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List
from typing_extensions import TypedDict

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

    code_handle: str
    """(Optional) Id of a code handle to mount to devbox."""

    entrypoint: str
    """
    (Optional) When specified, the Devbox will run this script as its main
    executable. The devbox lifecycle will be bound to entrypoint, shutting down when
    the process is complete.
    """

    environment_variables: Dict[str, str]
    """(Optional) Environment variables used to configure your Devbox."""

    name: str
    """(Optional) A user specified name to give the Devbox."""

    setup_commands: List[str]
    """(Optional) List of commands needed to set up your Devbox.

    Examples might include fetching a tool or building your dependencies. Runloop
    will look optimize these steps for you.
    """
