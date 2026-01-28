from data.database import Database

class DatabaseInterface:
    """
    High-level interface between domain models and the database layer.

    This class acts as a facade over the low-level `Database` class,
    translating domain objects (e.g. Habit) to and from database rows.

    Responsibilities:
    - Persist and retrieve Habit-related data
    - Enforce database-level constraints (e.g. unique habit names)
    - Shield the rest of the application from SQL details

    This class does NOT handle:
    - User interaction
    - CLI output
    - Business rules such as patterns or scheduling
    """

    def __init__(self,name="habit.db") -> None:
        """
        Initialize the database interface and underlying database connection.
        """
        self.database = Database(name)

    def get_all_habits(self):
        """
        Retrieve all habits stored in the database.

        Returns:
            list: A list of database rows representing habits and their content.
        """
        return self.database.get_all_entries()

    def get_habit(self, id):
        """
        Retrieve a single habit by its unique identifier.

        Args:
            id (int): The habit ID.

        Returns:
            tuple: Habit data if found.
            tuple(): Empty tuple if the habit does not exist.
        """
        message, result = self.database.get_entry(id)
        if message == 'success':
            return result
        return ()

    def get_name_with_text(self, name):
        """
        Search for habits whose names contain the given text.

        Args:
            name (str): Partial or full habit name.

        Returns:
            list: Matching habit records.
        """
        return self.database.get_name_with_text(name)

    def add_habit(self, habit):
        """
        Persist a new Habit object to the database.

        This operation:
        1. Ensures the habit name is unique
        2. Saves the habit content
        3. Saves the habit metadata
        4. Assigns generated IDs back to the Habit object

        Args:
            habit (Habit): The habit domain object to be saved.

        Returns:
            tuple:
                ("success", Habit) on success
                ("error", message) on failure
        """
        description = habit.content.get_description()
        reflections = habit.content.get_reflections()

        # habit_names = [habit[2].lower() for habit in self.get_all_habits()]
        # if habit.get_name().lower() in habit_names:
        #     return "error", f"habit with name '{habit.get_name()}' already exists"

        status, expected_result = self.database.add_entry(
            "habit_content",
            ["description", "reflection"],
            [description, reflections],
        )
        # print(status, expected_result)
        if status == "success":
            habit.set_id(expected_result)

            status, expected_result = self.database.add_entry(
                "habit",
                ["habit_content_id", "name", "start_datetime", "duration", "status"],
                [
                    habit.get_id(),
                    habit.get_name(),
                    str(habit.get_start_datetime()),
                    str(habit.get_duration()),
                    habit.get_status(),
                ],
            )
            # print(status,expected_result,'add-habit adding time')
            if status == "success":
                return "success", habit

            # Roll back partially created data
            self.delete_habit(habit)

        return "error", expected_result

    def get_habits_by_status(self, status):
        """
        Retrieve all habits matching a given status.

        Args:
            status (str): Habit status (e.g. UPCOMING, DONE).

        Returns:
            list: Matching habit records.
        """
        return self.database.get_habits_by_status(status.upper())

    def delete_habit(self, habit, table_name="habit_content"):
        """
        Delete a habit from the database after verifying its integrity.

        The habit is reconstructed from the database and compared against
        the provided Habit object before deletion.

        Args:
            habit (Habit): The habit to delete.
            table_name (str): Table to delete from (default is habit_content).

        Returns:
            tuple:
                ("success", None) on successful deletion
                ("error", message) if deletion fails
        """
        habit_id = habit.get_id()
        habit_class_obj = type(habit)

        if habit_id is None:
            return "error", "the habit does not exist in the database"

        status, result = self.database.get_entry(habit_id)
        if status == "error":
            return status, result

        (
            habit_id,
            habit_content_id,
            name,
            start_datetime,
            duration,
            status,
            description,
            reflections,
        ) = result

        habit_obj = habit_class_obj(name, start_datetime, duration, habit_id)
        habit_obj.set_status(status)
        habit_obj.content.set_description(description)
        habit_obj.content.set_reflections(reflections)
        habit_obj.content.set_id(habit_content_id)

        if habit == habit_obj:
            return self.database.delete_entry(table_name, habit_id)

        return "error", "objects do not match!"

    def update_habit(self, table_name, id, **kwargs):
        """
        Update one or more fields of a habit record.

        Args:
            table_name (str): Database table name.
            id (int): Habit ID.
            **kwargs: Fields and values to update.
        """
        self.database.update_entry(table_name=table_name, id=id, **kwargs)

    def search_by_content(self, content):
        """
        Search habit content by text.

        Args:
            content (str): Text to search for.

        Returns:
            list: Matching habit content records.
        """
        return self.database.search_by_content(content)

    def search_by_month(self, month, year=None):
        """
        Retrieve habits scheduled for a specific month.

        Args:
            month (int): Month number.
            year (int, optional): Year (defaults to current year).

        Returns:
            tuple: Status and list of matching habits.
        """
        return self.database.search_by_month(month, year)

    def search_by_date(self, date):
        """
        Retrieve habits scheduled for a specific date.

        Args:
            date (str): Date in YYYY-MM-DD format.

        Returns:
            tuple: Status and list of matching habits.
        """
        return self.database.search_by_date(date)

if __name__=="__main__":
    a = DatabaseInterface()
    print(a.get_habits_by_status('UPCOMING'))