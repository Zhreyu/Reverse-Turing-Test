# phases/notify.py

from utils.formatting import print_system_message
from utils.formatting import print_result

def notify_imposter():
    """
    Notifies players that one among them is actually human.
    """
    print_system_message(
        "🎭 ATTENTION! One among you is a human pretending to be an AI agent.\n"
        "Can you spot who it is? Or will the human successfully blend in?"
    )

def print_result(message: str, success: bool = True):
    """Print a result message with appropriate styling."""
    if success:
        print(f"\n{Fore.GREEN}{Style.BRIGHT}✓ {message}{Style.RESET_ALL}")
    else:
        print(f"\n{Fore.RED}{Style.BRIGHT}✗ {message}{Style.RESET_ALL}")
