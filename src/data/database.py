import sqlite3
from datetime import datetime

class Database:
    """
    Handles SQLite database operations for the Habit Tracker application.

    Responsibilities:
        - Create and manage database tables for habits and habit content.
        - Add, update, delete, and query habit records.
        - Provide utility methods to search habits by status, date, month, or content.
        - Ensures foreign key integrity between `habit` and `habit_content` tables.
    """

    def __init__(self, db_name="habit.db") -> None:
        """
        Initialize the database connection and create required tables if they don't exist.

        Args:
            db_name (str): Name of the SQLite database file. Defaults to "habit.db".
        """
        self.__connect = sqlite3.connect(db_name)
        self.__cursor = self.__connect.cursor()
        self.__connect.execute("PRAGMA foreign_keys = ON")
        self.__create_tables()

    def __create_table(self, sql_query):
        """
        Execute a SQL query to create a single table.

        Args:
            sql_query (str): SQL CREATE TABLE statement.

        Returns:
            tuple: ("success", None) on success, ("error", Exception) on failure.
        """
        try:
            with self.__connect:
                self.__cursor.execute(sql_query)
                return "success", None
        except Exception as e:
            return "error", e

    def __create_tables(self):
        """
        Create `habit` and `habit_content` tables if they do not exist.
        """
        self.__create_table(
            """
            CREATE TABLE IF NOT EXISTS habit_content
            (
                id INTEGER PRIMARY KEY,
                description TEXT, 
                reflection TEXT
            );
            """
        )

        self.__create_table(
            """
            CREATE TABLE IF NOT EXISTS habit
            (
                id INTEGER PRIMARY KEY, 
                habit_content_id INTEGER, 
                name TEXT,
                start_datetime TEXT, 
                duration TEXT,
                status TEXT,
                FOREIGN KEY(habit_content_id) REFERENCES habit_content(id) ON DELETE CASCADE
            );
            """
        )

    def add_entry(self, table_name, field_names, field_values):
        """
        Add a new entry to the specified table.

        Args:
            table_name (str): Table to insert into.
            field_names (list): List of field/column names.
            field_values (list): List of values corresponding to the field names.

        Returns:
            tuple: ("success", lastrowid) on success, ("error", Exception) on failure.
        """
        values = ",".join(["?" for _ in field_names])
        fields = ",".join(field_names)
        try:
            entry_obj = self.__cursor.execute(
                f"INSERT INTO {table_name} ({fields}) VALUES ({values})",
                field_values,
            )
            self.__connect.commit()
            return "success", entry_obj.lastrowid
        except Exception as e:
            return "error", e

    def delete_entry(self, table_name, id):
        """
        Delete an entry from a table by its ID.

        Args:
            table_name (str): Table from which to delete.
            id (int): ID of the entry to delete.

        Returns:
            tuple: ("success", None) on success, ("error", Exception) on failure.
        """
        try:
            self.__cursor.execute(f"DELETE FROM {table_name} WHERE id=?", (id,))
            self.__connect.commit()
            return "success", None
        except Exception as e:
            return "error", e

    def __make_double_digit(self, month):
        """
        Ensure a month is represented as a two-digit string (e.g., 1 -> '01').

        Args:
            month (int or str): Month value.

        Returns:
            tuple: ("success", "MM") on success, ("error", str) if invalid month.
        """
        if not str(month).isdigit() or not int(month) <= 12:
            return "error", "month must be a digit that is less than 12"
        return ("success", f"0{month}" if len(str(month)) == 1 else str(month))

    def update_entry(self, table_name, id, **kwargs):
        """
        Update fields of an existing entry in the specified table.

        Args:
            table_name (str): Table to update.
            id (int): ID of the entry to update.
            **kwargs: Field-value pairs to update.

        Returns:
            tuple: ("success", None) on success, ("error", Exception) on failure.
        """
        try:
            fields = [(f"{field_name}=?", value) for field_name, value in zip(kwargs.keys(), kwargs.values())]
            field_names = [i[0] for i in fields]
            field_values = [i[1] for i in fields]
            self.__cursor.execute(
                f"UPDATE {table_name} SET {','.join(field_names) if len(field_names) > 1 else field_names[0]} WHERE id=?",
                [*field_values, id]
            )
            self.__connect.commit()
            return "success", None
        except Exception as e:
            return "error", e

    def get_all_entries(self):
        """
        Retrieve all habits along with their content.

        Returns:
            list: List of tuples combining habit and habit_content fields.
        """
        habits = self.__cursor.execute("SELECT * FROM habit").fetchall()
        habit_content = self.__cursor.execute("SELECT * FROM habit_content").fetchall()
        return list(map(lambda habit, content: (*habit, *content[1:]), habits, habit_content))

    def get_habits_by_status(self, status):
        """
        Retrieve habits filtered by status.

        Args:
            status (str): Status to filter by.

        Returns:
            list: List of habits with matching status.
        """
        return self.__cursor.execute(f"SELECT * FROM habit WHERE status = '{status}'").fetchall()

    def get_name_with_text(self, name):
        """
        Search habits by name substring.

        Args:
            name (str): Substring to search for in habit names.

        Returns:
            list: List of matching habits.
        """
        return self.__cursor.execute(f"SELECT * FROM habit WHERE name LIKE '%{name}%'").fetchall()

    def get_entry(self, id):
        """
        Retrieve a habit entry along with its content by ID.

        Args:
            id (int): ID of the habit to retrieve.

        Returns:
            tuple: ("success", habit_tuple) or ("error", str/Exception)
        """
        if id is None:
            return "error", "the habit does not exist in the database"
        try:
            habit = self.__cursor.execute(f"SELECT * FROM habit WHERE id={id}").fetchone()
            if habit is None:
                return "error", f"the habit with id={id} does not exist in the database"
            habit_content = self.__cursor.execute(f"SELECT * FROM habit_content WHERE id={id}").fetchone()
            return "success", (*habit, *habit_content[1:])
        except Exception as e:
            return "error", e

    def search_by_month(self, month, year: int = None):
        """
        Search habits by month (and optionally year).

        Args:
            month (int): Month to search for.
            year (int, optional): Year to search for. Defaults to current year.

        Returns:
            tuple: ("success", list_of_habits) or ("error", str)
        """
        if not year:
            year = datetime.now().year
        message, result = self.__make_double_digit(month)
        if message == "error":
            return message, result
        return "success", self.__cursor.execute(f"SELECT * FROM habit WHERE start_datetime LIKE '{year}-{result}-%'").fetchall()

    def search_by_date(self, input_date):
        """
        Search habits by exact date.

        Args:
            input_date (str): Date string in "YYYY-MM-DD" format.

        Returns:
            tuple: ("success", list_of_habits) or ("error", Exception)
        """
        try:
            datetime.strptime(input_date, "%Y-%m-%d")
        except Exception as e:
            return "error", e
        
        result = self.__cursor.execute(f"SELECT * FROM habit WHERE start_datetime LIKE '{input_date}%'").fetchall()
        return "success", result

    def search_by_content(self, content_field):
        """
        Search habit content by description or reflection text.

        Args:
            content_field (str): Text to search for in habit descriptions or reflections.

        Returns:
            list: List of matching habit_content entries.
        """
        return self.__cursor.execute(
            f"SELECT * FROM habit_content WHERE description LIKE '%{content_field}%' OR reflection LIKE '%{content_field}%'"
        ).fetchall()

    def close(self):
        """
        Close the SQLite database connection and cursor.
        """
        try:
            if hasattr(self, "__cursor") and self.__cursor:
                self.__cursor.close()
        except Exception:
            pass
        try:
            if hasattr(self, "__connect") and self.__connect:
                self.__connect.close()
        except Exception:
            pass


if __name__ == "__main__":
    a = Database()
    a.update_entry(table_name='habit', name='soweto2', status='xyz', id=3)
