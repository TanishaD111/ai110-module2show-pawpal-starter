from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime, date, time, timedelta


@dataclass
class Owner:
    id: int
    name: str
    time_zone: str
    availability: List["Availability"] = field(default_factory=list)
    preferences: Dict = field(default_factory=dict)
    notification_settings: Dict = field(default_factory=dict)
    pets: List["Pet"] = field(default_factory=list)

    def update_availability(self) -> None:
        raise NotImplementedError

    def set_preferences(self, preferences: Dict) -> None:
        raise NotImplementedError

    def add_pet(self, pet: "Pet") -> None:
        """Associate a Pet with this Owner (enforce ownership invariants)."""
        raise NotImplementedError

    def remove_pet(self, pet_id: int, transfer_to_owner_id: Optional[int] = None) -> "Pet":
        """Remove or transfer a pet; because owner_id is required, require transfer id."""
        raise NotImplementedError

    def get_pet(self, pet_id: int) -> Optional["Pet"]:
        raise NotImplementedError

    def list_pets(self) -> List["Pet"]:
        raise NotImplementedError

    def transfer_pet(self, pet: "Pet", new_owner: "Owner") -> None:
        """Atomic transfer of pet to another owner."""
        raise NotImplementedError

@dataclass
class Pet:
	id: int
	owner_id: int
	name: str
	type: str
	age: int
	constraints: Dict = field(default_factory=dict)
	preferences: Dict = field(default_factory=dict)

	def update_info(self, **kwargs) -> None:
		"""Update pet information."""
		raise NotImplementedError

	def set_constraints(self, constraints: Dict) -> None:
		"""Set scheduling constraints for the pet."""
		raise NotImplementedError

	def recommended_tasks(self) -> List["Task"]:
		"""Return recommended tasks for this pet."""
		raise NotImplementedError


@dataclass
class Task:
	id: int
	pet_id: Optional[int]
	title: str
	duration_minutes: int
	priority: int
	recurrence: Optional[str] = None
	notes: Optional[str] = None
	tags: List[str] = field(default_factory=list)

	def update(self, **kwargs) -> None:
		"""Update task fields."""
		raise NotImplementedError

	def set_recurrence(self, recurrence: str) -> None:
		"""Set recurrence rule for the task."""
		raise NotImplementedError

	def estimate_effort(self) -> int:
		"""Return an estimated effort value for scheduling heuristics."""
		raise NotImplementedError


@dataclass
class Availability:
	id: int
	owner_id: int
	date_or_weekday: str
	start_time: str
	end_time: str
	is_flexible: bool = False

	def overlaps_with(self, window: "Availability") -> bool:
		"""Return True if this availability overlaps with another window."""
		raise NotImplementedError

	def contains_interval(self, start: str, end: str) -> bool:
		"""Return True if the given interval is contained in this availability."""
		raise NotImplementedError

	def intersection(self, window: "Availability") -> Optional["Availability"]:
		"""Return the intersection Availability window or None if no overlap."""
		raise NotImplementedError


@dataclass
class ScheduledTask:
	id: int
	task_id: int
	scheduled_start: str
	scheduled_end: str
	status: str
	assigned_pet_id: Optional[int] = None

	def move(self, start: str) -> None:
		"""Move scheduled task to a new start time (adjust end accordingly)."""
		raise NotImplementedError

	def mark_complete(self) -> None:
		"""Mark this scheduled task as completed."""
		raise NotImplementedError

	def duration(self) -> int:
		"""Return duration in minutes for this scheduled task."""
		raise NotImplementedError


@dataclass
class Schedule:
	date: str
	owner_id: int
	scheduled_tasks: List[ScheduledTask] = field(default_factory=list)
	summary: Optional[str] = None

	def add_scheduled_task(self, scheduled_task: ScheduledTask) -> None:
		"""Add a ScheduledTask to the schedule."""
		raise NotImplementedError

	def remove_scheduled_task(self, scheduled_task_id: int) -> None:
		"""Remove a ScheduledTask from the schedule by id."""
		raise NotImplementedError

	def detect_conflicts(self) -> List[ScheduledTask]:
		"""Detect and return a list of conflicting scheduled tasks."""
		raise NotImplementedError

	def explain_decisions(self) -> str:
		"""Return a human-readable explanation of scheduling decisions."""
		raise NotImplementedError

	@staticmethod
	def generate_schedule(owner: Owner, date_: str) -> "Schedule":
		"""Generate a schedule for the given owner and date."""
		raise NotImplementedError

