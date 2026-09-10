# task-cli

A simple, no-nonsense command-line task manager written in Python. Tasks are stored locally in a JSON file — no server, no database, no accounts.

## Features

- Add tasks with a priority (`low`, `medium`, `high`) and optional tags
- List tasks, optionally filtered by tag or including completed ones
- Mark tasks as done
- Delete tasks
- Fully tested with `pytest`

## Installation

Clone the repo and install it locally:

```bash
git clone https://github.com/<your-username>/task-cli.git
cd task-cli
pip install -e .
```

This exposes a `task-cli` command on your system.

## Usage

```bash
# Add a task
task-cli add "Write the quarterly report" -p high -t work

# List active tasks
task-cli list

# List everything, including completed tasks
task-cli list --all

# Filter by tag
task-cli list --tag work

# Mark a task as done
task-cli done 1

# Delete a task
task-cli delete 1
```

Example output:

```
[ ]   1  !!! Write the quarterly report #work
[ ]   2  !!  Buy groceries #home
[x]   3  !   Call the dentist
```

## Project structure

```
task-cli/
├── taskcli/
│   ├── __init__.py
│   ├── cli.py        # argparse-based CLI
│   └── storage.py     # Task model + JSON persistence
├── tests/
│   ├── test_cli.py
│   └── test_storage.py
├── setup.py
└── requirements-dev.txt
```

## Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Where tasks are stored

By default, tasks are saved to `~/.task-cli/tasks.json`. You can point `TaskStore` at a different path if you're using it as a library.

## License

MIT — see [LICENSE](LICENSE).
