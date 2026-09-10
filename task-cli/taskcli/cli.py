"""Command-line interface for task-cli."""

import argparse
import sys

from .storage import TaskStore, VALID_PRIORITIES

PRIORITY_ICON = {"high": "!!!", "medium": "!!", "low": "!"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="task-cli",
        description="A simple, no-nonsense command-line task manager.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_p = subparsers.add_parser("add", help="Add a new task")
    add_p.add_argument("title", help="Task description")
    add_p.add_argument(
        "-p", "--priority", choices=VALID_PRIORITIES, default="medium", help="Task priority"
    )
    add_p.add_argument("-t", "--tags", nargs="*", default=[], help="Tags for the task")

    list_p = subparsers.add_parser("list", help="List tasks")
    list_p.add_argument("--all", action="store_true", help="Include completed tasks")
    list_p.add_argument("--tag", help="Filter by tag")

    done_p = subparsers.add_parser("done", help="Mark a task as completed")
    done_p.add_argument("id", type=int, help="Task ID")

    delete_p = subparsers.add_parser("delete", help="Delete a task")
    delete_p.add_argument("id", type=int, help="Task ID")

    return parser


def format_task(task) -> str:
    status = "[x]" if task.done else "[ ]"
    tags = f" #{' #'.join(task.tags)}" if task.tags else ""
    icon = PRIORITY_ICON.get(task.priority, "")
    return f"{status} {task.id:>3}  {icon:<4}{task.title}{tags}"


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = TaskStore()

    try:
        if args.command == "add":
            task = store.add(args.title, priority=args.priority, tags=args.tags)
            print(f"Added task #{task.id}: {task.title}")

        elif args.command == "list":
            tasks = store.list(show_done=args.all, tag=args.tag)
            if not tasks:
                print("No tasks found.")
            for task in tasks:
                print(format_task(task))

        elif args.command == "done":
            task = store.complete(args.id)
            print(f"Completed task #{task.id}: {task.title}")

        elif args.command == "delete":
            store.delete(args.id)
            print(f"Deleted task #{args.id}")

    except (ValueError, KeyError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
