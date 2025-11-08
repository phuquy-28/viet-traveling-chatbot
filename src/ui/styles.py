"""CSS Styles for the application"""

import streamlit as st


def load_custom_css():
    """Load minimal CSS - using native Streamlit styling to avoid deployment issues"""
    # Minimal CSS only for essential fixes - no custom HTML/JS needed
    st.markdown("""
    <style>
    /* Hide Streamlit branding only - keep everything else native */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

