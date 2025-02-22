"""
Character selection and management module.
"""
import random
from typing import List, Tuple

HISTORICAL_FIGURES = [
    {
        "name": "Albert Einstein",
        "era": "1879-1955",
        "known_for": "Theory of relativity, quantum mechanics"
    },
    {
        "name": "Leonardo da Vinci",
        "era": "1452-1519",
        "known_for": "Renaissance polymath, art, science"
    },
    {
        "name": "Joan of Arc",
        "era": "1412-1431",
        "known_for": "French military leader, saint"
    }
]

def select_characters(num_ai_characters: int = 3) -> Tuple[dict, List[dict]]:
    """
    Randomly select characters for the game, ensuring we use only the core figures.
    
    Args:
        num_ai_characters: Number of AI characters (default is 3 to match original figures)
        
    Returns:
        Tuple containing:
        - Dictionary for human player's character
        - List of dictionaries for AI characters
    """
    if num_ai_characters > len(HISTORICAL_FIGURES):
        raise ValueError(f"Cannot select {num_ai_characters} AI characters. Only {len(HISTORICAL_FIGURES)} available.")
    
    # Create a copy to avoid modifying the original
    available_chars = HISTORICAL_FIGURES.copy()
    random.shuffle(available_chars)
    
    # Select human character
    human_character = available_chars.pop()
    
    # The rest become AI characters
    ai_characters = available_chars
    
    return human_character, ai_characters
