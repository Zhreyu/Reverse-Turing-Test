"""
LLM utilities for interacting with the GROQ API.
"""
import requests
from config import GROQ_API_KEY

def get_groq_response(model: str, system_prompt: str, conversation_history: list, max_tokens: int = 200) -> str:
    """
    Get a response from the GROQ API.
    
    Args:
        model: Model name to use
        system_prompt: System prompt for the conversation
        conversation_history: List of conversation messages
        
    Returns:
        Generated response text
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    
    for msg in conversation_history:
        messages.append(msg)
    
    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": max_tokens
    }
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise Exception(f"Error from GROQ API: {response.text}")
    
    return response.json()["choices"][0]["message"]["content"]
