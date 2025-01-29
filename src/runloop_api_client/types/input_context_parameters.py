# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["InputContextParameters"]


class InputContextParameters(BaseModel):
    problem_statement: str
    """The problem statement for the Scenario."""
