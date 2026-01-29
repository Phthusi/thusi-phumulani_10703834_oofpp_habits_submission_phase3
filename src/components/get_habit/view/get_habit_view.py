from services.colors import Colors
from services.inputs import (
    command_loop,
    run_until_successful,
    command_once,
    prompt_input_for_commands,
    display_habit,
    unsuccessful,
    successful
)
from components.search_habit.controller.search_habit_controller import (
    SearchHabit,
    HabitFactory
)


class GetHabitView:
    """
    Handles searching and retrieving habits through multiple search strategies.

    This view provides a command-driven interface for locating habits before
    viewing, modifying, or deleting them. It coordinates user input,
    delegates searches to controller classes, and displays formatted results.
    """

    def __init__(self):
        """
        Initializes the GetHabitView.

        Sets up color formatting, search controllers, internal state,
        and result storage for subsequent search operations.
        """
        self.color = Colors()
        self._init_colors()

        self.search_habit = SearchHabit()
        self.habit_factory = HabitFactory()

        self.search_results = ""
        self.question_repeated = False
        self.__is_result_found = False
        self.id_of_habit_to_modify = 0
        self.__method_name = "Get"

    def _init_colors(self):
        """
        Configures commonly used color and style attributes.

        Centralizes color initialization to keep __init__ clean
        and ensure consistent CLI styling.
        """
        BRIGHT = self.color.choose_brightness("BRIGHTEN")

        self.DARK = self.color.choose_brightness("Darken")
        self.UNSUCCESSFUL = BRIGHT + self.color.choose_color("UNSUCCESSFUL")
        self.SUCCESSFUL = BRIGHT + self.color.choose_color("SUCCESSFUL")
        self.INPUT = BRIGHT + self.color.choose_color("INPUT")
        self.WHITE = BRIGHT + self.color.choose_color("WHITE")
        self.BLUE = BRIGHT + self.color.choose_color("BLUE")
        self.HELP = BRIGHT + self.color.choose_color("HELP")
        self.LIGHTBLACK_EX = self.color.FORE.LIGHTBLACK_EX
        self.BACK = self.color.BACK

    def get_is_result_found(self):
        """
        Returns whether the last search produced at least one result.

        Returns:
            bool: True if a result was found, otherwise False.
        """
        return self.__is_result_found

    def set_is_result_found(self, value):
        """
        Updates the internal result-found flag.

        Args:
            value (bool): Flag indicating if search results exist.
        """
        self.__is_result_found = value

    def get_method_name(self):
        return self.__method_name
    
    def set_method_name(self,method_name):
        self.__method_name = method_name

    def _normalize_results(self):
        """
        Normalizes raw search results into a list structure.

        Ensures consistent iteration whether a single tuple or list
        of tuples is returned from controllers.

        Returns:
            list: List of result tuples.
        """
        if not self.search_results:
            return []
        if isinstance(self.search_results, tuple):
            return [tuple(self.search_results)]
        return self.search_results

    def display_results(self):
        """
        Displays summarized habit search results in formatted CLI output.

        Shows habit id, name, start datetime, duration, and status.
        If no results exist, a 'No results found' message is printed.
        """
        results = self._normalize_results()

        print(f"{'-'*107}")
        print(f"{self.HELP}RESULTS {self.WHITE}: {self.SUCCESSFUL}{len(results)}")
        print(f"{'-'*107}")

        if not results:
            print(self.UNSUCCESSFUL + "No results found!")
            print(f"{'-'*107}")
            return

        for r in results:
            print(self.BACK.CYAN + " " * 107, end="")
            print(f"""{self.WHITE}
    id             : {r[0]}
    name           : {r[2]}
    start datetime : {self.HELP + r[3] + self.WHITE}
    duration       : {self.SUCCESSFUL + r[4] + self.WHITE}
    status         : {r[5]}
""")
        print(f"{'-'*107}")

    def content_display_results(self):
        """
        Displays content-based search results.

        Shows habit id, description, and reflection fields.
        Used when searching by textual content.
        """
        results = self._normalize_results()
        if not results:
            print("No results found!")
            return

        for r in results:
            print(self.BACK.CYAN + " " * 107, end="")
            print(f"""
    id             : {r[0]}
    description    : {r[1]}
    reflection     : {r[2]}
""")

    def _simple_search(self, prompt_msg, validator, search_function, display_function):
        """
        Generic wrapper for simple search flows.

        Handles:
        - Prompting user input
        - Validating input
        - Calling search function
        - Displaying results

        Returns:
            tuple: (command, message, success)
        """
        command = prompt_input_for_commands(prompt_msg)

        if command == "esc":
            return command, "", True

        if command == "clear_screen":
            return command, "", False

        _, message, valid = validator(command)
        if isinstance(message, tuple):
            _, message = message

        if not valid:
            return command, message, False

        self.search_results = search_function(command)
        display_function()
        self.search_results = ""
        return command, "success...", True

    @run_until_successful
    @command_once
    def search_by_name(self):
        """
        Searches habits by name substring.

        Requires at least 3 characters input.
        Delegates search to SearchHabit controller.
        """
        message = "Enter characters in habit name: "
        def validator(cmd):
            if len(cmd) <= 2:
                return "", (len(cmd) <= 2, "Name must have more than 2 characters"), False
            print(cmd)
            return "", (len(cmd) >= 3, "Success..."), True

        return self._simple_search(
            message,
            validator,
            self.search_habit.search_by_name,
            self.display_results
        )

    @run_until_successful
    @command_once
    def search_by_content(self):
        """
        Searches habits by content appearing in description or reflection fields.

        Requires at least 3 characters input.
        """
        message = "Enter characters in habit content: "
        def validator(cmd):
            if len(cmd) <= 2:
                return "", (len(cmd) <= 2, "Name must have more than 2 characters"), False
            return "", (len(cmd) >= 3, "Success..."), True

        return self._simple_search(
            message,
            validator,
            self.search_habit.search_by_content,
            self.content_display_results
        )

    @run_until_successful
    @command_once
    def search_by_date(self):
        """
        Searches habits occurring on a specific date.

        Expected input format: YYYY-MM-DD.
        """
        message = "Enter date (YYYY-MM-DD): "
        command = prompt_input_for_commands(message)

        if command == "esc":
            return command, "", True

        status, results = self.search_habit.search_by_date(command)

        if status == "error":
            return command, str(results), False

        self.search_results = results
        self.display_results()
        self.search_results = ""
        return command, "success...", True

    @run_until_successful
    @command_once
    def search_by_month(self):
        """
        Searches habits by month.

        User selects a month name, which is mapped to its numeric value
        before querying the controller.
        """
        message = "Enter month: "
        months = {
            'January': 1, 'February': 2, 'March': 3,
            'April': 4, 'May': 5, 'June': 6,
            'July': 7, 'August': 8, 'September': 9,
            'October': 10, 'November': 11, 'December': 12
        }

        command = prompt_input_for_commands(message, list(months.keys()))
        if command == "esc":
            return command, "", True

        command = command.capitalize()
        if command not in months:
            return command, f"'{command}' is not a valid month", False

        month_number = months[command]
        status, results = self.search_habit.search_by_month(month_number)

        if status == "error":
            return command, results, False

        self.search_results = results
        self.display_results()
        self.search_results = ""
        return command, "success...", True

    @run_until_successful
    @command_once
    def search_by_status(self):
        """
        Searches habits by current status.

        Allowed statuses: ONGOING, UPCOMING, ACTIVE, DONE, MISSED.
        """
        message = "Enter status: "
        statuses = ["ONGOING", "UPCOMING", "ACTIVE", "DONE", "MISSED"]
        status = prompt_input_for_commands(message, statuses)

        if status == "esc":
            return status, "", True

        if status.upper() not in statuses:
            return status, "Invalid status!", False

        self.search_results = self.search_habit.search_by_status(status)
        self.display_results()
        self.search_results = ""
        return status, "successful...", True

    @run_until_successful
    @command_once
    def view_habit_information(self):
        """
        Displays full information for a single habit by ID.

        Prints all stored fields including description and reflection.
        """
        message = "Enter habit id: "
        habit_id = prompt_input_for_commands(message)

        if habit_id == "esc":
            return habit_id, "", True

        if not habit_id.isdigit():
            return habit_id, "Invalid ID. Must be numeric.", False

        result = self.habit_factory.get_habit(habit_id)

        if not result:
            return habit_id, "No results found!", True

        print(f"{'-'*107}")
        print(self.HELP + "RESULTS " + self.WHITE + ": " + self.SUCCESSFUL + "1")
        print(f"{'-'*107}")
        print(self.BACK.CYAN + " " * 107)
        print(f"""    id             : {result[1]}
    name           : {result[2]}
    start datetime : {result[3]}
    duration       : {result[4]}
    description    : {result[6]}
    reflection     : {result[7]}
    status         : {result[5]}
{self.WHITE}{'-'*107}""")

        return habit_id, "success", True

    @run_until_successful
    @command_once
    def set_id_of_habit_to_modify(self, method_name, validator_function,to_delete=False):
        """
        Prompts the user to select a habit ID for modification or deletion.

        Args:
            method_name (str): Action being performed (e.g., 'delete', 'edit').
            validator_function (callable): Function that verifies if ID exists.

        Returns:
            tuple: (command, message, success)
        """
        habit_id = prompt_input_for_commands(
            f"Enter the id of what you decided to {method_name}: "
        )

        if habit_id == "esc":
            return habit_id, "", True

        if not habit_id.isdigit():
            return habit_id, "ID must be numeric", False

        
        if not validator_function(int(habit_id)):
            return habit_id, f"ID {habit_id} not found in database", False

        self.id_of_habit_to_modify = habit_id
        id,_,title,date,duration,status,*content = self.habit_factory.get_habit(int(habit_id))
        if status!="UPCOMING":
            return habit_id, f"""Habit
name     : {title}
datetime : {date}
duration : {duration}
status   : {status} 
is not an upcoming event, you can only modify an upcoming event""", False
        return habit_id, "success...", True

    def get_habits_display(self):
        """
        Retrieves and displays all stored habits.
        """
        self.search_results = self.habit_factory.get_habits()
        self.display_results()

    def get_habit(self, method_name="delete"):
        """
        Starts the main command loop for habit retrieval operations.

        Provides menu-driven access to all search strategies.
        """
        commands = {
            "get all habits": self.get_habits_display,
            "search by habit name": self.search_by_name,
            "search by habit status": self.search_by_status,
            "search by habit content": self.search_by_content,
            "search by habit date": self.search_by_date,
            "search by habit month": self.search_by_month,
            "view habit information": self.view_habit_information
        }
        command_loop(commands, commands.keys(),switched_to="view habits")
        return True

if __name__ == "__main__":
    view = GetHabitView()
    view.get_habit("get")
