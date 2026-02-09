"""
Input validation functions for the Phase I In-Memory Python Console App.

This module provides functions to validate user inputs.
"""

from typing import Union
import re


def validate_task_description(description: str) -> tuple[bool, str]:
    """
    Validate a task description.

    Args:
        description: The task description to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not description or not description.strip():
        return False, "Task description cannot be empty"

    if len(description.strip()) > 1000:  # Reasonable limit to prevent memory issues
        return False, "Task description is too long (max 1000 characters)"

    # Check for potentially problematic characters or patterns if needed
    # For now, just ensure it's not empty after stripping whitespace
    if not description.strip():
        return False, "Task description cannot be empty or just whitespace"

    return True, ""


def validate_task_id(task_id: str) -> tuple[bool, str]:
    """
    Validate a task ID.

    Args:
        task_id: The task ID to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not task_id or not isinstance(task_id, str):
        return False, "Task ID must be a non-empty string"

    # Basic UUID format check (simple pattern)
    uuid_pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    if not re.match(uuid_pattern, task_id.lower()):
        return False, "Invalid task ID format"

    return True, ""


def validate_positive_integer(value: Union[str, int]) -> tuple[bool, str]:
    """
    Validate that a value is a positive integer.

    Args:
        value: The value to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    try:
        num_value = int(value)
        if num_value <= 0:
            return False, "Value must be a positive integer"
        return True, ""
    except (ValueError, TypeError):
        return False, "Value must be a valid integer"


def validate_boolean_string(value: str) -> tuple[bool, str]:
    """
    Validate that a string represents a boolean value.

    Args:
        value: The string to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    if value.lower() not in ['true', 'false', '1', '0', 'yes', 'no']:
        return False, "Value must be a boolean (true/false, yes/no, 1/0)"
    return True, ""


def sanitize_input(input_str: str) -> str:
    """
    Sanitize user input by removing potentially harmful characters.

    Args:
        input_str: The input string to sanitize

    Returns:
        A sanitized version of the input string
    """
    # For now, just strip leading/trailing whitespace
    # In a more complex application, you might want to remove or escape certain characters
    return input_str.strip()


def validate_command(command: str) -> tuple[bool, str]:
    """
    Validate a CLI command.

    Args:
        command: The command to validate

    Returns:
        A tuple of (is_valid, error_message)
    """
    if not command or not command.strip():
        return False, "Command cannot be empty"

    # Check for potentially dangerous patterns
    dangerous_patterns = [
        r'[;&|$<>]',  # Shell metacharacters
        r'\.\./',     # Path traversal
        r'eval\s*\(', # eval function calls
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, command, re.IGNORECASE):
            return False, "Command contains potentially dangerous characters"

    return True, ""