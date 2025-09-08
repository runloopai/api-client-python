# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ExecutionUpdateChunk"]


class ExecutionUpdateChunk(BaseModel):
    output: str
    """The latest log stream chunk."""

    offset: Optional[int] = None
    """The byte offset of this chunk of log stream."""
