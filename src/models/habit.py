"""Model representing a Habit and its core attributes.

This module defines the Habit class which encapsulates the name, start
datetime, duration, status and content for a habit. The class includes
convenience methods for manipulating the habit's datetime (e.g. moving to
the next day) and for converting the stored datetime into a human-readable
string. Equality and representation helpers are provided to make instances
easy to compare in tests.
"""

from models.status import HabitStatus
from models.content import HabitContent
from data.database_interface import DatabaseInterface
from services.handle_time import DateTimeHandler

class Habit:
    """Data model for a habit.

    Attributes:
        db (DatabaseInterface): Class-level database interface used by
            higher-level services (kept here for historical reasons).
    """
    db = DatabaseInterface()

    def __init__(self, name, start_datetime, duration, id=None) -> None:
        """Initialize a Habit instance.

        Args:
            name (str): Name of the habit.
            start_datetime: Datetime representation used by the project
                (usually a string produced by the input flow).
            duration: Duration value for the habit session (string/number).
            id: Optional external identifier for the habit.
        """
        self.__name = name
        self.__start_datetime = start_datetime
        self.__duration = duration
        self.__status = HabitStatus.UPCOMING
        self.content = HabitContent()
        self.date_time_handler = DateTimeHandler()
        self.__id = id

    def get_name(self):
        """Return the habit's name."""
        return self.__name

    def set_name(self, name):
        """Set or update the habit's name.

        Args:
            name (str): New habit name.
        """
        self.__name = name

    def get_start_datetime(self):
        """Return the stored start datetime."""
        return self.__start_datetime
    
    def stringify_datetime(self,datetime):
        """Convert an internal datetime representation to a readable string.

        The method accepts a datetime-like string, normalizes the time to
        'HH:MM' and returns a string formatted as 'YYYY-MM-DD, HH:MM'. This
        string is compatible with the project's DateTimeHandler input.
        """
        year,time = str(datetime).replace(',','').split(' ')
        time_split = time.split(':')
        
        if len(time_split) == 3:
            time = ':'.join([str(time_split[0]),str(time_split[1])])
        year,month,day= year.split('-')
        return f'{year}-{month}-{day}, {time}'
    
    def next_day(self, days=1):
        """Advance the habit's start datetime by a number of days.

        Args:
            days (int): Number of days to advance (default 1).
        """
        self.date_time_handler.set_start_datetime( self.stringify_datetime(self.__start_datetime))
        self.date_time_handler.increase_by_day(days)
        self.__start_datetime = self.date_time_handler.get_startdatetime()
    
    def weekday(self):
        """Return the weekday name of the habit's start datetime.

        Delegates to DateTimeHandler.get_weekday().
        """
        self.date_time_handler.set_start_datetime(self.stringify_datetime(self.__start_datetime))
        return self.date_time_handler.get_weekday()

    def set_start_datetime(self, start_datetime):
        """Set a new start datetime for the habit.

        Args:
            start_datetime: New start datetime value.
        """
        self.__start_datetime = start_datetime
    
    def get_duration(self):
        """Return the habit's duration."""
        return self.__duration

    def set_duration(self, duration):
        """Set or update the habit duration.

        Args:
            duration: New duration value.
        """
        self.__duration = duration

    def get_status(self):
        """Return the status value (string) of the habit."""
        return self.__status.value

    def set_status(self, status):
        """Set the habit status using HabitStatus helper.

        Args:
            status: A status string or value understood by HabitStatus.
        """
        self.__status = HabitStatus.get_status(status)

    def get_id(self):
        """Return the external identifier for this habit."""
        return self.__id
    
    def set_id(self,id):
        """Set an external identifier for this habit.

        Args:
            id: Identifier value (type depends on persistence layer).
        """
        self.__id = id

    def __repr__(self) -> str:
        """Return a compact developer-facing representation of the habit."""
        return f"Habit({self.__name},{self.__start_datetime},{self.__duration},{self.__id})"
    
    def __eq__(self, habit):
        """Value-style equality comparison with another Habit instance.

        Two habits are considered equal when name, id, content, duration,
        start datetime and status string representations are equal. This is
        used primarily in tests.
        """

        return all([
            self.__name == habit.get_name(), 
            self.__id == habit.get_id(), 
            self.content==habit.content,
            str(self.__duration)==habit.get_duration(),
            str(self.__start_datetime)==habit.get_start_datetime(),
            str(self.get_status())==habit.get_status(),
            ])

if __name__ == "__main__":
    habit = Habit('name1', 'start_datetime', 'duration',2)
