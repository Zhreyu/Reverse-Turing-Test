# phases/introductions.py

from conversation import get_groq_response
from config import MODEL_NAME
from utils.formatting import print_ai_message, dramatic_pause

def introductions(ai_figures, conversations):
    """
    The introduction phase: each AI figure introduces themselves briefly.
    """
    for idx, figure in enumerate(ai_figures, 1):
        system_prompt = f"You are {figure}, a historical figure."
        conversation_history = []
        
        # The user asks them to introduce themselves
        conversation_history.append({
            'role': 'User', 
            'content': 'Introduce yourself briefly in 2-3 sentences, highlighting your most significant achievement.'
        })
        
        response = get_groq_response(MODEL_NAME, system_prompt, conversation_history)
        
        print_ai_message(figure, response)
        dramatic_pause()
        
        # Update conversation history
        conversation_history.append({
            'role': 'Assistant', 
            'content': response
        })
        
        # Store this conversation history
        conversations[figure] = conversation_history
