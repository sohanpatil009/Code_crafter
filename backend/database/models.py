from datetime import datetime
from typing import Dict, List, Optional

class PredictionRecord:
    """Model for disease prediction records"""
    
    def __init__(self, image_path: str, disease_name: str, confidence: float, 
                 language: str = 'en', user_id: Optional[str] = None):
        self.image_path = image_path
        self.disease_name = disease_name
        self.confidence = confidence
        self.language = language
        self.user_id = user_id
        self.timestamp = datetime.utcnow()
        self.audio_file = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for database storage"""
        return {
            'image_path': self.image_path,
            'disease_name': self.disease_name,
            'confidence': self.confidence,
            'language': self.language,
            'user_id': self.user_id,
            'timestamp': self.timestamp,
            'audio_file': self.audio_file
        }

class DiseaseInfo:
    """Model for disease information"""
    
    def __init__(self, name: str, description: str, symptoms: List[str],
                 treatment: str, prevention: str):
        self.name = name
        self.description = description
        self.symptoms = symptoms
        self.treatment = treatment
        self.prevention = prevention
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'description': self.description,
            'symptoms': self.symptoms,
            'treatment': self.treatment,
            'prevention': self.prevention
        }

class UserPreference:
    """Model for user language preferences"""
    
    def __init__(self, user_id: str, language: str = 'en'):
        self.user_id = user_id
        self.language = language
        self.updated_at = datetime.utcnow()
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'user_id': self.user_id,
            'language': self.language,
            'updated_at': self.updated_at
        }
