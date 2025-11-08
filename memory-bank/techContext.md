# Technical Context

## Technology Stack

### Core Technologies
- **Python**: 3.9+ (primary language)
- **Langchain**: Orchestration, chains, RAG, function calling
- **Pinecone**: Vector database for semantic search
- **Streamlit**: Web UI framework
- **Azure OpenAI**: LLM and embeddings
- **gTTS (Google Text-to-Speech)**: Text-to-Speech API

### Key Dependencies

```
langchain>=0.1.0
langchain-openai>=0.0.5
langchain-pinecone>=0.0.1
pinecone>=3.0.0
streamlit>=1.30.0
openai>=1.0.0
python-dotenv>=1.0.1
requests>=2.31.0
gtts==2.5.1
```

## Development Setup

### Environment Variables Required

```env
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4  # or gpt-35-turbo
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
AZURE_OPENAI_API_VERSION=2024-02-15-preview

# Pinecone
PINECONE_API_KEY=your_key
PINECONE_ENVIRONMENT=your_env  # e.g., us-east-1-aws
PINECONE_INDEX_NAME=vietnam-travel

# Hugging Face (for TTS) - NO LONGER NEEDED
# HUGGINGFACE_API_KEY=your_key  # Optional, not required
```

### Project Structure

```
viet-traveling-chatbot/
├── memory-bank/              # Documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   └── progress.md
├── data/                     # Mock data
│   ├── raw/                  # Raw travel content
│   │   ├── vietnamese/
│   │   │   ├── destinations.txt
│   │   │   ├── food.txt
│   │   │   └── culture.txt
│   │   └── english/
│   │       ├── destinations.txt
│   │       ├── food.txt
│   │       └── culture.txt
│   └── mock_links.json       # External links data
├── src/                      # Source code
│   ├── __init__.py
│   ├── vector_store.py       # Pinecone operations
│   ├── llm_chain.py          # Langchain setup
│   ├── function_calls.py     # Function calling handlers
│   ├── conversation.py       # Chat history management
│   ├── tts.py                # Text-to-Speech
│   └── utils.py              # Helper functions
├── app.py                    # Streamlit main app
├── ingest_data.py            # One-time data ingestion
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables
├── .env.example              # Template for .env
├── .gitignore                # Git ignore rules
└── README.md                 # Setup instructions
```

## Technical Constraints

### Pinecone Specifications
- **Dimension**: 1536 (for text-embedding-3-small)
- **Metric**: Cosine similarity
- **Namespace**: Optional (can separate vi/en if needed)
- **Metadata**: Store language, category, source

### Azure OpenAI Specifications
- **Model**: GPT-4 or GPT-3.5-Turbo
- **Max Tokens**: 4096-8192 (depending on model)
- **Temperature**: 0.7 (balanced creativity)
- **Function Calling**: Supported in chat completion

### Streamlit Constraints
- **Session State**: Used for chat history
- **File Upload**: Not needed (mock data only)
- **Caching**: Use @st.cache_resource for clients
- **Audio**: Use st.audio() for TTS playback

### gTTS (Google Text-to-Speech)
- **Service**: Google Text-to-Speech API
- **Languages**: Vietnamese (vi), English (en)
- **Format**: MP3 audio output
- **API Key**: NOT REQUIRED (free service)
- **Advantages**: No API key needed, stable, high quality voices

## Integration Points

### 1. Langchain + Pinecone
```python
from langchain_pinecone import PineconeVectorStore
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(...)
vectorstore = PineconeVectorStore(index_name="vietnam-travel", embedding=embeddings)
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

### 2. Langchain + Azure OpenAI + Function Calling
```python
from langchain_openai import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent

llm = AzureChatOpenAI(...)
tools = [get_external_links_tool]
agent = create_openai_functions_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)
```

### 3. Streamlit + Session State
```python
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
```

### 4. gTTS Integration
```python
from gtts import gTTS
import io

def text_to_speech(text, language="en"):
    lang_code = "vi" if language == "vietnamese" else "en"
    tts = gTTS(text=text, lang=lang_code, slow=False)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.read()  # audio bytes
```

## Performance Considerations

### Optimization Strategies
1. **Caching**: Cache Pinecone/OpenAI clients in Streamlit
2. **Batch Embedding**: Embed documents in batches during ingestion
3. **Top-K Retrieval**: Limit to 3-5 documents for speed
4. **Async Calls**: Consider async for TTS if implemented
5. **Connection Pooling**: Reuse HTTP connections

### Expected Latency
- Pinecone query: ~200-500ms
- Azure OpenAI completion: 2-4 seconds
- Function call overhead: +1 second
- TTS generation: 1-3 seconds (gTTS, no model loading)
- **Total**: < 5 seconds (NFR1)

## Security Considerations
- Store API keys in .env (never commit)
- Add .env to .gitignore
- Use environment variables in production
- Validate user inputs (prevent injection)
- Rate limit API calls if needed

