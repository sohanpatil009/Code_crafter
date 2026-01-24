from googletrans import Translator
from langdetect import detect
from config import Config

class TranslationService:
    """Translation service for multi-language support"""
    
    def __init__(self):
        self.translator = Translator()
        self.supported_languages = Config.SUPPORTED_LANGUAGES
    
    def translate_text(self, text: str, target_lang: str = 'hi', source_lang: str = 'en') -> str:
        """Translate text to target language"""
        try:
            # Check if target language is supported
            if target_lang not in self.supported_languages:
                print(f"⚠️ Language {target_lang} not supported, using English")
                target_lang = 'en'
            
            # Skip translation if already in target language
            if source_lang == target_lang:
                return text
            
            # Translate
            translated = self.translator.translate(text, src=source_lang, dest=target_lang)
            return translated.text
        except Exception as e:
            print(f"❌ Translation error: {e}")
            return text  # Return original text on error
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            lang = detect(text)
            return lang
        except Exception as e:
            print(f"❌ Language detection error: {e}")
            return 'en'  # Default to English
    
    def translate_disease_info(self, disease_info: dict, target_lang: str = 'hi') -> dict:
        """Translate complete disease information"""
        try:
            translated_info = {
                'name': self.translate_text(disease_info.get('name', ''), target_lang),
                'description': self.translate_text(disease_info.get('description', ''), target_lang),
                'symptoms': [self.translate_text(symptom, target_lang) 
                           for symptom in disease_info.get('symptoms', [])],
                'treatment': self.translate_text(disease_info.get('treatment', ''), target_lang),
                'prevention': self.translate_text(disease_info.get('prevention', ''), target_lang)
            }
            return translated_info
        except Exception as e:
            print(f"❌ Error translating disease info: {e}")
            return disease_info  # Return original on error
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages"""
        return self.supported_languages
    
    def is_language_supported(self, lang_code: str) -> bool:
        """Check if language is supported"""
        return lang_code in self.supported_languages

# Global translation service instance
translation_service = TranslationService()
