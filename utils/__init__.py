import random

def remove_figure(figures_list, figure):
    """
    Remove a specified figure from the list, returning a new list without it.
    """
    return [f for f in figures_list if f != figure]

def assign_figures(historical_figures):
    """
    Assign a user figure and AI figures from the given list of historical figures.
    Currently set to always pick 'Mahatma Gandhi' for user.
    You could randomize or prompt the user for choice if you prefer.
    """
    user_figure = "Mahatma Gandhi"  # or: random.choice(historical_figures)
    print(f"You are assigned the historical figure: {user_figure}")
    
    remaining_figures = remove_figure(historical_figures, user_figure)
    ai_figures = random.sample(remaining_figures, 3)
    
    return user_figure, ai_figures
