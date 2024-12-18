# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["BaseCommand"]


class BaseCommand(BaseModel):
    command: str

    title: str

    arguments: Optional[List[object]] = None
