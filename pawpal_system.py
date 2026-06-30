# pawpal_system.py
# Skeleton generated from UML class diagram (diagrams/uml.mmd)
# Classes: Task, Pet, Schedule, Owner
# Task and Pet use @dataclass for clean attribute declaration
# Schedule and Owner use regular classes (mutable state, richer __init__ logic)
# All methods are stubs (pass) — ready for implementation

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date
from typing import Optional


# --- Task ---
# Represents a single pet care activity (walk, feeding, meds, grooming, enrichment, etc.)
@dataclass
class Task:
    title: str
    description: str
    category: str  # e.g. "walk", "feeding", "meds", "grooming", "enrichment"
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
    name: str
    species: str
    breed: str
    age: int
    medical_notes: str = ""
    tasks: list[Task] = field(default_factory=list)  # starts empty; populated via add_task

    def add_task(self, _task: Task) -> None:
        # TODO: append _task to self.tasks
        pass

    def get_upcoming_tasks(self) -> list[Task]:
        # TODO: return tasks where is_completed is False
        pass


# --- Schedule ---
# Holds the ordered list of tasks planned for a date range and exposes day-level queries
class Schedule:
    def __init__(self, start_date: date, end_date: date) -> None:
        self.scheduled_tasks: list[Task] = []
        self.start_date: date = start_date
        self.end_date: date = end_date

    def add_task(self, _task: Task, _date_time: date) -> None:
        # TODO: append _task to scheduled_tasks, associated with _date_time
        pass

    def remove_task(self, _task_id: str) -> None:
        # TODO: find and remove the task matching _task_id
        pass

    def get_tasks_for_day(self, _day: date) -> list[Task]:
        # TODO: filter and return tasks scheduled on _day
        pass


# --- Owner ---
# Top-level user who owns pets and generates/manages their schedule
class Owner:
    def __init__(self, name: str, email: str, phone: str) -> None:
        self.name: str = name
        self.email: str = email
        self.phone: str = phone
        self.pets: list[Pet] = []
        self.schedule: Optional[Schedule] = None  # assigned when a schedule is generated

    def add_pet(self, _pet: Pet) -> None:
        # TODO: append _pet to self.pets
        pass

    def remove_pet(self, _pet_id: str) -> None:
        # TODO: find and remove the pet matching _pet_id
        pass

    def get_schedule(self) -> Optional[Schedule]:
        # TODO: return self.schedule
        pass
