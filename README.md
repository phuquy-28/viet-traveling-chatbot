# 🇻🇳 Vietnam Travel Advisory Chatbot

An intelligent RAG (Retrieval-Augmented Generation) chatbot for Vietnamese travel advisory, built with Langchain, Pinecone, and Azure OpenAI.

## 🎯 Features

- **Bilingual Support**: Handles both Vietnamese and English queries
- **RAG Architecture**: Retrieves accurate information from curated knowledge base
- **Function Calling**: Dynamically fetches external links (maps, reviews, videos)
- **Conversational AI**: Maintains context and suggests follow-up questions
- **Text-to-Speech**: Audio responses in both languages via Hugging Face
- **Interactive UI**: Clean Streamlit interface

## 🏗️ Architecture

```
User → Streamlit UI → Langchain → Pinecone (Vector Search)
                         ↓
                    Azure OpenAI (LLM + Embeddings)
                         ↓
                    Function Calling → External Links
                         ↓
                    Hugging Face TTS → Audio Output
```

## 📋 Prerequisites

- Python 3.9+
- Azure OpenAI account with API access
- Pinecone account and API key
- Hugging Face account and API token

## 🚀 Setup Instructions

### 1. Clone and Setup Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables

```bash
# Copy example file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env and fill in your API keys
```

Required variables:
- `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key
- `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint URL
- `AZURE_OPENAI_DEPLOYMENT_NAME`: Your GPT model deployment name
- `AZURE_OPENAI_EMBEDDING_DEPLOYMENT`: Your embedding model deployment
- `PINECONE_API_KEY`: Your Pinecone API key
- `PINECONE_ENVIRONMENT`: Your Pinecone environment
- `PINECONE_INDEX_NAME`: Name for your Pinecone index
- `HUGGINGFACE_API_KEY`: Your Hugging Face API token

### 3. Ingest Data into Pinecone

```bash
# Run one-time data ingestion
python ingest_data.py
```

This will:
- Create Pinecone index (if not exists)
- Load Vietnamese and English travel documents
- Generate embeddings
- Upload to Pinecone vector store

### 4. Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
viet-traveling-chatbot/
├── memory-bank/           # Project documentation
├── data/                  # Mock travel data
│   ├── raw/
│   │   ├── vietnamese/    # Vietnamese content
│   │   └── english/       # English content
│   └── mock_links.json    # External links database
├── src/                   # Source code
│   ├── vector_store.py    # Pinecone operations
│   ├── llm_chain.py       # Langchain setup
│   ├── function_calls.py  # Function calling handlers
│   ├── conversation.py    # Chat history management
│   ├── tts.py            # Text-to-Speech integration
│   └── utils.py          # Helper functions
├── app.py                # Streamlit main application
├── ingest_data.py        # Data ingestion script
└── requirements.txt      # Python dependencies
```

## 💬 Usage Examples

### Q&A in Vietnamese
```
User: Thời tiết ở Sa Pa tháng 12 như thế nào?
Bot: [Provides weather information with TTS button]
```

### Q&A in English
```
User: What is the best time to visit Ha Long Bay?
Bot: [Provides recommendation with TTS button]
```

### Recommendations with External Links
```
User: Recommend good pho restaurants in Hanoi
Bot: [Provides recommendations + Google Maps links + review links]
```

### Context-Aware Follow-up
```
User: Tell me about Da Nang
Bot: [Provides information about Da Nang]
User: What activities can I do there?
Bot: [Understands "there" refers to Da Nang from context]
```

## 🧪 Testing

Test cases cover:
- TC1: Vietnamese Q&A
- TC2: English Q&A
- TC3: Function calling with external links
- TC4: Context-aware responses
- TC5: Follow-up question suggestions
- TC6: Text-to-Speech in both languages

## 🛠️ Technical Stack

- **Framework**: Langchain (orchestration, RAG, function calling)
- **Vector Store**: Pinecone (semantic search)
- **LLM**: Azure OpenAI (GPT-4 or GPT-3.5-Turbo)
- **UI**: Streamlit
- **TTS**: Hugging Face Inference API
- **Language**: Python 3.9+

## 📝 Workshop Requirements

This project fulfills Workshop 4 requirements:
- ✅ RAG implementation with Pinecone
- ✅ Langchain orchestration
- ✅ Function Calling integration
- ✅ Streamlit UI
- ✅ Hugging Face TTS
- ✅ Synthetic dataset creation
- ✅ Multilingual support

## 🤝 Contributing

This is a workshop project. For improvements:
1. Review memory-bank/ documentation
2. Follow existing patterns in src/
3. Update relevant documentation

## 📄 License

Educational project for Workshop 4.

## 🐛 Troubleshooting

### Pinecone Connection Issues
- Verify API key and environment in `.env`
- Check if index exists: `python -c "from pinecone import Pinecone; pc = Pinecone(api_key='YOUR_KEY'); print(pc.list_indexes())"`

### Azure OpenAI Errors
- Verify endpoint URL format
- Check deployment names match your Azure resource
- Ensure API version is compatible

### TTS Not Working
- Verify Hugging Face API token
- Check internet connection
- Try alternative TTS models if needed

## 📞 Support

For workshop-related questions, refer to:
- `memory-bank/` documentation
- SRS document (original requirements)
- Workshop materials

