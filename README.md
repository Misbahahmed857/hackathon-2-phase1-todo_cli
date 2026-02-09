# Hacathon2 Phase1 - In Memory Application

This project implements an in-memory application for the hacathon2 phase1 challenge.

## Project Structure
- `.specify/memory/constitution.md` — Project principles
- `specs/<feature>/spec.md` — Feature requirements
- `specs/<feature>/plan.md` — Architecture decisions
- `specs/<feature>/tasks.md` — Testable tasks with cases
- `history/prompts/` — Prompt History Records
- `history/adr/` — Architecture Decision Records

## Quick Start

### Prerequisites
- Python 3.8+
- Virtual environment (optional but recommended)

### Installation
1. Clone the repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install dependencies (if any exist):
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application
1. Navigate to the project directory
2. Run the application:
   ```bash
   python -m src.app
   ```
3. The CLI interface will start and you can use commands like:
   - `list` or `ls` - Show all tasks
   - `add <task>` or `create <task>` - Add a new task
   - `update <id> <new_task>` - Update a task
   - `delete <id>` or `remove <id>` - Delete a task
   - `complete <id>` or `done <id>` - Mark task as complete
   - `help` - Show available commands
   - `quit` or `exit` or `q` - Exit the application

## Data Model
The in-memory application uses a flexible data model designed for high-performance operations. See the specs directory for detailed information.

## Contributing
Please follow the SDD (Spec-Driven Development) methodology outlined in the project documentation.

## License
[Specify license type here]
