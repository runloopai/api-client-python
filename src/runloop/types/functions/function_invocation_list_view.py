# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["FunctionInvocationListView", "Invocation"]


class Invocation(BaseModel):
    id: Optional[str] = None
    """Unique ID of the invocations."""

    name: Optional[str] = None
    """Name of the invoked function."""

    project_name: Optional[str] = None
    """Project name associated with invoked function."""

    status: Optional[Literal["created", "running", "success", "failure", "canceled", "suspended"]] = None


class FunctionInvocationListView(BaseModel):
    invocations: Optional[List[Invocation]] = None
    """List of functions matching given query."""
