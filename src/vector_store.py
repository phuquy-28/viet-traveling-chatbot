"""Pinecone Vector Store Management"""

import os
from typing import List, Optional
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document


class VectorStoreManager:
    """Manages Pinecone vector store operations"""
    
    def __init__(self, verbose: bool = False):
        """Initialize Pinecone client and embeddings
        
        Args:
            verbose: If True, print initialization details
        """
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.environment = os.getenv("PINECONE_ENVIRONMENT")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "vietnam-travel")
        
        if not self.api_key:
            raise ValueError("PINECONE_API_KEY not found in environment variables")
        
        # Initialize Pinecone client
        self.pc = Pinecone(api_key=self.api_key)
        
        # Initialize embeddings
        # Use separate API key for embeddings if available, otherwise fallback to main API key
        embedding_api_key = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY") or os.getenv("AZURE_OPENAI_API_KEY")
        embedding_endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT") or os.getenv("AZURE_OPENAI_ENDPOINT")
        embedding_deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
        
        if not embedding_api_key:
            raise ValueError("AZURE_OPENAI_EMBEDDING_API_KEY or AZURE_OPENAI_API_KEY not found in environment variables")
        
        if not embedding_deployment:
            raise ValueError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT not found in environment variables")
        
        if verbose:
            print(f"[VectorStore] Using embedding deployment: {embedding_deployment}")
        
        # IMPORTANT: Set both azure_deployment AND model to ensure correct model is used
        # azure_deployment = your deployment name in Azure Portal
        # model = actual model name (e.g., text-embedding-3-small)
        self.embeddings = AzureOpenAIEmbeddings(
            azure_deployment=embedding_deployment,
            model=embedding_deployment,  # Explicitly set model name to match deployment
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_endpoint=embedding_endpoint,
            api_key=embedding_api_key
        )
        
        self.vectorstore = None
    
    def delete_index(self):
        """Delete the Pinecone index if it exists"""
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        
        if self.index_name in existing_indexes:
            print(f"Deleting existing index '{self.index_name}'...")
            self.pc.delete_index(self.index_name)
            print(f"Index '{self.index_name}' deleted successfully!")
            # Wait for deletion to complete
            import time
            time.sleep(5)
        else:
            print(f"Index '{self.index_name}' does not exist, nothing to delete.")
    
    def create_index_if_not_exists(self, dimension: int = 1536, force_recreate: bool = False):
        """Create Pinecone index if it doesn't exist
        
        Args:
            dimension: Vector dimension (1536 for text-embedding-3-small)
            force_recreate: If True, delete and recreate the index even if it exists
        """
        existing_indexes = [index.name for index in self.pc.list_indexes()]
        
        if force_recreate and self.index_name in existing_indexes:
            print(f"Force recreate enabled. Deleting existing index '{self.index_name}'...")
            self.delete_index()
            existing_indexes = []
        
        if self.index_name not in existing_indexes:
            print(f"Creating index '{self.index_name}'...")
            self.pc.create_index(
                name=self.index_name,
                dimension=dimension,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region=self.environment or "us-east-1"
                )
            )
            print(f"Index '{self.index_name}' created successfully!")
            # Wait for index to be ready
            import time
            time.sleep(10)
        else:
            print(f"Index '{self.index_name}' already exists.")
    
    def load_documents(self, file_paths: List[str], language: str) -> List[Document]:
        """Load documents from text files
        
        Args:
            file_paths: List of file paths to load
            language: Language of the documents (vietnamese or english)
            
        Returns:
            List of Document objects
        """
        documents = []
        
        for file_path in file_paths:
            if not os.path.exists(file_path):
                print(f"Warning: File not found: {file_path}")
                continue
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Determine category from filename
            category = "general"
            if "destinations" in file_path.lower():
                category = "destinations"
            elif "food" in file_path.lower():
                category = "food"
            elif "culture" in file_path.lower():
                category = "culture"
            
            # Create document with metadata
            doc = Document(
                page_content=content,
                metadata={
                    "source": file_path,
                    "language": language,
                    "category": category
                }
            )
            documents.append(doc)
        
        print(f"Loaded {len(documents)} documents in {language}")
        return documents
    
    def chunk_documents(self, documents: List[Document], chunk_size: int = 1000, 
                       chunk_overlap: int = 200) -> List[Document]:
        """Split documents into chunks
        
        Args:
            documents: List of documents to chunk
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of chunked documents
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n## ", "\n\n", "\n", " ", ""]
        )
        
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        return chunks
    
    def ingest_documents(self, documents: List[Document]):
        """Ingest documents into Pinecone
        
        Args:
            documents: List of documents to ingest
        """
        if not documents:
            print("No documents to ingest")
            return
        
        print(f"Ingesting {len(documents)} documents into Pinecone...")
        
        # Create vector store and ingest
        self.vectorstore = PineconeVectorStore.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=self.index_name
        )
        
        print("Documents ingested successfully!")
    
    def get_vectorstore(self) -> PineconeVectorStore:
        """Get or initialize vector store
        
        Returns:
            PineconeVectorStore instance
        """
        if self.vectorstore is None:
            self.vectorstore = PineconeVectorStore(
                index_name=self.index_name,
                embedding=self.embeddings
            )
        
        return self.vectorstore
    
    def similarity_search(self, query: str, k: int = 3, 
                         filter: Optional[dict] = None) -> List[Document]:
        """Perform similarity search
        
        Args:
            query: Search query
            k: Number of results to return
            filter: Metadata filter (e.g., {"language": "vietnamese"})
            
        Returns:
            List of relevant documents
        """
        vectorstore = self.get_vectorstore()
        
        if filter:
            results = vectorstore.similarity_search(query, k=k, filter=filter)
        else:
            results = vectorstore.similarity_search(query, k=k)
        
        return results
    
    def get_retriever(self, k: int = 3, filter: Optional[dict] = None):
        """Get retriever for RAG chain
        
        Args:
            k: Number of documents to retrieve
            filter: Metadata filter
            
        Returns:
            Retriever instance
        """
        vectorstore = self.get_vectorstore()
        
        search_kwargs = {"k": k}
        if filter:
            search_kwargs["filter"] = filter
        
        return vectorstore.as_retriever(search_kwargs=search_kwargs)

