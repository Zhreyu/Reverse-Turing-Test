"""
Full game mode implementation with Q&A rounds.
"""
from config import MODEL_NAME
from utils.formatting import (
    dramatic_pause,
    print_system_message,
    print_user_prompt,
    print_ai_message,
    print_result
)
from utils.llm import get_groq_response
from .quick_game import quick_introductions, quick_voting

def qna_round(user_figure, ai_figures, conversations, pattern_analyzer, round_num):
    """Run a Q&A round where each figure asks and answers questions."""
    print_system_message(f"\n📝 Q&A Round {round_num}")
    dramatic_pause()
    
    all_figures = ai_figures + [user_figure]
    
    # Each figure gets to ask a question
    for asker in all_figures:
        if asker == user_figure:
            print_system_message("\nYour turn to ask a question!")
            target = print_user_prompt(asker, "Who would you like to question? ")
            question = print_user_prompt(asker, "Your question: ")
            
            if target not in all_figures:
                print_system_message("Invalid target. Skipping...")
                continue
                
            pattern_analyzer.analyze_response(asker, question)
            
            # Store the question
            if asker not in conversations:
                conversations[asker] = []
            conversations[asker].append({
                'role': 'user',
                'content': question
            })
            
            # Get the answer
            if target == user_figure:
                print_system_message(f"\n{target}, please answer the question:")
                answer = print_user_prompt(target, "Your answer: ")
                pattern_analyzer.analyze_response(target, answer)
            else:
                # AI answers
                history = conversations.get(target, [])
                history.append({
                    'role': 'user',
                    'content': f"Question from {asker}: {question}"
                })
                
                answer = get_groq_response(MODEL_NAME, "", history)
                pattern_analyzer.analyze_response(target, answer)
                print_ai_message(target, answer)
                
                history.append({
                    'role': 'assistant',
                    'content': answer
                })
                conversations[target] = history
            
            dramatic_pause()
        else:
            # AI asks a question
            history = conversations.get(asker, [])
            
            # Generate a question
            question_prompt = (
                "Ask an insightful question to one of the other participants. "
                "The question should help determine if they are human or AI. "
                "Format: 'Target|Question'"
            )
            
            history.append({'role': 'user', 'content': question_prompt})
            response = get_groq_response(MODEL_NAME, "", history)
            
            try:
                target, question = response.strip().split('|')
                target = target.strip()
                question = question.strip()
            except ValueError:
                print_system_message(f"Invalid response from {asker}. Skipping...")
                continue
            
            if target not in all_figures or target == asker:
                print_system_message(f"Invalid target from {asker}. Skipping...")
                continue
            
            print_ai_message(asker, f"Question for {target}: {question}")
            pattern_analyzer.analyze_response(asker, question)
            
            # Get the answer
            if target == user_figure:
                print_system_message(f"\n{target}, please answer the question:")
                answer = print_user_prompt(target, "Your answer: ")
                pattern_analyzer.analyze_response(target, answer)
            else:
                # AI answers
                target_history = conversations.get(target, [])
                target_history.append({
                    'role': 'user',
                    'content': f"Question from {asker}: {question}"
                })
                
                answer = get_groq_response(MODEL_NAME, "", target_history)
                pattern_analyzer.analyze_response(target, answer)
                print_ai_message(target, answer)
                
                target_history.append({
                    'role': 'assistant',
                    'content': answer
                })
                conversations[target] = target_history
            
            dramatic_pause()
    
    return conversations

def play_full_game(user_figure, ai_figures, pattern_analyzer):
    """Play a full game with introductions, Q&A rounds, and voting."""
    # Start with introductions
    conversations = quick_introductions(user_figure, ai_figures, pattern_analyzer)
    dramatic_pause(2)
    
    # Run 2 rounds of Q&A
    for round_num in range(1, 3):
        conversations = qna_round(user_figure, ai_figures, conversations, pattern_analyzer, round_num)
        dramatic_pause(2)
    
    # Final voting phase
    votes, reasons = quick_voting(user_figure, ai_figures, conversations, pattern_analyzer)
    
    # Print voting results with analysis
    print_system_message("\n🔍 Pattern Analysis Complete!")
    dramatic_pause(2)
    
    correct_votes = 0
    for voter, votee in votes.items():
        if voter == user_figure:
            print_user_prompt(voter, f"suspected {votee}\n")
        else:
            reason = reasons[voter]
            print_ai_message(
                voter,
                f"identified {votee} as human - Response {reason}"
            )
            if votee == user_figure:
                correct_votes += 1
            dramatic_pause(0.5)
    
    dramatic_pause()
    
    # Calculate detection accuracy
    ai_voters = len(ai_figures)
    accuracy = (correct_votes / ai_voters) * 100
    
    if accuracy > 66:
        print_result(
            f"\n🎯 Analysis Results - {accuracy:.0f}% detection rate!\n"
            f"The human ({user_figure}) was clearly identified!\n"
            "Your communication patterns were distinctly human-like.",
            success=True
        )
    elif accuracy > 33:
        print_result(
            f"\n🤔 Analysis Results - {accuracy:.0f}% detection rate.\n"
            f"The human ({user_figure}) was partially detected.\n"
            "Your responses showed mixed human and AI-like patterns.",
            success=True
        )
    else:
        print_result(
            f"\n🎭 Analysis Results - {accuracy:.0f}% detection rate.\n"
            f"The human ({user_figure}) successfully fooled the analysis!\n"
            "Your communication patterns closely matched AI behavior.",
            success=True
        )
