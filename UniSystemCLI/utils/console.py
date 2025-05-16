from enum import Enum
class CONSOLE_COLORS(Enum):
    RED = "red"
    GREEN = "green"
    YELLOW = "yellow"
    BLUE = "blue"
    MAGENTA = "magenta"
    CYAN = "cyan"
    WHITE = "white"
    RESET = "reset"

def console(msg: str, color = CONSOLE_COLORS.WHITE):
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
    print(f"{color_codes.get(color.value, color_codes['white'])}{msg}{reset_code}")

def display_table(headers, rows, color=CONSOLE_COLORS.WHITE):
    """Display data in a formatted table.
    
    Args:
        headers: List of column headers
        rows: List of rows, where each row is a list of values
        color: Color to display the table in
    """
    if not rows:
        console("No data to display.", CONSOLE_COLORS.YELLOW)
        return
        
    # Calculate column widths
    col_widths = [len(str(h)) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Create format string for rows
    format_str = "| " + " | ".join([f"{{:<{w}}}" for w in col_widths]) + " |"
    
    # Calculate total width of table
    total_width = sum(col_widths) + (len(headers) * 3) + 1
    
    # Create separator line
    separator = "+" + "-" * (total_width - 2) + "+"
    
    # Display the table
    console(separator, color)
    console(format_str.format(*headers), color)
    console(separator, color)
    
    for row in rows:
        # Ensure row has same number of columns as headers
        padded_row = row + [""] * (len(headers) - len(row))
        console(format_str.format(*[str(cell) for cell in padded_row[:len(headers)]]), color)
    
    console(separator, color)

