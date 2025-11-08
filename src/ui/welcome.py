"""Welcome Screen Component"""

import streamlit as st


def display_welcome_screen():
    """Display welcome screen with example questions in main area"""
    ui_lang = st.session_state.get("ui_lang", "en")
    
    # Title - using native Streamlit components only
    if ui_lang == "en":
        st.title("🇻🇳 Welcome to Vietnam Travel Chatbot")
        st.subheader("Your AI-powered Vietnamese travel assistant")
    else:
        st.title("🇻🇳 Chào mừng đến với Vietnam Travel Chatbot")
        st.subheader("Trợ lý du lịch Việt Nam được hỗ trợ bởi AI")
    
    st.divider()
    
    # Example questions in grid - using native Streamlit components
    examples = _get_example_questions(ui_lang)
    
    # Display examples in 2x2 grid with styled cards
    col1, col2 = st.columns(2, gap="medium")
    
    for i, example in enumerate(examples):
        col = col1 if i % 2 == 0 else col2
        
        with col:
            # Card with tag and subtext (info only, not clickable)
            st.markdown(
                f"""
                <div style='padding: 16px; background-color: #f7f7f8; border-radius: 12px; border: 1px solid #e5e5e5; margin-bottom: 12px;'>
                    <div style='font-size: 16px; font-weight: 600; color: #1f1f1f; margin-bottom: 8px;'>
                        {example['icon']} {example['title']}
                    </div>
                    <div style='font-size: 14px; color: #666; line-height: 1.4;'>
                        {example['text']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Action button below card - native Streamlit (secondary type for neutral colors)
            if st.button(
                example['text'],
                key=f"example_{i}",
                use_container_width=True,
                type="secondary"
            ):
                st.session_state.current_input = example['text']
                st.rerun()
            
            # Spacing between card groups
            st.markdown("<div style='margin-bottom: 24px;'></div>", unsafe_allow_html=True)


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

