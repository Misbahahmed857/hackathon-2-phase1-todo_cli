"""
TaskService for the Phase I In-Memory Python Console App.

This module implements the business logic for managing tasks.
"""

from typing import List, Optional
from src.storage.in_memory_store import InMemoryStore
from src.models.task import Task


class TaskService:
    """Service class to manage tasks using the InMemoryStore."""

    def __init__(self, store: InMemoryStore):
        """
        Initialize the TaskService.

        Args:
            store: The InMemoryStore instance to use for storage
        """
        self.store = store

    def create_task(self, description: str) -> str:
        """
        Create a new task.

        Args:
            description: The description of the task

        Returns:
            The ID of the created task
        """
        task = Task(description=description)
        success = self.store.create(task.id, task)

        if success:
            return task.id
        else:
            # This shouldn't happen with UUIDs, but just in case
            raise Exception(f"Failed to create task with ID {task.id}")

    def get_all_tasks(self) -> List[Task]:
        """
        Get all tasks.

        Returns:
            A list of all Task objects
        """
        return self.store.list()

    def update_task(self, task_id: str, description: Optional[str] = None, completed: Optional[bool] = None) -> bool:
        """
        Update an existing task.

        Args:
            task_id: The ID of the task to update
            description: Optional new description
            completed: Optional new completion status

        Returns:
            True if the task was updated, False if it didn't exist
        """
        existing_task = self.store.read(task_id)
        if existing_task is None:
            return False

        # Update the task properties if provided
        if description is not None:
            existing_task.update_description(description)
        if completed is not None:
            if completed:
                existing_task.mark_completed()
            else:
                existing_task.mark_incomplete()

        # Save the updated task back to the store
        return self.store.update(task_id, existing_task)

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was deleted, False if it didn't exist
        """
        return self.store.delete(task_id)

    def toggle_task_completion(self, task_id: str) -> bool:
        """
        Toggle the completion status of a task.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            True if the task was toggled, False if it didn't exist
        """
        existing_task = self.store.read(task_id)
        if existing_task is None:
            return False

        # Toggle the completion status
        if existing_task.completed:
            existing_task.mark_incomplete()
        else:
            existing_task.mark_completed()

        # Save the updated task back to the store
        return self.store.update(task_id, existing_task)