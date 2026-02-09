"""
CLI Handler for the Phase I In-Memory Python Console App.

This module processes user commands and manages the CLI interface.
"""

from typing import Optional
from src.controllers.task_controller import TaskController
from src.utils.validation import validate_command, sanitize_input
from src.utils.errors import handle_error
from src.cli.menu import display_menu
from src.cli.display import display_tasks


class CliHandler:
    """Handles user input and commands for the CLI interface."""

    def __init__(self, task_controller: TaskController):
        """
        Initialize the CLI handler.

        Args:
            task_controller: The TaskController instance to use for operations
        """
        self.task_controller = task_controller

    def run(self):
        """Start the main CLI loop."""
        print("Welcome to the Phase I In-Memory Python Console App!")
        print("Type 'help' for available commands or 'quit' to exit.\n")

        while True:
            try:
                # Display prompt and get user input
                user_input = input("> ").strip()

                # Process the command
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("Thank you for using the Phase I In-Memory Python Console App!")
                    break
                elif user_input.lower() in ['help', 'h']:
                    self._show_help()
                elif user_input.lower() in ['list', 'ls']:
                    self._handle_list_tasks()
                elif user_input.lower().startswith('add ') or user_input.lower().startswith('create '):
                    self._handle_add_task(user_input)
                elif user_input.lower().startswith('update '):
                    self._handle_update_task(user_input)
                elif user_input.lower().startswith('delete ') or user_input.lower().startswith('remove '):
                    self._handle_delete_task(user_input)
                elif user_input.lower().startswith('complete ') or user_input.lower().startswith('done '):
                    self._handle_toggle_completion(user_input)
                elif user_input.lower() == '':
                    continue  # Empty input, just show prompt again
                else:
                    print(f"Unknown command: {user_input}. Type 'help' for available commands.")
            except KeyboardInterrupt:
                print("\n\nReceived interrupt signal. Goodbye!")
                break
            except EOFError:
                print("\n\nEnd of input received. Goodbye!")
                break
            except Exception as e:
                print(handle_error(e, "CLI command processing"))

    def _show_help(self):
        """Display help information."""
        print("\nAvailable commands:")
        print("  list/ls          - Show all tasks")
        print("  add <task>       - Add a new task")
        print("  create <task>    - Add a new task")
        print("  update <id> <new_task> - Update a task")
        print("  delete <id>      - Delete a task")
        print("  remove <id>      - Delete a task")
        print("  complete <id>    - Mark task as complete")
        print("  done <id>        - Mark task as complete")
        print("  help/h           - Show this help message")
        print("  quit/exit/q      - Exit the application\n")

    def _handle_list_tasks(self):
        """Handle the list tasks command."""
        try:
            tasks = self.task_controller.get_all_tasks()
            display_tasks(tasks)
        except Exception as e:
            print(handle_error(e, "listing tasks"))

    def _handle_add_task(self, user_input: str):
        """Handle the add task command."""
        try:
            # Extract the task description from the command
            parts = user_input.split(' ', 1)
            if len(parts) < 2:
                print("Please provide a task description. Usage: add <task>")
                return

            description = parts[1].strip()
            if not description:
                print("Task description cannot be empty.")
                return

            task_id = self.task_controller.create_task(description)
            print(f"Task created with ID: {task_id[:8]}...")
        except Exception as e:
            print(handle_error(e, "adding task"))

    def _handle_update_task(self, user_input: str):
        """Handle the update task command."""
        try:
            # Extract task ID and new description from the command
            parts = user_input.split(' ', 2)
            if len(parts) < 3:
                print("Please provide both task ID and new description. Usage: update <id> <new_task>")
                return

            task_id_full = parts[1]
            new_description = parts[2].strip()

            if not new_description:
                print("New task description cannot be empty.")
                return

            # Find the full task ID by searching for the shortened version
            all_tasks = self.task_controller.get_all_tasks()
            matching_task_ids = [task.id for task in all_tasks if task.id.startswith(task_id_full)]

            if len(matching_task_ids) == 0:
                print(f"No task found with ID starting with: {task_id_full}")
                return
            elif len(matching_task_ids) > 1:
                print(f"Multiple tasks found with ID starting with: {task_id_full}")
                print("Please provide more characters to uniquely identify the task.")
                return

            task_id = matching_task_ids[0]
            success = self.task_controller.update_task(task_id, new_description)

            if success:
                print(f"Task {task_id[:8]}... updated successfully.")
            else:
                print(f"Failed to update task with ID: {task_id[:8]}...")
        except Exception as e:
            print(handle_error(e, "updating task"))

    def _handle_delete_task(self, user_input: str):
        """Handle the delete task command."""
        try:
            # Extract task ID from the command
            parts = user_input.split(' ', 1)
            if len(parts) < 2:
                print("Please provide a task ID. Usage: delete <id>")
                return

            task_id_short = parts[1].strip()
            if not task_id_short:
                print("Task ID cannot be empty.")
                return

            # Find the full task ID by searching for the shortened version
            all_tasks = self.task_controller.get_all_tasks()
            matching_task_ids = [task.id for task in all_tasks if task.id.startswith(task_id_short)]

            if len(matching_task_ids) == 0:
                print(f"No task found with ID starting with: {task_id_short}")
                return
            elif len(matching_task_ids) > 1:
                print(f"Multiple tasks found with ID starting with: {task_id_short}")
                print("Please provide more characters to uniquely identify the task.")
                return

            task_id = matching_task_ids[0]
            success = self.task_controller.delete_task(task_id)

            if success:
                print(f"Task {task_id[:8]}... deleted successfully.")
            else:
                print(f"Failed to delete task with ID: {task_id[:8]}...")
        except Exception as e:
            print(handle_error(e, "deleting task"))

    def _handle_toggle_completion(self, user_input: str):
        """Handle the toggle task completion command."""
        try:
            # Extract task ID from the command
            parts = user_input.split(' ', 1)
            if len(parts) < 2:
                print("Please provide a task ID. Usage: complete <id>")
                return

            task_id_short = parts[1].strip()
            if not task_id_short:
                print("Task ID cannot be empty.")
                return

            # Find the full task ID by searching for the shortened version
            all_tasks = self.task_controller.get_all_tasks()
            matching_task_ids = [task.id for task in all_tasks if task.id.startswith(task_id_short)]

            if len(matching_task_ids) == 0:
                print(f"No task found with ID starting with: {task_id_short}")
                return
            elif len(matching_task_ids) > 1:
                print(f"Multiple tasks found with ID starting with: {task_id_short}")
                print("Please provide more characters to uniquely identify the task.")
                return

            task_id = matching_task_ids[0]
            success = self.task_controller.toggle_task_completion(task_id)

            if success:
                # Check the new status by retrieving the task again
                updated_task = None
                for task in all_tasks:
                    if task.id == task_id:
                        updated_task = task
                        break

                status = "completed" if updated_task and updated_task.completed else "incomplete"
                print(f"Task {task_id[:8]}... marked as {status}.")
            else:
                print(f"Failed to toggle completion for task with ID: {task_id[:8]}...")
        except Exception as e:
            print(handle_error(e, "toggling task completion"))