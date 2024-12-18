# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .range_param import RangeParam
from .code_action_context_param import CodeActionContextParam

__all__ = ["LspCodeActionsParams"]


class LspCodeActionsParams(TypedDict, total=False):
    uri: Required[str]

    context: CodeActionContextParam
    """
    Contains additional diagnostic information about the context in which a {@link
    CodeActionProvider.provideCodeActions code action} is run. The CodeActionContext
    namespace provides helper functions to work with {@link CodeActionContext}
    literals.
    """

    range: RangeParam
    """A range in a text document expressed as (zero-based) start and end positions.

    If you want to specify a range that contains a line including the line ending
    character(s) then use an end position denoting the start of the next line. For
    example:

    ```ts
    {
        start: { line: 5, character: 23 }
        end : { line 6, character : 0 }
    }
    ```

    The Range namespace provides helper functions to work with {@link Range}
    literals.
    """
