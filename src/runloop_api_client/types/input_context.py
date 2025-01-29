# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["InputContext"]


class InputContext(BaseModel):
    problem_statement: str
    """The problem statement for the Scenario."""
