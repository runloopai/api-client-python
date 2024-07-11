# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["FunctionInvocationListView", "Invocation"]


class Invocation(BaseModel):
    end_time_ms: int
    """End time of the invocation."""

    start_time_ms: int
    """Start time of the invocation."""

    id: Optional[str] = None
    """Unique ID of the invocation."""

    error: Optional[str] = None

    function_name: Optional[str] = None
    """Unique name of the function."""

    project_name: Optional[str] = None
    """Unique name of the project associated with function."""

    status: Optional[Literal["created", "running", "success", "failure", "canceled", "suspended"]] = None


class FunctionInvocationListView(BaseModel):
    invocations: Optional[List[Invocation]] = None
    """List of functions matching given query."""
