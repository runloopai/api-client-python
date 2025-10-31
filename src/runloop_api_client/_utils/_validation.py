from __future__ import annotations

from typing import List, Optional


class ValidationNotification:
    """Collects validation errors without raising exceptions.

    This follows the notification pattern: validations append errors, and callers
    decide how to react (e.g., surface all messages at once or abort).
    """

    def __init__(self) -> None:
        self._errors: List[str] = []
        self._causes: List[Optional[Exception]] = []

    def add_error(self, message: str, cause: Optional[Exception] = None) -> None:
        self._errors.append(message)
        self._causes.append(cause)

    def has_errors(self) -> bool:
        return len(self._errors) > 0

    @property
    def errors(self) -> List[str]:
        # Return a copy to avoid external mutation
        return list(self._errors)

    def error_message(self) -> str:
        # Join with semicolons to present multiple issues succinctly
        return "; ".join(self._errors)
