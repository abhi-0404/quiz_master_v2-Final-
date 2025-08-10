from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, cache
from app.models.user import User
from app.models.subject import Subject, Chapter
from app.models.quiz import Quiz, Question
from app.models.score import Score
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def get_user_dashboard():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Get user statistics
        user_scores = Score.query.filter_by(user_id=user_id).all()
        total_attempts = len(user_scores)
        
        avg_score = 0
        best_score = 0
        
        if total_attempts > 0:
            scores_percentage = [score.total_scored / score.total_questions * 100 for score in user_scores]
            avg_score = sum(scores_percentage) / len(scores_percentage)
            best_score = max(scores_percentage)
        
        # Get available quizzes (limit to 5 for dashboard)
        available_quizzes = Quiz.query.filter_by(is_active=True).limit(5).all()
        
        dashboard_data = {
            'user': user.to_dict(),
            'stats': {
                'total_attempts': total_attempts,
                'average_score': round(avg_score, 2),
                'best_score': round(best_score, 2)
            },
            'available_quizzes': [quiz.to_dict() for quiz in available_quizzes]
        }
        
        return jsonify(dashboard_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/quizzes', methods=['GET'])
@jwt_required()
def get_available_quizzes():
    try:
        # Check cache first
        cache_key = 'available_quizzes'
        cached_quizzes = cache.get(cache_key)
        
        if cached_quizzes:
            return jsonify(cached_quizzes), 200
        
        quizzes = Quiz.query.filter_by(is_active=True).all()
        quiz_data = []
        
        for quiz in quizzes:
            quiz_info = quiz.to_dict()
            # Add subject information
            if quiz.chapter and quiz.chapter.subject:
                quiz_info['subject_name'] = quiz.chapter.subject.name
            quiz_data.append(quiz_info)
        
        # Cache for 10 minutes
        cache.set(cache_key, quiz_data, timeout=600)
        
        return jsonify(quiz_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/subjects', methods=['GET'])
@jwt_required()
def get_subjects_with_quizzes():
    try:
        # Check cache first
        cache_key = 'subjects_with_quizzes'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return jsonify(cached_data), 200
        
        subjects = Subject.query.all()
        subjects_data = []
        
        for subject in subjects:
            subject_info = subject.to_dict()
            chapters_with_quizzes = []
            
            for chapter in subject.chapters:
                active_quizzes = [quiz for quiz in chapter.quizzes if quiz.is_active]
                if active_quizzes:
                    chapter_info = chapter.to_dict()
                    chapter_info['quizzes'] = [quiz.to_dict() for quiz in active_quizzes]
                    chapters_with_quizzes.append(chapter_info)
            
            if chapters_with_quizzes:
                subject_info['chapters'] = chapters_with_quizzes
                subjects_data.append(subject_info)
        
        # Cache for 15 minutes
        cache.set(cache_key, subjects_data, timeout=900)
        
        return jsonify(subjects_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    try:
        user_id = get_jwt_identity()
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        scores = Score.query.filter_by(user_id=user_id)\
                     .order_by(Score.timestamp_of_attempt.desc())\
                     .paginate(page=page, per_page=per_page, error_out=False)
        
        scores_data = []
        for score in scores.items:
            score_info = score.to_dict()
            # Add additional quiz information
            if score.quiz:
                score_info['quiz_title'] = score.quiz.title
                if score.quiz.chapter:
                    score_info['chapter_name'] = score.quiz.chapter.name
                    if score.quiz.chapter.subject:
                        score_info['subject_name'] = score.quiz.chapter.subject.name
            scores_data.append(score_info)
        
        return jsonify({
            'scores': scores_data,
            'pagination': {
                'page': page,
                'pages': scores.pages,
                'per_page': per_page,
                'total': scores.total,
                'has_next': scores.has_next,
                'has_prev': scores.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if data.get('full_name'):
            user.full_name = data['full_name']
        
        if data.get('qualification'):
            user.qualification = data['qualification']
        
        if data.get('dob'):
            try:
                user.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Password change
        if data.get('current_password') and data.get('new_password'):
            if not user.check_password(data['current_password']):
                return jsonify({'error': 'Current password is incorrect'}), 400
            user.set_password(data['new_password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
