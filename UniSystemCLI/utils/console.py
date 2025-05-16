from enum import Enum


def console( msg: str, color = "white"):
    color_codes = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
    }
    reset_code = "\033[0m"
    print(f"{color_codes.get(color, color_codes['white'])}{msg}{reset_code}")

class CONSOLE_COLORS(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    RESET = "reset"
