from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit.history import FileHistory


class AutoCompleter:
    """
    Provides auto-completion functionality for command-line input using prompt_toolkit.

    Features:
        - Maintains a command history in a file.
        - Provides fuzzy matching for command suggestions.
        - Returns a prompt session ready for input.
    """

    def __init__(self, commands):
        """
        Initialize the AutoCompleter with a list of commands.

        Args:
            commands (list[str]): List of command strings to provide as suggestions.
        """
        self.__history = FileHistory("command_history.txt")
        self.__commands = commands
        self.__session = PromptSession(completer=self.get_completer(), history=self.__history)
        
    def get_completer(self):
        """
        Get a FuzzyCompleter configured with the current list of commands.

        Returns:
            FuzzyCompleter: A fuzzy-matching completer for command-line input.
        """
        return FuzzyCompleter(WordCompleter(self.__commands, ignore_case=True))

    def get_commands(self):
        """
        Retrieve the current list of commands used for auto-completion.

        Returns:
            list[str]: List of commands.
        """
        return self.__commands
    
    def get_session(self):
        """
        Get the prompt session object for interactive command input.

        Returns:
            PromptSession: A prompt_toolkit session ready for user input with history and auto-completion.
        """
        return self.__session
