# System Patterns

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      User (Browser)                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Streamlit Frontend                          │
│  - Chat Interface                                            │
│  - TTS Buttons                                               │
│  - Follow-up Suggestions                                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Langchain Orchestration                      │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  Prompt    │→ │   Retrieval  │→ │   Generation     │    │
│  │  Template  │  │   (Pinecone) │  │  (Azure OpenAI)  │    │
│  └────────────┘  └──────────────┘  └──────────────────┘    │
│                                                               │
│  ┌────────────────────────────────────────────────────┐     │
│  │         Function Calling Handler                   │     │
│  │  - get_external_links(topic)                       │     │
│  │  - Returns: maps, reviews, social media            │     │
│  └────────────────────────────────────────────────────┘     │
└───────────────────────────┬─────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
    ┌──────────────┐  ┌──────────┐  ┌─────────────┐
    │   Pinecone   │  │  Azure   │  │  Google     │
    │ Vector Store │  │  OpenAI  │  │  TTS (gTTS) │
    └──────────────┘  └──────────┘  └─────────────┘
```

## RAG Flow Pattern

```
User Query (Vi/En)
    │
    ▼
[Language Detection]
    │
    ▼
[Embedding Generation] ─────────► Azure OpenAI Embeddings
    │
    ▼
[Vector Search] ────────────────► Pinecone Query
    │                              (Returns top-k docs)
    ▼
[Context + History + Query]
    │
    ▼
[Prompt Construction]
    │
    ▼
[LLM Call] ─────────────────────► Azure OpenAI GPT
    │                              (May trigger Function Call)
    ▼
[Function Call?]
    │
    ├─Yes─► [Execute Function] ──► mock_links.json
    │           │
    │           ▼
    │       [Re-call LLM with function result]
    │           │
    └─No────────┘
    │
    ▼
[Final Response]
    │
    ├─► [Display in UI]
    ├─► [Generate Follow-up Questions]
    └─► [Enable TTS Button]
```

## Key Design Patterns

### 1. RAG Pattern
- **Retrieval**: Semantic search in Pinecone
- **Augmentation**: Add retrieved docs to prompt
- **Generation**: LLM creates answer based on context
- **Benefit**: Reduces hallucinations, grounds answers in data

### 2. Function Calling Pattern
- **Declaration**: Define functions with JSON schema
- **Detection**: LLM decides when to call function
- **Execution**: Python executes function, returns data
- **Re-generation**: LLM incorporates function result
- **Use Case**: Dynamic link retrieval

### 3. Conversation Memory Pattern
- **Storage**: Session state in Streamlit
- **Format**: List of (role, content) tuples
- **Context Window**: Last N messages included in prompt
- **Benefit**: Context-aware responses

### 4. Multi-language Pattern
- **Detection**: Implicit from query language
- **Prompt**: System message specifies language matching
- **Data**: Bilingual embeddings in Pinecone
- **TTS**: Language-specific models

## Component Relationships

### Core Components

**1. Vector Store Manager**
- Initializes Pinecone connection
- Loads and chunks documents
- Creates embeddings
- Upserts to index
- Handles queries

**2. LLM Chain Manager**
- Configures Azure OpenAI client
- Manages prompt templates
- Handles function calling setup
- Processes responses

**3. Conversation Manager**
- Maintains chat history
- Formats history for prompts
- Generates follow-up questions
- Manages session state

**4. Function Call Handler**
- Defines available functions
- Loads mock_links.json
- Executes function calls
- Returns structured data

**5. TTS Manager**
- gTTS (Google Text-to-Speech) client
- Text-to-speech conversion for Vietnamese and English
- Audio playback handling
- No API key required

**6. UI Controller**
- Streamlit layout
- Event handlers
- State management
- Response rendering

## Data Flow

### Initialization (Once)
1. Load environment variables
2. Initialize Pinecone client
3. Initialize Azure OpenAI client
4. Load mock_links.json
5. Initialize session state

### Per Query
1. User types message
2. Add to chat history
3. Retrieve relevant docs (Pinecone)
4. Build prompt with context + history
5. Call LLM (may trigger function)
6. Display response
7. Generate follow-ups
8. Enable TTS

### Function Call Flow
1. LLM returns function_call object
2. Extract function name + arguments
3. Execute function (lookup in mock_links.json)
4. Format function result
5. Re-call LLM with function result
6. Return final answer with links

## Error Handling Patterns
- Pinecone connection failures → graceful fallback
- LLM API errors → retry logic
- TTS failures → disable button, show text only (gTTS is stable, rarely fails)
- Function call errors → return default message
- Empty retrieval → use LLM general knowledge (with warning)

## TTS Implementation History

### Initial Implementation (Hugging Face)
- Attempted to use Hugging Face Inference API
- Encountered 401 errors (token permissions)
- After fixing token, encountered 404 errors (endpoints deprecated/not available)
- All tested endpoints returned 404 or 410 (deprecated)

### Current Implementation (gTTS)
- Switched to Google Text-to-Speech (gTTS)
- No API key required
- Stable and reliable
- Supports Vietnamese (vi) and English (en)
- Simple integration with io.BytesIO for audio buffer
- Backup of Hugging Face implementation saved in `src/tts_huggingface_backup.py`

