from components.add_habit.view.add_habit_view import AddHabitView
from services.habit_factory import HabitFactory, Habit
from services.handle_time import DateTimeHandler


class AddHabitController:
    """
    Controller responsible for coordinating the habit creation workflow.

    This controller connects the AddHabitView (user input layer)
    with the HabitFactory (data persistence layer). It gathers user input,
    constructs Habit objects, and stores them in the database.
    
    If a repetition pattern is defined, it also generates future habit
    instances according to weekly and monthly pattern rules.
    """

    def __init__(self):
        """
        Initialize AddHabitController with its required services and views.
        """
        self.command_name = "create-habit"
        self.add_habit_view = AddHabitView()
        self.habit_factory = HabitFactory()

    def execute(self):
        """
        Execute the habit creation process.

        Steps:
        1. Launch the AddHabitView to collect user input.
        2. If the user confirms saving:
           - Build a Habit object from collected input.
           - Store the base habit in the database.
        3. If repetition patterns were defined:
           - Generate repeated habit instances according to
             ordered monthly and weekly patterns.
           - Store generated habits in the database.
        """
        print('here')
        self.add_habit_view.execute()
        habit = ''

        # Create and save the base habit
        habit_name = self.add_habit_view.get_habit_name()
        start_datetime = self.add_habit_view.get_start_datetime()
        duration = self.add_habit_view.get_habit_duration()
        description = self.add_habit_view.get_description()
        description = "" if not description else description

        habit = Habit(habit_name, start_datetime, duration)
        habit.content.set_description(description)

        # self.habit_factory.add_habit(habit)

        # Generate repeated habits if patterns were defined
        if self.add_habit_view.save_called:
            for monthly_pattern in self.add_habit_view.habit_time_repeats_view.ordered_monthly_patterns:
                for week_entry in monthly_pattern:
                    week_pattern = list(week_entry.values())[0]
                    print("week begins--------------",week_pattern,habit.weekday())
                    # Iterate through a 7-day window per week pattern
                    for _ in range(7):
                        # Skip empty weeks
                        if week_pattern is None:
                            habit.next_day(7)
                            break

                        print(habit.weekday(),week_pattern,habit.weekday() in week_pattern)
                        # Save habit only if weekday matches the pattern
                        if habit.weekday() in week_pattern:
                            self.habit_factory.add_habit(habit)
                    
                        habit.next_day()
                    print('end week')


if __name__ == '__main__':
    a = AddHabitController()
    a.execute()
