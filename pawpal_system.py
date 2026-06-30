# pawpal_system.py
# Skeleton generated from UML class diagram (diagrams/uml.mmd)
# Classes: Task, Pet, Schedule, Owner
# Task and Pet use @dataclass for clean attribute declaration
# Schedule and Owner use regular classes (mutable state, richer __init__ logic)
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
        """Mark this task as completed."""
        self.is_completed = True

    def reset(self) -> None:
        """Clear completion status so the task can be rescheduled."""
        self.is_completed = False


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
        """Append a task to this pet's task list."""
        self.tasks.append(_task)

    def get_upcoming_tasks(self) -> list[Task]:
        """Return all incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.is_completed]


# Time-of-day ordering for sort key
_TIME_ORDER = {"morning": 0, "afternoon": 1, "evening": 2}


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
        """Register a task on a specific date and stamp its scheduled_at field."""
        self.task_map[_task.id] = (_task, _date_time)
        _task.scheduled_at = _date_time

    def remove_task(self, _task_id: str) -> None:
        """Remove a task from the schedule by its id."""
        self.task_map.pop(_task_id, None)

    def get_tasks_for_day(self, _day: date) -> list[Task]:
        """Return tasks scheduled on _day, sorted by priority then time of day."""
        tasks = [task for task, scheduled_date in self.task_map.values()
                 if scheduled_date == _day]
        return sorted(tasks, key=lambda t: (t.priority, _TIME_ORDER.get(t.preferred_time_of_day, 99)))

    def get_plan_rationale(self) -> str:
        """Return a human-readable summary of the scheduled tasks grouped by day."""
        if not self.task_map:
            return "No tasks scheduled."

        lines = []
        # Group by date so multi-day schedules are readable
        days: dict[date, list[Task]] = {}
        for task, scheduled_date in self.task_map.values():
            days.setdefault(scheduled_date, []).append(task)

        for day in sorted(days):
            ordered = sorted(days[day], key=lambda t: (t.priority, _TIME_ORDER.get(t.preferred_time_of_day, 99)))
            lines.append(f"--- {day} ---")
            for rank, task in enumerate(ordered, start=1):
                time_label = f" ({task.preferred_time_of_day})" if task.preferred_time_of_day else ""
                lines.append(
                    f"  {rank}. [{task.pet.name}] {task.title}{time_label} - "
                    f"priority {task.priority}, ~{task.estimated_minutes} min"
                )

        return "\n".join(lines)


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
        """Add a pet to this owner's roster."""
        self.pets.append(_pet)

    def remove_pet(self, _pet_id: str) -> None:
        """Remove the pet matching _pet_id from the roster."""
        self.pets = [pet for pet in self.pets if pet.id != _pet_id]

    def collect_all_tasks(self) -> list[Task]:
        """Flatten all tasks across every pet into a single list."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_schedule(self) -> Optional[Schedule]:
        """Return the most recently generated schedule, or None if none exists."""
        return self.schedule

    def generate_daily_plan(self, _plan_date: date) -> Schedule:
        """Build a priority-sorted Schedule for _plan_date within the owner's daily time budget."""
        schedule = Schedule(self, _plan_date, _plan_date)

        # Candidates: incomplete tasks not yet scheduled on another day
        candidates = [
            task for task in self.collect_all_tasks()
            if not task.is_completed and task.scheduled_at is None
        ]

        # Sort by priority (ascending = highest first), then time-of-day preference
        candidates.sort(key=lambda t: (t.priority, _TIME_ORDER.get(t.preferred_time_of_day, 99)))

        minutes_used = 0
        for task in candidates:
            if minutes_used + task.estimated_minutes > self.available_minutes_per_day:
                continue  # skip tasks that don't fit; keep trying smaller ones
            schedule.add_task(task, _plan_date)
            minutes_used += task.estimated_minutes

        self.schedule = schedule
        return schedule
