from data.database_interface import DatabaseInterface
from models.habit import Habit

class HabitFactory:
    """
    Factory class to manage Habit objects and their persistence in the database.

    Responsibilities:
        - Add, update, delete, and retrieve Habit objects.
        - Interface with the underlying DatabaseInterface.
        - Provide convenience methods for searching and checking IDs.
    """

    def __init__(self):
        """
        Initialize the HabitFactory with a DatabaseInterface instance.
        """
        self.db = DatabaseInterface()

    def add_habit(self, habit: Habit):
        """
        Add a new habit to the database, checking for clashes.

        Args:
            habit (Habit): Habit object to be added.

        Returns:
            tuple: Result of the add operation, typically ("success", habit_id) or ("error", exception).
        """
        return self.db.add_habit(habit)
    
    def id_exists(self, id):
        """
        Check if a habit with a given ID exists in the database.

        Args:
            id (int): Habit ID to check.

        Returns:
            bool: True if the ID exists, False otherwise.
        """
        return id in [i[0] for i in self.db.get_all_habits()]
    
    def update_habit(self, table_name, id, **kwargs):
        """
        Update fields of a habit in the database.

        Args:
            table_name (str): Name of the table ("habit" or "habit_content").
            id (int): ID of the habit to update.
            **kwargs: Key-value pairs of fields to update.

        Returns:
            tuple: Result of the update operation, typically ("success", None) or ("error", exception).
        """
        return self.db.update_habit(table_name, id, **kwargs)
    
    def delete_habit(self, habit: Habit):
        """
        Delete a habit from the database.

        Args:
            habit (Habit): Habit object to delete.

        Returns:
            tuple: Result of the delete operation, typically ("success", None) or ("error", exception).
        """
        return self.db.delete_habit(habit)
    
    def get_habits(self):
        """
        Retrieve all habits from the database.

        Returns:
            list: List of all habits, each as a tuple of habit fields.
        """
        return self.db.get_all_habits()
    
    def get_habit(self, id):
        """
        Retrieve a single habit by its ID.

        Args:
            id (int): Habit ID to retrieve.

        Returns:
            tuple: Habit record, or ("error", message) if not found.
        """
        return self.db.get_habit(id)
    
    def get_habits_by_status(self, status):
        """
        Retrieve all habits filtered by status.

        Args:
            status (str): Status to filter by (e.g., "UPCOMING", "DONE").

        Returns:
            list: List of habit tuples matching the status.
        """
        return self.db.get_habits_by_status(status)
    
    def get_name_with_text(self, name):
        """
        Retrieve all habits whose names contain the given text.

        Args:
            name (str): Substring to search for in habit names.

        Returns:
            list: List of habit tuples that match the search.
        """
        return self.db.get_name_with_text(name)
