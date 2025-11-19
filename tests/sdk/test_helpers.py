"""Tests for helper utilities."""

from __future__ import annotations

from typing import Mapping, TypedDict

from runloop_api_client.sdk._helpers import filter_params


class ExampleParams(TypedDict):
    foo: int
    bar: str


def test_filter_params_with_dict() -> None:
    """filter_params should include only keys defined in the TypedDict."""
    params = {"foo": 1, "bar": "value", "extra": True}

    result = filter_params(params, ExampleParams)

    assert result == {"foo": 1, "bar": "value"}


def test_filter_params_with_mapping() -> None:
    """filter_params should work with Mapping inputs."""
    params: Mapping[str, object] = {"foo": 42, "bar": "hello", "other": "ignored"}

    result = filter_params(params, ExampleParams)

    assert result == {"foo": 42, "bar": "hello"}
