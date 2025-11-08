"""Sidebar Display Components"""

import streamlit as st
from .session_manager import create_new_chat, load_chat_session, delete_chat_session


def display_sidebar():
    """Display ChatGPT-style sidebar with chat history and user profile"""
    ui_lang = st.session_state.get("ui_lang", "en")
    
    with st.sidebar:
        # 0. Logo and Title (Top)
        _display_logo(ui_lang)
        
        st.markdown("---")
        
        # 1. New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            create_new_chat()
        
        st.markdown("---")
        
        # 2. Chat History Section (Middle - takes most space)
        _display_chat_history(ui_lang)
        
        # Spacer to push settings and profile to bottom
        st.markdown("<br>" * 5, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # 3. Settings (Collapsed in expander)
        _display_settings(ui_lang)
        
        # 4. User Profile at bottom
        _display_user_profile()


def _display_logo(ui_lang: str):
    """Display app logo and title
    
    Args:
        ui_lang: Current UI language ('en' or 'vi')
    """
    title_text = "Vietnam Travel" if ui_lang == "en" else "Du Lịch Việt Nam"
    subtitle_text = "Your AI Travel Assistant" if ui_lang == "en" else "Trợ Lý Du Lịch AI"
    
    st.markdown(f"""
    <div style='text-align: center; padding: 0.5rem 0 0.25rem 0;'>
        <div style='font-size: 2.5rem; margin-bottom: 0.25rem;'>🇻🇳</div>
        <h2 style='margin: 0; font-size: 1.1rem; font-weight: 600;'>{title_text}</h2>
        <p style='margin: 0; font-size: 0.8rem; color: #666; margin-top: 0.1rem;'>{subtitle_text}</p>
    </div>
    """, unsafe_allow_html=True)


def _display_chat_history(ui_lang: str):
    """Display chat history section
    
    Args:
        ui_lang: Current UI language ('en' or 'vi')
    """
    if ui_lang == "en":
        st.subheader("💬 Chat History")
    else:
        st.subheader("💬 Lịch sử trò chuyện")
    
    # Display chat history with delete buttons
    if "chat_sessions" in st.session_state and st.session_state.chat_sessions:
        # Add CSS for text truncation - force no wrap
        st.markdown("""
        <style>
        /* Force chat history buttons to never wrap */
        div[data-testid="column"] button {
            padding: 0.25rem 0.5rem !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            display: block !important;
        }
        
        /* Ensure button content doesn't wrap */
        div[data-testid="column"] button > div {
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            max-width: 100% !important;
        }
        
        /* Target the paragraph inside button */
        div[data-testid="column"] button p {
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            margin: 0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        for session_id, session_data in reversed(list(st.session_state.chat_sessions.items())[-10:]):
            # Get first user message as preview
            preview = session_data.get("preview", "New conversation")
            timestamp = session_data.get("timestamp", "")
            is_active = session_id == st.session_state.get("current_chat_id")
            
            # Create columns: 85% for chat button, 15% for delete button
            col1, col2 = st.columns([0.85, 0.15])
            
            with col1:
                # Chat button with full preview (CSS will handle truncation)
                if st.button(
                    f"{'📌' if is_active else '💬'} {preview}",
                    key=f"chat_{session_id}",
                    use_container_width=True,
                    help=timestamp
                ):
                    load_chat_session(session_id)
            
            with col2:
                # Delete button
                if st.button("🗑️", key=f"delete_{session_id}", help="Delete chat"):
                    delete_chat_session(session_id)
    else:
        if ui_lang == "en":
            st.caption("No chat history yet")
        else:
            st.caption("Chưa có lịch sử")


def _display_settings(ui_lang: str):
    """Display settings section
    
    Args:
        ui_lang: Current UI language ('en' or 'vi')
    """
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


def _display_user_profile():
    """Display user profile at bottom of sidebar"""
    st.markdown("""
    <div class="user-profile">
        <div class="user-avatar">VT</div>
        <div>
            <div class="user-name" style="font-weight: 500; font-size: 14px;">Vietnam Traveler</div>
            <div class="user-plan" style="font-size: 12px;">Free Plan</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

