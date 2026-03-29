import pytest
from pawpal_system import Owner, Pet, Task, Scheduler


# -------------------------
# Fixture: Setup Owner, Pets, Tasks
# -------------------------
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


# -------------------------
# Edge Case: No Tasks
# -------------------------
def test_scheduler_no_tasks():
    owner = Owner(id=2, name="Alex")
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_plan(start_time="08:00")
    assert schedule == []
    explanation = scheduler.explain_plan(schedule)
    assert "Schedule generated" in explanation


# -------------------------
# Edge Case: Tasks with Same Priority
# -------------------------
def test_same_priority_tasks():
    owner = Owner(id=3, name="Sam")
    pet = Pet(id=1, name="Max", type="Dog", age=4)
    owner.add_pet(pet)
    # Two tasks, same priority, different durations
    task1 = Task(id=1, description="Task A", duration_minutes=15, priority=3)
    task2 = Task(id=2, description="Task B", duration_minutes=10, priority=3)
    pet.add_task(task1)
    pet.add_task(task2)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_plan(start_time="08:00")
    # Task with shorter duration should come first if priority equal
    assert schedule[0]['task_id'] == task2.id
    assert schedule[1]['task_id'] == task1.id


# -------------------------
# Edge Case: Task Already Completed
# -------------------------
def test_scheduler_skips_completed_task():
    owner = Owner(id=4, name="Lina")
    pet = Pet(id=1, name="Charlie", type="Cat", age=2)
    owner.add_pet(pet)
    task = Task(id=1, description="Nap", duration_minutes=20, priority=4)
    pet.add_task(task)
    task.mark_complete()
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_plan(start_time="08:00")
    # Completed task should not appear in schedule
    assert all(item['task_id'] != task.id for item in schedule)


# -------------------------
# Edge Case: Multiple Pets, Overlapping Tasks
# -------------------------
def test_scheduler_multiple_pets_order():
    owner = Owner(id=5, name="Jordan")
    dog = Pet(id=1, name="Buddy", type="Dog", age=3)
    cat = Pet(id=2, name="Whiskers", type="Cat", age=2)
    owner.add_pet(dog)
    owner.add_pet(cat)
    t1 = Task(id=1, description="Walk Dog", duration_minutes=30, priority=5, pet_id=dog.id)
    t2 = Task(id=2, description="Feed Cat", duration_minutes=10, priority=4, pet_id=cat.id)
    t3 = Task(id=3, description="Brush Dog", duration_minutes=20, priority=4, pet_id=dog.id)
    dog.add_task(t1)
    dog.add_task(t3)
    cat.add_task(t2)
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_plan(start_time="08:00")
    # First task should be highest priority
    assert schedule[0]['task_id'] == t1.id
    # Tasks of equal priority ordered by duration
    assert schedule[1]['task_id'] == t2.id or schedule[1]['task_id'] == t3.id