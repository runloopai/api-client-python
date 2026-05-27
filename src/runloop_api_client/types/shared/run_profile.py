# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .mount import Mount
from ..._models import BaseModel
from .launch_parameters import LaunchParameters

__all__ = ["RunProfile"]


class RunProfile(BaseModel):
    env_vars: Optional[Dict[str, str]] = FieldInfo(alias="envVars", default=None)
    """Mapping of Environment Variable to Value.

    May be shown in devbox logging. Example: {"DB_PASS": "DATABASE_PASSWORD"} would
    set the environment variable 'DB_PASS' to the value 'DATABASE_PASSWORD_VALUE'.
    """

    launch_parameters: Optional[LaunchParameters] = FieldInfo(alias="launchParameters", default=None)
    """
    LaunchParameters enable you to customize the resources available to your Devbox
    as well as the environment set up that should be completed before the Devbox is
    marked as 'running'.
    """

    mounts: Optional[List[Mount]] = None
    """A list of mounts to be included in the scenario run."""

    purpose: Optional[str] = None
    """Purpose of the run."""

    secrets: Optional[Dict[str, str]] = None
    """Mapping of Environment Variable to User Secret Name.

    Never shown in devbox logging. Example: {"DB_PASS": "DATABASE_PASSWORD"} would
    set the environment variable 'DB_PASS' to the value of the secret
    'DATABASE_PASSWORD'.
    """
