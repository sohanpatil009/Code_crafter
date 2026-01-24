import os
from werkzeug.utils import secure_filename
from config import Config

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def validate_image_file(file) -> tuple:
    """Validate uploaded image file"""
    if not file:
        return False, "No file provided"
    
    if file.filename == '':
        return False, "No file selected"
    
    if not allowed_file(file.filename):
        return False, f"Invalid file type. Allowed: {', '.join(Config.ALLOWED_EXTENSIONS)}"
    
    return True, "Valid file"

def validate_language(lang_code: str) -> tuple:
    """Validate language code"""
    if lang_code not in Config.SUPPORTED_LANGUAGES:
        return False, f"Unsupported language. Supported: {', '.join(Config.SUPPORTED_LANGUAGES.keys())}"
    return True, "Valid language"

def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage"""
    return secure_filename(filename)
