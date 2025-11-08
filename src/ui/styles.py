"""CSS Styles for the application"""

import streamlit as st


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

