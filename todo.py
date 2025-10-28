# todo/app.py
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import List, Optional

CONFIG_PATH = Path.home() / ".todo_cli.json"

@dataclass
class Task:
    id: int
    text: str
    done: bool = False

class TodoStore:
    def __init__(self, path: Path = CONFIG_PATH):
        self.path = path
        self.tasks: List[Task] = []
        self._load()

    def _load(self):
        if not self.path.exists():
            self.tasks = []
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.tasks = [Task(**t) for t in data]
        except Exception:
            # If file corrupted, start fresh
            self.tasks = []

    def _save(self):
        data = [asdict(t) for t in self.tasks]
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _next_id(self):
        return (max((t.id for t in self.tasks), default=0) + 1)

    def add(self, text: str) -> Task:
        task = Task(id=self._next_id(), text=text)
        self.tasks.append(task)
        self._save()
        return task

    def list(self, show_all: bool = True) -> List[Task]:
        if show_all:
            return list(self.tasks)
        return [t for t in self.tasks if not t.done]

    def get(self, task_id: int) -> Optional[Task]:
        for t in self.tasks:
            if t.id == task_id:
                return t
        return None

    def done(self, task_id: int) -> bool:
        t = self.get(task_id)
        if not t:
            return False
        t.done = True
        self._save()
        return True

    def delete(self, task_id: int) -> bool:
        t = self.get(task_id)
        if not t:
            return False
        self.tasks = [x for x in self.tasks if x.id != task_id]
        self._save()
        return True
