from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
# from app.models.user import User  # Moved import inside functions to avoid circular import
import pytz
from datetime import datetime

def to_ist(dt=None):
    """
    Convert a datetime object to Indian Standard Time (IST).
    If dt is None, use current UTC time.
    """
    ist = pytz.timezone('Asia/Kolkata')
    if dt is None:
        dt = datetime.utcnow()
        dt = pytz.utc.localize(dt)
    elif dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    return dt.astimezone(ist)

def admin_required(f):
    """Decorator to require admin access"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        from app.models.user import User
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    """Decorator to require user authentication"""
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        from app.models.user import User
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        return f(*args, **kwargs)
    return decorated_function

def validate_required_fields(data, required_fields):
    """Validate that all required fields are present in data"""
    missing_fields = []
    for field in required_fields:
        if field not in data or not data[field]:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, None

def format_time_duration(seconds):
    """Format time duration from seconds to readable format"""
    if not seconds:
        return "N/A"
    
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"

def calculate_percentage(scored, total):
    """Calculate percentage score"""
    if total == 0:
        return 0
    return round((scored / total) * 100, 2)

def get_performance_level(percentage):
    """Get performance level based on percentage"""
    if percentage >= 90:
        return "Excellent"
    elif percentage >= 80:
        return "Very Good"
    elif percentage >= 70:
        return "Good"
    elif percentage >= 60:
        return "Average"
    elif percentage >= 50:
        return "Below Average"
    else:
        return "Poor"

def sanitize_filename(filename):
    """Sanitize filename for safe file operations"""
    import re
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing whitespace and dots
    filename = filename.strip(' .')
    # Limit length
    if len(filename) > 100:
        filename = filename[:100]
    return filename
