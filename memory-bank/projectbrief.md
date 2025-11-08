# Project Brief: Vietnam Travel Advisory Chatbot

## Project Overview
Building an intelligent RAG (Retrieval-Augmented Generation) chatbot system for Vietnamese travel advisory using Langchain, Pinecone, and Azure OpenAI. This is a Workshop 4 project focused on implementing advanced AI application engineering concepts.

## Core Objectives
1. **RAG Implementation**: Create a semantic search system using Pinecone vector store with synthetic Vietnamese travel data
2. **Multilingual Support**: Handle both Vietnamese and English queries with appropriate responses
3. **Function Calling**: Implement dynamic link retrieval for locations, restaurants, and activities
4. **Conversational AI**: Maintain chat history and suggest relevant follow-up questions
5. **Text-to-Speech**: Integrate Hugging Face TTS for audio responses

## Target Users
- International tourists planning to visit Vietnam
- Domestic travelers exploring new destinations
- Anyone interested in Vietnamese culture and tourism

## Key Requirements
- **Bilingual**: Vietnamese and English support
- **Context-aware**: Maintain conversation history
- **Accurate**: Minimize hallucinations through RAG
- **Interactive**: TTS support and follow-up suggestions
- **Integrated**: External links via Function Calling

## Success Criteria
- Response time < 5 seconds
- Accurate retrieval from mock data
- Proper language detection and response
- Working TTS for both languages
- Functional external link integration
- Clean and intuitive Streamlit interface

## Tech Stack
- **Framework**: Langchain (orchestration)
- **Vector Store**: Pinecone (required by workshop)
- **LLM**: Azure OpenAI
- **UI**: Streamlit (required by workshop)
- **TTS**: Hugging Face API
- **Language**: Python

## Out of Scope
- Real booking/transaction capabilities
- Real-time data updates
- User authentication
- Payment processing

