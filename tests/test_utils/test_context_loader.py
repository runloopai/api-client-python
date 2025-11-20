from pathlib import Path

from runloop_api_client.lib.context_loader import (
    _is_ignored,
    _path_match,
    _segment_match,
    _DockerignorePattern,
    _iter_build_context_files,
    _load_dockerignore_patterns,
)


def test_segment_match_basic_globs():
    assert _segment_match("*.log", "app.log")
    assert not _segment_match("*.log", "app.txt")
    assert _segment_match("foo?", "fooa")
    assert not _segment_match("foo?", "fooba")
    assert _segment_match("[ab].txt", "a.txt")
    assert not _segment_match("[ab].txt", "c.txt")


def test_path_match_anchored_and_unanchored():
    pat = _DockerignorePattern(pattern="foo/bar.txt", negated=False, directory_only=False, anchored=True)
    assert _path_match(pat, "foo/bar.txt", is_dir=False)
    assert not _path_match(pat, "a/foo/bar.txt", is_dir=False)

    pat_unanchored = _DockerignorePattern(pattern="foo/bar.txt", negated=False, directory_only=False, anchored=False)
    assert _path_match(pat_unanchored, "a/foo/bar.txt", is_dir=False)
    assert _path_match(pat_unanchored, "foo/bar.txt", is_dir=False)


def test_path_match_double_star():
    pat = _DockerignorePattern(pattern="**/*.log", negated=False, directory_only=False, anchored=False)
    assert _path_match(pat, "app.log", is_dir=False)
    assert _path_match(pat, "a/b/app.log", is_dir=False)
    assert not _path_match(pat, "a/b/app.txt", is_dir=False)


def test_is_ignored_last_match_wins():
    patterns = [
        _DockerignorePattern(pattern="*.log", negated=False, directory_only=False, anchored=False),
        _DockerignorePattern(pattern="keep.log", negated=True, directory_only=False, anchored=False),
    ]
    assert _is_ignored("foo.log", is_dir=False, patterns=patterns)
    assert not _is_ignored("keep.log", is_dir=False, patterns=patterns)


def test_load_dockerignore_patterns_basic(tmp_path: Path):
    dockerignore = tmp_path / ".dockerignore"
    dockerignore.write_text(
        "\n# comment\n *.log  \n!keep.log\n\\#literal\n\\!literal\n",
        encoding="utf-8",
    )

    patterns = _load_dockerignore_patterns(dockerignore)
    assert len(patterns) == 4
    assert patterns[0].pattern == "*.log"
    assert not patterns[0].negated
    assert patterns[1].pattern == "keep.log"
    assert patterns[1].negated
    assert patterns[2].pattern == "#literal"
    assert not patterns[2].negated
    assert patterns[3].pattern == "!literal"
    assert not patterns[3].negated


def test_iter_build_context_files_respects_dockerignore(tmp_path: Path):
    # Layout:
    #   foo.txt
    #   app.log
    #   build/ignored.txt
    root = tmp_path
    (root / "foo.txt").write_text("ok", encoding="utf-8")
    (root / "app.log").write_text("ignored", encoding="utf-8")
    build_dir = root / "build"
    build_dir.mkdir()
    (build_dir / "ignored.txt").write_text("ignored", encoding="utf-8")

    dockerignore = root / ".dockerignore"
    dockerignore.write_text("*.log\nbuild/\n", encoding="utf-8")

    files = {p.relative_to(root).as_posix() for p in _iter_build_context_files(root, dockerignore_path=dockerignore)}
    assert "foo.txt" in files
    assert "app.log" not in files
    assert "build/ignored.txt" not in files
