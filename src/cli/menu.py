"""
Menu module for the Phase I In-Memory Python Console App.

This module handles displaying the menu interface.
"""

from src.config import CLI_MENU_HEADER, CLI_MENU_FOOTER


def display_menu():
    """Display the main menu interface."""
    print(CLI_MENU_HEADER)
    print("1. List all tasks")
    print("2. Add a new task")
    print("3. Update a task")
    print("4. Delete a task")
    print("5. Mark task as complete/incomplete")
    print("6. Help")
    print("7. Quit")
    print(CLI_MENU_FOOTER)
    print()


def display_welcome_message():
    """Display the welcome message."""
    print("Welcome to the Phase I In-Memory Python Console App!")
    print("Type 'help' for available commands or 'quit' to exit.\n")