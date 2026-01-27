from datetime import datetime, timedelta
from random import choice

class DateTimeHandler:
    """
    Handles all date, time, and duration logic for habits.

    Standard formats:
        - Start datetime : YYYY-MM-DD, HH:MM
        - Duration       : HH:MM:SS

    Responsibilities:
        - Set and validate start datetime for a habit.
        - Set and retrieve habit session duration.
        - Increment habit datetime by days.
        - Map habit datetime and duration to a status (ONGOING, UPCOMING, MISSED, etc.).
        - Provide utility functions for weekdays and random time generation.
    """

    def __init__(self):
        """
        Initialize a DateTimeHandler object.

        Attributes:
            __createdOn (datetime): Timestamp when the handler was created.
            __duration (timedelta): Duration of a habit session.
            __start_datetime (datetime): Start datetime of a habit.
        """
        self.__createdOn = datetime.now()
        self.__duration = None
        self.__start_datetime = None

    def set_start_datetime(self, input_date: str):
        """
        Set the start datetime for a habit.

        Args:
            input_date (str): Date-time string in format "YYYY-MM-DD, HH:MM".

        Returns:
            tuple: (message:str, success:bool)
                - success True if the date is valid and in the future.
                - success False if invalid format or date is in the past.
        """
        try:
            input_dt = datetime.strptime(str(input_date), "%Y-%m-%d, %H:%M")

            if input_dt <= datetime.now():
                return "UNSUCCESSFUL: date has already passed", False

            self.__start_datetime = input_dt
            return "SUCCESSFUL: start date-time successfully entered", True

        except ValueError:
            return "UNSUCCESSFUL: invalid date format (YYYY-MM-DD, HH:MM)", False
        
    def get_today(self):
        """
        Get today's date.

        Returns:
            datetime.date: Current date.
        """
        now = datetime.now()
        return now.date()

    def increase_by_day(self, days=1):
        """
        Increment the start datetime by a given number of days.

        Args:
            days (int): Number of days to increment (default 1).

        Raises:
            ValueError: If start datetime is not set.
        """
        if not self.__start_datetime:
            raise ValueError("Start datetime not set")

        self.__start_datetime += timedelta(days=days)

    def set_habit_session_duration(self, my_duration: str):
        """
        Set the duration for a habit session.

        Args:
            my_duration (str): Duration string in format "HH:MM:SS".

        Returns:
            tuple: (message:str, success:bool)
                - True if the duration was parsed successfully.
                - False if the duration format is invalid.
        """
        try:
            hours, minutes, seconds = map(int, my_duration.split(":"))
            self.__duration = timedelta(
                hours=hours,
                minutes=minutes,
                seconds=seconds
            )
            return "SUCCESSFUL: duration set", True

        except Exception:
            return "UNSUCCESSFUL: invalid duration format (HH:MM:SS)", False

    def map_time_to_status(self, start_datetime: str, duration: str):
        """
        Determine the status of a habit based on its start datetime and duration.

        Args:
            start_datetime (str): Start datetime in format "YYYY-MM-DD HH:MM:SS".
            duration (str): Duration in format "HH:MM:SS".

        Returns:
            str: One of "ONGOING", "UPCOMING", "MISSED", "TO_BE_CONFIRMED", or "UNKNOWN".
        """
        try:
            start_dt = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
            hours, minutes, seconds = map(int, duration.split(":"))
            duration_td = timedelta(hours=hours, minutes=minutes, seconds=seconds)
            end_dt = start_dt + duration_td
            now = datetime.now()

            if start_dt <= now < end_dt:
                return "ONGOING"

            if start_dt > now:
                return "UPCOMING"

            if (end_dt < now) and (now - end_dt) > timedelta(days=1):
                return "MISSED"

            return "TO_BE_CONFIRMED"

        except Exception:
            return "UNKNOWN"    

    def get_created_on(self):
        """
        Get the timestamp when this handler was created.

        Returns:
            datetime: Creation timestamp.
        """
        return self.__createdOn

    def get_duration(self):
        """
        Retrieve the habit session duration as a string "HH:MM:SS".

        Returns:
            str: Duration in HH:MM:SS format.
        """
        hours, minutes, seconds = str(self.__duration).split(':')
        double_digit = lambda value: value if len(value)==2 else f'0{value}'
        return f'{double_digit(hours)}:{double_digit(minutes)}:{double_digit(seconds)}'

    def get_startdatetime(self):
        """
        Retrieve the habit's start datetime.

        Returns:
            datetime: Start datetime.
        """
        return self.__start_datetime

    def get_weekday(self):
        """
        Get the weekday of the habit's start datetime as a short string.

        Returns:
            str: One of ["mon","tue","wed","thurs","fri","sat","sun"].

        Raises:
            ValueError: If start datetime is not set.
        """
        if not self.__start_datetime:
            raise ValueError("Start datetime not set")

        weekday = ['mon', 'tue', 'wed', 'thurs', 'fri', 'sat', 'sun']
        return weekday[self.__start_datetime.weekday()]
    
    def generate_random_time(self):
        """
        Generate a random time in HH:MM format.

        Returns:
            str: Random time string.
        """
        x = lambda random_num: random_num if len(random_num)==2 else f'0{random_num}'
        random_minutes = str(choice(range(0,60)))
        random_minutes = x(random_minutes)
        random_hours   = str(choice(range(0,23)))
        random_hours = x(random_hours)
        return f'{random_hours}:{random_minutes}'
