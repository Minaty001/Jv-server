"""
neural_core/src/memory.py — JARVIS Neural Memory (MongoDB Edition)
Persistent, cloud-synced memory for Render.com deployment.
"""
import pymongo
from typing import List, Dict, Optional
import time
from neural_core.config.config import MONGO_URI

class Memory:
    """
    Unified neural memory manager for the JARVIS backend.
    Uses MongoDB for high availability and cross-device synchronization.
    """
    
    def __init__(self, db_name="jarvis"):
        """
        Initialize the MongoDB client and select collections.
        
        Args:
            db_name (str): The name of the database to use.
        """
        self._client = pymongo.MongoClient(MONGO_URI)
        self._db = self._client[db_name]
        
        # Collections
        self._history = self._db["chat_history"]
        self._facts = self._db["personal_facts"]
        self._tasks = self._db["task_logs"]
    
    def add(self, role: str, content: str):
        """
        Add a new message to the chat history.
        
        Args:
            role (str): The role of the speaker (user/assistant).
            content (str): The message content.
        """
        self._history.insert_one({
            "role": role,
            "content": str(content),
            "timestamp": time.time()
        })
        
    def get_recent_chat(self, limit: int = 10) -> List[Dict]:
        """
        Fetch a sliding window of recent chat history.
        
        Args:
            limit (int): The maximum number of messages to retrieve.
            
        Returns:
            List[Dict]: List of message objects.
        """
        cursor = self._history.find({}, {"_id": 0}).sort("timestamp", -1).limit(limit)
        return list(reversed(list(cursor)))
    
    def learn_fact(self, key: str, value: str, fact_type="personal", priority=1):
        """
        Store neural facts about the owner or environment.
        
        Args:
            key (str): Fact key (e.g., 'name').
            value (str): Fact value.
            fact_type (str): Category of the fact.
            priority (int): Importance level.
        """
        self._facts.update_one(
            {"key": key},
            {"$set": {
                "value": str(value),
                "type": fact_type,
                "priority": priority,
                "updated_at": time.time()
            }},
            upsert=True
        )
        
    def get_facts(self) -> List[Dict]:
        """Fetch all learned facts for LLM context injection."""
        return list(self._facts.find({}, {"_id": 0}))

    def add_task(self, command: str, status: str):
        """Log task execution for reliability tracking."""
        self._tasks.insert_one({
            "command": str(command),
            "status": str(status),
            "timestamp": time.time()
        })

    def clear(self):
        """Clear all session memory (Reset)."""
        self._history.delete_many({})
        self._facts.delete_many({})
        self._tasks.delete_many({})
