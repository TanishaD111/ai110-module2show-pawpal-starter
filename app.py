from pawpal_system import Owner, Pet, Task, Scheduler

import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# -------------------------
# SESSION STATE: OWNER
# -------------------------
if "owner" not in st.session_state:
    # Only create a new Owner once
    st.session_state.owner = Owner(id=1, name="Jordan")
    st.session_state.scheduler = Scheduler(st.session_state.owner)

# Shortcut for easier access
owner = st.session_state.owner
scheduler = st.session_state.scheduler

# -------------------------
# Quick Demo Inputs
# -------------------------
st.subheader("Owner & Pet Info")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

pet_name = st.text_input("Pet name", value="")  # default blank for adding new pets
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet") and pet_name:
    # Create pet with a unique ID based on count
    pet_id = len(owner.pets) + 1
    new_pet = Pet(id=pet_id, name=pet_name, type=species, age=1)
    owner.add_pet(new_pet)
    st.success(f"Added pet: {pet_name} ({species})")

if owner.pets:
    st.write("Current Pets:")
    for p in owner.pets:
        st.text(f"- {p.name} ({p.type})")
else:
    st.info("No pets yet. Add one above.")

# -------------------------
# Owner Preferences
# -------------------------
st.subheader("Owner Preferences & Availability")

# Availability: simple start/end input
col1, col2 = st.columns(2)
with col1:
    avail_start = st.text_input("Available from (HH:MM)", value="08:00")
with col2:
    avail_end = st.text_input("Available until (HH:MM)", value="20:00")

if st.button("Add Availability"):
    owner.add_availability(avail_start, avail_end)
    st.success(f"Added availability: {avail_start} - {avail_end}")

if owner.availability:
    st.write("Current Availability:")
    for idx, a in enumerate(owner.availability, start=1):
        st.text(f"{idx}. {a['start']} - {a['end']}")
else:
    st.info("No availability set yet. Add one above.")

# Example preference: morning tasks first
morning_first = st.checkbox("Prioritize morning tasks?", value=owner.preferences.get("morning_tasks_first", True))
owner.set_preferences({"morning_tasks_first": morning_first})

# -------------------------
# Tasks (assigned to specific pets)
# -------------------------
st.markdown("### Tasks")
st.caption("Add a few tasks for your pets. These will feed into your scheduler.")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Only show pet selection if there are pets
if owner.pets:
    pet_options = {p.name: p.id for p in owner.pets}
    selected_pet_name = st.selectbox("Select Pet for Task", options=list(pet_options.keys()))
    selected_pet_id = pet_options[selected_pet_name]
else:
    st.info("Add at least one pet to assign tasks.")
    selected_pet_id = None

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

if st.button("Add Task") and selected_pet_id is not None:
    pet = next((p for p in owner.pets if p.id == selected_pet_id), None)
    if pet:
        prio_map = {"low": 1, "medium": 3, "high": 5}
        task_id = len(pet.tasks) + 1
        task = Task(
            id=task_id,
            description=task_title,
            duration_minutes=int(duration),
            priority=prio_map[priority],
            pet_id=pet.id
        )
        pet.add_task(task)  # task is now part of the pet
        st.success(f"Added task '{task_title}' for {pet.name}")
        # OPTIONAL: keep track in session state for UI table
        st.session_state.tasks.append({
            "pet_name": pet.name,
            "title": task_title,
            "duration_minutes": int(duration),
            "priority": priority
        })

if st.session_state.tasks:
    st.write("Current Tasks:")
    st.table(st.session_state.tasks)
else:
    st.info("No tasks yet. Add one above.")

# -------------------------
# Build Schedule
# -------------------------
st.subheader("Build Schedule")
st.caption("This button will call your scheduler and show a daily plan.")

if st.button("Generate schedule"):
    if not owner.pets:
        st.warning("Add at least one pet first.")
    else:
        # Scheduler now reads tasks directly from the pets
        schedule = scheduler.generate_daily_plan(start_time="08:00")
        st.write("### Today's Schedule")
        for item in schedule:
            pet_name = next((p.name for p in owner.pets if p.id == item["pet_id"]), "Unknown")
            st.text(f"{item['start']} - {item['end']} | {item['description']} ({pet_name}, Priority {item['priority']})")

        st.write("### Schedule Explanation")
        st.text(scheduler.explain_plan(schedule))