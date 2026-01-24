import os
import uuid
from gtts import gTTS
import pyttsx3
from config import Config

class TTSService:
    """Text-to-Speech service for generating audio from text"""
    
    def __init__(self):
        self.engine_type = Config.TTS_ENGINE
        self.audio_folder = Config.AUDIO_FOLDER
        os.makedirs(self.audio_folder, exist_ok=True)
    
    def generate_audio_gtts(self, text: str, language: str = 'hi') -> str:
        """Generate audio using Google TTS (online)"""
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.audio_folder, filename)
            
            # Create TTS object and save
            tts = gTTS(text=text, lang=language, slow=False)
            tts.save(filepath)
            
            print(f"✅ Audio generated: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error generating audio with gTTS: {e}")
            return None
    
    def generate_audio_pyttsx3(self, text: str, language: str = 'hi') -> str:
        """Generate audio using pyttsx3 (offline)"""
        try:
            # Generate unique filename
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(self.audio_folder, filename)
            
            # Initialize engine
            engine = pyttsx3.init()
            engine.setProperty('rate', 150)  # Speed
            engine.setProperty('volume', 0.9)  # Volume
            
            # Save to file
            engine.save_to_file(text, filepath)
            engine.runAndWait()
            
            print(f"✅ Audio generated: {filename}")
            return filename
        except Exception as e:
            print(f"❌ Error generating audio with pyttsx3: {e}")
            return None
    
    def generate_audio(self, text: str, language: str = 'hi') -> str:
        """Generate audio based on configured engine"""
        if self.engine_type == 'gtts':
            return self.generate_audio_gtts(text, language)
        elif self.engine_type == 'pyttsx3':
            return self.generate_audio_pyttsx3(text, language)
        else:
            print(f"❌ Unknown TTS engine: {self.engine_type}")
            return None
    
    def get_audio_path(self, filename: str) -> str:
        """Get full path to audio file"""
        return os.path.join(self.audio_folder, filename)
    
    def audio_exists(self, filename: str) -> bool:
        """Check if audio file exists"""
        filepath = self.get_audio_path(filename)
        return os.path.exists(filepath)
    
    def delete_audio(self, filename: str) -> bool:
        """Delete audio file"""
        try:
            filepath = self.get_audio_path(filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                print(f"🗑️ Audio deleted: {filename}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error deleting audio: {e}")
            return False

# Global TTS service instance
tts_service = TTSService()
