"""
neural_core/src/command_processor.py — Deterministic Processing Engine
Orchestrates the 7-stage neural command processing flow.
"""

import json
import re
from neural_core.src.brain import conscious_subconscious_process, mem

def process_command(user_input: str, last_command: str = "", system_state: dict = None) -> dict:
    """
    Core Deterministic 7-Stage Engine.
    1. Normalize, 2. Decode, 3. Route, 4. Validate, 5. Plan, 6. Memory, 7. Respond
    
    Args:
        user_input (str): Raw string from user.
        last_command (str, optional): Previous command for duplicate detection.
        system_state (dict, optional): Current state of the mobile client.
        
    Returns:
        dict: Structured JSON response for the mobile client.
    """
    
    # --- 1. Normalize ---
    clean_command = user_input.strip().lower()
    
    # --- 2. Decode & 3. Route ---
    history = mem.get_recent_chat(limit=10)
    intent, facts = conscious_subconscious_process(clean_command, history=history)
    
    action = intent.get("action", "general_chat")
    target = intent.get("target", "")
    
    # --- 4. Validate ---
    valid = True
    reason = "Validated."
    action_decision = "execute"
    
    if clean_command == last_command:
        valid = False; reason = "Duplicate command detected."; action_decision = "reject"
    
    if action == "general_chat" and not intent.get("response"):
        valid = True; reason = "Forwarded to LLM."; action_decision = "execute"
    
    # --- 5. Plan ---
    steps = [
        {"step": 1, "action": f"Routing to {action}", "target": target}
    ]
    
    # --- 6. Memory Update ---
    # Store LLM extracted subconscious facts
    if facts:
        for f in facts:
            key, val = f.get("key"), f.get("value")
            if key and val:
                mem.learn_fact(key, val, fact_type=f.get("type", "personal"), priority=f.get("priority", 1))

    # Add to history
    mem.add("user", user_input)
    if intent.get("response"):
        mem.add("assistant", intent.get("response"))

    # --- 7. Final Response JSON ---
    return {
        "preprocessing": {"clean_command": clean_command},
        "decoding": {
            "intent": action,
            "entities": {"target": target, "modifier": intent.get("modifier", "")},
            "command_type": "neural",
            "priority": "normal"
        },
        "routing": {
            "route": "cloud_to_mobile",
            "function": action,
            "requires_confirmation": False
        },
        "validation": {
            "valid": valid,
            "reason": reason,
            "action": action_decision
        },
        "execution_plan": {"steps": steps},
        "memory": {"last_command": user_input, "facts_extracted": len(facts)},
        "response": {"text": intent.get("response", ""), "speak": True}
    }
