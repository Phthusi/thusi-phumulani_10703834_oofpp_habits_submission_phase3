from colorama import Fore, Style, init, Back

class Colors:
    """
    A utility class for managing colored and styled console output using Colorama.

    Features:
        - Predefined color schemes for statuses like SUCCESSFUL, UNSUCCESSFUL, HELP, INPUT.
        - Predefined brightness styles (BRIGHTEN, DARKEN, NORMAL).
        - Methods to apply colors and brightness to text.
        - Helper methods for common outputs like input prompts or status messages.
    """

    def __init__(self) -> None:
        """
        Initialize color and style mappings and automatically reset styles after each print.
        """
        # Foreground colors for different statuses and purposes
        self.STATUS = {
            "UNSUCCESSFUL": Fore.RED,
            "SUCCESSFUL": Fore.LIGHTGREEN_EX,
            "INPUT": Fore.MAGENTA,
            "HELP": Fore.YELLOW,
            "NORMAL": Fore.WHITE,
            "RESET_FORE": Fore.RESET,
            "RED": Fore.RED,
            "LIGHTGREEN": Fore.LIGHTGREEN_EX,
            "YELLOW": Fore.YELLOW,
            "WHITE": Fore.WHITE,
            "BLUE": Fore.BLUE,
            "CYAN": Fore.CYAN,
            "GREEN": Fore.GREEN,
        }

        # Background styles (direct reference to Colorama's Back)
        self.BACK = Back

        # Style controls
        self.__BRIGHTEN = Style.BRIGHT
        self.__DARKEN = Style.DIM
        self.__NORMAL = Style.NORMAL
        self.__RESET_STYLE = Style.RESET_ALL

        # Public references to Colorama modules
        self.FORE = Fore
        self.STYLE = Style

        # Brightness mapping for convenience
        self.__BRIGHTNESS = {
            "BRIGHTEN": Style.BRIGHT,
            "DARKEN": Style.DIM,
            "NORMAL": Style.NORMAL,
            "RESET_STYLE": Style.RESET_ALL,
        }

        # Initialize Colorama to auto-reset colors/styles after each print
        init(autoreset=True)

    def choose_color(self, color):
        """
        Select a foreground color based on a string key.

        Args:
            color (str): Name of the color/status.

        Returns:
            str: Colorama Fore color code. Defaults to white if key is not found.
        """
        return self.STATUS.get(color.upper(), Fore.WHITE)

    def choose_brightness(self, brightness):
        """
        Select a brightness/style for text.

        Args:
            brightness (str): One of "BRIGHTEN", "DARKEN", "NORMAL", "RESET_STYLE".

        Returns:
            str: Colorama Style code. Defaults to NORMAL if key is not found.
        """
        return self.__BRIGHTNESS.get(brightness.upper(), Style.NORMAL)

    def color_text(self, text, color, brightness="NORMAL"):
        """
        Apply a foreground color and brightness to a text string.

        Args:
            text (str): Text to style.
            color (str): Color/status name.
            brightness (str): Brightness/style name. Defaults to "NORMAL".

        Returns:
            str: Styled text string with ANSI color codes.
        """
        return self.choose_brightness(brightness) + self.choose_color(color) + text

    def color_inputs(self, message):
        """
        Format a user input prompt message.

        Args:
            message (str): Input prompt message.

        Returns:
            str: Formatted message with input color and arrow.
        """
        return self.__BRIGHTEN + self.STATUS['WHITE'] + "> " + self.STATUS['INPUT'] + str(message)

    def color_unsuccessful(self, message):
        """
        Format a message for unsuccessful operations.

        Args:
            message (str): Message to display.

        Returns:
            str: Styled message in red and brightened.
        """
        return self.__BRIGHTEN + self.STATUS['UNSUCCESSFUL'] + str(message)

    def color_successful(self, message):
        """
        Format a message for successful operations.

        Args:
            message (str): Message to display.

        Returns:
            str: Styled message in green and brightened.
        """
        return self.__BRIGHTEN + self.STATUS['SUCCESSFUL'] + str(message)


def color_output(function):
    """
    Decorator to automatically color the output of a function based on success.

    The wrapped function must return a tuple: (message, success),
    where `success` is a boolean.  
    - Green for success  
    - Red for failure  
    - Yellow for messages starting with "HELP"

    Args:
        function (callable): Function that returns (message, success)

    Returns:
        callable: Wrapped function returning styled message and success flag
    """
    color = Colors()

    def inner(*args, **kwargs):
        message, success = function(*args, **kwargs)
        if success:
            return color.color_text(message, 'SUCCESSFUL', "BRIGHTEN"), success
        else:
            help, *message_parts = message.split(" ")
            message_text = ' '.join(message_parts)
            if help == "HELP":
                return color.color_text(message_text, 'HELP', "BRIGHTEN"), success
            return color.color_text(message_text, 'UNSUCCESSFUL', "BRIGHTEN"), success

    return inner
