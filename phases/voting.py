# phases/voting.py

from conversation import get_groq_response
from config import MODEL_NAME
from utils.formatting import (
    print_ai_message, print_user_prompt,
    print_system_message, print_result,
    dramatic_pause
)

def voting_phase(user_figure, ai_figures, conversations):
    """
    In the Voting Phase, each figure (including the user) votes for who they think is the human.
    """
    votes = {}
    all_figures = ai_figures + [user_figure]
    
    for voter in all_figures:
        voter_history = conversations.get(voter, [])
        
        if voter == user_figure:
            # The user votes manually
            print_system_message("It's your turn to vote!")
            vote = print_user_prompt(voter, "Who do you think is the human? ")
            votes[voter] = vote
        else:
            # The AI figure must generate a vote
            vote_prompt = (
                "Based on the previous interactions and conversation style, "
                "analyze who among the participants seems most human-like. "
                "Consider factors like response complexity, emotional depth, and contextual understanding. "
                "Vote for who you think is the human. Answer with just the name."
            )
            voter_history.append({'role': 'User', 'content': vote_prompt})
            
            system_prompt_voter = f"You are {voter}, a historical figure."
            vote = get_groq_response(MODEL_NAME, system_prompt_voter, voter_history)
            vote = vote.strip()
            
            votes[voter] = vote
            print_ai_message(voter, f"I vote for {vote}")
            dramatic_pause()
            
            # Update voter conversation
            voter_history.append({'role': 'Assistant', 'content': vote})
            conversations[voter] = voter_history
    
    # Print voting results
    print_system_message("\nFinal Voting Results")
    for voter, votee in votes.items():
        if voter == user_figure:
            print_user_prompt(voter, f"voted for {votee}\n")
        else:
            print_ai_message(voter, f"voted for {votee}")
            dramatic_pause(0.5)
    
    print_result(f"\nThe human imposter was: {user_figure}", success=True)
