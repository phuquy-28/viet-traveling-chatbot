"""Text-to-Speech using gTTS (Google Text-to-Speech) - Simple and Free"""

from typing import Optional
from gtts import gTTS
import io


class TTSManager:
    """Manages Text-to-Speech conversion using gTTS (Google)"""
    
    def __init__(self):
        """Initialize TTS manager"""
        print("[TTS] gTTS (Google Text-to-Speech) initialized - No API key needed!")
        
        # Language mapping
        self.language_codes = {
            "vietnamese": "vi",
            "english": "en"
        }
    
    def text_to_speech(self, text: str, language: str = "english") -> Optional[bytes]:
        """Convert text to speech using Google TTS
        
        Args:
            text: Text to convert
            language: 'vietnamese' or 'english'
            
        Returns:
            Audio bytes or None if failed
        """
        if language not in self.language_codes:
            print(f"Unsupported language: {language}")
            return None
        
        lang_code = self.language_codes[language]
        
        try:
            # Limit text length
            text = text[:500]
            
            # Create gTTS object
            tts = gTTS(text=text, lang=lang_code, slow=False)
            
            # Save to bytes buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)
            
            return audio_buffer.read()
            
        except Exception as e:
            print(f"TTS error: {str(e)}")
            return None
    
    def is_available(self) -> bool:
        """Check if TTS is available
        
        Returns:
            True (gTTS is always available, no API key needed)
        """
        return True


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
