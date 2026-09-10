"""Persistence layer for tasks, backed by a local JSON file."""

import json
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional
from datetime import datetime

DEFAULT_DB_PATH = Path.home() / ".task-cli" / "tasks.json"

VALID_PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    done: bool = False
    priority: str = "medium"
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat(timespec="seconds"))

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data: dict) -> "Task":
        return Task(
            id=data["id"],
            title=data["title"],
            done=data.get("done", False),
            priority=data.get("priority", "medium"),
            tags=data.get("tags", []),
            created_at=data.get("created_at", datetime.now().isoformat(timespec="seconds")),
        )


class TaskStore:
    """Reads and writes tasks to a JSON file on disk."""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.db_path.exists():
            self._write([])

    def _read(self) -> List[Task]:
        with open(self.db_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Task.from_dict(item) for item in raw]

    def _write(self, tasks: List[Task]) -> None:
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in tasks], f, indent=2, ensure_ascii=False)

    def _next_id(self, tasks: List[Task]) -> int:
        return max((t.id for t in tasks), default=0) + 1

    def add(self, title: str, priority: str = "medium", tags: Optional[List[str]] = None) -> Task:
        if priority not in VALID_PRIORITIES:
            raise ValueError(f"Invalid priority '{priority}'. Choose from {VALID_PRIORITIES}.")
        tasks = self._read()
        task = Task(id=self._next_id(tasks), title=title, priority=priority, tags=tags or [])
        tasks.append(task)
        self._write(tasks)
        return task

    def list(self, show_done: bool = True, tag: Optional[str] = None) -> List[Task]:
        tasks = self._read()
        if not show_done:
            tasks = [t for t in tasks if not t.done]
        if tag:
            tasks = [t for t in tasks if tag in t.tags]
        return sorted(tasks, key=lambda t: (t.done, VALID_PRIORITIES.index(t.priority) * -1))

    def complete(self, task_id: int) -> Task:
        tasks = self._read()
        for t in tasks:
            if t.id == task_id:
                t.done = True
                self._write(tasks)
                return t
        raise KeyError(f"No task found with id {task_id}")

    def delete(self, task_id: int) -> None:
        tasks = self._read()
        filtered = [t for t in tasks if t.id != task_id]
        if len(filtered) == len(tasks):
            raise KeyError(f"No task found with id {task_id}")
        self._write(filtered)
