"""View component for updating existing habits.

This module exposes the UpdateHabitView class which provides interactive
flows for selecting a habit to update and modifying its fields such as name,
start datetime, duration, description and reflections. The view delegates
input handling to the project's input utilities and reuses the
AddHabitView for common input flows (e.g. entering names, datetimes,
durations and descriptions).

All methods return or are compatible with the project's convention of
returning tuples in the form (value, message, success) when they participate
in the decorated command flows.
"""

from services.colors import Colors
from components.add_habit.view.add_habit_view import AddHabitView
from services.inputs import (
    run_until_successful,
    command_once,
    prompt_input_for_commands,
    display_habit,
    unsuccessful,
)

class UpdateHabitView:
    """Interactive view for updating an existing habit.

    The view manages internal state used while a user walks through the
    update workflow. It does not perform persistence itself; it only gathers
    validated values to be applied by the surrounding controller or service.

    Attributes:
        color (Colors): Terminal color helper.
        add_habit_view (AddHabitView): Helper used to collect habit field
            values (reused from the add-habit flow).
        table_name (str): Target table for update operations (e.g. 'habit' or
            'habit_content').
        fields_to_update (dict): Collected field name -> value pairs to apply.
        update (bool): Flag set when the user indicates they want to save
            changes.
    """
    def __init__(self):
        self.color = Colors()
        self.BRIGHT            = self.color.choose_brightness("BRIGHTEN")
        self.DARK              = self.color.choose_brightness("Darken")
        self.UNSUCCESSFUL      = self.BRIGHT + self.color.choose_color("UNSUCCESSFUL") 
        self.SUCCESSFUL        = self.BRIGHT + self.color.choose_color("SUCCESSFUL") 
        self.INPUT             = self.BRIGHT + self.color.choose_color("INPUT") 
        self.WHITE             = self.BRIGHT + self.color.choose_color("WHITE")
        self.BLUE              = self.BRIGHT + self.color.choose_color("BLUE")
        self.HELP              = self.BRIGHT + self.color.choose_color("HELP")
        self.LIGHTBLACK_EX     = self.color.FORE.LIGHTBLACK_EX
        self.BACK              = self.color.BACK
        self.table_name        = ""
        self.add_habit_view    = AddHabitView()
        self.status            = None
        self.allow_habit_display = False
        self.fields_to_update    = {}
        self.update              = False

    @run_until_successful
    @command_once
    def show_habits(self,method_name):
        """Ask whether the user knows the habit id or wants to view habits.

        Args:
            method_name (str): The high-level operation the user is performing
                (used to render the prompt).

        Returns:
            tuple: (response, message, success) where response is one of
                'yes', 'no', 'esc' or 'clear_screen'.
        """
        allow_habit_display = prompt_input_for_commands(f"Do you know the id of the habit you want to {method_name} : ",['yes','no'])
        if allow_habit_display=='esc':
            return allow_habit_display,'SKIP DISPLAY',True
        
        if allow_habit_display=='clear_screen':
            return allow_habit_display,"",False
        
        if allow_habit_display not in ['yes','no']:
            return allow_habit_display,'The input is not in the given options',False 
        
        if allow_habit_display=='no':
            self.allow_habit_display = True
        return allow_habit_display,'Success...',True

    @run_until_successful
    @command_once
    def set_table_name(self):
        """Prompt the user to choose which table/portion of the habit to update.

        The user selects between updating `habit_content` (description and
        reflections) or `habit` (name, start_datetime, duration, etc.).

        Returns:
            tuple: (choice, message, success)
        """
        table_names = {
            'A':'habit_content','B':'habit'
        } 
        table_name = prompt_input_for_commands(f"Enter what do you want to update: \n{self.WHITE+self.DARK} A-(description or reflections), B-for everything else",['A','B']).upper()
        
        if table_name == 'esc':
            return table_name,"SKIP DISPLAY",True
        
        if table_name == 'clear_screen':
            return table_name,"SKIP DISPLAY",False
        
        if table_name not in table_names:
            return table_name, f"{table_name} is not an option to choose from!",False
        
        self.table_name = table_names.get(table_name)
        return table_name,'success..',True
    
    @run_until_successful
    @command_once
    def set_status(self):
        """Prompt and set a new status for the habit.

        Returns:
            tuple: (status, message, success)
        """
        statuses = ["UPCOMING","MISSED","ONGOING","DONE"]
        status = prompt_input_for_commands("Enter status: ", statuses)

        if status not in statuses:
            return status,f'Status {status} does not exist',False
        self.status = status
        return status,"Success...",True

    def update_name(self):
        """Use the AddHabitView flow to collect a new habit name.

        The collected name is stored in `self.fields_to_update` under the
        'name' key.
        """
        self.add_habit_view.set_habit_name()
        self.fields_to_update.update({'name':self.add_habit_view.get_habit_name()})

    def update_start_datetime(self):
        """Collect a new start datetime via the AddHabitView helper.

        The collected datetime is stored under 'start_date_time' in
        `self.fields_to_update`.
        """
        self.add_habit_view.set_start_datetime()
        self.fields_to_update.update({'start_date_time':self.add_habit_view.get_start_datetime()})

    @run_until_successful
    @command_once
    def set_table_fields(self):
        """Interactive loop to select and set fields to be updated.

        The method validates that a table has been chosen, then repeatedly
        prompts the user for which field to edit. Valid options depend on the
        selected table. When the user selects 'save changes' the accumulated
        `fields_to_update` dictionary is validated and `self.update` is set to
        True to indicate readiness for persistence.

        Returns:
            tuple: (last_input, message, success)
        """
        try:
            assert self.table_name!="","choose what you want to update first"
        except Exception as e:
            return "",f'{e}',True
        
        field_name = {
            "habit":[
                "name",
                "start_datetime",
                "duration",
                # "status"
            ],
            "habit_content":[
                "description",
                "reflections"
            ]
        }

        while True:
            table_field_name = prompt_input_for_commands("Enter habit field name you want to modify: ",[*field_name.get(self.table_name),'save changes']).lower()
            if table_field_name == 'clear_screen':
                return table_field_name,"SKIP DISPLAY",False
 
            if table_field_name == 'esc':
                return table_field_name,"",True
            
            if table_field_name == 'save changes':
                try:
                    self.fields_to_update = {
                        i:self.fields_to_update.get(i) 
                        for i in self.fields_to_update.keys() 
                        if self.fields_to_update.get(i)
                                             }
                    assert len(self.fields_to_update)>0
                except Exception:
                    return table_field_name,"In order to update a habit at least one field must have a value!",False
                self.update = True
                return table_field_name,"Success...",True
            
            if table_field_name not in field_name.get(self.table_name):
                return table_field_name,f"{table_field_name} is not in the given options",False
            
            if 'name'==table_field_name:
                self.update_name()
                
            if 'start_datetime'==table_field_name and not self.add_habit_view.get_start_datetime():
                self.add_habit_view.set_start_datetime()
                print(self.fields_to_update.update({'start_datetime':self.add_habit_view.get_start_datetime()}))

            if 'duration'==table_field_name and not self.add_habit_view.get_habit_duration():
                self.add_habit_view.get_habit_session_duration()
                self.fields_to_update.update({'duration':self.add_habit_view.get_habit_duration()})
 
            # if 'status'==table_field_name and not self.status:
            #     self.set_status()
            #     self.fields_to_update.update({'status':self.status})

            if 'description'==table_field_name:
                self.add_habit_view.set_habit_description()
                self.fields_to_update.update({'description':self.add_habit_view.get_description()})

            if 'reflections'==table_field_name:
                self.add_habit_view.set_habit_reflections()
                self.fields_to_update.update({'reflection':self.add_habit_view.get_reflections()})

if __name__ == '__main__':
    pass