"""Vietnam Travel Advisory Chatbot - Streamlit Application

Main Streamlit application for the Vietnam Travel Chatbot with RAG, 
Function Calling, and Text-to-Speech capabilities.

Usage:
    streamlit run app.py
"""

import streamlit as st
import os
import sys
from pathlib import Path
import base64
import uuid
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.vector_store import VectorStoreManager
from src.llm_chain import LLMChainManager
from src.conversation import ConversationManager
from src.tts import TTSManager
from src.chat_storage import ChatStorageManager
from src.utils import load_env_file, validate_environment, format_error_message


# Page configuration
st.set_page_config(
    page_title="Vietnam Travel Chatbot",
    page_icon="🇻🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Custom CSS for ChatGPT-like interface
def load_custom_css():
    """Load custom CSS for modern ChatGPT-like interface (Light Mode)"""
    # Light mode colors
    colors = {
        "bg_primary": "#ffffff",
        "bg_secondary": "#f7f7f8",
        "bg_sidebar": "#ffffff",
        "text_primary": "#000000",
        "text_secondary": "#666666",
        "border_color": "#e5e5e5",
        "button_hover": "#f7f7f8",
        "chat_user_bg": "#f7f7f8",
        "chat_assistant_bg": "#ffffff"
    }
    
    st.markdown(f"""
    <style>
    /* Apply theme colors */
    .stApp {{
        background-color: {colors['bg_primary']};
        color: {colors['text_primary']};
    }}
    
    /* Main container */
    .main {{
        background-color: {colors['bg_primary']};
        color: {colors['text_primary']};
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {colors['bg_sidebar']};
        border-right: 1px solid {colors['border_color']};
    }}
    
    [data-testid="stSidebar"] * {{
        color: {colors['text_primary']} !important;
    }}
    
    [data-testid="stSidebar"] .stMarkdown {{
        color: {colors['text_primary']};
    }}
    
    /* Example cards in main area */
    .example-card {{
        padding: 16px;
        border-radius: 12px;
        border: 1px solid {colors['border_color']};
        background-color: {colors['bg_secondary']};
        cursor: pointer;
        transition: all 0.2s;
        margin-bottom: 12px;
    }}
    
    .example-card:hover {{
        background-color: {colors['button_hover']};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .example-title {{
        font-size: 16px;
        font-weight: 500;
        color: {colors['text_primary']};
        margin-bottom: 4px;
    }}
    
    .example-text {{
        font-size: 14px;
        color: {colors['text_secondary']};
    }}
    
    /* User profile section */
    .user-profile {{
        padding: 12px;
        border-top: 1px solid {colors['border_color']};
        display: flex;
        align-items: center;
        gap: 10px;
    }}
    
    .user-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }}
    
    .user-name {{
        color: {colors['text_primary']} !important;
    }}
    
    .user-plan {{
        color: {colors['text_secondary']} !important;
    }}
    
    /* Chat messages */
    [data-testid="stChatMessage"] {{
        background-color: transparent;
        border: none;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* Markdown text color */
    .stMarkdown {{
        color: {colors['text_primary']};
    }}
    
    /* Expander styling */
    .streamlit-expanderHeader {{
        background-color: {colors['bg_secondary']};
        color: {colors['text_primary']};
    }}
    </style>
    """, unsafe_allow_html=True)


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


def display_sidebar():
    """Display ChatGPT-style sidebar with chat history and user profile"""
    ui_lang = st.session_state.get("ui_lang", "en")
    
    with st.sidebar:
        # 1. New Chat Button (Top - minimal height)
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            # Create new chat session
            st.session_state.current_chat_id = str(uuid.uuid4())
            st.session_state.conversation_manager.clear_history()
            st.session_state.messages = []
            st.session_state.followup_questions = []
            st.rerun()
        
        st.markdown("---")
        
        # 2. Chat History Section (Middle - takes most space)
        if ui_lang == "en":
            st.subheader("💬 Chat History")
        else:
            st.subheader("💬 Lịch sử trò chuyện")
        
        # Display chat history
        if "chat_sessions" in st.session_state and st.session_state.chat_sessions:
            for session_id, session_data in reversed(list(st.session_state.chat_sessions.items())[-10:]):
                # Get first user message as preview
                preview = session_data.get("preview", "New conversation")
                timestamp = session_data.get("timestamp", "")
                
                # Truncate preview
                if len(preview) > 40:
                    preview = preview[:40] + "..."
                
                is_active = session_id == st.session_state.get("current_chat_id")
                
                if st.button(
                    f"{'📌' if is_active else '💬'} {preview}",
                    key=f"chat_{session_id}",
                    use_container_width=True,
                    help=timestamp
                ):
                    # Load this chat session
                    load_chat_session(session_id)
        else:
            if ui_lang == "en":
                st.caption("No chat history yet")
            else:
                st.caption("Chưa có lịch sử")
        
        # Spacer to push settings and profile to bottom
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 3. Settings (Collapsed in expander)
        settings_label = "⚙️ Settings" if ui_lang == "en" else "⚙️ Cài đặt"
        with st.expander(settings_label, expanded=False):
            # UI Language Selection
            lang_label = "Interface Language" if ui_lang == "en" else "Ngôn ngữ giao diện"
            selected_lang = st.selectbox(
                lang_label,
                ["English", "Tiếng Việt"],
                key="ui_language",
                index=0 if ui_lang == "en" else 1
            )
            if selected_lang != ("English" if ui_lang == "en" else "Tiếng Việt"):
                st.session_state.ui_lang = "en" if selected_lang == "English" else "vi"
                st.rerun()
        
        # 4. User Profile at bottom
        st.markdown("""
        <div class="user-profile">
            <div class="user-avatar">VT</div>
            <div>
                <div class="user-name" style="font-weight: 500; font-size: 14px;">Vietnam Traveler</div>
                <div class="user-plan" style="font-size: 12px;">Free Plan</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def display_welcome_screen():
    """Display welcome screen with example questions in main area"""
    ui_lang = st.session_state.get("ui_lang", "en")
    
    # Title
    if ui_lang == "en":
        st.markdown("# 🇻🇳 Welcome to Vietnam Travel Chatbot")
        st.markdown("### Your AI-powered Vietnamese travel assistant")
    else:
        st.markdown("# 🇻🇳 Chào mừng đến với Vietnam Travel Chatbot")
        st.markdown("### Trợ lý du lịch Việt Nam được hỗ trợ bởi AI")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Example questions in grid
    if ui_lang == "en":
        st.markdown("### 💡 Try asking about...")
        
        examples = [
            {"icon": "🏖️", "title": "Destinations", "text": "What's the best time to visit Ha Long Bay?"},
            {"icon": "🍜", "title": "Food", "text": "Recommend good pho restaurants in Hanoi"},
            {"icon": "🎭", "title": "Culture", "text": "Tell me about Vietnamese water puppetry"},
            {"icon": "🗺️", "title": "Travel Tips", "text": "How do I get around in Saigon?"},
        ]
    else:
        st.markdown("### 💡 Thử hỏi về...")
        
        examples = [
            {"icon": "🏖️", "title": "Điểm đến", "text": "Thời tiết ở Sa Pa tháng 12 như thế nào?"},
            {"icon": "🍜", "title": "Ẩm thực", "text": "Gợi ý quán bún chả ngon ở Hà Nội"},
            {"icon": "🎭", "title": "Văn hóa", "text": "Tết Nguyên Đán là gì?"},
            {"icon": "🗺️", "title": "Thông tin", "text": "Cần visa để đến Việt Nam không?"},
        ]
    
    # Display examples in 2x2 grid
    col1, col2 = st.columns(2)
    
    for i, example in enumerate(examples):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            card_html = f"""
            <div class="example-card">
                <div class="example-title">{example['icon']} {example['title']}</div>
                <div class="example-text">{example['text']}</div>
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)
            
            if st.button(example['text'], key=f"example_{i}", use_container_width=True):
                st.session_state.current_input = example['text']
                st.rerun()


def load_chat_session(session_id: str):
    """Load a previous chat session"""
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


def display_message(role: str, content: str, show_tts: bool = False, 
                   language: str = "english", message_id: str = None):
    """Display a chat message with optional TTS and audio controls
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        show_tts: Whether to show TTS button
        language: Message language
        message_id: Unique message identifier
    """
    with st.chat_message(role):
        st.markdown(content)
        
        # TTS controls for assistant messages
        if show_tts and role == "assistant" and message_id:
            # Initialize audio state for this message
            audio_key = f"audio_playing_{message_id}"
            if audio_key not in st.session_state:
                st.session_state[audio_key] = False
            
            col1, col2, col3 = st.columns([1, 1, 10])
            
            with col1:
                # Play button
                if st.button("🔊", key=f"tts_play_{message_id}", help="Listen to this message"):
                    try:
                        tts_manager = st.session_state.tts_manager
                        audio_bytes = tts_manager.text_to_speech(content, language)
                        
                        if audio_bytes:
                            # Store audio data in session state
                            st.session_state[f"audio_data_{message_id}"] = audio_bytes
                            st.session_state[audio_key] = True
                            
                            # Create unique audio ID
                            audio_id = f"audio_{message_id}_{uuid.uuid4().hex[:8]}"
                            
                            # Convert to base64 for playback
                            audio_base64 = base64.b64encode(audio_bytes).decode()
                            audio_html = f"""
                            <audio id="{audio_id}" autoplay>
                                <source src="data:audio/mpeg;base64,{audio_base64}" type="audio/mpeg">
                            </audio>
                            <script>
                                var audio = document.getElementById('{audio_id}');
                                audio.onended = function() {{
                                    console.log('Audio playback finished');
                                }};
                            </script>
                            """
                            st.markdown(audio_html, unsafe_allow_html=True)
                        else:
                            pass  # Silent fail, just don't play
                    except Exception as e:
                        pass  # Silent fail
            
            with col2:
                # Stop button (only show if audio has been generated)
                if st.session_state.get(f"audio_data_{message_id}"):
                    if st.button("⏹️", key=f"tts_stop_{message_id}", help="Stop audio"):
                        st.session_state[audio_key] = False
                        # Inject JavaScript to stop all audio
                        stop_audio_html = """
                        <script>
                            var audios = document.getElementsByTagName('audio');
                            for(var i = 0; i < audios.length; i++) {
                                audios[i].pause();
                                audios[i].currentTime = 0;
                            }
                        </script>
                        """
                        st.markdown(stop_audio_html, unsafe_allow_html=True)


def display_followup_questions(questions: list, language: str):
    """Display follow-up question buttons
    
    Args:
        questions: List of follow-up questions
        language: Current language
    """
    if not questions:
        return
    
    title = "❓ Suggested questions:" if language == "english" else "❓ Câu hỏi gợi ý:"
    st.markdown(f"**{title}**")
    
    cols = st.columns(len(questions))
    for i, (col, question) in enumerate(zip(cols, questions)):
        with col:
            if st.button(question, key=f"followup_{i}", use_container_width=True):
                st.session_state.current_input = question
                st.rerun()


def main():
    """Main application function"""
    
    # Initialize session state first (before CSS)
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
    
    # Initialize components FIRST (before sidebar)
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
    
    # Load custom CSS (Light Mode only)
    load_custom_css()
    
    # Display sidebar with new ChatGPT-style layout (after loading chat sessions)
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


if __name__ == "__main__":
    main()

