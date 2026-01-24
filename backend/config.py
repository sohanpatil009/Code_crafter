import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Flask settings
    DEBUG = os.getenv('DEBUG', 'True') == 'True'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Database settings
    DATABASE_TYPE = os.getenv('DATABASE_TYPE', 'mongodb')  # mongodb or postgresql
    MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
    MONGODB_DB = os.getenv('MONGODB_DB', 'crop_disease_db')
    POSTGRES_URI = os.getenv('POSTGRES_URI', 'postgresql://localhost:5432/crop_disease_db')
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # ML Model settings
    MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'trained_models', 'crop_disease_model.h5')
    IMAGE_SIZE = (224, 224)  # Model input size
    
    # Audio settings
    AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), 'audio_files', 'generated')
    TTS_ENGINE = os.getenv('TTS_ENGINE', 'gtts')  # gtts or pyttsx3
    
    # Supported languages
    SUPPORTED_LANGUAGES = {
        'hi': 'Hindi',
        'en': 'English',
        'mr': 'Marathi',
        'ta': 'Tamil',
        'te': 'Telugu',
        'gu': 'Gujarati',
        'pa': 'Punjabi',
        'bn': 'Bengali'
    }
    
    # Disease classes (example - update based on your model)
    DISEASE_CLASSES = [
        'Tomato_Early_Blight',
        'Tomato_Late_Blight',
        'Tomato_Healthy',
        'Potato_Early_Blight',
        'Potato_Late_Blight',
        'Potato_Healthy',
        'Corn_Common_Rust',
        'Corn_Gray_Leaf_Spot',
        'Corn_Healthy'
    ]
    
    @staticmethod
    def init_app(app):
        """Initialize application directories"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.AUDIO_FOLDER, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
