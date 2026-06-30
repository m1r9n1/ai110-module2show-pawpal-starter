import sys
import os

# Make the project root importable when running pytest from any directory
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Pet, Task


# Helper: build a minimal Task without needing a full Owner/Schedule setup
def make_task(task_id="t1", priority=1, minutes=10, time_of_day="morning"):
    # A Pet is required by Task's pet field; create a throwaway one
    pet = Pet(id="p0", name="TestPet", species="Dog", breed="Mixed", age=1)
    return Task(
        id=task_id,
        title="Test Task",
        description="Used in unit tests",
        category="test",
        pet=pet,
        priority=priority,
        estimated_minutes=minutes,
        preferred_time_of_day=time_of_day,
    )


# --- Task completion tests ---

def test_task_starts_incomplete():
    # A new Task should default to is_completed=False before anything is called
    task = make_task()
    print(f"[DEBUG] is_completed before complete(): {task.is_completed}")  # DELETE AFTER VERIFY
    assert task.is_completed is False


def test_complete_marks_task_done():
    # Calling complete() must flip is_completed to True
    task = make_task()
    print(f"[DEBUG] is_completed before complete(): {task.is_completed}")  # DELETE AFTER VERIFY
    task.complete()
    print(f"[DEBUG] is_completed after complete(): {task.is_completed}")   # DELETE AFTER VERIFY
    assert task.is_completed is True


# --- Task addition tests ---

def test_add_multiple_tasks_increases_count():
    # Adding multiple tasks should accumulate — catches overwrite-instead-of-append bugs
    pet = Pet(id="p2", name="Maki", species="Dog", breed="Dachshund", age=3)
    task_a = make_task(task_id="t1")
    task_b = make_task(task_id="t2")
    pet.add_task(task_a)
    print(f"[DEBUG] task count after 1st add_task(): {len(pet.tasks)}")  # DELETE AFTER VERIFY
    pet.add_task(task_b)
    print(f"[DEBUG] task count after 2nd add_task(): {len(pet.tasks)}")  # DELETE AFTER VERIFY
    assert len(pet.tasks) == 2
