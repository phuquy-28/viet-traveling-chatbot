"""Welcome Screen Component"""

import streamlit as st


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
    examples = _get_example_questions(ui_lang)
    
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


def _get_example_questions(ui_lang: str) -> list:
    """Get example questions based on UI language
    
    Args:
        ui_lang: Current UI language ('en' or 'vi')
        
    Returns:
        List of example question dictionaries
    """
    if ui_lang == "en":
        return [
            {"icon": "🏖️", "title": "Destinations", "text": "What's the best time to visit Ha Long Bay?"},
            {"icon": "🍜", "title": "Food", "text": "Recommend good pho restaurants in Hanoi"},
            {"icon": "🎭", "title": "Culture", "text": "Tell me about Vietnamese water puppetry"},
            {"icon": "🗺️", "title": "Travel Tips", "text": "How do I get around in Saigon?"},
        ]
    else:
        return [
            {"icon": "🏖️", "title": "Điểm đến", "text": "Thời tiết ở Sa Pa tháng 12 như thế nào?"},
            {"icon": "🍜", "title": "Ẩm thực", "text": "Gợi ý quán bún chả ngon ở Hà Nội"},
            {"icon": "🎭", "title": "Văn hóa", "text": "Tết Nguyên Đán là gì?"},
            {"icon": "🗺️", "title": "Thông tin", "text": "Cần visa để đến Việt Nam không?"},
        ]

