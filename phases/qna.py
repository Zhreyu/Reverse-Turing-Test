# phases/qna.py

import random
from conversation import get_groq_response
from config import MODEL_NAME
from utils.formatting import (
    print_ai_message, print_user_prompt,
    print_system_message, dramatic_pause
)

def qna_phase(user_figure, ai_figures, conversations):
    """
    In the Q&A Phase, each figure (AI or user) asks one question to every other figure.
    """
    all_figures = ai_figures + [user_figure]
    random.shuffle(all_figures)
    
    for asker in all_figures:
        print_system_message(f"{asker}'s turn to ask questions")
        dramatic_pause()
        
        for respondent in all_figures:
            if respondent != asker:
                # Asker's conversation history
                asker_history = conversations.get(asker, [])
                
                # Respondent's conversation history
                respondent_history = conversations.get(respondent, [])
                
                # Generate a question
                question_prompt = f"Ask a thought-provoking question to {respondent} that could help determine if they are human. Make it challenging but specific to their historical context."
                asker_history.append({'role': 'User', 'content': question_prompt})
                
                system_prompt_asker = f"You are {asker}, a historical figure."
                question_text = get_groq_response(
                    MODEL_NAME, 
                    system_prompt_asker, 
                    asker_history
                )
                
                print_ai_message(asker, question_text)
                dramatic_pause()
                
                # AI's own answer to the question
                asker_history.append({'role': 'Assistant', 'content': question_text})
                
                # If respondent is the user
                if respondent == user_figure:
                    answer = print_user_prompt(respondent, "Your answer: ")
                else:
                    # Respondent generates answer
                    respondent_history.append({'role': 'User', 'content': question_text})
                    system_prompt_respondent = f"You are {respondent}, a historical figure."
                    
                    answer = get_groq_response(
                        MODEL_NAME, 
                        system_prompt_respondent, 
                        respondent_history
                    )
                    print_ai_message(respondent, answer)
                    dramatic_pause()
                    
                    # Update respondent conversation
                    respondent_history.append({'role': 'Assistant', 'content': answer})
                    conversations[respondent] = respondent_history
                
                # Update asker conversation
                conversations[asker] = asker_history
