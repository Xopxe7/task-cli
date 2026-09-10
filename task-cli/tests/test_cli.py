import json
import pytest
from taskcli import cli
from taskcli.storage import TaskStore


@pytest.fixture(autouse=True)
def isolated_store(tmp_path, monkeypatch):
    """Point the CLI's TaskStore at a temp file for every test."""
    db_path = tmp_path / "tasks.json"
    monkeypatch.setattr(cli, "TaskStore", lambda: TaskStore(db_path=db_path))
    yield db_path


def test_add_and_list(capsys):
    cli.main(["add", "Write report", "-p", "high", "-t", "work"])
    cli.main(["list"])
    captured = capsys.readouterr()
    assert "Write report" in captured.out
    assert "#work" in captured.out


def test_done_marks_task_complete(capsys):
    cli.main(["add", "Wash car"])
    cli.main(["done", "1"])
    captured = capsys.readouterr()
    assert "Completed task #1" in captured.out


def test_delete_removes_task(capsys):
    cli.main(["add", "Old task"])
    cli.main(["delete", "1"])
    captured = capsys.readouterr()
    assert "Deleted task #1" in captured.out


def test_done_unknown_id_returns_error(capsys):
    exit_code = cli.main(["done", "42"])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error" in captured.err
