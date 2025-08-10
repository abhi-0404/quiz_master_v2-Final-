from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db, cache
from app.models.user import User
from app.models.subject import Subject, Chapter
from app.models.quiz import Quiz, Question
from app.models.score import Score
from functools import wraps
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

# (Keep your existing dashboard, subject, and chapter routes here...)
# --- DASHBOARD ENDPOINTS ---

@admin_bp.route('/dashboard/stats', methods=['GET'])
@admin_required
def get_dashboard_stats():
    try:
        cache_key = 'admin_dashboard_stats'
        cached_stats = cache.get(cache_key)
        if cached_stats:
            return jsonify(cached_stats), 200
        stats = {
            'totalUsers': User.query.filter_by(role='user').count(),
            'totalSubjects': Subject.query.count(),
            'totalQuizzes': Quiz.query.count(),
            'totalAttempts': Score.query.count()
        }
        cache.set(cache_key, stats, timeout=300)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/dashboard/chart-data', methods=['GET'])
@admin_required
def get_chart_data():
    try:
        labels = []
        attempts = []
        today = datetime.utcnow().date()
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            labels.append(day.strftime('%b %d'))
            sample_attempts = Score.query.filter(db.func.date(Score.timestamp_of_attempt) == day).count()
            attempts.append(sample_attempts)
        chart_data = {'labels': labels, 'attempts': attempts}
        return jsonify(chart_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- SUBJECT MANAGEMENT ---

@admin_bp.route('/subjects', methods=['GET'])
@admin_required
def get_subjects():
    try:
        subjects = Subject.query.all()
        return jsonify([subject.to_dict() for subject in subjects]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/subjects', methods=['POST'])
@admin_required
def create_subject():
    try:
        data = request.get_json()
        if not data.get('name'):
            return jsonify({'error': 'Subject name is required'}), 400
        if Subject.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Subject already exists'}), 400
        subject = Subject(name=data['name'], description=data.get('description', ''))
        db.session.add(subject)
        db.session.commit()
        cache.delete('admin_dashboard_stats')
        return jsonify({'message': 'Subject created successfully', 'subject': subject.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/subjects/<int:subject_id>', methods=['PUT'])
@admin_required
def update_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        data = request.get_json()
        if data.get('name'):
            existing = Subject.query.filter(Subject.name == data['name'], Subject.id != subject_id).first()
            if existing:
                return jsonify({'error': 'Subject name already exists'}), 400
            subject.name = data['name']
        if 'description' in data:
            subject.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Subject updated successfully', 'subject': subject.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/subjects/<int:subject_id>', methods=['DELETE'])
@admin_required
def delete_subject(subject_id):
    try:
        subject = Subject.query.get_or_404(subject_id)
        db.session.delete(subject)
        db.session.commit()
        cache.delete('admin_dashboard_stats')
        return jsonify({'message': 'Subject deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- CHAPTER MANAGEMENT ---

@admin_bp.route('/chapters', methods=['GET'])
@admin_required
def get_chapters():
    try:
        chapters = db.session.query(Chapter, Subject.name.label('subject_name')) \
            .join(Subject, Chapter.subject_id == Subject.id).all()
        chapter_list = []
        for chapter, subject_name in chapters:
            chap_dict = chapter.to_dict()
            chap_dict['subject_name'] = subject_name
            chapter_list.append(chap_dict)
        return jsonify(chapter_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/chapters', methods=['POST'])
@admin_required
def create_chapter():
    try:
        data = request.get_json()
        if not data.get('name') or not data.get('subject_id'):
            return jsonify({'errors': {'name': 'Name is required', 'subject_id': 'Subject is required'}}), 400
        subject = Subject.query.get(data['subject_id'])
        if not subject:
            return jsonify({'errors': {'subject_id': 'Invalid subject selected.'}}), 400
        new_chapter = Chapter(name=data['name'], description=data.get('description', ''), subject_id=data['subject_id'])
        db.session.add(new_chapter)
        db.session.commit()
        return jsonify({'message': 'Chapter created successfully', 'chapter': new_chapter.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/chapters/<int:chapter_id>', methods=['PUT'])
@admin_required
def update_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        data = request.get_json()
        if data.get('name'):
            chapter.name = data['name']
        if 'description' in data:
            chapter.description = data['description']
        if data.get('subject_id'):
            chapter.subject_id = data['subject_id']
        db.session.commit()
        return jsonify({'message': 'Chapter updated successfully', 'chapter': chapter.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/chapters/<int:chapter_id>', methods=['DELETE'])
@admin_required
def delete_chapter(chapter_id):
    try:
        chapter = Chapter.query.get_or_404(chapter_id)
        db.session.delete(chapter)
        db.session.commit()
        return jsonify({'message': 'Chapter deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- QUIZ MANAGEMENT ---

@admin_bp.route('/quizzes', methods=['GET'])
@admin_required
def get_quizzes():
    try:
        quizzes = db.session.query(Quiz, Chapter.name.label('chapter_name'), Subject.name.label('subject_name'))\
            .join(Chapter, Quiz.chapter_id == Chapter.id)\
            .join(Subject, Chapter.subject_id == Subject.id).all()
        quiz_list = []
        for quiz, chapter_name, subject_name in quizzes:
            quiz_dict = quiz.to_dict()
            quiz_dict['chapter_name'] = chapter_name
            quiz_dict['subject_name'] = subject_name
            quiz_dict['question_count'] = Question.query.filter_by(quiz_id=quiz.id).count()
            quiz_list.append(quiz_dict)
        return jsonify(quiz_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/quizzes', methods=['POST'])
@admin_required
def create_quiz():
    try:
        data = request.get_json()
        errors = {}
        if not data.get('chapter_id'): errors['chapter_id'] = 'Chapter is required.'
        if not data.get('date_of_quiz'): errors['date_of_quiz'] = 'Date is required.'
        if not data.get('duration'): errors['duration'] = 'Duration is required.'
        if not data.get('title'): errors['title'] = 'Title is required.'
        if errors:
            return jsonify({'errors': errors}), 400

        new_quiz = Quiz(
            chapter_id=data['chapter_id'],
            date_of_quiz=datetime.strptime(data['date_of_quiz'], '%Y-%m-%d'),
            duration=data['duration'],
            title=data['title']
        )
        db.session.add(new_quiz)
        db.session.commit()
        cache.delete('admin_dashboard_stats')
        return jsonify({'message': 'Quiz created successfully', 'quiz': new_quiz.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['PUT'])
@admin_required
def update_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.get_json()
        
        quiz.chapter_id = data.get('chapter_id', quiz.chapter_id)
        quiz.date_of_quiz = datetime.strptime(data.get('date_of_quiz'), '%Y-%m-%d') if data.get('date_of_quiz') else quiz.date_of_quiz
        quiz.duration = data.get('duration', quiz.duration)
        quiz.title = data.get('title', quiz.title)
            
        db.session.commit()
        return jsonify({'message': 'Quiz updated successfully', 'quiz': quiz.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/quizzes/<int:quiz_id>', methods=['DELETE'])
@admin_required
def delete_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        Question.query.filter_by(quiz_id=quiz_id).delete()
        db.session.delete(quiz)
        db.session.commit()
        cache.delete('admin_dashboard_stats')
        return jsonify({'message': 'Quiz deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- USER MANAGEMENT ---
@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    try:
        users = User.query.filter_by(role='user').all()
        user_data = []
        for user in users:
            user_scores = Score.query.filter_by(user_id=user.id).all()
            total_attempts = len(user_scores)
            avg_score = 0
            if total_attempts > 0:
                total_questions_sum = sum(score.total_questions for score in user_scores if score.total_questions)
                if total_questions_sum > 0:
                    avg_score = sum(score.total_scored for score in user_scores) / total_questions_sum * 100
            user_info = user.to_dict()
            user_info.update({
                'total_attempts': total_attempts,
                'average_score': round(avg_score, 2)
            })
            user_data.append(user_info)
        return jsonify(user_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
