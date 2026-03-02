import os

def clear_screen():
    """Limpa o terminal de acordo com o Sistema Operacional."""
    os.system('cls' if os.name == 'nt' else 'clear')

def color_text(text, color):
    """
    Adiciona cores ao texto no terminal usando códigos ANSI.
    Cores disponíveis: green, red, blue, yellow, cyan, white.
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
    """Transforma um número em formato de moeda brasileira: R$ 1.234,56"""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")