# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["FunctionInvocationList", "Invocation"]


class Invocation(BaseModel):
    id: Optional[str] = None
    """Unique ID of the invocations."""

    name: Optional[str] = None
    """Name of the invoked function."""

    project_name: Optional[str] = FieldInfo(alias="projectName", default=None)
    """Project name associated with invoked function."""

    status: Optional[Literal["created", "running", "success", "failure", "canceled", "suspended"]] = None


class FunctionInvocationList(BaseModel):
    invocations: Optional[List[Invocation]] = None
    """List of functions matching given query."""
