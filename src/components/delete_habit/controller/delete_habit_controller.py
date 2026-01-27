from src.services.habit_factory import HabitFactory, Habit
from src.components.get_habit.view.get_habit_view import GetHabitView
from src.services.inputs import command_loop


class DeleteHabitController:
    """
    Controller responsible for handling habit deletion.

    This controller allows the user to locate a habit using
    GetHabitView search tools, select a habit by ID, reconstruct
    the Habit object from stored data, and remove it from storage
    via the HabitFactory.
    """

    def __init__(self):
        """
        Initialize DeleteHabitController with required services and views.
        """
        self.habit_factory = HabitFactory()
        self.get_habit_view = GetHabitView()

    def delete(self):
        """
        Delete a habit selected by the user.

        Steps:
        1. Ask the user to choose a habit ID using GetHabitView.
        2. Validate that the habit exists in storage.
        3. Retrieve the habit record from the database.
        4. Reconstruct a Habit object from stored values.
        5. Pass the Habit object to HabitFactory for deletion.
        6. Reset selected habit ID after deletion.
        """
        self.get_habit_view.set_id_of_habit_to_modify(
            'delete',
            self.habit_factory.id_exists
        )

        if self.get_habit_view.id_of_habit_to_modify != 0:
            habit_from_db = self.habit_factory.get_habit(
                self.get_habit_view.id_of_habit_to_modify
            )

            id, _, name, start_datetime, duration, status, description, reflections = habit_from_db

            habit = Habit(name, start_datetime, duration, id)
            habit.content.set_description(description)
            habit.content.set_reflections(reflections)
            habit.set_status(status)

            self.habit_factory.delete_habit(habit)

            # Reset selection after deletion
            self.get_habit_view.id_of_habit_to_modify = 0

    def execute(self):
        """
        Launch the delete habit command loop.

        Available commands:
        - 'use get commands' → browse/search habits
        - 'delete' → delete selected habit
        """
        commands = {
            'use get commands': self.get_habit_view.get_habit,
            'delete': self.delete
        }
        command_loop(commands, switched_to="delete habit")


if __name__ == "__main__":
    x = DeleteHabitController()
    x.execute()
