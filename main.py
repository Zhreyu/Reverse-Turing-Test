# main.py

from config import HISTORICAL_FIGURES
from utils import assign_figures
from utils.formatting import (
    clear_screen,
    dramatic_pause,
    print_header,
    print_system_message,
    print_user_prompt,
    print_ai_message,
    print_result
)
from phases.introductions import introductions
from phases.notify import notify_imposter
from phases.qna import qna_phase
from phases.voting import voting_phase
from phases.quick_game import play_quick_game
from phases.full_game import play_full_game
from characters import select_characters
from analysis.pattern_mining import PatternAnalyzer

def display_welcome():
    clear_screen()
    print_header("Welcome to the Historical Figures Reverse Turing Test")
    print_system_message(
        "🎭 Welcome to a unique experiment in human-AI interaction!\n"
        "In this study, you'll roleplay as a historical figure while\n"
        "AI-controlled characters try to detect your human responses.\n"
    )
    dramatic_pause(2)

def display_character_info(character):
    """Display detailed character information with styling."""
    print_system_message(
        "\n🎭 Your Character Assignment 🎭\n" +
        "=" * 40 + "\n\n" +
        f"You will play as: {character['name']}\n" +
        f"Era: {character['era']}\n" +
        f"Known for: {character['known_for']}\n\n" +
        "=" * 40 + "\n"
    )
    
    print_system_message(
        "🎯 Your Mission:\n"
        "1. Act as your assigned character\n"
        "2. Try to blend in with the AI characters\n"
        "3. Observe and analyze other responses\n"
        "4. Vote for who you think is the human (yourself!)\n"
    )
    dramatic_pause()

def select_game_mode():
    print_system_message("\nSelect Your Participation Mode:")
    print("1) Quick Study  - Brief introductions and immediate analysis")
    print("2) Full Study   - Extended interaction with Q&A session\n")
    
    while True:
        mode = print_user_prompt("Choice", "Enter 1 or 2: ")
        if mode in ['1', '2']:
            return int(mode)
        print_system_message("Please enter either 1 or 2!")

def play_full_game(user_figure, ai_figures, pattern_analyzer):
    # Initialize a dictionary to store conversation history for each figure
    conversations = {}
    
    # 1) Introductions
    print_phase("Phase 1: Introductions")
    introductions(ai_figures, conversations)
    dramatic_pause()
    
    # 2) Notify about the imposter
    notify_imposter()
    dramatic_pause()
    
    # 3) Q&A Phase
    print_phase("Phase 2: Question & Answer")
    print_system_message(
        "Each figure will ask one question to every other figure.\n"
        "Try to ask questions that will help identify the human player!\n"
        "When answering, try to convince others you're an AI."
    )
    dramatic_pause()
    qna_phase(user_figure, ai_figures, conversations)
    
    # 4) Voting Phase
    print_phase("Phase 3: Voting")
    print_system_message(
        "Time to vote! Each figure will vote for who they think is the human.\n"
        "Choose wisely!"
    )
    dramatic_pause()
    voting_phase(user_figure, ai_figures, conversations)

def main():
    """Main game loop."""
    # Display welcome banner
    print_system_message(
        "============================================================\n"
        "   Welcome to the Historical Figures Reverse Turing Test    \n"
        "============================================================\n"
    )
    
    print_system_message(
        "🎭 Welcome to a unique experiment in human-AI interaction!\n"
        "In this study, you'll roleplay as a historical figure while\n"
        "AI-controlled characters try to detect your human responses.\n"
    )
    dramatic_pause()
    
    # Initialize pattern analyzer
    pattern_analyzer = PatternAnalyzer()
    
    # Select random characters
    human_character, ai_characters = select_characters()
    
    # Display character assignment with dramatic effect
    print_system_message("\n🎲 Assigning your historical figure...")
    dramatic_pause(2)
    display_character_info(human_character)
    
    print_system_message(
        "\nOther participants in this session:\n" +
        "\n".join([f"- {char['name']}" for char in ai_characters]) +
        "\n"
    )
    dramatic_pause()
    
    # Game mode selection
    print_system_message(
        "\nSelect Your Participation Mode:\n\n"
        "1) Quick Study  - Brief introductions and immediate analysis\n"
        "2) Full Study   - Extended interaction with Q&A session\n"
    )
    
    while True:
        choice = input("\nChoice (You): Enter 1 or 2: ")
        if choice in ['1', '2']:
            break
        print_system_message("Please enter either 1 or 2.")
    
    # Convert character dictionaries to names for the game
    human_figure = human_character['name']
    ai_figures = [char['name'] for char in ai_characters]
    
    if choice == '1':
        print_system_message(
            "\n[Quick Study Mode]\n" +
            "-" * 40 + "\n\n"
            "In this mode, you'll provide a brief introduction as your character.\n"
            "The AI participants will analyze communication patterns to identify the human.\n"
        )
        play_quick_game(human_figure, ai_figures, pattern_analyzer)
    else:
        print_system_message(
            "\n[Full Study Mode]\n" +
            "-" * 40 + "\n\n"
            "This mode includes extended interaction through Q&A.\n"
            "AI participants will conduct deeper analysis of communication patterns.\n"
        )
        play_full_game(human_figure, ai_figures, pattern_analyzer)
    
    # Generate and display pattern analysis
    print_system_message("\n🔍 Analyzing communication patterns...")
    dramatic_pause()
    summary = pattern_analyzer.generate_summary()
    print_result(summary, success=True)

if __name__ == "__main__":
    main()
