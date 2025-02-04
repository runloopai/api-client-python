# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._models import BaseModel

__all__ = ["ScorerRetrieveResponse"]


class ScorerRetrieveResponse(BaseModel):
    id: str
    """ID for the scenario scorer."""

    bash_script: str
    """Bash script that takes in $RL_TEST_CONTEXT as env variable and runs scoring."""

    name: str
    """Name of the scenario scorer."""
