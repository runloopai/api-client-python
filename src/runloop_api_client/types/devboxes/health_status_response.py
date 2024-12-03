# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["HealthStatusResponse"]


class HealthStatusResponse(BaseModel):
    dirty_files: List[str] = FieldInfo(alias="dirtyFiles")

    module_name: str = FieldInfo(alias="moduleName")

    pending_work: Dict[str, object] = FieldInfo(alias="pendingWork")

    status: str

    uptime: str

    watch_directory: str = FieldInfo(alias="watchDirectory")
