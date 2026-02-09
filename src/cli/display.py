"""
Display module for the Phase I In-Memory Python Console App.

This module handles displaying tasks and other information to the user.
"""

from typing import List
from src.models.task import Task


def display_tasks(tasks: List[Task]):
    """
    Display a list of tasks to the user.

    Args:
        tasks: A list of Task objects to display
    """
    if not tasks:
        print("No tasks found.")
        return

    print(f"\nFound {len(tasks)} task(s):\n")
    print("-" * 60)

    # Sort tasks by creation date (newest first)
    sorted_tasks = sorted(tasks, key=lambda t: t.created_at, reverse=True)

    for i, task in enumerate(sorted_tasks, 1):
        status = "✓" if task.completed else "○"
        print(f"{i:2d}. [{status}] {task.id[:8]}... : {task.description}")
        print(f"    Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        if task.updated_at != task.created_at:
            print(f"    Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print()

    print("-" * 60)


def display_single_task(task: Task):
    """
    Display a single task to the user.

    Args:
        task: A Task object to display
    """
    status = "Completed" if task.completed else "Pending"
    print(f"\nTask Details:")
    print(f"  ID: {task.id}")
    print(f"  Description: {task.description}")
    print(f"  Status: {status}")
    print(f"  Created: {task.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
    if task.updated_at != task.created_at:
        print(f"  Updated: {task.updated_at.strftime('%Y-%m-%d %H:%M:%S')}")