# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from ..._models import BaseModel
from ..devbox_view import DevboxView

__all__ = ["BrowserView"]


class BrowserView(BaseModel):
    connection_url: str
    """
    The url to enable remote connection from browser automation tools like
    playwright.
    """

    devbox: DevboxView
    """The underlying devbox the browser setup is running on."""

    live_view_url: str
    """
    The url to view the browser window and enable user interactions via their own
    browser.
    """
