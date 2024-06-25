# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["FunctionInvocationDetailView"]


class FunctionInvocationDetailView(BaseModel):
    id: Optional[str] = None
    """Unique ID of the invocation."""

    error: Optional[str] = None

    function_name: Optional[str] = None
    """Unique name of the function."""

    project_name: Optional[str] = None
    """Unique name of the project associated with function."""

    result: Optional[object] = None

    status: Optional[Literal["created", "running", "success", "failure", "canceled", "suspended"]] = None
