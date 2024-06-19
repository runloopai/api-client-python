# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .devbox import Devbox
from .._models import BaseModel

__all__ = ["DevboxList"]


class DevboxList(BaseModel):
    devboxes: Optional[List[Devbox]] = None
    """List of devboxes matching filter."""
