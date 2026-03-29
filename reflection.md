# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

Three core actions a user should be able to perform:
1. Add availability and pet/s information to account
2. Create, edit, and delete pet care tasks, such as walking, grooming, etc
3. See a daily editable schedule according to pet care tasks and owner availability

Attributes and methods:
Owner:
- Attributes: id, name, time_zone, availability (list of Availability), preferences (dict), notification_settings.
- Methods: update_availability(), set_preferences(), add_pet(), get_available_windows(date).

Pet:
- Attributes: id, owner_id, name, type (dog/cat/etc.), age, constraints (e.g., no stairs), preferences (e.g., short walks).
- Methods: update_info(), set_constraints(), recommended_tasks().

Task (task template):
- Attributes: id, pet_id (or null for owner-level), title, duration_minutes, priority (int), recurrence (e.g., daily/weekly), notes, tags.
- Methods: update(), set_recurrence(), estimate_effort().

Availability (time window):
- Attributes: id, owner_id, date (or weekday), start_time, end_time, is_flexible (bool).
- Methods: overlaps_with(window), contains_interval(start,end), intersection(window).

ScheduledTask (task placed in a schedule):
- Attributes: id, task_id, scheduled_start, scheduled_end, status (planned/completed/conflict), assigned_pet_id.
- Methods: move(start), mark_complete(), duration().

Schedule (daily plan):
- Attributes: date, owner_id, scheduled_tasks (list of ScheduledTask), summary (optional explanation).
- Methods: add_scheduled_task(), remove_scheduled_task(), detect_conflicts(), explain_decisions(), generate_schedule(owner, date).

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

I realized that owner has no pets collection and only the pet stores the owner id. I added a pet list for owners.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
