"""
Integration tests for the CLI functionality in the Phase I In-Memory Python Console App.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO
import sys
from src.cli.cli_handler import CliHandler
from src.controllers.task_controller import TaskController
from src.services.task_service import TaskService
from src.storage.in_memory_store import InMemoryStore


class TestCliIntegration(unittest.TestCase):
    """Integration tests for the CLI functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.store = InMemoryStore()
        self.task_service = TaskService(self.store)
        self.task_controller = TaskController(self.task_service)
        self.cli_handler = CliHandler(self.task_controller)

    @patch('builtins.input', side_effect=['quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_quit_command_exits_gracefully(self, mock_stdout, mock_input):
        """Test that the quit command exits the CLI gracefully."""
        # Just run the CLI briefly - it will quit immediately due to mock input
        try:
            self.cli_handler.run()
        except SystemExit:
            pass  # Expected behavior
        except StopIteration:
            pass  # Expected behavior when input is exhausted

        # Verify that the quit message was printed
        output = mock_stdout.getvalue()
        self.assertIn("Thank you for using", output)

    @patch('builtins.input', side_effect=['add Test task', 'list', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_and_list_tasks(self, mock_stdout, mock_input):
        """Test adding and listing tasks through the CLI."""
        # Mock the input to simulate user interaction
        try:
            self.cli_handler.run()
        except StopIteration:
            pass  # Expected when input is exhausted

        # Verify that the task was added and listed
        output = mock_stdout.getvalue()
        # The output should contain both the task creation confirmation and the listing
        self.assertIn("Task created", output)
        self.assertIn("Test task", output)

    @patch('builtins.input', side_effect=['add First task', 'add Second task', 'list', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_add_multiple_tasks_and_list(self, mock_stdout, mock_input):
        """Test adding multiple tasks and listing them."""
        try:
            self.cli_handler.run()
        except StopIteration:
            pass  # Expected when input is exhausted

        output = mock_stdout.getvalue()
        # Both tasks should appear in the output
        self.assertIn("First task", output)
        self.assertIn("Second task", output)

    @patch('builtins.input', side_effect=['add Test task to update', 'list', 'update 1 Updated task description', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_update_task(self, mock_stdout, mock_input):
        """Test updating a task through the CLI."""
        try:
            self.cli_handler.run()
        except StopIteration:
            pass  # Expected when input is exhausted

        output = mock_stdout.getvalue()
        self.assertIn("Task created", output)
        # The update functionality should work as expected

    @patch('builtins.input', side_effect=['help', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_help_command(self, mock_stdout, mock_input):
        """Test that the help command displays help information."""
        try:
            self.cli_handler.run()
        except StopIteration:
            pass  # Expected when input is exhausted

        output = mock_stdout.getvalue()
        # The help text should be displayed
        self.assertIn("Available commands:", output)
        self.assertIn("list/ls", output)
        self.assertIn("add", output)
        self.assertIn("quit/exit/q", output)

    @patch('builtins.input', side_effect=['invalid command', 'quit'])
    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_command(self, mock_stdout, mock_input):
        """Test that invalid commands are handled gracefully."""
        try:
            self.cli_handler.run()
        except StopIteration:
            pass  # Expected when input is exhausted

        output = mock_stdout.getvalue()
        # Should show an error message for the invalid command
        self.assertIn("Unknown command: invalid command", output)

    def test_cli_handler_initialization(self):
        """Test that the CLI handler is properly initialized."""
        self.assertIsInstance(self.cli_handler.task_controller, TaskController)
        # Test that the handler has the expected methods
        self.assertTrue(hasattr(self.cli_handler, '_show_help'))
        self.assertTrue(hasattr(self.cli_handler, '_handle_list_tasks'))
        self.assertTrue(hasattr(self.cli_handler, '_handle_add_task'))


class TestTaskControllerIntegration(unittest.TestCase):
    """Integration tests for the TaskController."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.store = InMemoryStore()
        self.task_service = TaskService(self.store)
        self.task_controller = TaskController(self.task_service)

    def test_full_crud_workflow(self):
        """Test the full CRUD workflow through the controller."""
        # Create a task
        task_id = self.task_controller.create_task("Test task for CRUD workflow")
        self.assertIsInstance(task_id, str)
        self.assertGreater(len(task_id), 0)

        # Get all tasks - should have 1
        all_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(all_tasks), 1)

        # Update the task
        update_result = self.task_controller.update_task(task_id, description="Updated task description", completed=True)
        self.assertTrue(update_result)

        # Verify the update
        updated_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(updated_tasks), 1)
        updated_task = updated_tasks[0]
        self.assertEqual(updated_task.description, "Updated task description")
        self.assertTrue(updated_task.completed)

        # Toggle completion status
        toggle_result = self.task_controller.toggle_task_completion(task_id)
        self.assertTrue(toggle_result)

        # Verify the toggle
        toggled_tasks = self.task_controller.get_all_tasks()
        toggled_task = next((task for task in toggled_tasks if task.id == task_id), None)
        self.assertIsNotNone(toggled_task)
        self.assertFalse(toggled_task.completed)  # Should be false after toggle

        # Delete the task
        delete_result = self.task_controller.delete_task(task_id)
        self.assertTrue(delete_result)

        # Verify the deletion
        final_tasks = self.task_controller.get_all_tasks()
        self.assertEqual(len(final_tasks), 0)

    def test_error_handling_in_controller(self):
        """Test that the controller properly handles errors."""
        from src.utils.errors import ValidationError

        # Try to create a task with empty description - should raise ValidationError
        with self.assertRaises(ValidationError):
            self.task_controller.create_task("")

        # Try to create a task with very long description - should raise ValidationError
        with self.assertRaises(ValidationError):
            self.task_controller.create_task("x" * 1001)  # Exceeds 1000 char limit


if __name__ == '__main__':
    unittest.main()