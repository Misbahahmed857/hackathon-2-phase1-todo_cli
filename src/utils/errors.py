"""
Error handling utilities for the Phase I In-Memory Python Console App.

This module defines custom exception classes and error handling utilities.
"""


class TaskNotFoundError(Exception):
    """Raised when a task is not found."""

    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Task with ID '{task_id}' not found")


class InvalidTaskError(Exception):
    """Raised when a task is invalid."""

    def __init__(self, message: str):
        super().__init__(message)


class StorageFullError(Exception):
    """Raised when the storage is full."""

    def __init__(self, message: str = "Storage capacity reached"):
        super().__init__(message)


class ValidationError(Exception):
    """Raised when validation fails."""

    def __init__(self, field: str, message: str):
        self.field = field
        super().__init__(f"Validation error for {field}: {message}")


def handle_error(error: Exception, context: str = "") -> str:
    """
    Handle an error and return an appropriate message.

    Args:
        error: The exception that occurred
        context: Additional context about where the error occurred

    Returns:
        A user-friendly error message
    """
    if isinstance(error, TaskNotFoundError):
        return f"Error: {error}"
    elif isinstance(error, InvalidTaskError):
        return f"Invalid task: {error}"
    elif isinstance(error, StorageFullError):
        return f"Storage error: {error}"
    elif isinstance(error, ValidationError):
        return f"Validation error: {error}"
    else:
        error_context = f" in {context}" if context else ""
        return f"Unexpected error{error_context}: {str(error)}"