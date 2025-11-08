"""Message Display Components"""

import streamlit as st


def display_message(role: str, content: str, show_tts: bool = False, 
                   language: str = "english", message_id: str = None):
    """Display a chat message with optional TTS using native Streamlit audio player
    
    Args:
        role: 'user' or 'assistant'
        content: Message content
        show_tts: Whether to show TTS button
        language: Message language
        message_id: Unique message identifier
    """
    with st.chat_message(role):
        st.markdown(content)
        
        # TTS controls for assistant messages - simplified, no JavaScript
        if show_tts and role == "assistant" and message_id:
            _display_tts_controls(content, language, message_id)


def _display_tts_controls(content: str, language: str, message_id: str):
    """Display TTS control using native Streamlit audio player (no custom JS)
    
    Args:
        content: Message content to convert to speech
        language: Message language
        message_id: Unique message identifier
    """
    # Simple button to generate audio
    if st.button("🔊 Play Audio", key=f"tts_play_{message_id}", help="Listen to this message"):
        try:
            tts_manager = st.session_state.tts_manager
            audio_bytes = tts_manager.text_to_speech(content, language)
            
            if audio_bytes:
                # Use native Streamlit audio player - no custom HTML/JS
                st.audio(audio_bytes, format='audio/mp3')
            else:
                st.warning("Could not generate audio")
        except Exception as e:
            st.error(f"Audio generation failed: {str(e)}")


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

