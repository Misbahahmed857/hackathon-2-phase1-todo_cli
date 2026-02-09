"""
Task model for the Phase I In-Memory Python Console App.

This module defines the Task class with id, description, and completed status.
"""

from datetime import datetime
from typing import Optional
import uuid


class Task:
    """Represents a task in the in-memory task list."""

    def __init__(self, description: str, task_id: Optional[str] = None, completed: bool = False):
        """
        Initialize a Task instance.

        Args:
            description: The task description
            task_id: Optional task ID (generated if not provided)
            completed: Whether the task is completed (default: False)
        """
        self.id: str = task_id if task_id else str(uuid.uuid4())
        self.description: str = description
        self.completed: bool = completed
        self.created_at: datetime = datetime.now()
        self.updated_at: datetime = datetime.now()

    def mark_completed(self) -> None:
        """Mark the task as completed."""
        self.completed = True
        self.updated_at = datetime.now()

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False
        self.updated_at = datetime.now()

    def update_description(self, new_description: str) -> None:
        """Update the task description."""
        self.description = new_description
        self.updated_at = datetime.now()

    def to_dict(self) -> dict:
        """Convert the task to a dictionary representation."""
        return {
            'id': self.id,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Task':
        """Create a Task instance from a dictionary."""
        task = cls(
            description=data['description'],
            task_id=data['id'],
            completed=data.get('completed', False)
        )
        return task

    def __str__(self) -> str:
        """String representation of the task."""
        status = "✓" if self.completed else "○"
        return f"[{status}] {self.id[:8]}: {self.description}"

    def __repr__(self) -> str:
        """Developer-friendly representation of the task."""
        return f"Task(id='{self.id}', description='{self.description}', completed={self.completed})"