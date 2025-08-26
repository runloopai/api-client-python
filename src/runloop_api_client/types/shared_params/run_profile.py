# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Annotated, TypedDict

from ..._utils import PropertyInfo
from .launch_parameters import LaunchParameters

__all__ = ["RunProfile"]


class RunProfile(TypedDict, total=False):
    env_vars: Annotated[Optional[Dict[str, str]], PropertyInfo(alias="envVars")]
    """Mapping of Environment Variable to Value.

    May be shown in devbox logging. Example: {"DB_PASS": "DATABASE_PASSWORD"} would
    set the environment variable 'DB_PASS' to the value 'DATABASE_PASSWORD_VALUE'.
    """

    launch_parameters: Annotated[Optional[LaunchParameters], PropertyInfo(alias="launchParameters")]
    """Additional runtime LaunchParameters to apply after the devbox starts."""

    purpose: Optional[str]
    """Purpose of the run."""

    secrets: Optional[Dict[str, str]]
    """Mapping of Environment Variable to User Secret Name.

    Never shown in devbox logging. Example: {"DB_PASS": "DATABASE_PASSWORD"} would
    set the environment variable 'DB_PASS' to the value of the secret
    'DATABASE_PASSWORD'.
    """
