"""Session Management Functions"""

import streamlit as st
import uuid
from datetime import datetime


def create_new_chat():
    """Create a new chat session"""
    st.session_state.current_chat_id = str(uuid.uuid4())
    st.session_state.conversation_manager.clear_history()
    st.session_state.messages = []
    st.session_state.followup_questions = []
    st.rerun()


def load_chat_session(session_id: str):
    """Load a previous chat session
    
    Args:
        session_id: Unique session identifier
    """
    if session_id in st.session_state.chat_sessions:
        session_data = st.session_state.chat_sessions[session_id]
        st.session_state.current_chat_id = session_id
        st.session_state.messages = session_data.get("messages", [])
        st.session_state.followup_questions = session_data.get("followup_questions", [])
        
        # Restore conversation history
        st.session_state.conversation_manager.clear_history()
        for msg in st.session_state.messages:
            st.session_state.conversation_manager.add_message(msg["role"], msg["content"])
        
        st.rerun()


def delete_chat_session(session_id: str):
    """Delete a chat session
    
    Args:
        session_id: Unique session identifier
    """
    # Remove from session state
    if session_id in st.session_state.chat_sessions:
        del st.session_state.chat_sessions[session_id]
    
    # Delete from file system
    if "chat_storage" in st.session_state:
        st.session_state.chat_storage.delete_session(session_id)
    
    # If deleting current chat, create new one
    if st.session_state.get("current_chat_id") == session_id:
        create_new_chat()
    else:
        st.rerun()


def save_current_chat():
    """Save current chat session to file system"""
    if not st.session_state.messages:
        return
    
    current_id = st.session_state.get("current_chat_id")
    if not current_id:
        current_id = str(uuid.uuid4())
        st.session_state.current_chat_id = current_id
    
    # Get preview from first user message
    preview = "New conversation"
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            preview = msg["content"]
            break
    
    # Prepare session data
    session_data = {
        "messages": st.session_state.messages.copy(),
        "followup_questions": st.session_state.followup_questions.copy(),
        "preview": preview,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    # Save to file system
    if "chat_storage" in st.session_state:
        st.session_state.chat_storage.save_session(current_id, session_data)
    
    # Also keep in session state for quick access
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}
    st.session_state.chat_sessions[current_id] = session_data

