from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from datetime import datetime
from app.models.user import User
from app.models.quiz import Quiz, Question
from app.models.score import Score
from app.models.answer import UserAnswer
from app.models.subject import Subject, Chapter
from sqlalchemy import func

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard/stats', methods=['GET'])
@jwt_required()
def get_user_dashboard_stats():
    """
    Provides statistics for the user dashboard cards.
    """
    try:
        user_id = get_jwt_identity()
        user_scores = Score.query.filter_by(user_id=user_id).all()
        
        quizzes_taken = len(user_scores)
        total_questions_answered = 0
        average_score = 0
        best_score = 0
        
        if quizzes_taken > 0:
            total_questions_answered = sum(score.total_questions for score in user_scores)
            percentages = [((score.total_scored / score.total_questions) * 100) for score in user_scores if score.total_questions > 0]
            if percentages:
                average_score = round(sum(percentages) / len(percentages), 1)
                best_score = round(max(percentages), 1)

        stats = {
            'quizzes_taken': quizzes_taken,
            'average_score': average_score,
            'best_score': best_score,
            'total_questions_answered': total_questions_answered
        }
        return jsonify({'stats': stats}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/dashboard/graph-data', methods=['GET'])
@jwt_required()
def get_user_graph_data():
    """
    Provides data for the user's performance graph.
    """
    try:
        user_id = get_jwt_identity()
        # Get the 10 most recent scores
        scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.asc()).limit(10).all()
        
        labels = []
        data = []
        for score in scores:
            labels.append(score.quiz.title if score.quiz else 'Unknown Quiz')
            percentage = (score.total_scored / score.total_questions) * 100 if score.total_questions > 0 else 0
            data.append(round(percentage, 2))
            
        return jsonify({'labels': labels, 'data': data}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# (Keep your other user routes like /quizzes, /scores, /profile as they are)
@user_bp.route('/quizzes', methods=['GET'])
@jwt_required()
def get_available_quizzes():
    try:
        user_id = get_jwt_identity()
        attempted_quiz_ids = {score.quiz_id for score in Score.query.filter_by(user_id=user_id).all()}
        quizzes = Quiz.query.filter_by(is_active=True).order_by(Quiz.date_of_quiz.desc()).all()
        quiz_data = []
        for quiz in quizzes:
            quiz_info = quiz.to_dict()
            quiz_info['user_has_attempted'] = quiz.id in attempted_quiz_ids
            quiz_data.append(quiz_info)
        return jsonify(quiz_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/scores', methods=['GET'])
@jwt_required()
def get_user_scores():
    try:
        user_id = get_jwt_identity()
        scores = Score.query.filter_by(user_id=user_id).order_by(Score.timestamp_of_attempt.desc()).all()
        return jsonify([score.to_dict() for score in scores]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@user_bp.route('/scores/<int:score_id>', methods=['GET'])
@jwt_required()
def get_score_details(score_id):
    try:
        user_id = get_jwt_identity()
        score = Score.query.filter_by(id=score_id, user_id=user_id).first_or_404()
        responses = UserAnswer.query.filter_by(user_id=user_id, quiz_id=score.quiz_id).all()
        detailed_results = []
        for res in responses:
            question = res.question
            is_correct = str(res.selected_option) == str(question.correct_answer)
            detailed_results.append({
                'question_statement': question.question_statement,
                'options': [question.option1, question.option2, question.option3, question.option4],
                'correct_answer': question.correct_answer,
                'selected_answer': res.selected_option,
                'is_correct': is_correct
            })
        return jsonify({'score': score.to_dict(), 'results': detailed_results}), 200
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
        if data.get('full_name'):
            user.full_name = data['full_name']
        if data.get('qualification'):
            user.qualification = data['qualification']
        if data.get('dob'):
            try:
                user.dob = datetime.strptime(data['dob'], '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
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
