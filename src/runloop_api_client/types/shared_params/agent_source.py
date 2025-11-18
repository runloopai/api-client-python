# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from ..._types import SequenceNotStr

__all__ = ["AgentSource", "Git", "Npm", "Object", "Pip"]


class Git(TypedDict, total=False):
    repository: Required[str]
    """Git repository URL"""

    agent_setup: Optional[SequenceNotStr[str]]
    """Setup commands to run after cloning"""

    ref: Optional[str]
    """Optional Git ref (branch/tag/commit), defaults to main/HEAD"""


class Npm(TypedDict, total=False):
    package_name: Required[str]
    """NPM package name"""

    agent_setup: Optional[SequenceNotStr[str]]
    """Setup commands to run after installation"""

    npm_version: Optional[str]
    """NPM version constraint"""

    registry_url: Optional[str]
    """NPM registry URL"""


class Object(TypedDict, total=False):
    object_id: Required[str]
    """Object ID"""

    agent_setup: Optional[SequenceNotStr[str]]
    """Setup commands to run after unpacking"""


class Pip(TypedDict, total=False):
    package_name: Required[str]
    """Pip package name"""

    agent_setup: Optional[SequenceNotStr[str]]
    """Setup commands to run after installation"""

    pip_version: Optional[str]
    """Pip version constraint"""

    registry_url: Optional[str]
    """Pip registry URL"""


class AgentSource(TypedDict, total=False):
    type: Required[str]
    """Source type: npm, pip, object, or git"""

    git: Optional[Git]
    """Git source configuration"""

    npm: Optional[Npm]
    """NPM source configuration"""

    object: Optional[Object]
    """Object store source configuration"""

    pip: Optional[Pip]
    """Pip source configuration"""
