# 🚀 Quick Setup Guide - Vietnam Travel Chatbot

## Prerequisites

- Python 3.9 or higher
- Virtual environment (recommended)
- API Keys:
  - **Azure OpenAI** (required)
  - **Pinecone** (required)

---

## Step 1: Install Dependencies

### Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Linux/Mac:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 2: Configure Environment Variables

1. **Copy the example file:**
   ```bash
   copy .env.example .env  # Windows
   # OR
   cp .env.example .env    # Linux/Mac
   ```

2. **Edit `.env` and fill in your API keys:**

   ```env
   # Azure OpenAI Configuration
   AZURE_OPENAI_API_KEY=your_actual_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-3-small
   AZURE_OPENAI_API_VERSION=2024-02-15-preview

   # Pinecone Configuration
   PINECONE_API_KEY=your_actual_pinecone_key_here
   PINECONE_INDEX_NAME=vietnam-travel
   ```

### Where to Get API Keys:

**Azure OpenAI:**
- Go to [Azure Portal](https://portal.azure.com/)
- Navigate to your Azure OpenAI resource
- Find "Keys and Endpoint" in the left menu
- Copy Key 1 and Endpoint

**Pinecone:**
- Go to [Pinecone Console](https://app.pinecone.io/)
- Create a free account (if needed)
- Go to "API Keys" section
- Copy your API key
- Note your environment (e.g., `us-east-1-aws`)

**Note:** Text-to-Speech uses Google TTS (gTTS) which does NOT require an API key. It's free and works automatically once gTTS is installed.

---

## Step 3: Ingest Data into Pinecone

This step creates the Pinecone index and uploads all Vietnamese and English travel content.

```bash
python ingest_data.py
```

**Expected Output:**
```
===================================================
Vietnam Travel Chatbot - Data Ingestion
===================================================

1. Loading environment variables...
2. Validating environment...
✅ All required environment variables are set!
3. Initializing Vector Store Manager...
✅ Vector Store Manager initialized
4. Creating Pinecone index (if not exists)...
✅ Pinecone index ready
5. Loading Vietnamese documents...
✅ Loaded 3 Vietnamese documents
6. Loading English documents...
✅ Loaded 3 English documents
7. Chunking documents...
✅ Created XX chunks
8. Ingesting chunks into Pinecone...
✅ Successfully ingested all documents into Pinecone!
9. Testing retrieval...
✅ Test query successful!

===================================================
✅ DATA INGESTION COMPLETED SUCCESSFULLY!
===================================================
```

**This step may take 2-5 minutes.** ⏱️

---

## Step 4: Launch the Application

```bash
streamlit run app.py
```

**The browser will automatically open to:**
```
http://localhost:8501
```

If it doesn't open automatically, manually navigate to that URL.

---

## Step 5: Test the Application

### Quick Tests:

1. **Test Vietnamese:**
   - Type: `Thời tiết ở Sa Pa tháng 12 như thế nào?`
   - Expected: Response in Vietnamese about Sapa weather

2. **Test English:**
   - Type: `What is the best time to visit Ha Long Bay?`
   - Expected: Response in English with travel recommendations

3. **Test Function Calling:**
   - Type: `Recommend good pho restaurants in Hanoi`
   - Expected: Response with external links (Google Maps, reviews)

4. **Test Follow-up:**
   - Ask about any destination
   - Click one of the suggested follow-up questions
   - Expected: Context-aware response

5. **Test TTS (if configured):**
   - Ask any question
   - Click 🔊 button next to bot response
   - Expected: Audio plays

### Full Test Suite:

For comprehensive testing, follow: **`TEST_CASES.md`**

---

## Troubleshooting

### Issue: "Module not found" error
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "AZURE_OPENAI_API_KEY not found"
**Solution:**
- Ensure `.env` file exists in project root
- Verify API keys are set correctly (no quotes needed)
- Restart the application

### Issue: Pinecone index creation fails
**Solution:**
- Check Pinecone API key is valid
- Verify your Pinecone plan allows index creation
- Free tier: 1 index limit (delete existing if needed)

### Issue: "Index not found" when running app
**Solution:**
- Ensure you ran `python ingest_data.py` first
- Check index name matches in `.env` and Pinecone console

### Issue: TTS not working
**Solution:**
- TTS uses Google TTS (gTTS) - no API key needed
- Verify gTTS is installed: `pip install gtts`
- Check internet connection (gTTS requires internet)
- First TTS call may take a few seconds

### Issue: Slow responses
**Solution:**
- First query after startup is slower (initialization)
- Typical response time: 3-5 seconds
- Check internet connection
- Verify Azure OpenAI quota not exceeded

### Issue: Empty responses or errors
**Solution:**
- Check console/terminal for error messages
- Verify all API keys are correct
- Ensure Pinecone index has data (run ingestion again)
- Check Azure OpenAI deployment names match

---

## Application Features

### 🌍 Multilingual Support
- Automatically detects Vietnamese or English
- Responds in the same language
- Seamless language switching

### 🤖 RAG (Retrieval-Augmented Generation)
- Searches knowledge base before answering
- Minimizes hallucinations
- Accurate, grounded responses

### 🔗 Function Calling
- Automatically retrieves external links
- Google Maps, blogs, videos, reviews
- Triggered when relevant

### 💬 Persistent Conversation History
- Remembers conversation context across sessions
- Chat history saved to disk (survives app restarts)
- Context-aware follow-ups
- "Smart" understanding of pronouns ("there", "it", etc.)

### ❓ Follow-up Suggestions
- AI-generated follow-up questions
- Click to ask instantly
- Contextually relevant

### 🔊 Text-to-Speech
- Listen to bot responses
- Supports Vietnamese and English
- Natural voice quality

### 📱 Clean Interface
- Example questions in sidebar
- Clear chat history button
- Mobile-friendly design

---

## File Structure Reference

```
viet-traveling-chatbot/
├── app.py                    # Main Streamlit application
├── ingest_data.py           # Data ingestion script
├── requirements.txt         # Python dependencies
├── .env.example             # Environment template
├── .env                     # Your configuration (create this)
├── README.md                # Project overview
├── SETUP_GUIDE.md          # This file
├── TEST_CASES.md           # Comprehensive test cases
│
├── memory-bank/             # Project documentation
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   └── progress.md
│
├── src/                     # Source code modules
│   ├── __init__.py
│   ├── ui/                  # UI Components (modular)
│   │   ├── __init__.py
│   │   ├── styles.py        # CSS styling
│   │   ├── sidebar.py       # Sidebar components
│   │   ├── messages.py      # Message display + TTS
│   │   ├── welcome.py       # Welcome screen
│   │   └── session_manager.py  # Session management
│   ├── vector_store.py      # Pinecone operations
│   ├── llm_chain.py         # Langchain + Azure OpenAI
│   ├── function_calls.py    # Function calling logic
│   ├── conversation.py      # Chat history management
│   ├── chat_storage.py      # Persistent storage (file-based)
│   ├── tts.py              # Text-to-Speech
│   └── utils.py            # Helper functions
│
└── data/                    # Mock travel data
    ├── mock_links.json      # External links database
    └── raw/
        ├── vietnamese/      # Vietnamese content
        │   ├── destinations.txt
        │   ├── food.txt
        │   └── culture.txt
        └── english/         # English content
            ├── destinations.txt
            ├── food.txt
            └── culture.txt
```

---

## Performance Tips

1. **First Run:** Initial responses may be slower (30-60s) due to:
   - Component initialization
   - Streamlit caching
   - Model loading

2. **Subsequent Queries:** Should be 3-5 seconds

3. **TTS Performance:** 
   - First call per session: 5-10 seconds
   - Subsequent calls: 2-5 seconds

4. **Optimization:**
   - Keep session open (avoid restarting)
   - Use smaller text for TTS (auto-truncated to 500 chars)

---

## Need Help?

1. **Check Console Logs:** Look for error messages in terminal
2. **Review Documentation:**
   - `README.md` - Project overview
   - `TEST_CASES.md` - Detailed test scenarios
   - `memory-bank/` - Technical documentation
3. **Common Issues:** See Troubleshooting section above
4. **API Limits:** Check your Azure OpenAI and Pinecone quotas

---

## Next Steps

After setup:
1. ✅ Run through all test cases in `TEST_CASES.md`
2. ✅ Explore different types of questions
3. ✅ Test bilingual capabilities
4. ✅ Try follow-up suggestions
5. ✅ Experiment with TTS
6. ✅ Test Function Calling with recommendation queries

---

## Workshop Deliverables Checklist

- [x] SRS Document (provided)
- [x] Pinecone index with embeddings (run `ingest_data.py`)
- [x] Python source code (complete)
- [x] Mock data files (Vietnamese + English)
- [x] Working Streamlit application (run `streamlit run app.py`)
- [x] Test case documentation (see `TEST_CASES.md`)

---

**🎉 Congratulations! Your Vietnam Travel Chatbot is ready!**

Happy testing! 🇻🇳

