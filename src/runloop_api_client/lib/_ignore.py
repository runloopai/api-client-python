from __future__ import annotations

import os
from abc import ABC, abstractmethod
from typing import Iterable, Optional, Sequence
from pathlib import Path, PurePosixPath
from dataclasses import dataclass
from typing_extensions import override

__all__ = [
    "IgnorePattern",
    "IgnoreMatcher",
    "DockerIgnoreMatcher",
    "FilePatternMatcher",
    "read_ignorefile",
    "compile_ignore",
    "path_match",
    "is_ignored",
    "iter_included_files",
]


@dataclass(frozen=True)
class IgnorePattern:
    """Single parsed ignore pattern.

    Follows Docker-style ``.dockerignore`` semantics and supports other ignore
    use cases following the same approach.
    """

    pattern: str
    """The normalized pattern text with leading and trailing ``/`` removed.

    Always uses POSIX ``'/'`` separators.
    """

    negated: bool
    """Whether this is a negation pattern starting with ``!``."""

    directory_only: bool
    """Whether the original pattern ended with ``/`` and should apply only to
    directories and their descendants.
    """

    anchored: bool
    """Whether the pattern contains a path separator and should be matched
    relative to the root path rather than at any depth.
    """


def _normalize_pattern_string(raw: str) -> str:
    """Normalize a single ignore pattern string.

    Shared helper for patterns coming from both ignorefiles and inline pattern
    lists. Handles:

    - Optional leading ``!`` negation marker (with surrounding whitespace
      trimmed).
    - ``os.path.normpath`` cleanup.
    - Normalising path separators to POSIX ``'/'``.
    - Stripping a single leading ``/`` so absolute-style patterns behave like
      relative ones.

    Comment / blank-line handling is deliberately *not* included here; callers
    are responsible for that.
    """

    if not raw:
        return raw

    invert = raw[0] == "!"
    pattern = raw[1:].strip() if invert else raw.strip()

    if pattern:
        # filepath.Clean equivalent
        pattern = os.path.normpath(pattern)
        # filepath.ToSlash equivalent
        pattern = pattern.replace(os.sep, "/")
        # Leading forward-slashes are removed so "/some/path" and "some/path"
        # are considered equivalent.
        if len(pattern) > 1 and pattern[0] == "/":
            pattern = pattern[1:]

    if invert:
        pattern = "!" + pattern

    return pattern


def _normalize_pattern_line(raw: bytes, *, is_first_line: bool) -> Optional[str]:
    """Normalize a single ignorefile line, mirroring moby's ignorefile.ReadAll.

    Behavior is based on:
    https://github.com/moby/patternmatcher/blob/main/ignorefile/ignorefile.go

    :param raw: Raw line bytes from the ignore file, including any newline
        characters.
    :type raw: bytes
    :param is_first_line: Whether this is the first line in the file (used to
        detect and strip a UTF-8 BOM).
    :type is_first_line: bool
    :return: Normalized pattern string, or ``None`` if the line should be
        ignored (empty or comment).
    :rtype: Optional[str]
    """

    # Strip UTF-8 BOM from the first line if present
    if is_first_line and raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[len(b"\xef\xbb\xbf") :]

    # Decode as UTF-8; we are strict here to surface bad encodings
    text = raw.decode("utf-8", errors="strict")
    text = text.rstrip("\r\n")

    # Lines starting with '#' are comments and are ignored before processing,
    # i.e. we do *not* treat leading spaces as part of the comment detection.
    if text.startswith("#"):
        return None

    # Trim leading and trailing whitespace
    pattern = text.strip()
    if not pattern:
        return None

    normalized = _normalize_pattern_string(pattern)
    return normalized or None


def read_ignorefile(path: Path) -> list[str]:
    """Read an ignore file and return a list of normalized pattern strings.

    This mirrors the behavior of moby's ``ignorefile.ReadAll``:

    - UTF-8 BOM on the first line is stripped.
    - Lines starting with ``#`` are treated as comments and skipped.
    - Remaining lines are trimmed, optionally negated with ``!``, cleaned,
      have path separators normalized to ``/``, and leading and trailing ``/`` removed.

    :param path: Filesystem path to the ignore file to read.
    :type path: Path
    :return: List of normalized pattern strings in the order they appear in
        the ignore file.
    :rtype: list[str]
    """

    if not path.exists():
        return []

    patterns: list[str] = []
    with path.open("rb") as f:
        first = True
        for raw in f:
            normalized = _normalize_pattern_line(raw, is_first_line=first)
            first = False
            if normalized is None:
                continue
            patterns.append(normalized)

    return patterns


def compile_ignore(patterns: Sequence[str]) -> list[IgnorePattern]:
    """Compile raw pattern strings into :class:`IgnorePattern` objects.

    :param patterns: Raw pattern strings following Docker-style semantics.
    :type patterns: Sequence[str]
    :return: Compiled ignore patterns.
    :rtype: list[IgnorePattern]
    """

    compiled: list[IgnorePattern] = []

    for raw in patterns:
        if not raw:
            continue

        negated = raw[0] == "!"
        pattern_text = raw[1:] if negated else raw

        if not pattern_text:
            # Bare "!" is ignored, matching Docker / moby behavior.
            continue

        directory_only = pattern_text.endswith("/")
        if directory_only:
            pattern_text = pattern_text.rstrip("/")

        if not pattern_text:
            continue

        # Treat patterns containing a path separator as anchored to the root
        anchored = "/" in pattern_text

        compiled.append(
            IgnorePattern(
                pattern=PurePosixPath(pattern_text).as_posix(),
                negated=negated,
                directory_only=directory_only,
                anchored=anchored,
            )
        )

    return compiled


def _segment_match(pattern_segment: str, path_segment: str) -> bool:
    """Match a single path segment against a glob pattern segment.

    Supports:

    - ``*``: any sequence of characters except ``/``.
    - ``?``: any single character except ``/``.
    - ``[]``: character classes, excluding ``/``.

    :param pattern_segment: Glob-style pattern segment.
    :type pattern_segment: str
    :param path_segment: Path segment (no ``/``) to match against.
    :type path_segment: str
    :return: ``True`` if the path segment matches the pattern segment.
    :rtype: bool
    """

    import re

    escaped = ""
    i = 0
    while i < len(pattern_segment):
        ch = pattern_segment[i]
        if ch == "*":
            escaped += "[^/]*"
        elif ch == "?":
            escaped += "[^/]"
        elif ch == "[":
            # Copy character class as-is until closing ']'.
            j = i + 1
            while j < len(pattern_segment) and pattern_segment[j] != "]":
                j += 1
            if j < len(pattern_segment):
                escaped += pattern_segment[i : j + 1]
                i = j
            else:
                # Unterminated '['; treat it literally.
                escaped += re.escape(ch)
        else:
            escaped += re.escape(ch)
        i += 1

    regex = re.compile(rf"^{escaped}$")
    return regex.match(path_segment) is not None


def _match_parts_recursive(pattern_parts: list[str], path_parts: list[str]) -> bool:
    """Recursive helper implementing ``**`` segment semantics.

    :param pattern_parts: Pattern split into POSIX path segments.
    :type pattern_parts: list[str]
    :param path_parts: Path split into POSIX path segments.
    :type path_parts: list[str]
    :return: ``True`` if the pattern parts match the path parts.
    :rtype: bool
    """

    if not pattern_parts:
        return not path_parts

    if pattern_parts[0] == "**":
        # '**' matches zero or more segments.
        for i in range(len(path_parts) + 1):
            if _match_parts_recursive(pattern_parts[1:], path_parts[i:]):
                return True
        return False

    if not path_parts:
        return False

    if not _segment_match(pattern_parts[0], path_parts[0]):
        return False

    return _match_parts_recursive(pattern_parts[1:], path_parts[1:])


def path_match(pattern: IgnorePattern, relpath: str, *, is_dir: bool) -> bool:
    """Return ``True`` if ``relpath`` matches a compiled ignore pattern.

    :param pattern: Compiled ignore pattern to test.
    :type pattern: IgnorePattern
    :param relpath: Path to test, relative to the ignore root.
    :type relpath: str
    :param is_dir: Whether ``relpath`` refers to a directory.
    :type is_dir: bool
    :return: ``True`` if the path is matched by the pattern.
    :rtype: bool
    """

    relpath_posix = PurePosixPath(relpath).as_posix()
    path_parts = PurePosixPath(relpath_posix).parts
    pattern_parts = PurePosixPath(pattern.pattern).parts

    # Directory-only patterns never directly match files here; the effect on
    # descendants is enforced by directory pruning in the traversal.
    if pattern.directory_only and not is_dir:
        return False

    if pattern.anchored:
        return _match_parts_recursive(list(pattern_parts), list(path_parts))

    for start in range(len(path_parts)):
        if _match_parts_recursive(list(pattern_parts), list(path_parts[start:])):
            return True
    return False


def is_ignored(relpath: str, *, is_dir: bool, patterns: Sequence[IgnorePattern]) -> bool:
    """Apply ignore patterns with 'last match wins' semantics.

    Examples::

        *.log
        !important.log

    excludes all ``.log`` files except ``important.log``. Patterns are applied
    in order, and the last matching pattern determines inclusion.

    :param relpath: Path to evaluate, relative to the ignore root.
    :type relpath: str
    :param is_dir: Whether ``relpath`` refers to a directory.
    :type is_dir: bool
    :param patterns: Compiled ignore patterns to apply in order.
    :type patterns: Sequence[IgnorePattern]
    :return: ``True`` if the path should be treated as ignored.
    :rtype: bool
    """

    included = True  # include by default
    for pat in patterns:
        if path_match(pat, relpath, is_dir=is_dir):
            included = pat.negated
    return not included


def iter_included_files(
    root: Path,
    *,
    patterns: Sequence[IgnorePattern],
) -> Iterable[Path]:
    """Yield all files under ``root`` that are not ignored.

    This performs directory pruning so that ignored directories are never
    traversed, mirroring Docker's behavior for ``.dockerignore``.

    :param root: Root directory to walk.
    :type root: Path
    :param patterns: Compiled ignore patterns controlling which files and
        directories are included.
    :type patterns: Sequence[IgnorePattern]
    :return: Iterator over non-ignored file paths under ``root``.
    :rtype: Iterable[Path]
    """

    if not root.is_dir():
        raise ValueError(f"root must be a directory, got: {root}")

    for dirpath, dirs, files in os.walk(root):
        dir_path = Path(dirpath)

        # Prune ignored directories
        for name in list(dirs):
            subdir = dir_path / name
            rel_dir = subdir.relative_to(root).as_posix()
            if is_ignored(rel_dir, is_dir=True, patterns=patterns):
                dirs.remove(name)

        # Yield non-ignored files
        for name in files:
            file_path = dir_path / name
            rel_file = file_path.relative_to(root).as_posix()
            if is_ignored(rel_file, is_dir=False, patterns=patterns):
                continue
            yield file_path


class IgnoreMatcher(ABC):
    """Abstract interface for ignore matchers like .dockerignore and .gitignore.

    There is considerable variation for each ignore file format, so this interface
    provides a minimal contract for supporting each format. Implementations are
    responsible for interpreting any underlying ignore configuration (files, inline
    patterns, etc.) and returning all files that should be included under a given
    root directory.
    """

    @abstractmethod
    def iter_paths(self, root: Path) -> Iterable[Path]:
        """Yield filesystem paths to include under ``root``.

        :param root: Root directory to scan for files.
        :type root: Path
        :return: Iterator over filesystem paths that should be included.
        :rtype: Iterable[Path]
        """


@dataclass(frozen=True)
class DockerIgnoreMatcher(IgnoreMatcher):
    """Ignore matcher that mirrors Docker's .dockerignore semantics.

    This matcher:

    - Closely follows Docker's ``.dockerignore`` semantics.
    - Always loads patterns from ``.dockerignore`` in the provided context
      root, if present.
    - Optionally loads additional patterns from an extra ignorefile.
    - Optionally appends inline pattern strings.

    Note: Patterns follow Docker-style semantics (``!`` negation, ``**`` support).
    """

    extra_ignorefile: str | Path | None = None
    """Optional path to an additional ignorefile whose patterns are appended
    after the default ``.dockerignore``.
    """

    patterns: Sequence[str] | None = None
    """Optional inline pattern strings appended after any ignorefiles."""

    @override
    def iter_paths(self, root: Path) -> Iterable[Path]:
        """Yield non-ignored files under ``root`` honoring Docker-style patterns.

        :param root: Context directory whose contents should be filtered.
        :type root: Path
        :return: Iterator over non-ignored file paths under ``root``.
        :rtype: Iterable[Path]
        """
        root = root.resolve()

        all_patterns: list[str] = []

        # 1) Always consider .dockerignore under the context root, if present.
        default_ignorefile = root / ".dockerignore"
        all_patterns.extend(read_ignorefile(default_ignorefile))

        # 2) Optional additional ignorefile.
        if self.extra_ignorefile is not None:
            ignore_path = Path(self.extra_ignorefile)
            if not ignore_path.exists():
                raise FileNotFoundError(f"Ignore file does not exist: {ignore_path}")
            all_patterns.extend(read_ignorefile(ignore_path))

        # 3) Optional inline patterns appended last using same rules as .dockerignore
        # Some extra handling here for trailing slashes that is different from .gitignore.
        if self.patterns:
            for raw in self.patterns:
                if not raw:
                    continue
                normalized = _normalize_pattern_string(raw)
                if normalized:
                    all_patterns.append(normalized)

        compiled: list[IgnorePattern] = compile_ignore(all_patterns)
        return iter_included_files(root, patterns=compiled)


@dataclass(frozen=True)
class FilePatternMatcher(IgnoreMatcher):
    """Ignore matcher that applies only inline patterns, without .dockerignore.

    Patterns follow the same semantics as :func:`compile_ignore` / Docker-style
    ignore files and are treated as *ignore* rules (``!`` negation for
    re-inclusion, ``**`` support, etc.).

    The constructor accepts either a single pattern string or a sequence of
    pattern strings; a single string is automatically wrapped into a list.
    """

    patterns: Sequence[str] | str
    """Pattern or patterns to apply as ignore rules when matching files."""

    def __post_init__(self) -> None:
        # Normalise a single pattern string into a list for downstream helpers.
        if isinstance(self.patterns, str):
            object.__setattr__(self, "patterns", [self.patterns])

    @override
    def iter_paths(self, root: Path) -> Iterable[Path]:
        """Yield non-ignored files under ``root`` based only on ``patterns``.

        :param root: Root directory whose contents should be filtered.
        :type root: Path
        :return: Iterator over non-ignored file paths under ``root``.
        :rtype: Iterable[Path]
        """

        root = root.resolve()
        compiled: list[IgnorePattern] = compile_ignore(self.patterns)  # type: ignore[arg-type]
        return iter_included_files(root, patterns=compiled)
