"""
Formatting utilities for the game interface.
"""
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

def clear_screen():
    """Clear the terminal screen."""
    print("\033[H\033[J", end="")

def dramatic_pause(seconds: float = 1):
    """Add a dramatic pause between actions."""
    time.sleep(seconds)

def print_header(text: str):
    """Print a header with styling."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{text}{Style.RESET_ALL}\n")

def print_system_message(message: str):
    """Print a system message with styling."""
    print(f"{Fore.BLUE}{Style.BRIGHT}System: {Style.RESET_ALL}{message}")

def print_user_prompt(name: str, prompt: str = "") -> str:
    """Print a user prompt with styling and return input."""
    if prompt:
        return input(f"{Fore.GREEN}{Style.BRIGHT}{name} (You): {Style.RESET_ALL}{prompt}")
    return input(f"{Fore.GREEN}{Style.BRIGHT}{name} (You): {Style.RESET_ALL}")

def print_ai_message(name: str, message: str):
    """Print an AI message with styling."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}{name}: {Style.RESET_ALL}{message}")

def print_result(message: str, success: bool = True):
    """Print a result message with appropriate styling."""
    if success:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ {message}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}✗ {message}{Style.RESET_ALL}")

def print_phase(phase_name: str):
    """Print a phase header with styling."""
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}[{phase_name}]{Style.RESET_ALL}")
    print("-" * (len(phase_name) + 4))
