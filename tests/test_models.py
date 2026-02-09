"""
Unit tests for the Task model in the Phase I In-Memory Python Console App.
"""

import unittest
from datetime import datetime
from src.models.task import Task


class TestTask(unittest.TestCase):
    """Test cases for the Task model."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.task_description = "Test task description"
        self.task = Task(description=self.task_description)

    def test_task_initialization(self):
        """Test that a task is initialized correctly."""
        self.assertIsNotNone(self.task.id)
        self.assertEqual(self.task.description, self.task_description)
        self.assertFalse(self.task.completed)
        self.assertIsInstance(self.task.created_at, datetime)
        self.assertIsInstance(self.task.updated_at, datetime)

    def test_task_initialization_with_custom_id(self):
        """Test that a task can be initialized with a custom ID."""
        custom_id = "custom-task-id"
        task = Task(description=self.task_description, task_id=custom_id)

        self.assertEqual(task.id, custom_id)
        self.assertEqual(task.description, self.task_description)
        self.assertFalse(task.completed)

    def test_task_initialization_as_completed(self):
        """Test that a task can be initialized as completed."""
        task = Task(description=self.task_description, completed=True)

        self.assertTrue(task.completed)

    def test_mark_completed(self):
        """Test marking a task as completed."""
        self.assertFalse(self.task.completed)
        self.task.mark_completed()
        self.assertTrue(self.task.completed)
        # Check that updated_at was changed
        self.assertGreater(self.task.updated_at, self.task.created_at)

    def test_mark_incomplete(self):
        """Test marking a task as incomplete."""
        self.task.mark_completed()  # First mark as completed
        self.assertTrue(self.task.completed)
        self.task.mark_incomplete()
        self.assertFalse(self.task.completed)

    def test_update_description(self):
        """Test updating a task's description."""
        new_description = "Updated task description"
        self.task.update_description(new_description)
        self.assertEqual(self.task.description, new_description)
        # Check that updated_at was changed
        self.assertGreater(self.task.updated_at, self.task.created_at)

    def test_to_dict(self):
        """Test converting a task to dictionary."""
        task_dict = self.task.to_dict()

        self.assertEqual(task_dict['id'], self.task.id)
        self.assertEqual(task_dict['description'], self.task.description)
        self.assertEqual(task_dict['completed'], self.task.completed)
        self.assertEqual(task_dict['created_at'], self.task.created_at.isoformat())
        self.assertEqual(task_dict['updated_at'], self.task.updated_at.isoformat())

    def test_from_dict(self):
        """Test creating a task from dictionary."""
        task_dict = {
            'id': 'test-id',
            'description': 'Test description',
            'completed': True
        }
        task = Task.from_dict(task_dict)

        self.assertEqual(task.id, 'test-id')
        self.assertEqual(task.description, 'Test description')
        self.assertTrue(task.completed)

    def test_from_dict_defaults(self):
        """Test creating a task from dictionary with default values."""
        task_dict = {
            'id': 'test-id',
            'description': 'Test description'
            # 'completed' not provided, should default to False
        }
        task = Task.from_dict(task_dict)

        self.assertEqual(task.id, 'test-id')
        self.assertEqual(task.description, 'Test description')
        self.assertFalse(task.completed)

    def test_str_representation(self):
        """Test the string representation of a task."""
        # Test incomplete task
        task_str = str(self.task)
        self.assertIn("○", task_str)  # Unchecked symbol
        self.assertIn(self.task.id[:8], task_str)
        self.assertIn(self.task.description, task_str)

        # Test completed task
        self.task.mark_completed()
        task_str_completed = str(self.task)
        self.assertIn("✓", task_str_completed)  # Checked symbol

    def test_repr_representation(self):
        """Test the repr representation of a task."""
        task_repr = repr(self.task)
        self.assertIn("Task(", task_repr)
        self.assertIn(f"id='{self.task.id}'", task_repr)
        self.assertIn(f"description='{self.task.description}'", task_repr)
        self.assertIn(f"completed={self.task.completed}", task_repr)


if __name__ == '__main__':
    unittest.main()