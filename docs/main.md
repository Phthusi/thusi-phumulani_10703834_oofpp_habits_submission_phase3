# Habit Tracker Project Overview

## Project Purpose

This **Habit Tracker** is a command-line interface (CLI) application designed to help users:

* Track habits with start times, durations, and descriptions.
* Set repeat patterns for habits on a weekly and monthly basis.
* Automatically update habit statuses based on time and activity.
* Search, update, and delete habits efficiently.

It’s a lightweight but fully featured system for building **consistency, accountability, and growth tracking**.

---

## System Components

The project is structured into modular components:

| Component/Controller                  | Responsibility                                                         |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `AddHabitView` / `AddHabitController` | Guides the user to create a new habit and optional repeat patterns.    |
| `UpdateHabitController`               | Allows users to update habit details and mark tasks as complete.       |
| `DeleteHabitController`               | Deletes a habit from the database.                                     |
| `SearchHabit`                         | Searches habits by name, status, date, or content.                     |
| `HabitTimeRepeatsView`                | Configures weekly and monthly repeat patterns for habits.              |
| `HabitFactory`                        | Handles all CRUD operations for habits, interfacing with the database. |
| `DatabaseInterface` / `Database`      | Stores habits and their content in SQLite.                             |
| `DateTimeHandler`                     | Manages time, duration, and habit status calculations.                 |
| `Colors`                              | Manages CLI colors and styling for outputs.                            |
| `AutoCompleter`                       | Provides command auto-completion for CLI inputs.                       |

---

## How the System Works

### 1. Creating Habits

1. Users enter the **Add Habit** component via the CLI.
2. The system prompts for:

   * Habit name
   * Start date and time (format: `YYYY-MM-DD, HH:MM`)
   * Session duration (format: `HH:MM:SS`)
   * Optional description
3. Users can configure **repeat patterns**:

   * **Week pattern:** a set of days from Monday–Sunday.
   * **Month pattern:** 4 week patterns combined.
   * **Ordering months:** locks in the chosen week patterns and saves them.
4. The habit is then saved to the database via `HabitFactory`.

**Gif Example:**

![Add Habit Flow](./gifs/add_habit_flow.gif)

---

### 2. Understanding Weeks and Months

* **Week:** A sequence of 7 days, starting from any chosen day.
* **Month:** A collection of 4 consecutive week patterns.
* **Ordering Months:** After creating month patterns, the user can “order months” to define the habit schedule for multiple months. This ensures the system knows exactly when the habit repeats.

---

### 3. Habit Status Updates

The system tracks habit status automatically:

| Status            | Meaning                                                                  |
| ----------------- | ------------------------------------------------------------------------ |
| `UPCOMING`        | Habit has not started yet.                                               |
| `ONGOING`         | Habit is currently happening.                                            |
| `TO_BE_CONFIRMED` | Habit has ended but not yet marked complete.                             |
| `DONE`            | Habit marked complete by the user or system.                             |
| `MISSED`          | Habit is not done, and more than **24 hours** have passed since its end. |
| `UNKNOWN`         | Habit time or duration could not be interpreted.                         |

**Important:**

* After a habit’s scheduled end time, the system waits **24 hours** before automatically marking it as `MISSED`.
* Users can still mark a habit as `DONE` during this window.
* This logic is implemented in the **UpdateHabitController** using `DateTimeHandler`.

---

### 4. Completing Tasks

* Users can explicitly complete tasks via the **Update Habit** component.
* The system can also automatically mark `TO_BE_CONFIRMED` habits as `DONE` if applicable.
* Status updates are calculated using the start datetime and duration fields.

---

### 5. Searching and Managing Habits

The system provides multiple ways to query habits:

* By **name** or partial match
* By **status** (UPCOMING, ONGOING, DONE, etc.)
* By **content** (description or reflections)
* By **specific date or month**

Users can also **update** or **delete** habits directly via the CLI.

---

### 6. Repeat Patterns & Habit Time Repeats

**HabitTimeRepeatsView** enables flexible repeat scheduling:

* **Week Patterns:** User defines which days a habit repeats in a week.
* **Month Patterns:** User combines 4 week patterns to create a month.
* **Ordered Months:** After creation, users define the sequence of months, locking in the schedule.

This allows recurring habits to be tracked automatically and consistently.

---

### 7. Data Persistence

* The **HabitFactory** mediates between the CLI components and the **Database**.
* All habit data is stored in **SQLite**, including descriptions and reflections.
* Foreign key relationships ensure that habit content is linked to the habit entry.

---

### 8. Utility Components

* **DateTimeHandler:** Maps dates and durations to habit statuses.
* **Colors:** Improves user experience by highlighting success, error, and input prompts.
* **AutoCompleter:** Provides command completion for faster CLI interaction.

---

### 9. Example Flow (Add → Repeat → Status Update)

```
User -> AddHabitView -> AddHabitController -> HabitFactory -> Database -> HabitTimeRepeatsView

UpdateHabitController -> HabitFactory -> Database
SearchHabit -> HabitFactory -> Database
```

* Users add habits → optionally define repeat patterns → system saves habit → automatically updates statuses over time → users can search/update/delete.

---

### 10. Design Philosophy

* **Separation of Concerns:** CLI, business logic, database interaction are all separate.
* **Command-Driven:** Each action is mapped to a command loop for user-friendly CLI flow.
* **Time-Based Logic:** System tracks ongoing, upcoming, and missed habits automatically.
* **Repeatability:** Weeks and months patterns allow flexible recurring habits.
* **User Feedback:** Colors and messages clearly indicate success, errors, and guidance.

---
