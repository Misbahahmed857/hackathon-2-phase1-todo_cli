"""
Unit tests for the TaskService in the Phase I In-Memory Python Console App.
"""

import unittest
from src.services.task_service import TaskService
from src.storage.in_memory_store import InMemoryStore
from src.models.task import Task


class TestTaskService(unittest.TestCase):
    """Test cases for the TaskService."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.store = InMemoryStore()
        self.task_service = TaskService(self.store)

    def test_create_task(self):
        """Test creating a task."""
        description = "Test task description"
        task_id = self.task_service.create_task(description)

        # Check that a task ID was returned
        self.assertIsInstance(task_id, str)
        self.assertGreater(len(task_id), 0)

        # Check that the task exists in the store
        created_task = self.store.read(task_id)
        self.assertIsNotNone(created_task)
        self.assertEqual(created_task.description, description)
        self.assertFalse(created_task.completed)

    def test_get_all_tasks_empty(self):
        """Test getting all tasks when there are none."""
        tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(tasks), 0)
        self.assertEqual(tasks, [])

    def test_get_all_tasks_with_tasks(self):
        """Test getting all tasks when there are some."""
        # Create a few tasks
        task_id1 = self.task_service.create_task("Task 1")
        task_id2 = self.task_service.create_task("Task 2")

        # Get all tasks
        tasks = self.task_service.get_all_tasks()

        # Check that both tasks are returned
        self.assertEqual(len(tasks), 2)

        # Check that both tasks have the right descriptions
        descriptions = [task.description for task in tasks]
        self.assertIn("Task 1", descriptions)
        self.assertIn("Task 2", descriptions)

    def test_update_task_description(self):
        """Test updating a task's description."""
        original_description = "Original description"
        new_description = "New description"

        task_id = self.task_service.create_task(original_description)

        # Update the task description
        result = self.task_service.update_task(task_id, description=new_description)

        self.assertTrue(result)

        # Check that the task has the new description
        updated_task = self.store.read(task_id)
        self.assertEqual(updated_task.description, new_description)

    def test_update_task_completion_status(self):
        """Test updating a task's completion status."""
        task_id = self.task_service.create_task("Test task")

        # Initially, task should not be completed
        original_task = self.store.read(task_id)
        self.assertFalse(original_task.completed)

        # Update the task completion status to True
        result = self.task_service.update_task(task_id, completed=True)
        self.assertTrue(result)

        # Check that the task is now completed
        updated_task = self.store.read(task_id)
        self.assertTrue(updated_task.completed)

        # Update the task completion status back to False
        result = self.task_service.update_task(task_id, completed=False)
        self.assertTrue(result)

        # Check that the task is now incomplete
        updated_task = self.store.read(task_id)
        self.assertFalse(updated_task.completed)

    def test_update_task_both_description_and_completion(self):
        """Test updating both description and completion status."""
        original_description = "Original description"
        new_description = "New description"

        task_id = self.task_service.create_task(original_description)

        # Update both description and completion status
        result = self.task_service.update_task(task_id, description=new_description, completed=True)

        self.assertTrue(result)

        # Check that both changes were applied
        updated_task = self.store.read(task_id)
        self.assertEqual(updated_task.description, new_description)
        self.assertTrue(updated_task.completed)

    def test_update_nonexistent_task(self):
        """Test updating a nonexistent task."""
        result = self.task_service.update_task("nonexistent-id", description="New description")
        self.assertFalse(result)

    def test_delete_existing_task(self):
        """Test deleting an existing task."""
        task_id = self.task_service.create_task("Test task")

        # Verify task exists before deletion
        task_before = self.store.read(task_id)
        self.assertIsNotNone(task_before)

        # Delete the task
        result = self.task_service.delete_task(task_id)
        self.assertTrue(result)

        # Verify task no longer exists
        task_after = self.store.read(task_id)
        self.assertIsNone(task_after)

    def test_delete_nonexistent_task(self):
        """Test deleting a nonexistent task."""
        result = self.task_service.delete_task("nonexistent-id")
        self.assertFalse(result)

    def test_toggle_task_completion_not_completed(self):
        """Test toggling completion status of a task that's not completed."""
        task_id = self.task_service.create_task("Test task")

        # Initially, task should not be completed
        original_task = self.store.read(task_id)
        self.assertFalse(original_task.completed)

        # Toggle completion status
        result = self.task_service.toggle_task_completion(task_id)
        self.assertTrue(result)

        # Check that the task is now completed
        updated_task = self.store.read(task_id)
        self.assertTrue(updated_task.completed)

    def test_toggle_task_completion_already_completed(self):
        """Test toggling completion status of a task that's already completed."""
        task_id = self.task_service.create_task("Test task")

        # First, mark the task as completed
        self.task_service.update_task(task_id, completed=True)
        task_before = self.store.read(task_id)
        self.assertTrue(task_before.completed)

        # Toggle completion status
        result = self.task_service.toggle_task_completion(task_id)
        self.assertTrue(result)

        # Check that the task is now not completed
        updated_task = self.store.read(task_id)
        self.assertFalse(updated_task.completed)

    def test_toggle_nonexistent_task(self):
        """Test toggling completion status of a nonexistent task."""
        result = self.task_service.toggle_task_completion("nonexistent-id")
        self.assertFalse(result)

    def test_multiple_tasks_operations(self):
        """Test operations on multiple tasks."""
        # Create multiple tasks
        task_ids = []
        for i in range(5):
            task_id = self.task_service.create_task(f"Task {i}")
            task_ids.append(task_id)

        # Verify all tasks were created
        self.assertEqual(len(task_ids), 5)
        for task_id in task_ids:
            task = self.store.read(task_id)
            self.assertIsNotNone(task)

        # Update one task
        result = self.task_service.update_task(task_ids[0], description="Updated Task 0", completed=True)
        self.assertTrue(result)

        # Verify the update
        updated_task = self.store.read(task_ids[0])
        self.assertEqual(updated_task.description, "Updated Task 0")
        self.assertTrue(updated_task.completed)

        # Delete one task
        result = self.task_service.delete_task(task_ids[2])
        self.assertTrue(result)

        # Verify the deletion
        deleted_task = self.store.read(task_ids[2])
        self.assertIsNone(deleted_task)

        # Get all remaining tasks
        remaining_tasks = self.task_service.get_all_tasks()
        self.assertEqual(len(remaining_tasks), 4)  # Should be 4 after deletion


if __name__ == '__main__':
    unittest.main()