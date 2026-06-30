# pawpal_system.py
# Skeleton generated from UML class diagram (diagrams/uml.mmd)
# Classes: Task, Pet, Schedule, Owner
# Task and Pet use @dataclass for clean attribute declaration
# Schedule and Owner use regular classes (mutable state, richer __init__ logic)
# All methods are stubs (pass) — ready for implementation
#
# Revision notes:
# - Added id fields to Task and Pet so remove methods can do reliable lookup
# - Added priority, estimated_minutes, preferred_time_of_day to Task for constraint-aware scheduling
# - Added scheduled_at to Task so Schedule can filter by day without a separate mapping
# - Added pet back-reference to Task so a flat task list retains its pet association
# - Added Owner.collect_all_tasks() to gather tasks across all pets before building a schedule

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


# --- Task ---
# Represents a single pet care activity (walk, feeding, meds, grooming, enrichment, etc.)
@dataclass
class Task:
    id: str                        # unique identifier; used by remove methods
    title: str
    description: str
    category: str                  # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
    pet: Pet                       # back-reference so a flat task list keeps its pet association
    priority: int = 1              # 1 = highest; used by Schedule to order the daily plan
    estimated_minutes: int = 0     # time cost; checked against Owner.available_minutes_per_day
    preferred_time_of_day: str = ""  # e.g. "morning", "afternoon", "evening"
    scheduled_at: Optional[date] = None  # set when Schedule.add_task is called
    is_completed: bool = False

    def complete(self) -> None:
        # TODO: set is_completed to True
        pass

    def reset(self) -> None:
        # TODO: set is_completed back to False
        pass


# --- Pet ---
# Represents a pet owned by an Owner; holds the pet's tasks
@dataclass
class Pet:
    id: str                        # unique identifier; used by Owner.remove_pet
    name: str
    species: str
    breed: str
    age: int
    medical_notes: str = ""
    tasks: list[Task] = field(default_factory=list)  # populated via add_task

    def add_task(self, _task: Task) -> None:
        # TODO: append _task to self.tasks
        pass

    def get_upcoming_tasks(self) -> list[Task]:
        # TODO: return tasks where is_completed is False
        pass


# --- Schedule ---
# Holds the ordered daily plan for an Owner across all their pets.
# Uses a dict to associate each Task with its scheduled date, avoiding a
# separate date field lookup on the task itself during day-level queries.
class Schedule:
    def __init__(self, owner: Owner, start_date: date, end_date: date) -> None:
        self.owner: Owner = owner          # back-reference; needed to respect time/preference constraints
        self.start_date: date = start_date
        self.end_date: date = end_date
        self.task_map: dict[str, tuple[Task, date]] = {}  # task.id -> (task, scheduled_date)

    def add_task(self, _task: Task, _date_time: date) -> None:
        # TODO: store (_task, _date_time) in task_map keyed by _task.id
        # TODO: also set _task.scheduled_at = _date_time
        pass

    def remove_task(self, _task_id: str) -> None:
        # TODO: delete task_map[_task_id] if it exists
        pass

    def get_tasks_for_day(self, _day: date) -> list[Task]:
        # TODO: return all tasks in task_map whose scheduled date == _day
        # TODO: consider sorting by priority then preferred_time_of_day
        pass

    def get_plan_rationale(self) -> str:
        # TODO: return a human-readable string explaining why tasks were ordered/included
        # e.g. "Morning walk scheduled first (priority 1, 30 min). Meds after breakfast..."
        pass


# --- Owner ---
# Top-level user who owns pets and generates/manages their schedule
class Owner:
    def __init__(self, name: str, email: str, phone: str,
                 available_minutes_per_day: int = 120) -> None:
        self.name: str = name
        self.email: str = email
        self.phone: str = phone
        self.available_minutes_per_day: int = available_minutes_per_day  # time constraint for planner
        self.pets: list[Pet] = []
        self.schedule: Optional[Schedule] = None  # assigned when a schedule is generated

    def add_pet(self, _pet: Pet) -> None:
        # TODO: append _pet to self.pets
        pass

    def remove_pet(self, _pet_id: str) -> None:
        # TODO: find and remove the pet where pet.id == _pet_id
        pass

    def collect_all_tasks(self) -> list[Task]:
        # TODO: iterate self.pets, flatten all pet.tasks into one list
        # This feeds Schedule so it can plan across all pets in one pass
        pass

    def get_schedule(self) -> Optional[Schedule]:
        # TODO: return self.schedule
        pass

    def generate_daily_plan(self, _plan_date: date) -> Schedule:
        # TODO: call collect_all_tasks(), filter to unscheduled/incomplete tasks,
        # sort by priority, fit within available_minutes_per_day,
        # call schedule.add_task for each selected task, then set self.schedule
        pass
