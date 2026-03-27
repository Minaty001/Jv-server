# backend/config.py — JARVIS Neural API Server Configuration
import os

# --- API KEYS (Set in Render Environment Variables) ---
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "your_groq_key_here")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://user:pass@cluster.mongodb.net/jarvis")

# --- MODELS ---
GROQ_CHAT_MODEL = "llama-3.3-70b-versatile"
GROQ_CODING_MODEL = "llama-3.3-70b-versatile"

# --- SERVER ---
PORT = int(os.environ.get("PORT", 8000))
