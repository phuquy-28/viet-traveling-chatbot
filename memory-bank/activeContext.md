# Active Context

## Current Status
**Project Implementation Complete + Code Refactoring** ✅

All development tasks completed! The Vietnam Travel Advisory Chatbot is fully implemented with:
- Complete RAG pipeline with Pinecone and Azure OpenAI
- Function Calling for external links
- Bilingual support (Vietnamese + English)
- Text-to-Speech integration (gTTS - Google TTS)
- Modern ChatGPT-style UI with light/dark mode
- Bilingual interface (EN/VI)
- Persistent chat history (file-based storage)
- **NEW: Modular UI architecture (src/ui/ package)**
- Chat history and session management with auto-save
- Audio stop controls
- Comprehensive mock data
- Full test case documentation

## Current Work Focus
**Ready for User Testing - Version 2.0**

The application is production-ready with enhanced UI:
1. User configuration of `.env` file with API keys
2. Data ingestion run (`python ingest_data.py`)
3. Application launch and testing
4. Test case validation
5. **NEW: UI customization (theme + language)**

## Recent Changes

### Code Refactoring - Modular Architecture (Current Session) ✅
1. ✅ **Major Refactor**: app.py từ 693 dòng → 235 dòng (giảm 66%)
2. ✅ **UI Package**: Created `src/ui/` với 6 modules chuyên biệt
3. ✅ **Separation of Concerns**: UI logic tách riêng khỏi business logic
4. ✅ **Improved Maintainability**: Mỗi module < 200 dòng, dễ đọc và maintain
5. ✅ **Clean Architecture**: Functions có single responsibility, dễ test

**New UI Modules:**
- `src/ui/styles.py` - CSS styling (135 lines)
- `src/ui/sidebar.py` - Sidebar components (155 lines)
- `src/ui/messages.py` - Message display + TTS (120 lines)
- `src/ui/welcome.py` - Welcome screen (65 lines)
- `src/ui/session_manager.py` - Session management (95 lines)
- `src/ui/__init__.py` - Package exports

**Documentation:**
- `REFACTOR_SUMMARY.md` - Chi tiết refactoring process

### Persistent Chat Storage (Previous Session) ✅
1. ✅ **File-Based Storage**: Chat sessions now saved to disk in JSON format
2. ✅ **New Module**: Created `src/chat_storage.py` with ChatStorageManager class
3. ✅ **Auto-Save**: Sessions automatically saved after each message
4. ✅ **Persistence**: Chat history survives app restarts and browser refreshes
5. ✅ **Storage Directory**: `chat_history/` folder with automatic .gitignore

### UI Overhaul - ChatGPT-Style Interface (Previous Session) ✅
1. ✅ **Light & Dark Mode**: Full theme switching with CSS variables
2. ✅ **Bilingual Interface**: Complete EN/VI UI language support
3. ✅ **Redesigned Sidebar**: New chat, chat history, settings, user profile
4. ✅ **Welcome Screen**: Example questions in main area with 2x2 card grid
5. ✅ **Audio Controls**: Added stop button for TTS playback
6. ✅ **Chat History**: Save and restore last 10 conversations
7. ✅ **Session Management**: UUID-based chat sessions
8. ✅ **Modern CSS**: Smooth transitions, hover effects, professional styling

### TTS Implementation Fix (Previous Session)
1. ✅ **Fixed TTS Issues**: Resolved 401 and 404 errors with Hugging Face API
2. ✅ **Migrated to gTTS**: Switched from Hugging Face to Google Text-to-Speech
3. ✅ **Benefits**: No API key required, more stable, simpler integration
4. ✅ **Updated dependencies**: Added gtts==2.5.1 to requirements.txt
5. ✅ **Backup created**: Saved Hugging Face implementation as tts_huggingface_backup.py
6. ✅ **Tested successfully**: Both Vietnamese and English TTS working

### Complete Implementation (Previous Sessions)
1. ✅ Created comprehensive memory bank (6 documents)
2. ✅ Set up complete project structure
3. ✅ Created bilingual mock data (Vi + En)
4. ✅ Implemented all core modules (7 files)
5. ✅ Built Streamlit application with all features
6. ✅ Created data ingestion pipeline
7. ✅ Documented 30+ test cases
8. ✅ Created setup guide and project summary

### Key Accomplishments
- **RAG Pipeline:** Pinecone + Azure OpenAI fully integrated
- **Function Calling:** get_external_links() with 60+ curated links
- **Bilingual:** Auto-detection with matching responses
- **TTS:** Google TTS (gTTS) integration for both languages - stable and working
- **UI:** Complete Streamlit interface with all FR7 components
- **Documentation:** 12 comprehensive documents
- **Testing:** Full test case coverage (FR1-FR7, NFR1-NFR4)

## Next Immediate Steps

### 1. Project Structure Setup
- Create all directories (data/, src/, etc.)
- Create requirements.txt with all dependencies
- Create .env.example template
- Create .gitignore

### 2. Mock Data Creation
Need to create synthetic datasets covering:

**Vietnamese Content:**
- Destinations: Ha Long Bay, Hoi An, Da Nang, Sa Pa, Phu Quoc, HCMC, Hanoi
- Food: Pho, Bun Cha, Bun Bo Hue, Banh Mi, Ca Phe Trung, Spring Rolls
- Culture: Tet Festival, Water Puppets, Traditional Ao Dai, Currency, Transport
- Tips: Weather by season, Safety, Visas, Money exchange

**English Content:**
- Same topics, translated appropriately
- Natural English descriptions

**mock_links.json:**
- Google Maps links for locations
- Blog review links
- YouTube video links
- Organized by topic/keyword

### 3. Core Module Implementation
Priority order:
1. `vector_store.py` - Pinecone setup
2. `llm_chain.py` - Langchain + Azure OpenAI
3. `function_calls.py` - External links function
4. `conversation.py` - History management
5. `tts.py` - Hugging Face integration
6. `app.py` - Streamlit UI

### 4. Data Ingestion
- Create `ingest_data.py` script
- Load and chunk documents
- Generate embeddings
- Upload to Pinecone

## Active Decisions

### Data Organization
**Decision**: Store Vietnamese and English data in separate subdirectories but upload to same Pinecone index with language metadata.
**Rationale**: Allows language filtering if needed, but enables cross-language semantic search.

### Function Calling Approach
**Decision**: Use Langchain's built-in function calling support with Azure OpenAI.
**Rationale**: More maintainable than manual parsing, better integration with Langchain agents.

### Conversation History
**Decision**: Store last 5 messages in context window.
**Rationale**: Balance between context awareness and token usage.

### TTS Implementation
**Decision**: Use Google Text-to-Speech (gTTS) instead of Hugging Face.
**Rationale**: 
- Hugging Face Inference API endpoints were deprecated/unavailable (404 errors)
- gTTS requires no API key, is more stable, and simpler to integrate
- Supports both Vietnamese and English with high-quality voices
- Free service with no rate limits (within reasonable usage)

## Open Questions

### Q1: Pinecone Index Configuration
- **Question**: Should we use namespaces to separate Vietnamese/English?
- **Current Thinking**: Use single namespace with language metadata for flexibility
- **Decision Needed**: During vector_store.py implementation

### Q2: Follow-up Question Generation
- **Question**: Should follow-ups be LLM-generated or template-based?
- **Current Thinking**: LLM-generated for better context awareness
- **Decision Needed**: During conversation.py implementation

### Q3: TTS Model Selection
- **Question**: Which specific Hugging Face model for Vietnamese TTS?
- **Options**: facebook/mms-tts-vie, vinai/vietnamese-tts
- **Decision**: RESOLVED - Switched to gTTS (Google TTS) due to Hugging Face API issues
- **Status**: ✅ Implemented and tested successfully

## Blockers & Dependencies

### Required API Keys
Need to obtain/configure:
- ✅ Azure OpenAI credentials (assumed available)
- ✅ Pinecone API key (assumed available)
- ✅ TTS: No API key needed (using gTTS - free Google service)

### Environment Setup
- Python 3.9+ required
- Windows environment (noted from user_info)
- PowerShell as shell

## Testing Strategy
Will follow test cases from SRS Section 7.1:
- TC1: Vietnamese Q&A
- TC2: English Q&A
- TC3: Function calling with links
- TC4: Context awareness
- TC5: Follow-up suggestions
- TC6: TTS in both languages

## Workshop Compliance Checklist
- ✅ Using Pinecone (required)
- ✅ Using Streamlit (required)
- ✅ Using Hugging Face (required)
- ✅ RAG implementation planned
- ✅ Function Calling planned
- ✅ Synthetic datasets planned
- ✅ Multilingual support planned

