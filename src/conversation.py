"""Conversation Management for Chat History"""

from typing import List, Dict, Any


class ConversationManager:
    """Manages conversation history and context"""
    
    def __init__(self, max_history: int = 10):
        """Initialize conversation manager
        
        Args:
            max_history: Maximum number of messages to keep in history
        """
        self.max_history = max_history
        self.messages: List[Dict[str, str]] = []
    
    def add_message(self, role: str, content: str):
        """Add a message to history
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
        """
        self.messages.append({
            "role": role,
            "content": content
        })
        
        # Trim history if too long
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]
    
    def get_history(self, last_n: int = 5) -> List[Dict[str, str]]:
        """Get conversation history
        
        Args:
            last_n: Number of recent messages to return
            
        Returns:
            List of message dictionaries
        """
        return self.messages[-last_n:] if self.messages else []
    
    def clear_history(self):
        """Clear all conversation history"""
        self.messages = []
    
    def get_context_string(self, last_n: int = 5) -> str:
        """Get conversation history as a formatted string
        
        Args:
            last_n: Number of recent messages to include
            
        Returns:
            Formatted conversation string
        """
        recent_messages = self.get_history(last_n)
        
        if not recent_messages:
            return "No conversation history"
        
        context_parts = []
        for msg in recent_messages:
            role = "User" if msg["role"] == "user" else "Assistant"
            context_parts.append(f"{role}: {msg['content']}")
        
        return "\n".join(context_parts)
    
    def format_for_display(self) -> List[Dict[str, str]]:
        """Format messages for UI display
        
        Returns:
            List of formatted message dictionaries
        """
        return [
            {
                "role": msg["role"],
                "content": msg["content"]
            }
            for msg in self.messages
        ]

