"""Terminal colors"""


class bcolors:
    """
    A utility class for defining ANSI escape sequences for terminal text formatting.

    Attributes:
        HEADER (str): ANSI escape sequence for magenta text.
        OKBLUE (str): ANSI escape sequence for blue text.
        OKGREEN (str): ANSI escape sequence for green text.
        WARNING (str): ANSI escape sequence for yellow text.
        FAIL (str): ANSI escape sequence for red text.
        ENDC (str): ANSI escape sequence to reset text formatting.
        BOLD (str): ANSI escape sequence for bold text.
        UNDERLINE (str): ANSI escape sequence for underlined text.
    """

    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
