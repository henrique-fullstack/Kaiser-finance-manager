import os

def clear_screen():
    """Clears the terminal screen. Works on both Windows and Unix-based systems.
    Args:
        None
    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def color_text(text, color):
    """
    Adds colors to text in the terminal using ANSI codes.
    Available colors: green, red, blue, yellow, cyan, white.
    Args:
        text: string (the text to be colored)
        color: string (the color name)
    Returns:
        The input text wrapped in ANSI color codes for terminal display
    """
    colors = {
        "green": "\033[32m",
        "red": "\033[31m",
        "blue": "\033[34m",
        "yellow": "\033[33m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "bold": "\033[1m",
        "reset": "\033[0m" # Volta a cor ao normal
    }
    
    selected_color = colors.get(color.lower(), colors["white"])
    return f"{selected_color}{text}{colors['reset']}"

def format_currency(value):
    """Transforms a float value into a formatted currency string in Brazilian Real (R$) format.
    Args:
        value: float (the numeric value to be formatted as currency)
    Returns:
        A string representing the formatted currency value, e.g., "R$ 1.234,56"
    """
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
