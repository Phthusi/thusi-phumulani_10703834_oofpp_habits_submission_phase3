
# Update Habit Component

## Overview

The **UpdateHabitController** component allows users to update, complete, and view habits in the command-line interface.

It provides functionality to:

* Update habit details
* Mark tasks as completed
* Update habit statuses based on start time and duration
* View individual or multiple habits

The component follows a **command-driven loop**, where each command maps to a handler method.

Gifs can be used to illustrate each step in action.

---

## Responsibilities

The UpdateHabitController handles:

* Viewing habits
* Updating habit fields
* Completing tasks with status `TO_BE_CONFIRMED`
* Updating statuses of `UPCOMING` habits based on current time

---

## Internal State

| Field               | Type            | Description                   |
| ------------------- | --------------- | ----------------------------- |
| `habit_factory`     | HabitFactory    | Handles DB operations         |
| `get_habit_view`    | GetHabitView    | Handles displaying habits     |
| `update_habit_view` | UpdateHabitView | Handles updating habit fields |
| `datetime_handler`  | DateTimeHandler | Provides time-based logic     |

---

## High-Level Flow

1. User enters the Update Habit screen.
2. The command loop presents available commands.
3. Each command triggers a handler method.
4. Habit statuses are updated automatically if needed.
5. Completed tasks are marked automatically.

Gif example:

![Update Habit Flow](./gifs/update_habit_flow.gif)

---

## Command Loop

The `execute()` method starts the command loop.

Available commands:

| Command            | Description            | Gif                                        |
| ------------------ | ---------------------- | ------------------------------------------ |
| `view habit(s)`    | View habits for update | ![View Habit](./gifs/view_habit.gif)       |
| `update habit`     | Update selected habit  | ![Update Habit](./gifs/update_habit.gif)   |
| `complete task(s)` | Mark tasks as done     | ![Complete Task](./gifs/complete_task.gif) |

Each command maps directly to a handler method in the controller.

---

## Updating Habits

Steps:

1. User selects a habit by ID.
2. `UpdateHabitView` prompts for table name and fields to update.
3. Values are validated and updated in the DB.
4. Fields are updated atomically for consistency.

Gif:

![Update Habit Fields](./gifs/update_fields.gif)

---

## Completing Tasks

Tasks with status `TO_BE_CONFIRMED` can be automatically marked as `DONE`.

Methods:

* `complete_tasks()`

Gif:

![Complete Tasks](./gifs/complete_tasks.gif)

---

## Status Updates

Habits with status `UPCOMING` are automatically checked against current time.

Methods:

* `update_statuses()`
* Uses `DateTimeHandler.map_time_to_status()` for status calculation.

Gif:

![Update Statuses](./gifs/update_statuses.gif)

---

## Viewing Habits

The user can view habit details at any time before updating.

Methods:

* `view_habit()`

Gif:

![View Habit](./gifs/view_habit.gif)

---

## Design Notes

* Business logic is separated from user interaction.
* Updates and completions are idempotent and safe to re-run.
* Decorators are used in `HabitTimeRepeatsView`, but the controller itself relies on clean method calls.
* Status calculations use current time and duration for correctness.

---

## Entry Point

The component can be launched directly:

```python
if __name__ == "__main__":
    controller = UpdateHabitController()
    controller.execute()
```

Gif example:

![Update Habit Entry](./gifs/update_habit_entry.gif)

---