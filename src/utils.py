"""Utility Functions"""

import os
from typing import Dict, Any, Optional
from pathlib import Path


def load_env_file(env_path: str = ".env") -> bool:
    """Load environment variables from .env file
    
    Args:
        env_path: Path to .env file
        
    Returns:
        True if loaded successfully
    """
    from dotenv import load_dotenv
    
    if os.path.exists(env_path):
        load_dotenv(env_path)
        return True
    else:
        print(f"Warning: {env_path} not found")
        return False


def validate_environment(verbose: bool = True) -> Dict[str, bool]:
    """Validate required environment variables
    
    Args:
        verbose: If True, print validation details to console
    
    Returns:
        Dictionary with validation results
    """
    required_vars = {
        "Azure OpenAI API Key": "AZURE_OPENAI_API_KEY",
        "Azure OpenAI Endpoint": "AZURE_OPENAI_ENDPOINT",
        "Azure OpenAI Deployment": "AZURE_OPENAI_DEPLOYMENT_NAME",
        "Azure OpenAI Embedding": "AZURE_OPENAI_EMBEDDING_DEPLOYMENT",
        "Pinecone API Key": "PINECONE_API_KEY",
    }
    
    optional_vars = {
        "Pinecone Environment": "PINECONE_ENVIRONMENT",
        "Azure OpenAI Embedding API Key": "AZURE_OPENAI_EMBEDDING_API_KEY",
        "Azure OpenAI Embedding Endpoint": "AZURE_OPENAI_EMBEDDING_ENDPOINT",
    }
    
    results = {}
    
    # Validate required vars
    for name, var in required_vars.items():
        value = os.getenv(var)
        is_set = value is not None and len(value) > 0
        results[var] = is_set
        if verbose:
            status = "[OK] Set" if is_set else "[MISSING]"
            print(f"{name}: {status}")
    
    # Validate optional vars (silent unless verbose)
    for name, var in optional_vars.items():
        value = os.getenv(var)
        is_set = value is not None and len(value) > 0
        results[var] = is_set
    
    if verbose and any(results.get(var, False) for var in optional_vars.values()):
        print("\nOptional Variables:")
        for name, var in optional_vars.items():
            if results.get(var, False):
                print(f"{name}: [OK] Set")
    
    return results


def get_project_root() -> Path:
    """Get project root directory
    
    Returns:
        Path to project root
    """
    return Path(__file__).parent.parent


def ensure_directories():
    """Ensure all required directories exist"""
    root = get_project_root()
    
    directories = [
        root / "data" / "raw" / "vietnamese",
        root / "data" / "raw" / "english",
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"Directory ensured: {directory}")


def format_error_message(error: Exception, language: str = "english") -> str:
    """Format error message for display
    
    Args:
        error: Exception object
        language: Language for the message
        
    Returns:
        Formatted error message
    """
    error_str = str(error)
    
    if language == "vietnamese":
        return f"❌ Xin lỗi, đã xảy ra lỗi: {error_str}\n\nVui lòng thử lại hoặc đặt câu hỏi khác."
    else:
        return f"❌ Sorry, an error occurred: {error_str}\n\nPlease try again or ask a different question."


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to maximum length
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."


def count_tokens_approximate(text: str) -> int:
    """Approximate token count (rough estimate)
    
    Args:
        text: Text to count
        
    Returns:
        Approximate token count
    """
    # Rough approximation: 1 token ≈ 4 characters for English
    # Vietnamese might be different, but this is a simple estimate
    return len(text) // 4


def format_sources(sources: list, max_sources: int = 3) -> str:
    """Format source documents for display
    
    Args:
        sources: List of source documents
        max_sources: Maximum number of sources to display
        
    Returns:
        Formatted source string
    """
    if not sources:
        return ""
    
    result = "\n\n---\n**Sources:**\n"
    
    for i, doc in enumerate(sources[:max_sources], 1):
        metadata = doc.metadata
        category = metadata.get("category", "general")
        language = metadata.get("language", "unknown")
        
        result += f"{i}. {category.title()} ({language})\n"
    
    return result

