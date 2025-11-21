"""Helpers and strategy interface for packaging Docker build contexts.

This module exposes a small, pluggable abstraction around turning a local
filesystem directory into a tarball suitable for use as a Docker build
context, plus a default implementation built on top of
``lib.context_loader.build_docker_context_tar``.
"""

from __future__ import annotations

from typing import Optional
from pathlib import Path
from dataclasses import dataclass
from typing_extensions import Protocol

from ..lib.context_loader import build_docker_context_tar
from ..types.object_create_params import ContentType

__all__ = ["BuildContextArtifact", "BuildContextStrategy", "default_build_context_strategy"]


@dataclass(frozen=True)
class BuildContextArtifact:
    """Result of packaging a build context directory.

    Attributes:
        data: Tarball bytes containing the build context.
        content_type: Logical content type for the object payload. For the
            default implementation this is always ``\"tgz\"``.
        filename: Suggested filename to use when creating the backing Object.
    """

    data: bytes
    content_type: ContentType = "tgz"
    filename: Optional[str] = None


class BuildContextStrategy(Protocol):
    """Strategy interface for building Docker contexts.

    Implementations may perform caching, custom compression, or additional
    validation, but must return a fully materialised tarball in memory.
    """

    def __call__(
        self,
        context_root: Path,
        *,
        name: str | None = None,
        dockerignore: Path | None = None,
    ) -> BuildContextArtifact:
        """Package the given directory into a tarball.

        Args:
            context_root: Filesystem path to the Docker build context root.
            name: Optional logical name for the context; may be used to
                derive a filename.
            dockerignore: Optional explicit path to a .dockerignore file.
                When omitted, the default implementation will look for
                ``.dockerignore`` under ``context_root``.
        """


def default_build_context_strategy(
    context_root: Path,
    *,
    name: str | None = None,
    dockerignore: Path | None = None,
) -> BuildContextArtifact:
    """Default implementation that wraps ``build_docker_context_tar``.

    The tarball is rebuilt on each invocation (no cross-call caching) and
    returned as a :class:`BuildContextArtifact` with ``content_type=\"tgz\"``.
    """

    tar_bytes = build_docker_context_tar(
        context_root,
        dockerignore=dockerignore,
    )

    if name is None:
        base = context_root.name or "context"
        filename = f"{base}.tar.gz"
    else:
        filename = f"{name}.tar.gz"

    return BuildContextArtifact(
        data=tar_bytes,
        content_type="tgz",
        filename=filename,
    )
