from services.habit_factory import HabitFactory, Habit

class SearchHabit:
    """
    Controller for searching habits in the system.

    Responsibilities:
        - Search habits by various criteria including name, status, content, date, or month.
        - Acts as a layer between the habit database and user-facing commands.
    """

    def __init__(self):
        """
        Initialize the SearchHabit controller with a HabitFactory instance.
        """
        self.habit_factory = HabitFactory()

    def search_by_name(self, name):
        """
        Search for a habit by its exact name.

        Parameters:
            name (str): The name of the habit to search for.

        Returns:
            tuple or list:
                - If a habit with the exact name exists, returns the habit tuple.
                - If no exact match, returns search results containing the name text.
        """
        for habit in self.habit_factory.get_habits():
            if habit[2] == name:
                return habit
        return self.habit_factory.get_name_with_text(name)

    def search_by_status(self, status):
        """
        Search for all habits with a specific status.

        Parameters:
            status (str): Status of the habits to search (e.g., 'UPCOMING', 'DONE', 'TO_BE_CONFIRMED').

        Returns:
            list: List of habit tuples that match the given status.
        """
        return self.habit_factory.get_habits_by_status(status)

    def search_by_content(self, content):
        """
        Search habits by their content (description or reflections).

        Parameters:
            content (str): Text to search within habit content.

        Returns:
            list: List of habits containing the search content.
        """
        return self.habit_factory.db.search_by_content(content)

    def search_by_date(self, date):
        """
        Search habits by a specific date.

        Parameters:
            date (str): Date string in the format recognized by the database (e.g., 'YYYY-MM-DD').

        Returns:
            list: List of habits scheduled for the specified date.
        """
        return self.habit_factory.db.search_by_date(date)

    def search_by_month(self, month, year=None):
        """
        Search habits by month and optionally by year.

        Parameters:
            month (int): Month number (1-12) to search.
            year (int, optional): Year number to filter habits. Defaults to None.

        Returns:
            list: List of habits scheduled within the specified month (and year if provided).
        """
        return self.habit_factory.db.search_by_month(month, year)


if __name__ == '__main__':
    a = SearchHabit()
    print(a.search_by_status('UPCOMING'))
