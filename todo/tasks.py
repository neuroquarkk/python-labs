import os
import json

DB_FILE = "tasks.json"


def _load_tasks() -> list:
    if not os.path.exists(DB_FILE):
        return []
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


_tasks = _load_tasks()


def _save_tasks() -> None:
    with open(DB_FILE, "w") as f:
        json.dump(_tasks, f, indent=4)


def add_task(description: str) -> bool:
    if description.strip():
        task = {"title": description, "completed": False}
        _tasks.append(task)
        _save_tasks()
        return True
    return False


def get_tasks() -> list:
    return _tasks


def delete_task(task_number: str) -> str | None:
    try:
        # convert 1 based user input to 0 based index
        index = int(task_number) - 1
        if 0 <= index < len(_tasks):
            removed = _tasks.pop(index)
            _save_tasks()
            return removed['title']
        else:
            return None
    except ValueError:
        return None


def toggle_task(task_number: str) -> bool | None:
    try:
        index = int(task_number) - 1
        if 0 <= index < len(_tasks):
            _tasks[index]["completed"] = not _tasks[index]["completed"]
            _save_tasks()
            return _tasks[index]['completed']
    except ValueError:
        pass
    return None


def edit_task(task_number: str, description: str) -> str | None:
    try:
        index = int(task_number) - 1
        if 0 <= index < len(_tasks) and description.strip():
            _tasks[index]["title"] = description
            _save_tasks()
            return _tasks[index]['title']
    except ValueError:
        pass
    return None
