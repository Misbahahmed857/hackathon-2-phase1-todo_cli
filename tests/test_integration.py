"""
End-to-end tests for all user stories in the Phase I In-Memory Python Console App.
"""

import unittest
from src.app import main
from src.storage.in_memory_store import InMemoryStore
from src.services.task_service import TaskService
from src.controllers.task_controller import TaskController
from src.models.task import Task


class TestEndToEndUserStories(unittest.TestCase):
    """End-to-end tests for all user stories."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.store = InMemoryStore()
        self.task_service = TaskService(self.store)
        self.task_controller = TaskController(self.task_service)

    def test_user_story_1_complete_flow(self):
        """Test the complete flow for User Story 1: Create and Manage Tasks."""
        # Given: User wants to interact with the console application to create, view, update, and delete tasks

        # When: User adds a new task
        task_id = self.task_controller.create_task("Buy groceries")

        # Then: The task is added to the in-memory list
        all_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(all_tasks), 1)
        created_task = all_tasks[0]
        self.assertEqual(created_task.description, "Buy groceries")
        self.assertFalse(created_task.completed)

        # When: User lists all tasks
        tasks = self.task_controller.get_all_tasks()

        # Then: All tasks are displayed with their details
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].description, "Buy groceries")

        # When: User updates the task
        update_success = self.task_controller.update_task(task_id, description="Buy groceries - urgent")

        # Then: The task is updated in the in-memory list
        self.assertTrue(update_success)
        updated_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(updated_tasks), 1)
        self.assertEqual(updated_tasks[0].description, "Buy groceries - urgent")

        # When: User deletes the task
        delete_success = self.task_controller.delete_task(task_id)

        # Then: The task is removed from the in-memory list
        self.assertTrue(delete_success)
        final_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(final_tasks), 0)

    def test_user_story_1_multiple_tasks(self):
        """Test User Story 1 with multiple tasks."""
        # Add multiple tasks
        task_id_1 = self.task_controller.create_task("Task 1")
        task_id_2 = self.task_controller.create_task("Task 2")
        task_id_3 = self.task_controller.create_task("Task 3")

        # Verify all tasks exist
        all_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)

        # Update one task
        self.task_controller.update_task(task_id_2, description="Updated Task 2")

        # Verify update
        updated_tasks = self.task_controller.get_all_tasks()
        updated_task = next((t for t in updated_tasks if t.id == task_id_2), None)
        self.assertIsNotNone(updated_task)
        self.assertEqual(updated_task.description, "Updated Task 2")

        # Delete one task
        self.task_controller.delete_task(task_id_1)

        # Verify deletion
        final_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(final_tasks), 2)

    def test_user_story_2_console_interface_validation(self):
        """Test User Story 2: Console Command Interface validation."""
        # Test valid task creation with validation
        task_id = self.task_controller.create_task("Valid task description")
        self.assertIsInstance(task_id, str)
        self.assertGreater(len(task_id), 0)

        # Test that empty task description raises validation error
        from src.utils.errors import ValidationError
        with self.assertRaises(ValidationError):
            self.task_controller.create_task("")

        # Test that very long task description raises validation error
        with self.assertRaises(ValidationError):
            self.task_controller.create_task("x" * 1001)  # Exceeds 1000 char limit

        # Test task ID validation
        with self.assertRaises(ValidationError):
            self.task_controller.delete_task("")  # Empty ID

        # Test update validation
        valid_task_id = self.task_controller.create_task("Another task")
        with self.assertRaises(ValidationError):
            self.task_controller.update_task(valid_task_id, description="")  # Empty description

    def test_user_story_2_error_handling(self):
        """Test User Story 2: Error handling for invalid inputs."""
        from src.utils.errors import TaskNotFoundError, ValidationError

        # Try to update a non-existent task
        with self.assertRaises(ValidationError):  # Should fail validation first
            self.task_controller.update_task("", description="New description")

        # Try to delete a non-existent task with invalid ID format
        with self.assertRaises(ValidationError):
            self.task_controller.delete_task("invalid-id-format")

        # Try to toggle completion of non-existent task with invalid ID
        with self.assertRaises(ValidationError):
            self.task_controller.toggle_task_completion("invalid-id")

    def test_user_story_3_session_persistence(self):
        """Test User Story 3: Data Persistence in Memory during session."""
        # This test verifies that data persists during the session
        task_id_1 = self.task_controller.create_task("Session task 1")
        task_id_2 = self.task_controller.create_task("Session task 2")

        # Verify tasks exist in current session
        session_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(session_tasks), 2)

        # Perform various operations during the session
        self.task_controller.update_task(task_id_1, completed=True)
        self.task_controller.toggle_task_completion(task_id_2)

        # Verify changes persist in session
        updated_tasks = self.task_controller.get_all_tasks()
        task_1 = next((t for t in updated_tasks if t.id == task_id_1), None)
        task_2 = next((t for t in updated_tasks if t.id == task_id_2), None)

        self.assertIsNotNone(task_1)
        self.assertIsNotNone(task_2)
        self.assertTrue(task_1.completed)  # Was set to True
        self.assertTrue(task_2.completed)  # Was toggled to True

        # Add more tasks during session
        task_id_3 = self.task_controller.create_task("Session task 3")
        final_session_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(final_session_tasks), 3)

    def test_user_story_3_data_clears_on_new_store(self):
        """Test that data clears when a new store is created (simulating app restart)."""
        # Create tasks in first store/session
        first_store = InMemoryStore()
        first_service = TaskService(first_store)
        first_controller = TaskController(first_service)

        first_task_id = first_controller.create_task("Task in first session")
        first_tasks = first_controller.get_all_tasks()
        self.assertEqual(len(first_tasks), 1)

        # Create a new store/controller (simulating app restart)
        second_store = InMemoryStore()
        second_service = TaskService(second_store)
        second_controller = TaskController(second_service)

        # Verify that the new store is empty
        second_tasks = second_controller.get_all_tasks()
        self.assertEqual(len(second_tasks), 0)

        # Verify that the task from the first session doesn't exist in the second
        task_from_first_session_exists = second_store.read(first_task_id) is not None
        self.assertFalse(task_from_first_session_exists)

    def test_complete_user_workflow(self):
        """Test a complete user workflow combining all user stories."""
        # Create multiple tasks (User Story 1)
        task1_id = self.task_controller.create_task("Setup development environment")
        task2_id = self.task_controller.create_task("Implement core features")
        task3_id = self.task_controller.create_task("Write documentation")

        # Verify tasks were created
        all_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(all_tasks), 3)

        # Update a task (User Story 1)
        self.task_controller.update_task(task2_id, description="Implement core features with tests")

        # Mark a task as completed (User Story 1)
        self.task_controller.toggle_task_completion(task1_id)

        # Verify changes
        updated_tasks = self.task_controller.get_all_tasks()
        setup_task = next((t for t in updated_tasks if t.id == task1_id), None)
        features_task = next((t for t in updated_tasks if t.id == task2_id), None)

        self.assertIsNotNone(setup_task)
        self.assertIsNotNone(features_task)
        self.assertTrue(setup_task.completed)
        self.assertEqual(features_task.description, "Implement core features with tests")

        # Test validation and error handling (User Story 2)
        from src.utils.errors import ValidationError
        try:
            self.task_controller.create_task("")  # Should raise ValidationError
            self.fail("Expected ValidationError for empty task description")
        except ValidationError:
            pass  # Expected

        # Verify data persists during session (User Story 3)
        final_check_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(final_check_tasks), 3)


class TestAppInitialization(unittest.TestCase):
    """Tests for application initialization."""

    def test_components_instantiate_correctly(self):
        """Test that all components can be instantiated without errors."""
        # Test store initialization
        store = InMemoryStore(max_size=100, eviction_policy=None)
        self.assertIsNotNone(store)
        self.assertEqual(store.max_size, 100)

        # Test service initialization
        service = TaskService(store)
        self.assertIsNotNone(service)

        # Test controller initialization
        controller = TaskController(service)
        self.assertIsNotNone(controller)

        # Test that they work together
        task_id = controller.create_task("Test task for initialization")
        self.assertIsInstance(task_id, str)

        tasks = controller.get_all_tasks()
        self.assertEqual(len(tasks), 1)


if __name__ == '__main__':
    unittest.main()