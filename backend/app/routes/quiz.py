from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.quiz import Quiz, Question
from app.models.score import Score
from app.models.answer import UserAnswer
from datetime import datetime, timezone # 1. Import timezone

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/<int:quiz_id>/start', methods=['GET'])
@jwt_required()
def start_quiz(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        if not quiz.is_active:
            return jsonify({'error': 'Quiz is not active'}), 400
        
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        if not questions:
            return jsonify({'error': 'Quiz has no questions'}), 400
        
        quiz_data = {
            'quiz': quiz.to_dict(),
            'questions': [q.to_dict_without_answer() for q in questions],
            'start_time': datetime.now(timezone.utc).isoformat() # Use timezone-aware time
        }
        return jsonify(quiz_data), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        answers = data.get('answers', {})
        start_time_str = data.get('start_time')

        # Handle quiz retakes by deleting previous answers
        UserAnswer.query.filter_by(user_id=user_id, quiz_id=quiz_id).delete()
        
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        total_score = 0
        for question in questions:
            user_answer = answers.get(str(question.id))
            
            new_answer = UserAnswer(
                user_id=user_id,
                quiz_id=quiz_id,
                question_id=question.id,
                selected_option=user_answer if user_answer else 0,
            )
            db.session.add(new_answer)
            
            if user_answer and str(user_answer) == str(question.correct_answer):
                total_score += 1

        # Calculate time taken
        time_taken = 0
        if start_time_str:
            # --- FIX: Replace 'Z' with '+00:00' to handle the ISO format correctly ---
            start_time = datetime.fromisoformat(start_time_str.replace('Z', '+00:00'))
            end_time = datetime.now(timezone.utc)
            time_taken = (end_time - start_time).total_seconds()

        # Create a new score record for this attempt
        new_score = Score(
            user_id=user_id,
            quiz_id=quiz_id,
            total_scored=total_score,
            total_questions=len(questions),
            time_taken=int(time_taken)
        )
        db.session.add(new_score)
        db.session.commit()

        return jsonify({
            'message': 'Quiz submitted successfully',
            'results': { 'score': new_score.to_dict() }
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"An error occurred in submit_quiz: {e}")
        return jsonify({'error': 'An internal error occurred while submitting the quiz.'}), 500
