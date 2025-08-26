# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional

from pydantic import Field as FieldInfo

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
    """Additional runtime LaunchParameters to apply after the devbox starts."""

    purpose: Optional[str] = None
    """Purpose of the run."""

    secrets: Optional[Dict[str, str]] = None
    """Mapping of Environment Variable to User Secret Name.

    Never shown in devbox logging. Example: {"DB_PASS": "DATABASE_PASSWORD"} would
    set the environment variable 'DB_PASS' to the value of the secret
    'DATABASE_PASSWORD'.
    """
