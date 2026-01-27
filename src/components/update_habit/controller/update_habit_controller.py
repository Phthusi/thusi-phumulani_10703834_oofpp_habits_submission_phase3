from src.services.habit_factory import HabitFactory
from src.components.get_habit.view.get_habit_view import GetHabitView
from src.components.update_habit.view.update_habit_view import UpdateHabitView
from src.services.handle_time import DateTimeHandler
from src.services.inputs import command_loop
from src.components.search_habit.controller.search_habit_controller import SearchHabit


class UpdateHabitController:
    """
    Controller for updating and managing habits.

    Responsibilities:
        - Update habit details such as name, description, or schedule.
        - View habits.
        - Complete tasks that are marked as 'TO_BE_CONFIRMED'.
        - Update statuses of upcoming habits based on current datetime.
        - Acts as a bridge between views, habit factory, and user input commands.
    """

    def __init__(self):
        """
        Initialize UpdateHabitController with required services and views.
        """
        self.habit_factory  = HabitFactory()
        self.get_habit_view = GetHabitView()
        self.update_habit_view = UpdateHabitView() 
        self.datetime_handler   = DateTimeHandler()

    def complete_tasks(self):
        """
        Mark all habits with status 'TO_BE_CONFIRMED' as 'DONE'.
        """
        search_habit = SearchHabit()
        habits = search_habit.search_by_status('TO_BE_CONFIRMED')
        for habit in habits:
            id, _, name, start_datetime, duration, status = habit
            self.habit_factory.update_habit(table_name="habit", id=id, status="DONE")

    def update_statuses(self):
        """
        Update the status of all habits currently marked as 'UPCOMING'.

        Status is determined based on the current datetime and the habit's
        start datetime and duration. Updates status in the database if it
        has changed from 'UPCOMING' or is no longer unknown.
        """
        habits_to_update = [
            *self.habit_factory.get_habits_by_status("UPCOMING"),
            *self.habit_factory.get_habits_by_status("TO_BE_CONFIRMED"),
            *self.habit_factory.get_habits_by_status("ONGOING")
            ]
        for habit_to_update in habits_to_update:
            id, _, name, start_datetime, duration, status = habit_to_update
            status = self.datetime_handler.map_time_to_status(start_datetime, duration)
            if status != "UPCOMING":
                self.habit_factory.update_habit(table_name="habit", id=id, status=status)
    
    def view_habit(self):
        """
        Display habit(s) to the user using the GetHabitView interface.
        """
        self.get_habit_view.get_habit('update')

    def update_habit(self):
        """
        Update a specific habit based on user input.

        Process:
            1. Prompt user to select a habit to update.
            2. Set table name and fields to update using UpdateHabitView.
            3. Apply updates to the habit in the database.
        """
        self.update_statuses()
        self.get_habit_view.set_id_of_habit_to_modify('update', self.habit_factory.id_exists)
        if self.get_habit_view.id_of_habit_to_modify != 0:
            self.update_habit_view.set_table_name()
            self.update_habit_view.set_table_fields()
            if self.update_habit_view.update:
                table_name = self.update_habit_view.table_name
                id = self.get_habit_view.id_of_habit_to_modify 
                fields = self.update_habit_view.fields_to_update
                self.habit_factory.update_habit(table_name, id, **fields)

    def execute(self):
        """
        Run the command loop for habit updating.

        Available commands:
            - 'view habit(s)'      : Display habits.
            - 'update habit'       : Update selected habit.
            - 'complete task(s)'   : Complete all tasks marked 'TO_BE_CONFIRMED'.
        """
        commands = {
            'view habit(s)': self.view_habit,
            'update habit': self.update_habit,
            'complete task(s)': self.complete_tasks
        }
        command_loop(commands, switched_to="update habit")


if __name__ == "__main__":
    x = UpdateHabitController()
    x.execute()
