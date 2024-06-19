# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ...._models import BaseModel

__all__ = ["SessionKv", "Kv"]


class Kv(BaseModel):
    array: bool

    big_decimal: bool = FieldInfo(alias="bigDecimal")

    big_integer: bool = FieldInfo(alias="bigInteger")

    binary: bool

    boolean: bool

    container_node: bool = FieldInfo(alias="containerNode")

    double: bool

    empty: bool

    float: bool

    floating_point_number: bool = FieldInfo(alias="floatingPointNumber")

    int: bool

    integral_number: bool = FieldInfo(alias="integralNumber")

    long: bool

    missing_node: bool = FieldInfo(alias="missingNode")

    null: bool

    number: bool

    object: bool

    pojo: bool

    short: bool

    textual: bool

    value_node: bool = FieldInfo(alias="valueNode")

    node_type: Optional[
        Literal["ARRAY", "BINARY", "BOOLEAN", "MISSING", "NULL", "NUMBER", "OBJECT", "POJO", "STRING"]
    ] = FieldInfo(alias="nodeType", default=None)


class SessionKv(BaseModel):
    id: Optional[str] = None
    """The ID of the session."""

    kv: Optional[Dict[str, Kv]] = None
    """The session key value storage."""
