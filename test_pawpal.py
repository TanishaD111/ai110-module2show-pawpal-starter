import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


@pytest.fixture
def setup_owner_pets_tasks():
    # Create owner
    owner = Owner(id=1, name="Tanisha")
    
    # Create pets
    dog = Pet(id=1, name="Buddy", type="Dog", age=3)
    cat = Pet(id=2, name="Whiskers", type="Cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Create tasks
    task1 = Task(id=1, description="Feed Breakfast", duration_minutes=10, priority=5)
    task2 = Task(id=2, description="Morning Walk", duration_minutes=30, priority=3)
    task3 = Task(id=3, description="Playtime", duration_minutes=15, priority=4)

    # Assign tasks
    dog.add_task(task1)
    dog.add_task(task2)
    cat.add_task(task3)

    # Create scheduler
    scheduler = Scheduler(owner)

    return owner, dog, cat, task1, task2, task3, scheduler


# -------------------------
# Task Completion
# -------------------------
def test_task_completion(setup_owner_pets_tasks):
    _, _, _, task1, _, _, _ = setup_owner_pets_tasks
    assert not task1.completed
    task1.mark_complete()
    assert task1.completed
    task1.mark_incomplete()
    assert not task1.completed


# -------------------------
# Task Addition
# -------------------------
def test_task_addition_to_pet(setup_owner_pets_tasks):
    _, dog, _, _, _, _, _ = setup_owner_pets_tasks
    initial_count = len(dog.tasks)
    new_task = Task(id=4, description="Grooming", duration_minutes=20, priority=2)
    dog.add_task(new_task)
    assert len(dog.tasks) == initial_count + 1
    assert new_task in dog.tasks


# -------------------------
# Owner retrieves all tasks
# -------------------------
def test_owner_get_all_tasks(setup_owner_pets_tasks):
    owner, _, _, task1, task2, task3, _ = setup_owner_pets_tasks
    all_tasks = owner.get_all_tasks()
    assert len(all_tasks) == 3
    assert task1 in all_tasks
    assert task2 in all_tasks
    assert task3 in all_tasks


# -------------------------
# Scheduler generates daily plan
# -------------------------
def test_scheduler_generate_daily_plan(setup_owner_pets_tasks):
    _, _, _, task1, task2, task3, scheduler = setup_owner_pets_tasks
    schedule = scheduler.generate_daily_plan(start_time="08:00")
    assert len(schedule) == 3  # all tasks included
    # Verify first task is highest priority
    assert schedule[0]['task_id'] == task1.id
    # Verify start and end times of first task
    assert schedule[0]['start'] == "08:00"
    assert schedule[0]['end'] == "08:10"


# -------------------------
# Scheduler explanation
# -------------------------
def test_scheduler_explain_plan(setup_owner_pets_tasks):
    _, _, _, task1, _, _, scheduler = setup_owner_pets_tasks
    schedule = scheduler.generate_daily_plan(start_time="08:00")
    explanation = scheduler.explain_plan(schedule)
    assert isinstance(explanation, str)
    assert "Feed Breakfast" in explanation