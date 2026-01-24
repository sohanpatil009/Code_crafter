from flask import Flask
from flask_cors import CORS
from config import Config
from api.routes import api

def create_app():
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(Config)
    Config.init_app(app)
    
    # Enable CORS
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(api)
    
    @app.route('/')
    def index():
        return {
            'message': 'Crop Disease Detection API',
            'version': '1.0.0',
            'endpoints': {
                'health': '/api/health',
                'predict': '/api/predict',
                'tts_generate': '/api/tts/generate',
                'tts_audio': '/api/tts/audio/<filename>',
                'translate': '/api/translate',
                'languages': '/api/languages',
                'language_preference': '/api/language/preference',
                'history': '/api/history',
                'diseases': '/api/diseases',
                'disease_details': '/api/disease/<disease_name>',
                'feedback': '/api/feedback'
            }
        }
    
    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Crop Disease Detection API...")
    print(f"📍 Running on http://{Config.HOST}:{Config.PORT}")
    print(f"🔧 Debug mode: {Config.DEBUG}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
