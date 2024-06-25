# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["ProjectLogsView", "Log"]


class Log(BaseModel):
    level: Optional[str] = None

    message: Optional[str] = None

    source: Optional[str] = None

    timestamp: Optional[str] = None


class ProjectLogsView(BaseModel):
    logs: Optional[List[Log]] = None
    """List of logs for the given project."""
