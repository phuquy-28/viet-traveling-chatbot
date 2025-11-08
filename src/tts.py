"""Text-to-Speech using Hugging Face API"""

import os
import requests
import time
from typing import Optional


class TTSManager:
    """Manages Text-to-Speech conversion using Hugging Face"""
    
    def __init__(self):
        """Initialize TTS manager"""
        self.api_key = os.getenv("HUGGINGFACE_API_KEY")
        
        if not self.api_key:
            print("Warning: HUGGINGFACE_API_KEY not found. TTS will be disabled.")
        
        # TTS model endpoints
        self.models = {
            "vietnamese": "facebook/mms-tts-vie",
            "english": "facebook/mms-tts-eng"
        }
        
        # Updated to new Hugging Face router endpoint
        self.api_base_url = "https://router.huggingface.co/hf-inference/models/"
    
    def text_to_speech(self, text: str, language: str = "english") -> Optional[bytes]:
        """Convert text to speech
        
        Args:
            text: Text to convert
            language: 'vietnamese' or 'english'
            
        Returns:
            Audio bytes or None if failed
        """
        if not self.api_key:
            print("TTS disabled: No API key")
            return None
        
        if language not in self.models:
            print(f"Unsupported language: {language}")
            return None
        
        model = self.models[language]
        api_url = f"{self.api_base_url}{model}"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            # "Content-Type": "application/json"
        }
        
        payload = {
            "inputs": text[:500]  # Limit text length to avoid long processing
        }
        
        try:
            # Make request with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                response = requests.post(api_url, headers=headers, json=payload, timeout=30)
                
                if response.status_code == 200:
                    return response.content
                elif response.status_code == 503:
                    # Model is loading, wait and retry
                    wait_time = 5 * (attempt + 1)
                    print(f"Model loading... Retrying in {wait_time}s")
                    time.sleep(wait_time)
                else:
                    print(f"TTS API error: {response.status_code} - {response.text}")
                    return None
            
            print("TTS failed after max retries")
            return None
            
        except requests.exceptions.Timeout:
            print("TTS request timed out")
            return None
        except Exception as e:
            print(f"TTS error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        """Check if TTS is available
        
        Returns:
            True if API key is configured
        """
        return self.api_key is not None and len(self.api_key) > 0


# Fallback: Simple TTS status message
def get_tts_placeholder(language: str = "english") -> str:
    """Get placeholder message when TTS is not available
    
    Args:
        language: Language for the message
        
    Returns:
        Placeholder message
    """
    if language == "vietnamese":
        return "🔊 Tính năng Text-to-Speech tạm thời không khả dụng."
    else:
        return "🔊 Text-to-Speech feature is temporarily unavailable."

