from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, timedelta


@dataclass
class Task:
    id: int
    description: str
    duration_minutes: int
    priority: int
    frequency: Optional[str] = None  # e.g., "daily", "weekly"
    completed: bool = False
    pet_id: Optional[int] = None

    def mark_complete(self) -> None:
        self.completed = True

    def mark_incomplete(self) -> None:
        self.completed = False


@dataclass
class Pet:
    id: int
    name: str
    type: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        task.pet_id = self.id
        self.tasks.append(task)

    def remove_task(self, task_id: int) -> None:
        self.tasks = [t for t in self.tasks if t.id != task_id]

    def get_tasks(self) -> List[Task]:
        return self.tasks


@dataclass
class Owner:
    id: int
    name: str
    pets: List[Pet] = field(default_factory=list)
    
    # New: availability and preferences
    availability: List[Dict[str, str]] = field(default_factory=list)  # e.g., [{"start": "08:00", "end": "12:00"}]
    preferences: Dict = field(default_factory=dict)  # e.g., {"morning_tasks_first": True, "max_daily_minutes": 120}

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.get_tasks())
        return tasks

    # New methods
    def add_availability(self, start: str, end: str) -> None:
        """Add a time window when the owner is available."""
        self.availability.append({"start": start, "end": end})

    def set_preferences(self, preferences: Dict) -> None:
        """Update owner preferences."""
        self.preferences.update(preferences)


class Scheduler:
    def __init__(self, owner):
        self.owner = owner

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks from all pets of the owner."""
        return self.owner.get_all_tasks()

    def generate_daily_plan(self, start_time: str = "08:00") -> List[Dict]:
        """
        Generate a daily schedule based on:
        - Priority (higher first)
        - Duration (shorter first if same priority)
        - Owner availability
        """
        tasks = [t for t in self.get_all_tasks() if not t.completed]

        # Sort tasks by priority descending, then duration ascending
        tasks.sort(key=lambda t: (-t.priority, t.duration_minutes))

        schedule = []

        # Sort availability windows by start time
        available_windows = sorted(self.owner.availability, key=lambda w: w["start"])
        if not available_windows:
            # Default full day if no availability set
            available_windows = [{"start": start_time, "end": "20:00"}]

        window_index = 0
        current_time = datetime.strptime(available_windows[0]["start"], "%H:%M")

        for task in tasks:
            task_duration = timedelta(minutes=task.duration_minutes)

            # Skip windows until task fits
            while current_time + task_duration > datetime.strptime(available_windows[window_index]["end"], "%H:%M"):
                window_index += 1
                if window_index >= len(available_windows):
                    # No more availability windows left
                    return schedule
                current_time = datetime.strptime(available_windows[window_index]["start"], "%H:%M")

            end_time = current_time + task_duration

            schedule.append({
                "task_id": task.id,
                "description": task.description,
                "pet_id": task.pet_id,
                "start": current_time.strftime("%H:%M"),
                "end": end_time.strftime("%H:%M"),
                "priority": task.priority
            })

            # Move current time forward within the same window
            current_time = end_time

        return schedule

    def explain_plan(self, schedule: List[Dict]) -> str:
        explanation = []
        explanation.append("Schedule generated based on priority, task duration, and owner availability.")
        explanation.append("Higher priority tasks are scheduled earlier.")
        explanation.append("For equal priority, shorter tasks are scheduled first.\n")

        for item in schedule:
            explanation.append(
                f"Task '{item['description']}' scheduled at {item['start']} "
                f"(priority {item['priority']})."
            )

        return "\n".join(explanation)