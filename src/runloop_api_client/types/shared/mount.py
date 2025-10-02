# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union
from typing_extensions import Annotated, TypeAlias

from ..._utils import PropertyInfo
from .agent_mount_parameters import AgentMountParameters
from .object_mount_parameters import ObjectMountParameters

__all__ = ["Mount"]

Mount: TypeAlias = Annotated[Union[ObjectMountParameters, AgentMountParameters], PropertyInfo(discriminator="type")]
