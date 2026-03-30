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

I took into account the time an owner had, the priority of the task, and if the owner preferred to do tasks in the morning. I decided that higher priority tasks are scheduled earlier. For those with same priority, shorter tasks are scheduled first.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

A tradeoff this app makes is that it is applicable to one owner only. Even if I enter another name it won't matter, except in the backend. This is because only one person will run the app so it doesn't make sense to really have that functionality for the UI.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

With AI I used it for my entire process from creating the UML diagram all the way to testing the final app. I also used it to refactor or add any feature when I wanted to. The most helpful questions aren't to write the whole code but something very specific. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

In the beginning I initially accepted an AI suggestion when I made the UML diagram. However, I realized that this was overly complex and did my own, then asked AI to verify it and give suggestions, which worked out better.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested all core behavior of my app. These tests are important because it tests both regular interactions and edge cases.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am confident my scheduler works correctly with what features I wanted it to have. I think there are some confusing ones, but the way I implemented them makes sense to me. If I had more time, I would fix the UI and handle multiple owners being able to generate different schedules.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I am satisfied with the features I was able to add and how I was able to learn to include AI in the process.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

I would improve how I am checking off the completed tasks. I have it as a checkbox with the task right now, but I think it will be more efficient to maybe do this in the schedule area.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

I learned that it is complex if you give AI a very broad task or a very complex one as well. It does not process too much at once, but breaking it all apart helps a lot. Also, knowing what you want yourself is important since you can verify what AI gives to you. 
