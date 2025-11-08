"""Data Ingestion Script for Pinecone Vector Store

Run this script once to populate the Pinecone index with Vietnamese travel data.

Usage:
    python ingest_data.py
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.vector_store import VectorStoreManager
from src.utils import load_env_file, validate_environment


def main():
    """Main ingestion function"""
    print("=" * 60)
    print("Vietnam Travel Chatbot - Data Ingestion")
    print("=" * 60)
    
    # Load environment variables
    print("\n1. Loading environment variables...")
    load_env_file()
    
    # Validate environment
    print("\n2. Validating environment...")
    validation_results = validate_environment()
    
    required_vars = [
        "AZURE_OPENAI_API_KEY",
        "AZURE_OPENAI_ENDPOINT", 
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
        "PINECONE_API_KEY"
    ]
    
    missing_vars = [var for var in required_vars if not validation_results.get(var, False)]
    
    if missing_vars:
        print("\n❌ ERROR: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease configure these variables in your .env file.")
        sys.exit(1)
    
    print("✅ All required environment variables are set!")
    
    # Initialize vector store manager
    print("\n3. Initializing Vector Store Manager...")
    try:
        vs_manager = VectorStoreManager()
        print("✅ Vector Store Manager initialized")
    except Exception as e:
        print(f"❌ Failed to initialize Vector Store Manager: {e}")
        sys.exit(1)
    
    # Create Pinecone index if not exists
    print("\n4. Creating Pinecone index (if not exists)...")
    try:
        vs_manager.create_index_if_not_exists(dimension=1536)
        print("✅ Pinecone index ready")
    except Exception as e:
        print(f"❌ Failed to create Pinecone index: {e}")
        sys.exit(1)
    
    # Load Vietnamese documents
    print("\n5. Loading Vietnamese documents...")
    vietnamese_files = [
        "data/raw/vietnamese/destinations.txt",
        "data/raw/vietnamese/food.txt",
        "data/raw/vietnamese/culture.txt"
    ]
    
    try:
        vietnamese_docs = vs_manager.load_documents(vietnamese_files, "vietnamese")
        print(f"✅ Loaded {len(vietnamese_docs)} Vietnamese documents")
    except Exception as e:
        print(f"❌ Failed to load Vietnamese documents: {e}")
        sys.exit(1)
    
    # Load English documents
    print("\n6. Loading English documents...")
    english_files = [
        "data/raw/english/destinations.txt",
        "data/raw/english/food.txt",
        "data/raw/english/culture.txt"
    ]
    
    try:
        english_docs = vs_manager.load_documents(english_files, "english")
        print(f"✅ Loaded {len(english_docs)} English documents")
    except Exception as e:
        print(f"❌ Failed to load English documents: {e}")
        sys.exit(1)
    
    # Combine all documents
    all_docs = vietnamese_docs + english_docs
    print(f"\n📚 Total documents: {len(all_docs)}")
    
    # Chunk documents
    print("\n7. Chunking documents...")
    try:
        chunks = vs_manager.chunk_documents(all_docs, chunk_size=1000, chunk_overlap=200)
        print(f"✅ Created {len(chunks)} chunks")
    except Exception as e:
        print(f"❌ Failed to chunk documents: {e}")
        sys.exit(1)
    
    # Ingest into Pinecone
    print("\n8. Ingesting chunks into Pinecone...")
    print("   (This may take a few minutes...)")
    try:
        vs_manager.ingest_documents(chunks)
        print("✅ Successfully ingested all documents into Pinecone!")
    except Exception as e:
        print(f"❌ Failed to ingest documents: {e}")
        sys.exit(1)
    
    # Test retrieval
    print("\n9. Testing retrieval...")
    try:
        test_query = "Tell me about Ha Long Bay"
        results = vs_manager.similarity_search(test_query, k=2)
        print(f"✅ Test query successful! Retrieved {len(results)} documents")
        if results:
            print(f"\n   Sample result:")
            print(f"   Category: {results[0].metadata.get('category', 'N/A')}")
            print(f"   Language: {results[0].metadata.get('language', 'N/A')}")
            print(f"   Content preview: {results[0].page_content[:150]}...")
    except Exception as e:
        print(f"⚠️  Test query failed: {e}")
    
    print("\n" + "=" * 60)
    print("✅ DATA INGESTION COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nYou can now run the Streamlit app:")
    print("   streamlit run app.py")
    print("\n")


if __name__ == "__main__":
    main()

