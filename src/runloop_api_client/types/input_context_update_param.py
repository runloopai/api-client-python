# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Literal, Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["InputContextUpdateParam", "AdditionalContext"]


class AdditionalContext(TypedDict, total=False):
    array: Required[bool]

    big_decimal: Required[Annotated[bool, PropertyInfo(alias="bigDecimal")]]

    big_integer: Required[Annotated[bool, PropertyInfo(alias="bigInteger")]]

    binary: Required[bool]

    boolean: Required[bool]

    container_node: Required[Annotated[bool, PropertyInfo(alias="containerNode")]]

    double: Required[bool]

    empty: Required[bool]

    float: Required[bool]

    floating_point_number: Required[Annotated[bool, PropertyInfo(alias="floatingPointNumber")]]

    int: Required[bool]

    integral_number: Required[Annotated[bool, PropertyInfo(alias="integralNumber")]]

    long: Required[bool]

    missing_node: Required[Annotated[bool, PropertyInfo(alias="missingNode")]]

    null: Required[bool]

    number: Required[bool]

    object: Required[bool]

    pojo: Required[bool]

    short: Required[bool]

    textual: Required[bool]

    value_node: Required[Annotated[bool, PropertyInfo(alias="valueNode")]]

    node_type: Annotated[
        Literal["ARRAY", "BINARY", "BOOLEAN", "MISSING", "NULL", "NUMBER", "OBJECT", "POJO", "STRING"],
        PropertyInfo(alias="nodeType"),
    ]


class InputContextUpdateParam(TypedDict, total=False):
    additional_context: Optional[AdditionalContext]
    """Additional JSON structured input context."""

    problem_statement: Optional[str]
    """The problem statement for the Scenario."""
