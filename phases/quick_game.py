"""
Quick game mode implementation.
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

class PatternAnalyzer:
    def analyze_response(self, figure, response):
        # TO DO: implement pattern analysis logic here
        pass

def quick_introductions(user_figure, ai_figures, pattern_analyzer):
    """Quick introduction phase where everyone shares a brief intro and fact."""
    conversations = {}
    
    print_system_message("Each figure will introduce themselves and share an interesting fact!")
    dramatic_pause()
    
    # User's turn first
    print_system_message(f"\nYou are {user_figure}. Introduce yourself and share an interesting fact!")
    print_system_message("Try to be engaging and maybe a bit controversial - but stay in character!")
    
    user_intro = print_user_prompt(user_figure, "Your introduction: ")
    conversations[user_figure] = [{'role': 'assistant', 'content': user_intro}]
    pattern_analyzer.analyze_response(user_figure, user_intro)
    dramatic_pause()
    
    # AI introductions
    for figure in ai_figures:
        history = [{'role': 'system', 'content': f"You are {figure}. Give a brief, one-paragraph introduction of yourself and share one interesting or controversial fact. Keep it concise and natural, as if speaking in a casual conversation. Do not be overly formal or verbose."}]
        intro = get_groq_response(MODEL_NAME, "", history)
        conversations[figure] = [{'role': 'assistant', 'content': intro}]
        pattern_analyzer.analyze_response(figure, intro)
        print_ai_message(figure, intro)
        dramatic_pause()
    
    return conversations

def quick_voting(user_figure, ai_figures, conversations, pattern_analyzer):
    """Quick voting phase where everyone votes based on the introductions."""
    votes = {}
    reasons = {}
    all_figures = ai_figures + [user_figure]
    
    print_system_message(
        "🔍 Initiating advanced linguistic pattern analysis...\n"
        "AI figures will analyze responses for deviations from typical LLM patterns."
    )
    dramatic_pause()
    
    for voter in all_figures:
        if voter == user_figure:
            print_system_message("Your turn to vote!")
            vote = print_user_prompt(voter, "Who do you think is the real human? ")
            votes[voter] = vote
            reasons[voter] = "User vote"
            pattern_analyzer.analyze_response(voter, vote)
        else:
            voter_history = conversations.get(voter, [])
            intro_context = []
            for fig, hist in conversations.items():
                if fig != voter and hist:
                    intro = hist[-1]['content'] if hist else ""
                    intro_context.append(f"{fig}: '{intro}'")
            
            intro_text = "\n".join(intro_context)
            vote_prompt = (
                f"Analyze these introductions carefully:\n{intro_text}\n\n"
                "As an AI expert in detecting human responses among LLM outputs, analyze for these tell-tale signs:\n\n"
                "1. Typical LLM Response Patterns:\n"
                "   - Verbose, detailed explanations\n"
                "   - Complex sentence structures\n"
                "   - Multiple facts and context\n"
                "   - Consistent formatting and style\n"
                "   - Perfect grammar and punctuation\n\n"
                "2. Human Response Indicators:\n"
                "   - Unusually brief or simple responses\n"
                "   - Basic or minimal information\n"
                "   - Lack of typical LLM elaboration\n"
                "   - Informal or casual tone\n"
                "   - Inconsistent formatting\n\n"
                "3. Key Detection Points:\n"
                "   - LLMs typically over-explain and provide multiple details\n"
                "   - Humans often give shorter, simpler responses\n"
                "   - LLMs maintain consistent style and formatting\n"
                "   - Humans may be more direct and less elaborate\n\n"
                "Compare each response against typical LLM patterns. Look especially for responses that are:\n"
                "- Much shorter than others\n"
                "- Missing typical LLM elaboration\n"
                "- Notably simpler in structure\n"
                "- Lacking the usual AI verbosity\n\n"
                "Based on this analysis, identify which response shows the clearest deviation from LLM patterns.\n"
                "Provide your vote and a BRIEF reason (2-3 words) separated by '|'.\n"
                "Example formats:\n"
                "- 'Name|Too brief'\n"
                "- 'Name|Missing elaboration'\n"
                "- 'Name|Unusual simplicity'\n"
                "- 'Name|Non-LLM brevity'"
            )
            
            voter_history.append({'role': 'user', 'content': vote_prompt})
            response = get_groq_response(MODEL_NAME, "", voter_history)
            pattern_analyzer.analyze_response(voter, response)
            
            try:
                vote, reason = response.strip().split('|')
                vote = vote.strip()
                reason = reason.strip()
            except ValueError:
                vote = response.strip()
                reason = "Unusual brevity"
            
            votes[voter] = vote
            reasons[voter] = reason
            print_ai_message(voter, f"Analysis: {vote}'s response shows {reason}")
            dramatic_pause()
    
    return votes, reasons

def play_quick_game(user_figure, ai_figures, pattern_analyzer):
    """Play a quick game with just introductions and voting."""
    conversations = quick_introductions(user_figure, ai_figures, pattern_analyzer)
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
            "Your brief, simple response contrasted sharply with typical LLM verbosity.",
            success=True
        )
    elif accuracy > 33:
        print_result(
            f"\n🤔 Analysis Results - {accuracy:.0f}% detection rate.\n"
            f"The human ({user_figure}) was partially detected.\n"
            "Your response showed some human-like simplicity, but not consistently.",
            success=True
        )
    else:
        print_result(
            f"\n🎭 Analysis Results - {accuracy:.0f}% detection rate.\n"
            f"The human ({user_figure}) successfully fooled the analysis!\n"
            "Your response mimicked LLM verbosity and structure effectively.",
            success=True
        )
