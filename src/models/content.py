"""Model representing the textual content of a habit.

This module defines the HabitContent class which encapsulates a habit's
description and reflections. The class provides simple getters and setters
and a value-style equality implementation that compares the visible
description and reflections.
"""


class HabitContent:
    """Container for habit description and reflections.

    The class intentionally keeps attributes private and exposes simple
    accessor methods. If a value has not been set, the getters return a
    human-friendly placeholder string.
    """
    def __init__(self, description="", id=None) -> None:
        """Create a HabitContent instance.

        Args:
            description (str): Initial description text. Defaults to empty
                string which is interpreted as 'nothing written yet' by the
                getter.
            id: Optional identifier assigned externally (database id, etc.).
        """
        self.__description = description
        self.__reflections = ""
        self._id = id

    def get_description(self):
        """Return the description or a placeholder when empty.

        Returns:
            str: The description text, or 'nothing written yet' when empty.
        """
        return self.__description if self.__description!="" else "nothing written yet"

    def set_description(self, description):
        """Set or replace the description text.

        Args:
            description (str): New description to store.
        """
        self.__description = description

    def get_reflections(self):
        """Return the reflections text or a placeholder when empty.

        Returns:
            str: The reflections text, or 'nothing written yet' when empty.
        """
        return self.__reflections if self.__reflections!="" else "nothing written yet"

    def set_reflections(self, reflections):
        """Set or replace the reflections text.

        Args:
            reflections (str): New reflections text to store.
        """
        self.__reflections = reflections

    def set_id(self, id):
        """Set an external identifier for this content instance.

        Args:
            id: Identifier value (type depends on persistence layer).
        """
        self._id = id

    def get_id(self):
        """Return the externally assigned identifier.

        Returns:
            The id previously set or None if not assigned.
        """
        return self._id
    
    def __eq__(self, value):
        """Compare two HabitContent instances by visible content.

        Two instances are considered equal when both their description and
        reflections (as returned by the getters) are equal. The id is not
        considered for equality.

        Args:
            value (HabitContent): Other instance to compare.

        Returns:
            bool: True if descriptions and reflections match, False otherwise.
        """
        return all(
            [
                self.get_description()==value.get_description(),
                self.get_reflections()==value.get_reflections(),
            ]
        )