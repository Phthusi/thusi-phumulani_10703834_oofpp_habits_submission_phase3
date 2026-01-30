from services.colors import Colors
from services.handle_time import DateTimeHandler
from services.inputs import run_until_successful,command_once,prompt_input_for_commands,display_habit, unsuccessful, ManageMainLoop
# from src.services.read_json import read_json_files
from components.habit_time_repeats.view.habit_time_repeats_view import HabitTimeRepeatsView

class AddHabitView:
    """
    CLI View responsible for creating and configuring a new habit.

    This class handles user interaction for:
    - Capturing habit details (name, description, start time, duration)
    - Validating inputs
    - Optionally attaching repeat patterns
    - Displaying entered habit details
    - Saving the habit state

    Design note:
    Each user-facing method is split into:
    - *_logic()  → Pure logic, easily testable
    - Decorated wrapper → CLI input loop & command handling
    """

    def __init__(self):
        """
        Initialize AddHabitView with required services and default state.
        """
        self.datetime_handler = DateTimeHandler()
        self.habit_time_repeats_view = HabitTimeRepeatsView()
        self.color = Colors()

        self.__habit_name     = ""
        self.__reflections    = ""
        self.__start_datetime = ""
        self.__description    = None
        self.__habit_session_duration = ""

        self.LIGHTBLACK_EX    = self.color.FORE.LIGHTBLACK_EX
        self.DARK             = self.color.choose_brightness("Darken")

        self.save_called     = False
        self.pattern_is_set  = False


    # -------------------- Getters --------------------

    def get_habit_name(self):
        """Return the currently stored habit name."""
        return self.__habit_name

    def get_description(self):
        """Return the currently stored habit description."""
        return self.__description
    
    def get_reflections(self):
        return self.__reflections

    def get_start_datetime(self):
        """Return the currently stored habit start datetime."""
        return self.__start_datetime
    
    def get_habit_duration(self):
        """Return the currently stored habit session duration."""
        return self.__habit_session_duration
    

    # -------------------- State Management --------------------

    def reset(self):
        """
        Reset all stored habit fields to default state.
        Useful when restarting habit creation.
        """
        self.__habit_name     = ""
        self.__start_datetime = ""
        self.__description    = None
        self.__habit_session_duration = ""
        self.save_called     = False
        self.pattern_is_set  = False


    # -------------------- Habit Name --------------------

    def set_habit_name_logic(self, command):
        """
        Validate and store habit name.

        Parameters
        ----------
        command : str
            User input string.

        Returns
        -------
        tuple(command, message, success)
        """
        if command == "help":
            return command, (
                "Just enter the name of the habit, "
                "make sure it only has alphabets and length > 2"
            ), False

        if len(command) <= 2:
            return command, "name must have more than 2 characters", False

        if len(command) > 30:
            return command, "The habit name must have characters less than 30", False

        if command != "esc":
            self.__habit_name = command
        
        return command, "success...", True

    @run_until_successful
    @command_once
    def set_habit_name(self):
        """
        CLI wrapper for habit name input.
        Runs until valid name is entered or user exits.
        """
        command = prompt_input_for_commands("Enter habit-name: ")
        return self.set_habit_name_logic(command)


    # -------------------- Start Datetime --------------------

    def set_start_datetime_logic(self, command):
        """
        Validate and store habit start datetime.

        Parameters
        ----------
        command : str
            Datetime string in format yyyy-mm-dd, HH:MM

        Returns
        -------
        tuple(command, message, success)
        """
        result, status = self.datetime_handler.set_start_datetime(command)
        if command == "help":
            return command, (
                "Enter the date and time you want to start your habit at, e.g 2026-04-201, 15:00"
            ), False
        if status:
            self.__start_datetime = self.datetime_handler.get_startdatetime()
            return command, "success...", status
        return command, result, status

    @run_until_successful
    @command_once
    def set_start_datetime(self):
        """
        CLI wrapper for start datetime input.
        """
        command = prompt_input_for_commands(
            f"Enter the date and time you want to start at\n"
            f"{self.LIGHTBLACK_EX+f'(format: yyyy-mm-dd, HH:MM e.g {self.datetime_handler.get_today()}, {self.datetime_handler.generate_random_time()})'} ",
            [f"{self.datetime_handler.get_today()}, {self.datetime_handler.generate_random_time()}"]
        )
        return self.set_start_datetime_logic(command)


    # -------------------- Description --------------------

    def set_habit_description_logic(self, command):
        """
        Validate and store optional habit description.

        Parameters
        ----------
        command : str

        Returns
        -------
        tuple(command, message, success)
        """
        command = None if command == "" else command

        if command == "help":
            return command, "This is where you should enter the description of your habit, you can press enter if you do not want a description", False
        
        if len(str(command)) > 50:
            return command, "You have exceeded the maximum number of characters", False
        
        if command != "esc":
            self.__description = command

        return command, (
            f"Habit description successfully "
            f"{'entered' if command is not None else self.DARK+'skipped'}"
        ), True
    

    @run_until_successful
    @command_once
    def set_habit_description(self):
        """CLI wrapper for habit description input."""
        command = prompt_input_for_commands(
            "Enter habit-description: " + self.DARK + "\n press enter to skip"
        )
        return self.set_habit_description_logic(command)

    def set_habit_reflections_logic(self, command):
        """
        Validate and store optional habit description.

        Parameters
        ----------
        command : str

        Returns
        -------
        tuple(command, message, success)
        """
        command = None if command == "" else command

        if command == "help":
            return command, "This is where you should enter the reflections of your habit, you can press enter if you do not want reflections", False
                
        if command != "esc":
            self.__reflections = command

        return command, (
            f"Habit reflections successfully "
            f"{'entered' if command is not None else self.DARK+'skipped'}"
        ), True

    @run_until_successful
    @command_once
    def set_habit_reflections(self):
        """CLI wrapper for habit description input."""
        command = prompt_input_for_commands(
            "Enter habit-reflections: " + self.DARK + "\n press enter to skip"
        )
        return self.set_habit_reflections_logic(command)



    # -------------------- Session Duration --------------------

    def set_habit_session_duration_logic(self, command):
        """
        Validate and store habit session duration.

        Parameters
        ----------
        command : str
            Duration in HH:MM:SS format.

        Returns
        -------
        tuple(command, message, success)
        """
        result, status = self.datetime_handler.set_habit_session_duration(command)
        if status:
            self.__habit_session_duration = self.datetime_handler.get_duration()
        return command, result, status

    @run_until_successful
    @command_once
    def set_habit_session_duration(self):
        """CLI wrapper for session duration input."""
        command = prompt_input_for_commands(
            "Enter the duration of the habit session:\n" +
            self.DARK + self.color.choose_color('WHITE') +
            "(format: HH:MM:SS e.g 00:15:00 is 15 minutes)",
            [f'00:{self.datetime_handler.generate_random_time()}']
        )
        return self.set_habit_session_duration_logic(command)


    # -------------------- Validation --------------------

    def all_fields_exist(self):
        """
        Ensure required habit fields exist before saving.

        Returns
        -------
        tuple(command, message, success)
        """
        try:
            assert self.__habit_name, "UNSUCCESSFUL: habit name required"
            assert self.__start_datetime, "UNSUCCESSFUL: start time required"
            assert self.__habit_session_duration, "UNSUCCESSFUL: habit session duration required"
            return '', 'success', True
        except Exception as e:
            return '', f"{e}", False


    # -------------------- Repeat Pattern --------------------

    def set_pattern_logic(self, command):
        """
        Handle repeat-pattern selection.

        Returns
        -------
        bool
        """
        match command:
            case "yes":
                self.pattern_is_set = True
                self.habit_time_repeats_view.execute()
                return True
            case "no":
                return True
            case _:
                return False
            
    @run_until_successful
    def set_pattern(self):
        """CLI wrapper for repeat pattern selection."""
        command = prompt_input_for_commands(
            "Do you want to set a repeat pattern for this habit: ",
            ['yes', 'no']
        )
        return self.set_pattern_logic(command)


    # -------------------- Save --------------------

    def save_logic(self):
        """
        Validate fields, optionally set repeat pattern,
        and mark habit as saved.

        Returns
        -------
        tuple(command, message, success)
        """
        command, message, success = self.all_fields_exist()
        if not success:
            return command, message, success
        
        self.set_pattern()
        self.save_called = True
        return '', "Habit saved successfully", True

    @command_once
    def save(self):
        """CLI wrapper for saving habit."""
        return self.save_logic()


    def save_handler(self):
        success = self.save()
        if success:
            return 'done'
        return ''

    # -------------------- Display --------------------

    def display_habit_details_logic(self):
        """
        Display current habit details if all required fields exist.
        """
        command, message, success = self.all_fields_exist()
        if not success:
            return command, message, success
        
        display_habit(
            self.__habit_name,
            self.__description,
            self.__start_datetime,
            self.__habit_session_duration
        )
        return 'SKIP DISPLAY', "Displayed habit details successfully", True

    @command_once
    def display_habit_details(self):
        """CLI wrapper for displaying habit details."""
        return self.display_habit_details_logic()


    # -------------------- Execution Loop --------------------

    def execute_logic(self):
        """
        Main command router for AddHabitView CLI.
        """
        commands = {
            'set habit name': self.set_habit_name,
            'habit description': self.set_habit_description,
            'set start datetime': self.set_start_datetime,
            'set habit session duration': self.set_habit_session_duration,
            'display habit details': self.display_habit_details,
            'view filled field values': self.view_filled_field_values,
            'save habit': self.save_handler,
            'reset habit': self.reset,
        }
        ManageMainLoop().command_loop(commands,switched_to="add habit")

    # @command_once
    def execute(self):
        """Start AddHabitView CLI."""
        return self.execute_logic()


    # -------------------- Utility --------------------

    def view_filled_field_values(self):
        """
        Print currently filled habit fields for user inspection.
        """
        fields = {
            "habit_name": self.__habit_name,
            "start_datetime": self.__start_datetime,
            "description": self.__description,
            "habit_session_duration": self.__habit_session_duration,
            "save_called": self.save_called
        }

        count = 0
        for name, value in fields.items():
            if value:
                print(
                    f"{self.color.choose_color('HELP')}{name} "
                    f"{self.color.choose_color('WHITE')}: "
                    f"{self.color.color_successful(str(value))}"
                )
                count += 1

        if count == 0:
            print(self.color.color_unsuccessful("No fields have been filled yet."))

if __name__ == "__main__":
    view = AddHabitView()
    view.execute()
    # view.set_habit_session_duration()
    # view.set_habit_name()
    # print(view.get_habit_name())
    # view.set_start_datetime()
    # print(view.get_start_datetime())
    # view.set_habit_description()
    # print(view.get_description())