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

# Delete user
@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        if user.email == 'admin@quizmaster.com':
            return jsonify({'error': 'Cannot delete admin user'}), 403
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Update user role
@admin_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(user_id):
    try:
        data = request.get_json()
        role = data.get('role')
        if role not in ['user', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        user = User.query.get_or_404(user_id)
        # Always keep hardcoded admin as admin
        if user.email == 'admin@quizmaster.com':
            user.role = 'admin'
            return jsonify({'error': 'Cannot change admin role'}), 403
        else:
            user.role = role
        db.session.commit()
        return jsonify({'message': 'Role updated', 'user': user.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
# User count endpoint
@admin_bp.route('/users/count', methods=['GET'])
@admin_required
def get_user_count():
    try:
        count = User.query.filter(User.role != 'admin').count()
        return jsonify({'count': count}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['POST'])
@admin_required
def add_question(quiz_id):
    try:
        data = request.get_json()
        options = data.get('options', [])
        if len(options) != 4:
            return jsonify({'error': 'Exactly 4 options are required.'}), 400
        type_ = data.get('type', 'single')
        marks = data.get('marks', 1)
        negative_marks = data.get('negative_marks', 0)
        correct = data.get('correct', 0)
        correctMultiple = data.get('correctMultiple', [])
        if type_ == 'multiple':
            correct_answer = ','.join(str(i+1) for i in correctMultiple)
        else:
            correct_answer = str(correct + 1)
        question = Question(
            quiz_id=quiz_id,
            question_statement=data.get('text'),
            option1=options[0],
            option2=options[1],
            option3=options[2],
            option4=options[3],
            correct_answer=correct_answer,
            marks=marks,
            negative_marks=negative_marks,
            type=type_
        )
        db.session.add(question)
        db.session.commit()
        return jsonify({'message': 'Question added', 'question': question.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/quizzes/<int:quiz_id>/questions', methods=['GET'])
@admin_required
def get_questions(quiz_id):
    try:
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        return jsonify({'questions': [q.to_dict() for q in questions]}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Edit question
@admin_bp.route('/questions/<int:question_id>', methods=['PUT'])
@admin_required
def update_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        data = request.get_json()
        options = data.get('options', [])
        if len(options) == 4:
            question.option1, question.option2, question.option3, question.option4 = options
        question.question_statement = data.get('text', question.question_statement)
        question.marks = data.get('marks', question.marks)
        question.negative_marks = data.get('negative_marks', question.negative_marks)
        question.type = data.get('type', question.type)
        if question.type == 'multiple':
            correctMultiple = data.get('correctMultiple', [])
            question.correct_answer = ','.join(str(i+1) for i in correctMultiple)
        else:
            question.correct_answer = str(data.get('correct', 0) + 1)
        db.session.commit()
        return jsonify({'message': 'Question updated', 'question': question.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Delete question
@admin_bp.route('/questions/<int:question_id>', methods=['DELETE'])
@admin_required
def delete_question(question_id):
    try:
        question = Question.query.get_or_404(question_id)
        db.session.delete(question)
        db.session.commit()
        return jsonify({'message': 'Question deleted'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# --- USER MANAGEMENT ---

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    try:
        users = User.query.all()
        user_data = []
        for user in users:
            user_scores = Score.query.filter_by(user_id=user.id).all()
            total_attempts = len(user_scores)
            avg_score = 0
            quizzes_attempted = set()
            for score in user_scores:
                quizzes_attempted.add(score.quiz_id)
            if total_attempts > 0:
                total_questions_sum = sum(score.total_questions for score in user_scores if score.total_questions)
                if total_questions_sum > 0:
                    avg_score = sum(score.total_scored for score in user_scores) / total_questions_sum * 100
            user_info = user.to_dict()
            user_info.update({
                'total_attempts': total_attempts,
                'average_score': round(avg_score, 2),
                'total_quizzes_attempted': len(quizzes_attempted)
            })
            user_data.append(user_info)
        return jsonify({ 'users': user_data }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
