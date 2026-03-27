"""
neural_core/src/brain.py — JARVIS Neural Brain (Groq Optimized)
Handles interaction with Large Language Models and cognitive processing.
"""

import requests
import json
import re
from neural_core.config.config import GROQ_API_KEY, GROQ_CHAT_MODEL, GROQ_CODING_MODEL
from neural_core.src.personality import SYSTEM_PROMPT
from neural_core.src.memory import Memory

# Persistent global memory instance
mem = Memory()
API_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_llm(messages, history=None):
    """
    Send a list of messages to the Groq LLM and return the generated text.
    
    Args:
        messages (list): List of chat messages in OpenAI format.
        history (list, optional): Previous chat history for context.
        
    Returns:
        str: The assistant's reply.
    """
    # Neural context retrieval
    facts = mem.get_facts()
    fact_str = "\n\n[USER NEURAL PROFILE]\n" + "\n".join([f"- {f['key']}: {f['value']}" for f in facts]) if facts else ""
    
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    all_messages = [{"role": "system", "content": f"{SYSTEM_PROMPT}{fact_str}"}]
    
    if history:
        for h in history: all_messages.append({"role": h["role"], "content": h["content"]})
    
    all_messages.extend(messages)

    payload = {
        "model": GROQ_CHAT_MODEL,
        "messages": all_messages,
        "max_tokens": 1024, "temperature": 0.7,
    }

    try:
        r = requests.post(API_URL, headers=headers, json=payload, timeout=20)
        if r.status_code == 200:
            data = r.json()
            return data["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"LLM Connection Error: {e}")

    return "Neural connection failed."

def conscious_subconscious_process(command: str, history=None) -> tuple:
    """
    Dual-layer cognitive processing for intent extraction and fact learning.
    
    Args:
        command (str): The user input string.
        history (list, optional): Context history.
        
    Returns:
        tuple: (conscious_intent_dict, subconscious_facts_list)
    """
    system_instruction = """
You are the JARVIS neural cognitive core. 
CONSCIOUS MIND: Identify immediate system actions.
SUB-CONSCIOUS MIND: Extract personal facts or preferences.
Return ONLY valid JSON:
{
  "conscious": {
      "action": "open_app|close_app|play_youtube|search_google|write_note|get_news|volume_control|brightness_control|lock_screen|shutdown|restart|system_info|time_date|battery_status|open_website|call_contact|open_gallery|access_storage|take_photo|open_any_app|generate_image_task|general_chat",
      "target": "string",
      "modifier": "string",
      "response": "if general_chat, your intelligent reply"
  },
  "subconscious": [{"key": "name|habit|etc", "value": "fact", "type": "personal", "priority": 1}]
}
"""
    try:
        combined_prompt = f"{system_instruction}\n\n[USER INPUT]: \"{command}\""
        response = ask_llm([{"role": "user", "content": combined_prompt}], history=history)
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return data.get("conscious", {}), data.get("subconscious", [])
            
        return {"action": "general_chat", "target": command, "response": response}, []
    except:
        return {"action": "general_chat", "target": command}, []
