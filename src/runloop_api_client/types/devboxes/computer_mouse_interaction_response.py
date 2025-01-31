# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["ComputerMouseInteractionResponse"]


class ComputerMouseInteractionResponse(BaseModel):
    error: Optional[str] = None

    latest_screenshot_base64_img: Optional[str] = None

    output: Optional[str] = None
