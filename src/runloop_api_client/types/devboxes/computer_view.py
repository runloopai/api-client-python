# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel
from ..devbox_view import DevboxView

__all__ = ["ComputerView"]


class ComputerView(BaseModel):
    devbox: DevboxView
    """The underlying devbox the computer setup is running on."""

    live_screen_url: str
    """The http tunnel to connect and view the live screen of the computer.

    You can control the interactivity of the browser by adding or removing
    'view_only' query parameter. view_only=1 will allow interaction and view_only=0
    will disable interaction.
    """
