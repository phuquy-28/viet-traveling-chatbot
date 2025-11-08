"""Vietnam Travel Advisory Chatbot - Streamlit Application

Main Streamlit application for the Vietnam Travel Chatbot with RAG, 
Function Calling, and Text-to-Speech capabilities.

Usage:
    streamlit run app.py
"""

import streamlit as st
import sys
import uuid
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.vector_store import VectorStoreManager
from src.llm_chain import LLMChainManager
from src.conversation import ConversationManager
from src.tts import TTSManager
from src.chat_storage import ChatStorageManager
from src.utils import load_env_file, format_error_message

# Import UI components
from src.ui import (
    load_custom_css,
    display_sidebar,
    display_message,
    display_followup_questions,
    display_welcome_screen,
    save_current_chat
)


# Page configuration
st.set_page_config(
    page_title="Vietnam Travel Chatbot",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def initialize_components():
    """Initialize all components (cached)"""
    print("\n[APP] Starting initialization...")
    load_env_file()
    
    # Initialize components (silent mode)
    vs_manager = VectorStoreManager(verbose=False)
    llm_manager = LLMChainManager(vs_manager, verbose=False)
    tts_manager = TTSManager()
    chat_storage = ChatStorageManager()
    
    print("[APP] ✅ All components initialized successfully\n")
    return vs_manager, llm_manager, tts_manager, chat_storage


def initialize_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "conversation_manager" not in st.session_state:
        st.session_state.conversation_manager = ConversationManager()
    
    if "current_input" not in st.session_state:
        st.session_state.current_input = ""
    
    if "followup_questions" not in st.session_state:
        st.session_state.followup_questions = []
    
    if "current_language" not in st.session_state:
        st.session_state.current_language = "english"
    
    if "ui_lang" not in st.session_state:
        st.session_state.ui_lang = "en"
    
    if "current_chat_id" not in st.session_state:
        st.session_state.current_chat_id = str(uuid.uuid4())
    
    if "chat_sessions" not in st.session_state:
        st.session_state.chat_sessions = {}


def process_user_input(user_input: str, llm_manager, tts_manager):
    """Process user input and generate response
    
    Args:
        user_input: User's input message
        llm_manager: LLM chain manager
        tts_manager: TTS manager
    """
    ui_lang = st.session_state.ui_lang
    
    # Add user message to chat
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    st.session_state.conversation_manager.add_message("user", user_input)
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        thinking_msg = "Thinking..." if ui_lang == "en" else "Đang suy nghĩ..."
        with st.spinner(thinking_msg):
            try:
                # Get chat history
                chat_history = st.session_state.conversation_manager.get_history(last_n=5)
                
                # Run LLM chain
                result = llm_manager.run_chain(user_input, chat_history)
                
                answer = result["answer"]
                language = result["language"]
                function_called = result.get("function_called")
                
                # Display answer
                st.markdown(answer)
                
                # Show function call info if any
                if function_called:
                    expander_title = "🔗 External Links Retrieved" if ui_lang == "en" else "🔗 Liên kết bên ngoài"
                    with st.expander(expander_title):
                        st.info(f"Function called: `{function_called}`")
                        st.markdown(result.get("function_result", ""))
                
                # Add assistant message to chat
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "language": language
                })
                st.session_state.conversation_manager.add_message("assistant", answer)
                st.session_state.current_language = language
                
                # Save current chat session
                save_current_chat()
                
                # Generate follow-up questions
                try:
                    followup_questions = llm_manager.generate_followup_questions(
                        user_input, answer, language
                    )
                    st.session_state.followup_questions = followup_questions
                except Exception as e:
                    print(f"Failed to generate follow-up questions: {e}")
                    st.session_state.followup_questions = []
                
            except Exception as e:
                error_msg = format_error_message(e, st.session_state.current_language)
                st.error(error_msg)
                
                # Add error message
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "language": st.session_state.current_language
                })
    
    # Rerun to show follow-up questions
    st.rerun()


def main():
    """Main application function"""
    
    # Initialize session state
    initialize_session_state()
    
    # Initialize components
    try:
        vs_manager, llm_manager, tts_manager, chat_storage = initialize_components()
        st.session_state.vs_manager = vs_manager
        st.session_state.llm_manager = llm_manager
        st.session_state.tts_manager = tts_manager
        st.session_state.chat_storage = chat_storage
        
        # Load all chat sessions from file system (only once)
        if "chat_sessions_loaded" not in st.session_state:
            st.session_state.chat_sessions = chat_storage.load_all_sessions()
            st.session_state.chat_sessions_loaded = True
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {str(e)}")
        st.info("Please check your .env configuration and ensure all API keys are set correctly.")
        st.stop()
    
    # Load custom CSS
    load_custom_css()
    
    # Display sidebar
    display_sidebar()
    
    # Main chat area - show welcome screen if no messages
    if not st.session_state.messages:
        display_welcome_screen()
    else:
        # Display chat history
        for i, message in enumerate(st.session_state.messages):
            display_message(
                role=message["role"],
                content=message["content"],
                show_tts=message["role"] == "assistant" and tts_manager.is_available(),
                language=message.get("language", "english"),
                message_id=f"msg_{i}"
            )
        
        # Display follow-up questions after last message
        if st.session_state.followup_questions:
            display_followup_questions(
                st.session_state.followup_questions,
                st.session_state.current_language
            )
    
    # Chat input (always visible at bottom)
    ui_lang = st.session_state.ui_lang
    placeholder = "Type your question here..." if ui_lang == "en" else "Nhập câu hỏi của bạn..."
    
    user_input = st.chat_input(placeholder, key="chat_input")
    
    # Handle example question clicks
    if st.session_state.current_input:
        user_input = st.session_state.current_input
        st.session_state.current_input = ""
    
    # Process user input
    if user_input:
        process_user_input(user_input, llm_manager, tts_manager)


if __name__ == "__main__":
    main()
