import time
from services.colors import Colors
from services.word_prediction import AutoCompleter
import functools
import os

color = Colors()

def clear_screen():
    """
    Clears the terminal screen depending on OS.
    """
    os.system("cls" if os.name == "nt" else "clear")


def prompt_input(message, commands=None):
    """
    Displays a prompt with optional autocomplete commands.

    Parameters:
        message (str): Prompt message
        commands (iterable): Available commands for autocomplete

    Returns:
        str: User input
    """
    commands = list(commands) if commands else []
    autocompleter = AutoCompleter([*commands, "clear_screen"])
    print(message)
    return autocompleter.get_session().prompt().strip()

def colored_input(message, color_name="INPUT"):
    """
    Displays a colored input prompt.

    Parameters:
        message (str): Prompt message
        color_name (str): Color for the prompt

    Returns:
        str: User input
    """
    colored_message = color.color_inputs(message)
    return input(colored_message).strip()   

def prompt_input_for_commands(message, commands=None):
    """
    Displays a prompt with optional autocomplete commands.

    Parameters:
        message (str): Prompt message
        commands (iterable): Available commands for autocomplete

    Returns:
        str: User input
    """
    commands = list(commands) if commands else []
    autocompleter = AutoCompleter([*commands, "clear_screen","esc"])
    print(color.color_inputs(message))
    return autocompleter.get_session().prompt().lower().strip()

def run_until_successful(function):
    """
    Repeats a function call until it returns True.
    Intended for CLI input validation.
    """

    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
        while True:
            success = function(self, *args, **kwargs)
            if success:
                return True
    return wrapper

def command_loop(commands, break_on=None,switched_to="X"):
    """
    Runs commands in a loop until 'esc' or a break command is entered.

    Parameters:
        commands (dict): command -> callable
        break_on (list): commands that stop the loop
    """
    break_on = break_on or ['done']
    cleared_screen = False
    print('entered here')
    while True:
        # cleared_screen or successful("Switched to: "+switched_to+" console")
        
        command = prompt_input(
            color.color_inputs("Enter command: "),
            [*commands.keys(),'esc']
        )

        if command == "esc":
            break

        if command == "clear_screen":
            clear_screen()
            cleared_screen = True
            continue

        if command in commands:
            result = commands[command]()
            if result=='done':
                command = result

            if command in break_on:
                break
            
            if command!="esc":
                cleared_screen = False
                continue

        else:
            unsuccessful(f"'{command}' is not a valid command")
            cleared_screen = True
            continue

        cleared_screen = True
        
class ManageMainLoop:
    """
    Manages the main command loop with status handling.
    """
    consoles = []
    length_of_consoles = 0

    def __init__(self):
        self.cleared_screen = False

    def command_loop(self, commands, break_on=None, switched_to="X"):
        break_on = break_on or ['done']
        ManageMainLoop.consoles.append(switched_to)
        while True:
            if len(ManageMainLoop.consoles)!=ManageMainLoop.length_of_consoles:
                successful("Switched to: "+switched_to+" console")
                ManageMainLoop.length_of_consoles = len(ManageMainLoop.consoles)

            command = prompt_input(
                color.color_inputs("Enter command: "),
                [*commands.keys(),'esc',"get current console"]
            )

            if command == "esc":
                if not ManageMainLoop.consoles[-1]=="home":
                    ManageMainLoop.consoles.pop()
                # print(ManageMainLoop.consoles)
                break

            if command == "get current console":
                successful("Current console: "+str(ManageMainLoop.consoles[-1]))
                continue

            if command == "clear_screen":
                clear_screen()
                continue

            if command in commands:
                result = commands[command]()
                
                if result=='done':
                    command = result

                if command in break_on:
                    break
                
            else:
                unsuccessful(f"'{command}' is not a valid command")


def command_once(function):
    """
    Executes a single command and returns status.

    Returns:
        bool: True if caller should exit, False otherwise
    """
    
    @functools.wraps(function)
    def wrapper(self, *args, **kwargs):
            command, message, success = function(self, *args, **kwargs)
            if command == "esc":
                return True

            if command == "SKIP DISPLAY":
                return True
            
            if command == "clear_screen":
                clear_screen()
                return False

            if command == 'help':
                help(message)
                return False
            
            elif ':Unsuccessful' in message:
                unsuccessful(message.replace(':Unsuccessful',''))
            elif success:
                successful(message)
            else:
                unsuccessful(message)
            return success
    return wrapper

def unsuccessful(message):
    temporary_message(color.color_unsuccessful(message))

def successful(message):
    temporary_message(color.color_successful(message))

def help(message):
    print(color.choose_color("HELP")+color.choose_brightness('BRIGHTEN')+message)

def temporary_message(message, duration=2):
    """
    Displays a temporary message for a specified duration.

    Parameters:
        message (str): Message to display
        duration (int): Duration in seconds to display the message
    """
    print(message, end="", flush=True)
    time.sleep(duration)
    print("\r" + " " * len(message) + "\r", end="", flush=True)

@run_until_successful
def view_input(message,value_name,get_function):
    """
    Displays a simple input prompt.

    Parameters:
        message (str): Prompt message

    Returns:
        str: User input
    """
    command = prompt_input_for_commands(message,['yes','no'])
    print(command)
    if 'esc':
        return True
    
    if 'clear_screen':
        clear_screen()
        return False

    if command in ['yes','no']:
        if command == 'yes':
            temporary_message(f"{value_name} is {get_function()}")
        return True
    
    unsuccessful("Please enter 'yes' or 'no'")
    return False

def display_habit(habit_name,description,start_datetime,habit_session_duration):
        print(
            f"""{color.choose_color('WHITE')+'+-------------------------------------------------------------------+'}
                                                                        
    habit-name               : {color.color_successful(habit_name)} {color.choose_color('WHITE')}
    habit-description        : {color.color_successful(str(description)) if description else color.choose_color("BLUE")+str(description)} {color.choose_color('WHITE')}
    start-datetime           : {color.color_successful(str(start_datetime))}                    {color.choose_color('WHITE')}
    habit-session-duration   : {color.color_successful(str(habit_session_duration))}                     {color.choose_color('WHITE')}

+-------------------------------------------------------------------+\n""")