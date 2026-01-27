"""Habit status enumeration and helpers.

This module defines the HabitStatus enum used across the project to represent
the lifecycle state of a habit (e.g. UPCOMING, ONGOING, DONE). It also
provides a small helper to convert a status-like string into the corresponding
enum member.
"""

import enum 

class HabitStatus(enum.Enum):
    """Enumeration of valid habit lifecycle statuses.

    Members:
        ONGOING: Habit currently in progress.
        UPCOMING: Habit scheduled for the future.
        ACTIVE: Habit marked as active.
        DONE: Habit completed.
        DEAD: Habit terminated or cancelled.
        MISSED: Habit that has been missed.
    """

    ONGOING = "ONGOING"
    UPCOMING = "UPCOMING"
    ACTIVE = "ACTIVE"
    DONE = "DONE"
    DEAD = "DEAD"
    MISSED = "MISSED"

    @classmethod
    def get_status(cls, status):
        """Return the HabitStatus enum member matching the given string.

        Args:
            status (str): A string representing the desired status. Matching is
                performed case-insensitively.

        Returns:
            HabitStatus|None: The matching enum member, or None if no match is
                found.
        """

        match status.upper():
            case "ONGOING":
                return cls.ONGOING
            case "UPCOMING":
                return cls.UPCOMING
            case "ACTIVE":
                return cls.ACTIVE
            case "MISSED":
                return cls.MISSED
            case "DONE":
                return cls.DONE