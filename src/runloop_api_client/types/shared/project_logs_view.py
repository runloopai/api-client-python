# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel

__all__ = ["ProjectLogsView", "Log"]


class Log(BaseModel):
    level: str

    message: str

    source: str

    timestamp: str


class ProjectLogsView(BaseModel):
    logs: List[Log]
    """List of logs for the given project."""
