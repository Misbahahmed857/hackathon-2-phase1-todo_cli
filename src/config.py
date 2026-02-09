# Project configuration for Phase I In-Memory Python Console App

# Application settings
APP_NAME = "Phase I In-Memory Python Console App"
VERSION = "1.0.0"
DESCRIPTION = "A CLI-based todo application with in-memory storage"

# In-memory storage settings
DEFAULT_MAX_SIZE = 1000  # Maximum number of tasks to store
DEFAULT_EVICTION_POLICY = "FIFO"  # Default eviction policy when max size reached

# CLI settings
CLI_PROMPT = "> "
CLI_MENU_HEADER = "=== Phase I In-Memory Python Console App ==="
CLI_MENU_FOOTER = "============================="