"""
TaskController for the Phase I In-Memory Python Console App.

This module coordinates operations between the CLI and the TaskService.
"""

from typing import List, Optional
from src.services.task_service import TaskService
from src.models.task import Task
from src.utils.errors import TaskNotFoundError, ValidationError
from src.utils.validation import validate_task_description, validate_task_id


class TaskController:
    """Controller class to coordinate task operations between CLI and service layers."""

    def __init__(self, task_service: TaskService):
        """
        Initialize the TaskController.

        Args:
            task_service: The TaskService instance to use for business logic
        """
        self.task_service = task_service

    def create_task(self, description: str) -> Optional[str]:
        """
        Create a new task through the controller.

        Args:
            description: The description of the task to create

        Returns:
            The ID of the created task, or None if creation failed
        """
        # Validate the task description
        is_valid, error_msg = validate_task_description(description)
        if not is_valid:
            raise ValidationError("description", error_msg)

        # Create the task via the service
        return self.task_service.create_task(description)

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks through the controller.

        Returns:
            A list of all Task objects
        """
        return self.task_service.get_all_tasks()

    def update_task(self, task_id: str, description: Optional[str] = None, completed: Optional[bool] = None) -> bool:
        """
        Update an existing task through the controller.

        Args:
            task_id: The ID of the task to update
            description: Optional new description
            completed: Optional new completion status

        Returns:
            True if the task was updated, False if it didn't exist
        """
        # Validate the task ID
        is_valid, error_msg = validate_task_id(task_id)
        if not is_valid:
            raise ValidationError("task_id", error_msg)

        # Validate the description if provided
        if description is not None:
            is_valid, error_msg = validate_task_description(description)
            if not is_valid:
                raise ValidationError("description", error_msg)

        # Update the task via the service
        return self.task_service.update_task(task_id, description, completed)

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task through the controller.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        # Validate the task ID
        is_valid, error_msg = validate_task_id(task_id)
        if not is_valid:
            raise ValidationError("task_id", error_msg)

        # Delete the task via the service
        return self.task_service.delete_task(task_id)

    def toggle_task_completion(self, task_id: str) -> bool:
        """
        Toggle the completion status of a task through the controller.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task was toggled, False if it didn't exist
        """
        # Validate the task ID
        is_valid, error_msg = validate_task_id(task_id)
        if not is_valid:
            raise ValidationError("task_id", error_msg)

        # Toggle the task via the service
        return self.task_service.toggle_task_completion(task_id)