# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["ScorerCreateResponse"]


class ScorerCreateResponse(BaseModel):
    id: str
    """ID for the scenario scorer."""

    bash_script: str
    """Bash script that takes in $RL_TEST_CONTEXT as env variable and runs scoring."""

    type: str
    """Name of the type of scenario scorer."""
