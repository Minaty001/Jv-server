"""
neural_core/app.py — JARVIS Neural API Server (Render.com)
Cognitive Gateway for high-level reasoning and intent decoding.
"""

from flask import Flask, request, jsonify
from neural_core.src.command_processor import process_command
from neural_core.src.memory import Memory
from neural_core.src.brain import ask_llm
from neural_core.config.config import PORT
import os

app = Flask(__name__)
mem = Memory()

def print_branded_header():
    """Print the professional system startup header."""
    print("\n" + "═"*60)
    print("  🧠 JARVIS NEURAL BACKEND core v4.1 (Official)")
    print("     DESIGNED AND ENGINEERED BY SHANU")
    print("  Status: AGENT_ACTIVE | Role: CLOUD_COGNITIVE_HUB")
    print("═"*60 + "\n")

@app.route("/", methods=["GET"])
def health():
    """System health and identity verification endpoint."""
    return jsonify({
        "status": "online",
        "identity": "JARVIS by Shanu",
        "version": "4.1.0",
        "memory_sync": "active"
    })

@app.route("/process", methods=["POST"])
def structured_process():
    """Primary 7-Stage Neural Gateway for command decoding and planning."""
    data = request.json or {}
    user_input = data.get("user_input", "").strip()
    last_command = data.get("last_command", "").strip()
    system_state = data.get("system_state", {})

    if not user_input:
        return jsonify({"validation": {"valid": False, "action": "reject", "reason": "Empty input"}})

    # Execute the 7-stage engine
    result = process_command(user_input, last_command=last_command, system_state=system_state)
    return jsonify(result)

@app.route("/history", methods=["GET"])
def get_history():
    """Retrieve recent neural memory logs."""
    limit = int(request.args.get("limit", 20))
    return jsonify(mem.get_recent_chat(limit=limit))

@app.route("/brain", methods=["POST"])
def standalone_brain():
    """Direct LLM Brain access for complex reasoning tasks."""
    data = request.json or {}
    messages = data.get("messages", [])
    history = mem.get_recent_chat(limit=10)
    response = ask_llm(messages, history=history)
    return jsonify({"reply": response})

@app.route("/clear", methods=["POST"])
def clear_memory():
    """Wipe current session memory (Requires authorization in production)."""
    mem.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    print_branded_header()
    app.run(host="0.0.0.0", port=PORT, debug=False)
