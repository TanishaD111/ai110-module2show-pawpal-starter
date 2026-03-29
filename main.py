from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # -------------------------
    # CREATE OWNER
    # -------------------------
    owner = Owner(id=1, name="Tanisha")

    # -------------------------
    # CREATE PETS
    # -------------------------
    dog = Pet(id=1, name="Buddy", type="Dog", age=3)
    cat = Pet(id=2, name="Whiskers", type="Cat", age=2)

    owner.add_pet(dog)
    owner.add_pet(cat)

    # -------------------------
    # ADD TASKS TO DOG
    # -------------------------
    task1 = Task(id=1, description="Feed Breakfast", duration_minutes=10, priority=5)
    task2 = Task(id=2, description="Morning Walk", duration_minutes=30, priority=3)
    task3 = Task(id=3, description="Grooming", duration_minutes=20, priority=2)

    dog.add_task(task1)
    dog.add_task(task2)
    dog.add_task(task3)

    # -------------------------
    # ADD TASKS TO CAT
    # -------------------------
    task4 = Task(id=4, description="Feed Breakfast", duration_minutes=5, priority=5)
    task5 = Task(id=5, description="Playtime", duration_minutes=15, priority=4)
    task6 = Task(id=6, description="Litter Box Cleaning", duration_minutes=10, priority=3)

    cat.add_task(task4)
    cat.add_task(task5)
    cat.add_task(task6)

    # -------------------------
    # GENERATE SCHEDULE
    # -------------------------
    scheduler = Scheduler(owner)
    schedule = scheduler.generate_daily_plan(start_time="08:00")

    # -------------------------
    # PRINT SCHEDULE
    # -------------------------
    print("\n=== Today's Schedule ===\n")

    for item in schedule:
        # Find pet name
        pet_name = next((p.name for p in owner.pets if p.id == item['pet_id']), "Unknown")
        print(
            f"{item['start']} - {item['end']} | {item['description']} "
            f"({pet_name}, Priority {item['priority']})"
        )

    # -------------------------
    # PRINT EXPLANATION
    # -------------------------
    print("\n=== Explanation ===\n")
    print(scheduler.explain_plan(schedule))


if __name__ == "__main__":
    main()