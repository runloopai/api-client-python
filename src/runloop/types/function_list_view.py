# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["FunctionListView", "Function"]


class Function(BaseModel):
    name: Optional[str] = None
    """Unique name of the function."""

    project_name: Optional[str] = None
    """Unique name of the project."""


class FunctionListView(BaseModel):
    functions: Optional[List[Function]] = None
    """List of functions matching given query."""
