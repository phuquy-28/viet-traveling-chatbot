# Product Context

## Problem Statement
Travelers (both domestic and international) face challenges in finding comprehensive, reliable, and personalized travel information about Vietnam. They need a tool that can:
- Answer questions naturally in their preferred language
- Provide accurate information without hallucinations
- Suggest personalized itineraries and recommendations
- Link to relevant external resources
- Work interactively with conversational context

## Solution
An AI-powered travel chatbot that combines:
1. **Semantic Search (RAG)**: Retrieves relevant information from a curated knowledge base
2. **LLM Generation**: Creates natural, contextual responses
3. **Function Calling**: Dynamically fetches external links (maps, reviews, videos)
4. **Voice Output**: Supports audio responses for accessibility

## User Experience Goals

### Conversation Flow
1. User asks a question (Vietnamese or English)
2. System retrieves relevant context from vector store
3. LLM generates accurate response in same language
4. System suggests 2-3 follow-up questions
5. User can listen to response via TTS
6. User can access external links for more details

### Example Interactions

**Scenario 1: Basic Q&A**
- User: "Thời tiết ở Sa Pa tháng 12 như thế nào?"
- Bot: [Retrieves weather info from mock data] + TTS button + Follow-ups

**Scenario 2: Recommendations with Links**
- User: "Recommend good pho restaurants in Hanoi"
- Bot: [Retrieves + calls get_external_links()] + Google Maps + Reviews + TTS

**Scenario 3: Context-Aware Follow-up**
- User: "Tell me about Da Nang"
- Bot: [Provides info]
- User: "What activities can I do there?"
- Bot: [Understands "there" = "Da Nang" from history]

## Key Features

### FR1: Multilingual Support
- Auto-detect Vietnamese or English input
- Respond in the same language
- Support Vietnamese and English TTS

### FR2: Q&A System
- Answer factual questions about destinations, weather, culture, food
- Retrieve from Pinecone vector store
- Minimize hallucinations

### FR3: Recommendations
- Suggest itineraries (e.g., "2-day plan for Da Nang")
- Recommend restaurants, activities
- Personalize based on user context

### FR4: External Links (Function Calling)
- Google Maps links to locations
- Blog/review links
- Social media content (YouTube videos)
- All retrieved via Function Calling mechanism

### FR5: Conversation Management
- Maintain chat history in session
- Context-aware responses
- Auto-generate 2-3 follow-up questions

### FR6: Text-to-Speech
- Play button next to each bot response
- Natural voice in appropriate language
- Hugging Face TTS integration

### FR7: Streamlit UI
- Clean chat interface
- Message history display
- Input box for queries
- Follow-up question buttons
- TTS play buttons
- Display external links clearly

## Non-Functional Goals
- **Performance**: < 5 second response time
- **Usability**: Intuitive, clean interface
- **Reliability**: High accuracy, working links
- **Quality**: Natural TTS voices

