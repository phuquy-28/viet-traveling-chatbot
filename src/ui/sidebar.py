"""Sidebar Display Components"""

import streamlit as st
from .session_manager import create_new_chat, load_chat_session, delete_chat_session


def display_sidebar():
    """Display sidebar with native Streamlit components - no custom HTML/CSS"""
    ui_lang = st.session_state.get("ui_lang", "en")
    
    with st.sidebar:
        # 0. Logo and Title (Top) - using native components
        _display_logo(ui_lang)
        
        st.divider()
        
        # 1. New Chat Button
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            create_new_chat()
        
        st.divider()
        
        # 2. Chat History Section (Middle - takes most space)
        _display_chat_history(ui_lang)
        
        st.divider()
        
        # 3. Settings (Collapsed in expander)
        _display_settings(ui_lang)
        
        # 4. User Profile at bottom - simplified
        _display_user_profile()


def _display_logo(ui_lang: str):
    """Display app logo and title using native Streamlit components
    
    Args:
        ui_lang: Current UI language ('en' or 'vi')
    """
    title_text = "Vietnam Travel" if ui_lang == "en" else "Du Lịch Việt Nam"
    subtitle_text = "Your AI Travel Assistant" if ui_lang == "en" else "Trợ Lý Du Lịch AI"
    
    # Centered logo with larger emoji using minimal HTML for alignment
    st.markdown(
        f"""
        <div style='text-align: center;'>
            <div style='font-size: 4rem; line-height: 1.2;'>🇻🇳</div>
            <div style='font-size: 1.2rem; font-weight: 600; margin-top: 0.5rem;'>{title_text}</div>
            <div style='font-size: 0.85rem; color: #666; margin-top: 0.25rem;'>{subtitle_text}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def _display_chat_history(ui_lang: str):
    """Display chat history section using native components
    
    Args:
        ui_lang: Current UI language ('en' or 'vi')
    """
    if ui_lang == "en":
        st.subheader("💬 Chat History")
    else:
        st.subheader("💬 Lịch sử trò chuyện")
    
    # Add minimal CSS to ensure single-line display in sidebar
    st.markdown("""
        <style>
        /* Ensure chat history buttons stay on single line */
        [data-testid="stSidebar"] button {
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        [data-testid="stSidebar"] button p {
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display chat history with delete buttons - simplified layout
    if "chat_sessions" in st.session_state and st.session_state.chat_sessions:
        for session_id, session_data in reversed(list(st.session_state.chat_sessions.items())[-10:]):
            # Get first user message as preview
            preview = session_data.get("preview", "New conversation")
            
            # Truncate preview to 22 characters to ensure single line in sidebar
            if len(preview) > 22:
                preview = preview[:19] + "..."
            
            timestamp = session_data.get("timestamp", "")
            is_active = session_id == st.session_state.get("current_chat_id")
            
            # Create columns: 80% for chat button, 20% for delete button
            col1, col2 = st.columns([0.8, 0.2])
            
            with col1:
                # Chat button - will be truncated by CSS if still too long
                button_label = f"{'📌' if is_active else '💬'} {preview}"
                if st.button(
                    button_label,
                    key=f"chat_{session_id}",
                    use_container_width=True,
                    help=f"{session_data.get('preview', 'New conversation')}\n{timestamp}"
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
    """Display user profile with avatar using minimal HTML for styling"""
    st.divider()
    
    # User profile with circular avatar
    st.markdown(
        """
        <div style='display: flex; align-items: center; gap: 12px; padding: 8px 0;'>
            <div style='width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 16px; flex-shrink: 0;'>
                VT
            </div>
            <div style='flex: 1; min-width: 0;'>
                <div style='font-weight: 600; font-size: 14px; color: #1f1f1f; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;'>
                    Vietnam Traveler
                </div>
                <div style='font-size: 12px; color: #666; margin-top: 2px;'>
                    Free Plan
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

