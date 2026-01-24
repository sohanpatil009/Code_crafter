import os
import uuid
from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from config import Config
from api.validators import validate_image_file, validate_language, sanitize_filename
from api.middleware import log_request, error_handler
from services.ml_service import ml_service
from services.tts_service import tts_service
from services.translation_service import translation_service
from database.queries import db_queries
from database.models import PredictionRecord, UserPreference

# Create Blueprint
api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/health', methods=['GET'])
@log_request
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'message': 'API is running',
        'version': '1.0.0'
    })

@api.route('/predict', methods=['POST'])
@log_request
@error_handler
def predict_disease():
    """Upload image and get disease prediction"""
    # Check if file is present
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No image file provided'}), 400
    
    file = request.files['image']
    language = request.form.get('language', 'en')
    user_id = request.form.get('user_id', None)
    
    # Validate file
    is_valid, message = validate_image_file(file)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400
    
    # Validate language
    is_valid, message = validate_language(language)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400
    
    # Save uploaded file
    filename = f"{uuid.uuid4()}_{sanitize_filename(file.filename)}"
    filepath = os.path.join(Config.UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    # Make prediction
    prediction_result = ml_service.predict(filepath)
    if not prediction_result:
        return jsonify({'success': False, 'error': 'Prediction failed'}), 500
    
    # Get disease information
    disease_info = db_queries.get_disease_info(prediction_result['disease_name'])
    if not disease_info:
        disease_info = {
            'name': prediction_result['disease_name'],
            'description': 'Disease information not available',
            'symptoms': [],
            'treatment': 'Consult agricultural expert',
            'prevention': 'Follow good agricultural practices'
        }
    
    # Translate disease info if needed
    if language != 'en':
        disease_info = translation_service.translate_disease_info(disease_info, language)
    
    # Save prediction record
    record = PredictionRecord(
        image_path=filepath,
        disease_name=prediction_result['disease_name'],
        confidence=prediction_result['confidence'],
        language=language,
        user_id=user_id
    )
    prediction_id = db_queries.save_prediction(record)
    
    return jsonify({
        'success': True,
        'prediction_id': prediction_id,
        'disease_name': prediction_result['disease_name'],
        'confidence': prediction_result['confidence'],
        'disease_info': disease_info,
        'all_predictions': prediction_result['all_predictions']
    })

@api.route('/tts/generate', methods=['POST'])
@log_request
@error_handler
def generate_tts():
    """Generate text-to-speech audio"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'error': 'Text is required'}), 400
    
    text = data['text']
    language = data.get('language', 'hi')
    
    # Validate language
    is_valid, message = validate_language(language)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400
    
    # Generate audio
    audio_filename = tts_service.generate_audio(text, language)
    if not audio_filename:
        return jsonify({'success': False, 'error': 'Audio generation failed'}), 500
    
    return jsonify({
        'success': True,
        'audio_file': audio_filename,
        'audio_url': f'/api/tts/audio/{audio_filename}'
    })

@api.route('/tts/audio/<filename>', methods=['GET'])
@log_request
def get_audio(filename):
    """Stream or download audio file"""
    filepath = tts_service.get_audio_path(filename)
    
    if not tts_service.audio_exists(filename):
        return jsonify({'success': False, 'error': 'Audio file not found'}), 404
    
    return send_file(filepath, mimetype='audio/mpeg')

@api.route('/translate', methods=['POST'])
@log_request
@error_handler
def translate_text():
    """Translate text to target language"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({'success': False, 'error': 'Text is required'}), 400
    
    text = data['text']
    target_lang = data.get('target_lang', 'hi')
    source_lang = data.get('source_lang', 'en')
    
    # Validate language
    is_valid, message = validate_language(target_lang)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400
    
    # Translate
    translated_text = translation_service.translate_text(text, target_lang, source_lang)
    
    return jsonify({
        'success': True,
        'original_text': text,
        'translated_text': translated_text,
        'source_lang': source_lang,
        'target_lang': target_lang
    })

@api.route('/languages', methods=['GET'])
@log_request
def get_languages():
    """Get supported languages"""
    return jsonify({
        'success': True,
        'languages': Config.SUPPORTED_LANGUAGES
    })

@api.route('/language/preference', methods=['POST'])
@log_request
@error_handler
def set_language_preference():
    """Set user language preference"""
    data = request.get_json()
    
    if not data or 'user_id' not in data or 'language' not in data:
        return jsonify({'success': False, 'error': 'user_id and language are required'}), 400
    
    user_id = data['user_id']
    language = data['language']
    
    # Validate language
    is_valid, message = validate_language(language)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400
    
    # Save preference
    preference = UserPreference(user_id=user_id, language=language)
    success = db_queries.save_user_preference(preference)
    
    if success:
        return jsonify({'success': True, 'message': 'Language preference saved'})
    else:
        return jsonify({'success': False, 'error': 'Failed to save preference'}), 500

@api.route('/history', methods=['GET'])
@log_request
@error_handler
def get_history():
    """Get prediction history"""
    user_id = request.args.get('user_id', None)
    limit = int(request.args.get('limit', 50))
    
    history = db_queries.get_prediction_history(user_id, limit)
    
    return jsonify({
        'success': True,
        'count': len(history),
        'history': history
    })

@api.route('/diseases', methods=['GET'])
@log_request
@error_handler
def get_all_diseases():
    """Get all diseases"""
    diseases = db_queries.get_all_diseases()
    
    return jsonify({
        'success': True,
        'count': len(diseases),
        'diseases': diseases
    })

@api.route('/disease/<disease_name>', methods=['GET'])
@log_request
@error_handler
def get_disease_details(disease_name):
    """Get disease details"""
    language = request.args.get('language', 'en')
    
    disease_info = db_queries.get_disease_info(disease_name)
    if not disease_info:
        return jsonify({'success': False, 'error': 'Disease not found'}), 404
    
    # Translate if needed
    if language != 'en':
        disease_info = translation_service.translate_disease_info(disease_info, language)
    
    return jsonify({
        'success': True,
        'disease': disease_info
    })

@api.route('/feedback', methods=['POST'])
@log_request
@error_handler
def submit_feedback():
    """Submit user feedback"""
    data = request.get_json()
    
    if not data or 'prediction_id' not in data or 'feedback' not in data:
        return jsonify({'success': False, 'error': 'prediction_id and feedback are required'}), 400
    
    # TODO: Implement feedback storage
    
    return jsonify({
        'success': True,
        'message': 'Feedback submitted successfully'
    })
