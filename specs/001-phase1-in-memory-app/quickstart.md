# Quick Start Guide for Phase 1 In-Memory Application

## Overview
This guide will help you quickly set up and start using the in-memory application for hacathon2 phase1.

## Prerequisites
- Python 3.8 or higher
- Git (for cloning the repository)

## Setup Steps

### 1. Clone the Repository
```bash
git clone <repository-url>
cd hacathon2-phase1
```

### 2. Set Up Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

Note: Our application uses only Python standard library, so no external dependencies are required.

## Basic Usage

### Run the Console Application
The application provides a CLI interface for managing tasks:

```bash
python src/app.py
```

Once running, you can use the following commands:
- `list` or `ls` - Show all tasks
- `add <task>` or `create <task>` - Add a new task
- `update <id> <new_task>` - Update a task (use first 8 characters of task ID)
- `delete <id>` or `remove <id>` - Delete a task (use first 8 characters of task ID)
- `complete <id>` or `done <id>` - Mark task as complete (use first 8 characters of task ID)
- `help` - Show available commands
- `quit` or `exit` or `q` - Exit the application

### Example Session:
```
> add Buy groceries
Task created with ID: 550e8400-e29b-41d4-a716-446655440000
> add Walk the dog
Task created with ID: 6ba7b810-9dad-11d1-80b4-00c04fd430c8
> list
Found 2 task(s):

 1. [○] 550e8400... : Buy groceries
     Created: 2023-05-17 10:30:45

 2. [○] 6ba7b810... : Walk the dog
     Created: 2023-05-17 10:30:46

> complete 550e8400
Task 550e8400... marked as completed.
> list
Found 2 task(s):

 1. [✓] 550e8400... : Buy groceries
     Created: 2023-05-17 10:30:45

 2. [○] 6ba7b810... : Walk the dog
     Created: 2023-05-17 10:30:46

> quit
Thank you for using the Phase I In-Memory Python Console App!
```

## Architecture Overview

The application follows a layered architecture:
- `src/models/` - Data models (Task)
- `src/storage/` - In-memory storage (InMemoryStore)
- `src/services/` - Business logic (TaskService)
- `src/controllers/` - Coordination layer (TaskController)
- `src/cli/` - User interface (CliHandler, display functions)
- `src/utils/` - Utilities (validation, error handling)
- `src/config.py` - Configuration constants

## Development Workflow

### 1. Understanding the Project Structure
- `specs/`: Contains feature specifications, plans, and tasks
- `history/`: Stores prompt history records and architecture decision records
- `.specify/`: Contains project configuration and templates
- `data-model.md`: Describes the core data structures
- `README.md`: General project information

### 2. Making Changes
1. Create a new branch for your feature:
   ```bash
   git checkout -b feature/my-new-feature
   ```

2. Follow the Spec-Driven Development process:
   - Update specifications if needed
   - Create/update tasks in the appropriate tasks.md file
   - Implement the feature
   - Write tests
   - Document changes

### 3. Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_in_memory_store.py
```

## Common Tasks

### Setting up Time-To-Live (TTL) for Records
```python
# Create a record with TTL (expires in 300 seconds)
record_id = store.create(
    key="session:abc",
    value={"user_id": 123},
    ttl=300  # Expires in 5 minutes
)
```

### Configuring Eviction Policy
```python
# Create store with LRU eviction policy
store = InMemoryStore(
    max_size=1000,
    eviction_policy="LRU"  # Will remove least recently used items when full
)
```

## Troubleshooting

### Memory Issues
- Monitor store statistics regularly
- Set appropriate `max_size` limits
- Implement proper TTL values for temporary data

### Performance Issues
- Use efficient key structures
- Consider partitioning large datasets
- Monitor hit/miss ratios

## Next Steps
1. Review the detailed specifications in `specs/001-phase1-in-memory-app/`
2. Look at the data model in `data-model.md`
3. Check the implementation plan in `specs/001-phase1-in-memory-app/plan.md`
4. Begin implementing tasks from `specs/001-phase1-in-memory-app/tasks.md`