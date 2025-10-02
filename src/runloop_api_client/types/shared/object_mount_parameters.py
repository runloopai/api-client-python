# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing_extensions import Literal

from ..._models import BaseModel

__all__ = ["ObjectMountParameters"]


class ObjectMountParameters(BaseModel):
    object_id: str
    """The ID of the object to write."""

    object_path: str
    """The path to write the object on the Devbox.

    Use absolute path of object (ie /home/user/object.txt, or directory if archive
    /home/user/archive_dir)
    """

    type: Literal["object_mount"]
