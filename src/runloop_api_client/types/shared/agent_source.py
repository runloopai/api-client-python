# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from ..._models import BaseModel

__all__ = ["AgentSource", "Git", "Npm", "Object", "Pip"]


class Git(BaseModel):
    repository: str
    """Git repository URL"""

    agent_setup: Optional[List[str]] = None
    """Setup commands to run after cloning"""

    ref: Optional[str] = None
    """Optional Git ref (branch/tag/commit), defaults to main/HEAD"""


class Npm(BaseModel):
    package_name: str
    """NPM package name"""

    agent_setup: Optional[List[str]] = None
    """Setup commands to run after installation"""

    npm_version: Optional[str] = None
    """NPM version constraint"""

    registry_url: Optional[str] = None
    """NPM registry URL"""


class Object(BaseModel):
    object_id: str
    """Object ID"""

    agent_setup: Optional[List[str]] = None
    """Setup commands to run after unpacking"""


class Pip(BaseModel):
    package_name: str
    """Pip package name"""

    agent_setup: Optional[List[str]] = None
    """Setup commands to run after installation"""

    pip_version: Optional[str] = None
    """Pip version constraint"""

    registry_url: Optional[str] = None
    """Pip registry URL"""


class AgentSource(BaseModel):
    type: str
    """Source type: npm, pip, object, or git"""

    git: Optional[Git] = None
    """Git source configuration"""

    npm: Optional[Npm] = None
    """NPM source configuration"""

    object: Optional[Object] = None
    """Object store source configuration"""

    pip: Optional[Pip] = None
    """Pip source configuration"""
