# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["FunctionInvocationListView", "Invocation"]


class Invocation(BaseModel):
    id: Optional[str] = None
    """Unique ID of the invocation."""

    end_time_ms: Optional[int] = None
    """End time of the invocation."""

    error: Optional[str] = None

    function_name: Optional[str] = None
    """Unique name of the function."""

    gh_commit_sha: Optional[str] = None
    """The Git sha of the project this invocation used."""

    gh_owner: Optional[str] = None
    """The Github Owner of the Project."""

    linked_devboxes: Optional[List[str]] = None
    """The Devboxes created and used by this invocation."""

    project_name: Optional[str] = None
    """Unique name of the project associated with function."""

    start_time_ms: Optional[int] = None
    """Start time of the invocation."""

    status: Optional[Literal["created", "running", "success", "failure", "canceled", "suspended"]] = None


class FunctionInvocationListView(BaseModel):
    has_more: Optional[bool] = None

    invocations: Optional[List[Invocation]] = None
    """List of functions matching given query."""

    total_count: Optional[int] = None
