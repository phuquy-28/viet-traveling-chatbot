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

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.vector_store import VectorStoreManager
from src.llm_chain import LLMChainManager
from src.conversation import ConversationManager
from src.tts import TTSManager
from src.utils import load_env_file, validate_environment, format_error_message


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
    
    print("[APP] ✅ All components initialized successfully\n")
    return vs_manager, llm_manager, tts_manager


def display_welcome_message():
    """Display welcome message in sidebar"""
    st.sidebar.title("🇻🇳 Vietnam Travel Chatbot")
    st.sidebar.markdown("""
    Welcome to your AI-powered Vietnamese travel assistant!
    
    **I can help you with:**
    - 🏖️ Destination recommendations
    - 🍜 Vietnamese cuisine guide
    - 🎭 Cultural information
    - 🗺️ Travel tips & planning
    
    **Languages:** Vietnamese & English
    
    ---
    """)


def display_example_questions():
    """Display example questions in sidebar"""
    st.sidebar.subheader("💡 Example Questions")
    
    examples_en = [
        "What's the best time to visit Ha Long Bay?",
        "Recommend good pho restaurants in Hanoi",
        "Tell me about Vietnamese water puppetry",
        "How do I get around in Saigon?"
    ]
    
    examples_vi = [
        "Thời tiết ở Sa Pa tháng 12 như thế nào?",
        "Gợi ý quán bún chả ngon ở Hà Nội",
        "Tết Nguyên Đán là gì?",
        "Cần visa để đến Việt Nam không?"
    ]
    
    with st.sidebar.expander("🇬🇧 English Examples"):
        for ex in examples_en:
            if st.button(ex, key=f"en_{ex}"):
                st.session_state.current_input = ex
    
    with st.sidebar.expander("🇻🇳 Vietnamese Examples"):
        for ex in examples_vi:
            if st.button(ex, key=f"vi_{ex}"):
                st.session_state.current_input = ex


def display_settings():
    """Display settings in sidebar"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Settings")
    
    if st.sidebar.button("🗑️ Clear Chat History"):
        st.session_state.conversation_manager.clear_history()
        st.session_state.messages = []
        st.rerun()
    
    # Display environment status
    with st.sidebar.expander("🔧 System Status"):
        validation = validate_environment(verbose=False)  # Silent validation
        
        required_ok = all([
            validation.get("AZURE_OPENAI_API_KEY", False),
            validation.get("PINECONE_API_KEY", False)
        ])
        
        if required_ok:
            st.success("✅ Core systems operational")
        else:
            st.error("❌ Configuration issues detected")
        
        # TTS is always available with gTTS (no API key needed)
        tts_ok = tts_manager.is_available() if 'tts_manager' in st.session_state else True
        if tts_ok:
            st.info("🔊 TTS enabled (Google TTS)")


def display_message(role: str, content: str, show_tts: bool = False, 
                   language: str = "english", message_id: str = None):
    """Display a chat message with optional TTS
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        show_tts: Whether to show TTS button
        language: Message language
        message_id: Unique message identifier
    """
    with st.chat_message(role):
        st.markdown(content)
        
        # TTS button for assistant messages
        if show_tts and role == "assistant" and message_id:
            col1, col2 = st.columns([1, 10])
            with col1:
                if st.button("🔊", key=f"tts_{message_id}", help="Listen to this message"):
                    with st.spinner("Generating audio..."):
                        try:
                            tts_manager = st.session_state.tts_manager
                            audio_bytes = tts_manager.text_to_speech(content, language)
                            
                            if audio_bytes:
                                # Convert to base64 for auto-play
                                audio_base64 = base64.b64encode(audio_bytes).decode()
                                audio_html = f"""
                                <audio autoplay>
                                    <source src="data:audio/wav;base64,{audio_base64}" type="audio/wav">
                                </audio>
                                """
                                st.markdown(audio_html, unsafe_allow_html=True)
                                st.success("Playing audio...")
                            else:
                                st.error("TTS generation failed")
                        except Exception as e:
                            st.error(f"TTS error: {str(e)}")


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
    
    # Initialize session state
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
    
    # Display sidebar
    display_welcome_message()
    display_example_questions()
    display_settings()
    
    # Main chat interface
    st.title("🇻🇳 Vietnam Travel Advisory Chatbot")
    st.caption("Ask me anything about traveling in Vietnam! | Hỏi tôi bất cứ điều gì về du lịch Việt Nam!")
    
    # Initialize components
    try:
        vs_manager, llm_manager, tts_manager = initialize_components()
        st.session_state.vs_manager = vs_manager
        st.session_state.llm_manager = llm_manager
        st.session_state.tts_manager = tts_manager
    except Exception as e:
        st.error(f"❌ Failed to initialize system: {str(e)}")
        st.info("Please check your .env configuration and ensure all API keys are set correctly.")
        st.stop()
    
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
    if st.session_state.messages and st.session_state.followup_questions:
        display_followup_questions(
            st.session_state.followup_questions,
            st.session_state.current_language
        )
    
    # Chat input
    user_input = st.chat_input(
        "Type your question here... | Nhập câu hỏi của bạn...",
        key="chat_input"
    )
    
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
            with st.spinner("Thinking..."):
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
                        with st.expander("🔗 External Links Retrieved"):
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

