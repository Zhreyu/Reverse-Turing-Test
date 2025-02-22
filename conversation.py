# conversation.py

import sys
import requests
from config import MODEL_NAME, GROQ_API_KEY

def get_groq_response(model, system_prompt, conversation_history):
    """
    Calls GROQ API to generate a response for the given conversation history
    and system prompt. Returns the response text.
    """
    # Convert conversation history to GROQ chat format
    messages = [{"role": "system", "content": system_prompt}]
    for message in conversation_history:
        role = message['role'].lower()
        if role == 'user':
            messages.append({"role": "user", "content": message['content']})
        else:
            messages.append({"role": "assistant", "content": message['content']})

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except requests.exceptions.RequestException as e:
        print(f"Error calling GROQ API: {e}")
        sys.exit(1)
    except (KeyError, ValueError) as e:
        print(f"Error processing GROQ response: {e}")
        sys.exit(1)
