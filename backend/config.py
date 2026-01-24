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
    
    # Auto-generate audio for predictions
    AUTO_GENERATE_AUDIO = os.getenv('AUTO_GENERATE_AUDIO', 'False') == 'True'
    
    # Disease classes - New Plant Diseases Dataset (38 classes)
    DISEASE_CLASSES = [
        # Apple (4)
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        # Blueberry (1)
        'Blueberry___healthy',
        # Cherry (2)
        'Cherry_(including_sour)___Powdery_mildew',
        'Cherry_(including_sour)___healthy',
        # Corn (4)
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        'Corn_(maize)___Common_rust_',
        'Corn_(maize)___Northern_Leaf_Blight',
        'Corn_(maize)___healthy',
        # Grape (4)
        'Grape___Black_rot',
        'Grape___Esca_(Black_Measles)',
        'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
        'Grape___healthy',
        # Orange (1)
        'Orange___Haunglongbing_(Citrus_greening)',
        # Peach (2)
        'Peach___Bacterial_spot',
        'Peach___healthy',
        # Pepper (2)
        'Pepper,_bell___Bacterial_spot',
        'Pepper,_bell___healthy',
        # Potato (3)
        'Potato___Early_blight',
        'Potato___Late_blight',
        'Potato___healthy',
        # Raspberry (1)
        'Raspberry___healthy',
        # Soybean (1)
        'Soybean___healthy',
        # Squash (1)
        'Squash___Powdery_mildew',
        # Strawberry (2)
        'Strawberry___Leaf_scorch',
        'Strawberry___healthy',
        # Tomato (10)
        'Tomato___Bacterial_spot',
        'Tomato___Early_blight',
        'Tomato___Late_blight',
        'Tomato___Leaf_Mold',
        'Tomato___Septoria_leaf_spot',
        'Tomato___Spider_mites Two-spotted_spider_mite',
        'Tomato___Target_Spot',
        'Tomato___Tomato_Yellow_Leaf_Curl_Virus',
        'Tomato___Tomato_mosaic_virus',
        'Tomato___healthy'
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
