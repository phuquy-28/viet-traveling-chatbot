"""Chat Storage Manager - File System based chat history storage

This module handles saving and loading chat sessions to/from the file system
using JSON format for persistence across sessions.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ChatStorageManager:
    """Manages chat session storage in file system"""
    
    def __init__(self, storage_dir: str = "chat_history"):
        """Initialize chat storage manager
        
        Args:
            storage_dir: Directory to store chat session files
        """
        self.storage_dir = Path(storage_dir)
        self._ensure_storage_dir()
    
    def _ensure_storage_dir(self):
        """Create storage directory if it doesn't exist"""
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Create .gitignore to avoid committing chat history
        gitignore_path = self.storage_dir / ".gitignore"
        if not gitignore_path.exists():
            gitignore_path.write_text("# Ignore all chat history files\n*.json\n")
    
    def _get_session_file_path(self, session_id: str) -> Path:
        """Get file path for a session
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Path object for the session file
        """
        # Sanitize session_id to be filesystem-safe
        safe_id = "".join(c for c in session_id if c.isalnum() or c in ('-', '_'))
        return self.storage_dir / f"{safe_id}.json"
    
    def save_session(self, session_id: str, session_data: Dict) -> bool:
        """Save a chat session to file
        
        Args:
            session_id: Unique session identifier
            session_data: Dictionary containing session data
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_session_file_path(session_id)
            
            # Add metadata
            session_data_with_meta = {
                "session_id": session_id,
                "created_at": session_data.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M")),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "data": session_data
            }
            
            # Write to file
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(session_data_with_meta, f, ensure_ascii=False, indent=2)
            
            return True
        except Exception as e:
            print(f"[ChatStorage] Error saving session {session_id}: {e}")
            return False
    
    def load_session(self, session_id: str) -> Optional[Dict]:
        """Load a chat session from file
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            Session data dictionary or None if not found
        """
        try:
            file_path = self._get_session_file_path(session_id)
            
            if not file_path.exists():
                return None
            
            with open(file_path, 'r', encoding='utf-8') as f:
                session_data_with_meta = json.load(f)
            
            return session_data_with_meta.get("data")
        except Exception as e:
            print(f"[ChatStorage] Error loading session {session_id}: {e}")
            return None
    
    def load_all_sessions(self) -> Dict[str, Dict]:
        """Load all chat sessions from storage
        
        Returns:
            Dictionary mapping session_id to session data
        """
        sessions = {}
        
        try:
            # Get all JSON files in storage directory
            json_files = list(self.storage_dir.glob("*.json"))
            
            for file_path in json_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        session_data_with_meta = json.load(f)
                    
                    session_id = session_data_with_meta.get("session_id")
                    session_data = session_data_with_meta.get("data")
                    
                    if session_id and session_data:
                        sessions[session_id] = session_data
                except Exception as e:
                    print(f"[ChatStorage] Error loading file {file_path}: {e}")
                    continue
            
            print(f"[ChatStorage] Loaded {len(sessions)} chat sessions from storage")
            return sessions
        except Exception as e:
            print(f"[ChatStorage] Error loading sessions: {e}")
            return {}
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a chat session file
        
        Args:
            session_id: Unique session identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            file_path = self._get_session_file_path(session_id)
            
            if file_path.exists():
                file_path.unlink()
                return True
            return False
        except Exception as e:
            print(f"[ChatStorage] Error deleting session {session_id}: {e}")
            return False
    
    def get_all_session_ids(self) -> List[str]:
        """Get list of all session IDs
        
        Returns:
            List of session IDs
        """
        try:
            json_files = list(self.storage_dir.glob("*.json"))
            session_ids = []
            
            for file_path in json_files:
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        session_data_with_meta = json.load(f)
                    session_id = session_data_with_meta.get("session_id")
                    if session_id:
                        session_ids.append(session_id)
                except:
                    continue
            
            return session_ids
        except Exception as e:
            print(f"[ChatStorage] Error getting session IDs: {e}")
            return []
    
    def clear_all_sessions(self) -> int:
        """Delete all chat session files
        
        Returns:
            Number of sessions deleted
        """
        try:
            json_files = list(self.storage_dir.glob("*.json"))
            count = 0
            
            for file_path in json_files:
                try:
                    file_path.unlink()
                    count += 1
                except:
                    continue
            
            print(f"[ChatStorage] Cleared {count} chat sessions")
            return count
        except Exception as e:
            print(f"[ChatStorage] Error clearing sessions: {e}")
            return 0

