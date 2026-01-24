from functools import wraps
from flask import request, jsonify
import time

def log_request(f):
    """Middleware to log API requests"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        start_time = time.time()
        print(f"📥 {request.method} {request.path}")
        
        response = f(*args, **kwargs)
        
        duration = time.time() - start_time
        print(f"📤 {request.method} {request.path} - {duration:.2f}s")
        
        return response
    return decorated_function

def error_handler(f):
    """Middleware for error handling"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            print(f"❌ Error in {f.__name__}: {e}")
            return jsonify({
                'success': False,
                'error': str(e),
                'message': 'An error occurred processing your request'
            }), 500
    return decorated_function

def validate_content_type(content_type='application/json'):
    """Middleware to validate request content type"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if content_type not in request.content_type:
                return jsonify({
                    'success': False,
                    'error': f'Content-Type must be {content_type}'
                }), 400
            return f(*args, **kwargs)
        return decorated_function
    return decorator
