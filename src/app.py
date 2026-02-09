"""
Main application entry point for the Phase I In-Memory Python Console App.

This module initializes the application and starts the main loop.
"""

try:
    # Import as modules when running from project root
    from src.cli.cli_handler import CliHandler
    from src.controllers.task_controller import TaskController
    from src.storage.in_memory_store import InMemoryStore
    from src.services.task_service import TaskService
except ImportError:
    # Import as direct modules when running from src directory
    from cli.cli_handler import CliHandler
    from controllers.task_controller import TaskController
    from storage.in_memory_store import InMemoryStore
    from services.task_service import TaskService


def main():
    """Entry point for the application."""
    print("Starting Phase I In-Memory Python Console App...")

    # Initialize the in-memory store
    store = InMemoryStore()

    # Initialize the task service
    task_service = TaskService(store)

    # Initialize the task controller
    task_controller = TaskController(task_service)

    # Initialize the CLI handler
    cli_handler = CliHandler(task_controller)

    # Start the CLI loop
    cli_handler.run()


if __name__ == "__main__":
    main()