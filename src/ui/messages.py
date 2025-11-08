"""Message Display Components"""

import streamlit as st
import base64
import uuid


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
            _display_tts_controls(content, language, message_id)


def _display_tts_controls(content: str, language: str, message_id: str):
    """Display TTS control buttons (play/stop)
    
    Args:
        content: Message content to convert to speech
        language: Message language
        message_id: Unique message identifier
    """
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

