"""View for creating and managing habit repeat patterns.

This module provides the HabitTimeRepeatsView class which is responsible for
interacting with the user to create, edit, view and order weekly and monthly
repeat patterns for habits. It relies on the project's input utilities for
command handling and on a Colors helper for terminal coloring.

The view stores week patterns, named collections of week patterns and named
monthly patterns (which are composed of four weekly patterns). Methods are
decorated with project-specific decorators that control command flow and
retries.

Typical usage:
    view = HabitTimeRepeatsView()
    view.execute()

This file only contains presentation and interaction logic; it does not
perform database operations.
"""

from src.services.colors import Colors
from src.services.inputs import command_loop,run_until_successful,command_once,prompt_input_for_commands,display_habit, unsuccessful


class HabitTimeRepeatsView:
    """Interactive view for creating and managing time repeat patterns.

    Attributes:
        color (Colors): Helper for terminal color codes.
        week_pattern (list[str]): Current working week pattern (ordered weekdays).
        month_pattern (dict): Named monthly patterns mapping to lists of weeks.
            Example: {'month1': [{'week1': ['mon','tue']}, ...], ...}
        command (str): Last command input (used by some handlers).
        field_to_edit (str): Field selected for editing.
        month_pattern_name (str): Working name for a month pattern.
        use_auto_go_back (bool): Flag used by some flows to auto-return.
        week_pattern_collection (dict): Saved named week patterns.
        ordered_monthly_patterns (list): List of month patterns in user order.

    The class methods use the project's input decorators to manage prompting
    and validation loops. This class contains no persistence logic; it only
    collects and formats patterns in memory.
    """
    def __init__(self):
        self.color             = Colors()
        self.week_pattern      = []
        self.month_pattern     = {} #{'month1':[{'xyz':['mon','tue','fri']}],'month2':[],'month3':[{'pop':['tue','fri','sat']}]}
        self.command           = ""
        self.field_to_edit     = ""
        self.month_pattern_name = ""
        self.use_auto_go_back   = False
        self.week_pattern_collection = {}
        self.ordered_monthly_patterns = []

    def set_field_logic(self,field_to_update,month_pattern_to_edit):
        """Handle updating a field for a named week pattern.

        Args:
            field_to_update (str): The field to update; expected values are
                'title' or 'body'. 'body' refers to the actual week days list.
            month_pattern_to_edit (str): The existing name of the pattern to
                be edited (used when renaming or replacing body content).

        Returns:
            tuple: (value, message, success) where `value` is the new input or
                a sentinel, `message` is an informational or error message,
                and `success` is a boolean indicating whether the change
                should be accepted by the decorator handler.
        """
        if field_to_update=="body":
            self.set_week_pattern(False)
            self.week_pattern_collection.update({month_pattern_to_edit:self.week_pattern})
            return '','',True

        chosen_field = prompt_input_for_commands(f"Enter the new {field_to_update}")
        if len(chosen_field) < 3:
            return chosen_field, "name list must have at least 3 characters: ", False
        
        if len(self.week_pattern_collection)>0 and chosen_field in self.week_pattern_collection.keys():
            return chosen_field, "name already used, use another one...", False

        if field_to_update=="title":
            self.week_pattern_collection.update({chosen_field:self.week_pattern_collection.get(month_pattern_to_edit)})
            self.week_pattern_collection.pop(month_pattern_to_edit) 
            return chosen_field, "success",True   

    @run_until_successful
    @command_once
    def set_field(self,field_to_update,month_pattern_to_edit):
        """Wrapper that runs `set_field_logic` with retry/command decorators.

        The decorators handle prompting until a valid value is entered and
        ensure the command is executed once per user selection.
        """
        return self.set_field_logic(field_to_update,month_pattern_to_edit)    


    def set_pattern_name_logic(self):
        """Prompt the user for a name and save the current week pattern.

        Returns the same (value, message, success) tuple used across the
        view methods so the decorated wrappers can manage retries and
        messaging.
        """
        command = prompt_input_for_commands("What do you want to name this pattern: ")
        if len(command) < 3:
            return command, "name list must have at least 3 characters: ",False
        
        if len(self.week_pattern_collection)>0 and command in self.week_pattern_collection.keys():
            return command, "name already used, use another one...",False

        if command!="esc":
            self.week_pattern_collection.update({command:self.week_pattern})
        return command, "success",True

    @run_until_successful
    @command_once
    def set_pattern_name(self):
        """Wrapper for `set_pattern_name_logic` that applies decorators.

        Returns:
            tuple: (name, message, success)
        """
        return self.set_pattern_name_logic()

    def set_week_pattern_logic(self,get_name=True):
        """Prompt the user to create a week pattern from weekday tokens.

        Args:
            get_name (bool): If True, prompt the user to name the created
                week pattern after successful selection.

        Returns:
            tuple: (set_of_days_or_command, message, success)
        """
        week_days = ["mon","tues","wed","thurs","fri","sat","sun"]
        command = prompt_input_for_commands(f"Enter the pattern of a week for the habit: e.g wed thurs fri\n💡{self.color.choose_brightness('DARKEN')+self.color.choose_color('WHITE')} Note that selecting an option doesn't include pressing enter, just press space afer highlighting the option",[*week_days,"everyday"])
        
        if command == 'esc':
            return "SKIP DISPLAY", "",True
        
        if command == 'clear_screen':
            return command, "",False
        
        command = set(command.split(" "))        
        command = {day.strip() for day in command if day!=''}
        if 'everyday' in command:
            command= {*week_days}
            command= {day.strip() for day in week_days}
        
        if not all(map(lambda element:element in week_days,command)):
            return command, "make sure that all of the inputs are week days",False
        
        priority = {
            week_day:priority_num for week_day,priority_num in zip(week_days,range(1,8))
        }
        self.week_pattern = list(sorted(command, key= lambda day:priority.get(day)))

        if get_name:
            self.set_pattern_name()
        return command, "success",True

    @run_until_successful
    @command_once
    def set_week_pattern(self,get_name=True):
        """Decorator-wrapped entry point to set a week pattern.

        Delegates to `set_week_pattern_logic` so the same validation flow can
        be reused when called directly from other methods.
        """
        return self.set_week_pattern_logic(get_name)

    def view_week_patterns(self):
        """Print all saved week patterns to the console.

        This method is strictly presentational and will print a message when
        no patterns are available.
        """
        if len(self.week_pattern_collection)==0:
            print(self.color.choose_color('WHITE')+"no results")
            return
        for week_pattern in self.week_pattern_collection.keys():
            print(f"""{self.color.BACK.CYAN}                                                                                                           """)
            print(f"{self.color.choose_color('WHITE')}{'-'*107}\n\t{self.color.choose_color('SUCCESSFUL')}week pattern {self.color.choose_color('HELP')+'\''+week_pattern}'{self.color.choose_color('SUCCESSFUL')} has the following day pattern:{self.color.choose_color('WHITE')}\n{'-'*107}\n\t- {self.color.choose_color('HELP')}{"\n\t- ".join(self.week_pattern_collection.get(week_pattern))}\n{self.color.choose_color('WHITE')}{'-'*107}")

    def delete_week_pattern_logic(self):
        """Delete a named week pattern after prompting the user.

        Returns a tuple (value, message, success) consistent with other
        logic methods so decorators can control retry behavior.
        """
        command = ""
        try:
            assert len(self.week_pattern_collection.keys()) > 0
        except Exception:
            return command,"First create a week pattern",False
        
        week_pattern_to_delete = prompt_input_for_commands("Enter the name of the week pattern: ",self.week_pattern_collection.keys())
        
        if week_pattern_to_delete == "esc":
            return week_pattern_to_delete,"", True
        
        if week_pattern_to_delete == "clear_screen":
            return week_pattern_to_delete,"", True
        
        if week_pattern_to_delete not in self.week_pattern_collection.keys():
            return command, f"{week_pattern_to_delete} is not found in saved week pattern",False
        
        elif week_pattern_to_delete in self.week_pattern_collection.keys():
            self.week_pattern_collection.pop(week_pattern_to_delete)
            return command,f"successfully deleted {week_pattern_to_delete}",True

    @run_until_successful
    @command_once
    def delete_week_pattern(self):
        """Decorator-wrapped deletion entry point.

        Returns:
            tuple: (value, message, success)
        """
        return self.delete_week_pattern_logic()

    def set_month_pattern_name_logi(self):
        """Prompt for and validate a name for the month pattern being created.

        Note: the function name contains a minor typo (`logi`) to preserve the
        original public API of the project.

        Returns:
            tuple: (name_or_command, message, success)
        """
        command = prompt_input_for_commands("What do you want to name this pattern: ")

        if command=="clear_screen":
            return command,"",False

        if len(command) < 3:
            return command,"name list must have at least 3 characters: ",False

        if command in self.month_pattern.keys():
            return command,"name already used, use another one...",False

        if command!="esc":
            self.month_pattern_name = command
        return command,'success...',True

    @run_until_successful
    @command_once
    def set_month_pattern_name(self):
        """Wrapper around `set_month_pattern_name_logi`.

        Returns:
            tuple: (name, message, success)
        """
        return self.set_month_pattern_name_logi()
    
    def create_month_pattern_logic(self):
        """Create a named monthly pattern from four saved week patterns.

        Prompts the user to enter four week pattern names (or 'skip' for an
        empty week). The chosen pattern is stored in `self.month_pattern`
        under a user-provided name.

        Returns:
            tuple: (value, message, success)
        """
        try:
            assert len(self.week_pattern_collection.keys()) > 0
        except Exception:
            return month_pattern,"First create a week pattern",True

        month_pattern = prompt_input_for_commands(f"Enter the pattern of a month from created week patterns : e.g week1 week2 week3 week4\n{self.color.choose_color('WHITE')+self.color.choose_color('DARK')}💡 press space to get the months you have saved. Use the word skip for an empty week",[*self.week_pattern_collection.keys(),'skip','esc'])

        if month_pattern == 'clear_screen':
            return month_pattern,"",False
        
        if month_pattern == 'esc':
            return month_pattern,"",True

        month_pattern = month_pattern.split(' ')
        if not all(map(lambda element:element in [*self.week_pattern_collection.keys(),'skip'],month_pattern)):
            return month_pattern,"make sure that all of the inputs are saved week patterns",False

        if len(month_pattern) !=4:
            return month_pattern,"A month must have only four week patterns",False

        self.set_month_pattern_name()
        # if self.month_pattern_name=="":
        self.month_pattern.update({self.month_pattern_name:[
            {i:self.week_pattern_collection.get(i,None)} for i in month_pattern
        ]})
        return month_pattern,"success...",True
    
    @run_until_successful
    @command_once
    def create_month_pattern(self):
        """Decorator-wrapped entry to create a month pattern.

        Returns the standard (value, message, success) tuple.
        """
        return self.create_month_pattern_logic()

    @command_once
    def display_month_pattern(self):
        """Print saved month patterns to the console.

        Validates that week and month patterns exist and formats the saved
        structure for display. Returns a tuple that matches other logic
        functions so decorators can use the response consistently.
        """
        try:
            assert len(self.week_pattern_collection.keys()) > 0,"First create a week pattern"
            assert len(self.month_pattern.keys()) > 0,"First create a month pattern"
        except Exception as e:
            return '',f"{e}",False
        
        for i in self.month_pattern.keys():
            print(f"""{self.color.BACK.CYAN}                                                                                                           """)
            print(f'''{'-'*107}\n  pattern name: {i} \n{'-'*107}''')
            for j in self.month_pattern.get(i):
                print(f'''  week pattern name : {list(j.keys())[0]}
  week pattern      : {j.get(list(j.keys())[0]) if j.get(list(j.keys())[0]) is None else " ".join(j.get(list(j.keys())[0]))}
    ''')
        return 'SKIP DISPLAY',"success...",True

    def set_field_to_edit_logic(self,month_pattern_to_edit):
            """Allow the user to select which field of a week pattern to edit.

            Args:
                month_pattern_to_edit (str): The name of the week pattern to
                    modify.

            Returns:
                tuple: (field, message, success)
            """
            options = ["title","body"]
            field_to_update = prompt_input_for_commands(f"Enter the field name you want to update: \n{self.color.choose_color('WHITE')+self.color.choose_brightness('DARK')}Press space to see the options",[*options,"esc"])
            
            if field_to_update not in options:
                return field_to_update,f'You can only choose one the given options, {field_to_update} is not in the options',False

            if 'esc'!=field_to_update:
                self.set_field(field_to_update,month_pattern_to_edit)
            return field_to_update,"success...",True

    @run_until_successful
    @command_once
    def set_field_to_edit(self,month_pattern_to_edit):
        """Decorator-wrapped entry for selecting a field to edit.

        Returns the (field, message, success) tuple from the logic method.
        """
        return self.set_field_to_edit_logic(month_pattern_to_edit)

    def edit_week_pattern_logic(self):
        """Edit an existing named week pattern by allowing field updates.

        Prompts for which pattern to edit and then delegates to the field
        editing flow.

        Returns:
            tuple: (value, message, success)
        """
        try:
            assert len(self.week_pattern_collection.keys()) > 0
        except Exception:
            return '',f"First create a week pattern:Unsuccessful",True

        month_pattern_to_edit = prompt_input_for_commands("Enter the name of the month pattern you want to edit: ",[
        *self.week_pattern_collection.keys()])

        if month_pattern_to_edit == 'esc':
            return month_pattern_to_edit,"SKIP DISPLAY",False
        
        if month_pattern_to_edit not in self.week_pattern_collection.keys():
            return month_pattern_to_edit,"This week pattern does not exist",False

        if 'esc'!=month_pattern_to_edit:
            self.set_field_to_edit(month_pattern_to_edit)
        return month_pattern_to_edit,"success...",True

    @run_until_successful
    @command_once
    def edit_week_pattern(self):
        """Decorator-wrapped entry point for week pattern editing.

        Returns:
            tuple: (value, message, success)
        """
        return self.edit_week_pattern_logic()

    def order_month_patterns_logic(self):
        """Prompt the user to provide an ordering for saved month patterns.

        The user enters a space-separated list of month pattern names which
        will be appended to `self.ordered_monthly_patterns` in the provided
        order. Validation ensures entries exist in `self.month_pattern`.

        Returns:
            tuple: (value, message, success)
        """
        try:
            assert len(self.week_pattern_collection.keys()) > 0,"First create a week pattern"
            assert len(self.month_pattern.keys()) > 0,"First create a month pattern"
        except Exception as e:
            return '',f"{e}:Unsuccessful",False
        
        monthly_order = prompt_input_for_commands("Enter the order you want your month patterns to be arranged in: e.g month1 month2 month3",[
            *self.month_pattern.keys()
        ])
        monthly_ordered_pattern = [i.strip() for i in monthly_order.split(' ')]
        
        if not all(map(lambda element:element in [*self.month_pattern.keys(),'skip'],monthly_ordered_pattern)):
            return '',"make sure that all of the inputs are saved month patterns",False
        
        for i in monthly_ordered_pattern:
            self.ordered_monthly_patterns.append(self.month_pattern.get(i))
        
        # print(self.ordered_monthly_patterns)
        return '',"success...",True

    def order_month_patterns(self):
        """Public entry to order month patterns (direct call, no decorators).

        Returns:
            tuple: (value, message, success)
        """
        return self.order_month_patterns_logic()

    def order_month_patterns_handler(self):
        """Run the ordering flow and handle retry/error messaging.

        Calls `order_month_patterns` and, if unsuccessful, prints an error
        via `unsuccessful` and returns an empty string. On success returns
        the string 'done'.
        """
        success = False
        while not success:
            command,message,success = self.order_month_patterns()
            if success:
                return 'done'
            unsuccessful(message)
            return ''

    def execute(self):
        """Start the interactive command loop for the habit time repeats view.

        Maps user-friendly command strings to internal handler methods and
        delegates to `command_loop` which manages user I/O and navigation.
        """
        commands = {
            "create week pattern": self.set_week_pattern,
            "view week patterns": self.view_week_patterns,
            "delete week pattern": self.delete_week_pattern,
            "create month pattern": self.create_month_pattern,
            "edit week pattern": self.edit_week_pattern,
            "view month pattern": self.display_month_pattern,
            "order month patterns": self.order_month_patterns_handler
        }
        command_loop(commands,switched_to="habit time repeat")     

if __name__=="__main__":
    x = HabitTimeRepeatsView()
    x.execute()