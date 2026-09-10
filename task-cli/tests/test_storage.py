import pytest
from taskcli.storage import TaskStore


@pytest.fixture
def store(tmp_path):
    return TaskStore(db_path=tmp_path / "tasks.json")


def test_add_task(store):
    task = store.add("Buy milk", priority="high", tags=["errands"])
    assert task.id == 1
    assert task.title == "Buy milk"
    assert task.priority == "high"
    assert "errands" in task.tags


def test_add_invalid_priority_raises(store):
    with pytest.raises(ValueError):
        store.add("Bad task", priority="urgent")


def test_list_excludes_done_by_default(store):
    t1 = store.add("Task 1")
    store.add("Task 2")
    store.complete(t1.id)

    active = store.list(show_done=False)
    assert len(active) == 1
    assert active[0].title == "Task 2"


def test_list_all_includes_done(store):
    t1 = store.add("Task 1")
    store.complete(t1.id)

    all_tasks = store.list(show_done=True)
    assert len(all_tasks) == 1
    assert all_tasks[0].done is True


def test_filter_by_tag(store):
    store.add("Task 1", tags=["work"])
    store.add("Task 2", tags=["home"])

    filtered = store.list(tag="work")
    assert len(filtered) == 1
    assert filtered[0].title == "Task 1"


def test_complete_unknown_id_raises(store):
    with pytest.raises(KeyError):
        store.complete(999)


def test_delete_task(store):
    task = store.add("Temp task")
    store.delete(task.id)
    assert store.list() == []


def test_delete_unknown_id_raises(store):
    with pytest.raises(KeyError):
        store.delete(999)
