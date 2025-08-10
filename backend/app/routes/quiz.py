from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models.user import User
from app.models.quiz import Quiz, Question
from app.models.score import Score
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)

@quiz_bp.route('/<int:quiz_id>/start', methods=['GET'])
@jwt_required()
def start_quiz(quiz_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        quiz = Quiz.query.get_or_404(quiz_id)
        
        if not quiz.is_active:
            return jsonify({'error': 'Quiz is not active'}), 400
        
        # Get questions without correct answers
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        if not questions:
            return jsonify({'error': 'Quiz has no questions'}), 400
        
        quiz_data = {
            'quiz': quiz.to_dict(),
            'questions': [question.to_dict_without_answer() for question in questions],
            'start_time': datetime.utcnow().isoformat()
        }
        
        return jsonify(quiz_data), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/<int:quiz_id>/submit', methods=['POST'])
@jwt_required()
def submit_quiz(quiz_id):
    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        quiz = Quiz.query.get_or_404(quiz_id)
        data = request.get_json()
        
        if not data.get('answers'):
            return jsonify({'error': 'Answers are required'}), 400
        
        if not data.get('start_time'):
            return jsonify({'error': 'Start time is required'}), 400
        
        # Calculate time taken
        start_time = datetime.fromisoformat(data['start_time'].replace('Z', ''))
        end_time = datetime.utcnow()
        time_taken = int((end_time - start_time).total_seconds())
        
        # Get all questions for this quiz
        questions = Question.query.filter_by(quiz_id=quiz_id).all()
        
        if not questions:
            return jsonify({'error': 'Quiz has no questions'}), 400
        
        # Calculate score
        correct_answers = 0
        user_answers = data['answers']  # Dict with question_id as key and answer as value
        
        for question in questions:
            user_answer = user_answers.get(str(question.id))
            if user_answer is not None and int(user_answer) == question.correct_answer:
                correct_answers += 1
        
        # Save score
        score = Score(
            user_id=user_id,
            quiz_id=quiz_id,
            total_scored=correct_answers,
            total_questions=len(questions),
            time_taken=time_taken,
            answers=user_answers
        )
        
        db.session.add(score)
        db.session.commit()
        
        # Prepare detailed results
        results = {
            'score': score.to_dict(),
            'questions_review': []
        }
        
        # Add question review
        for question in questions:
            user_answer = user_answers.get(str(question.id))
            is_correct = user_answer is not None and int(user_answer) == question.correct_answer
            
            question_review = {
                'question': question.to_dict(),
                'user_answer': int(user_answer) if user_answer is not None else None,
                'is_correct': is_correct
            }
            results['questions_review'].append(question_review)
        
        return jsonify({
            'message': 'Quiz submitted successfully',
            'results': results
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/<int:quiz_id>/details', methods=['GET'])
@jwt_required()
def get_quiz_details(quiz_id):
    try:
        quiz = Quiz.query.get_or_404(quiz_id)
        
        quiz_details = quiz.to_dict()
        
        # Add question count
        question_count = Question.query.filter_by(quiz_id=quiz_id).count()
        quiz_details['questions_count'] = question_count
        
        # Add chapter and subject info
        if quiz.chapter:
            quiz_details['chapter'] = {
                'id': quiz.chapter.id,
                'name': quiz.chapter.name,
                'description': quiz.chapter.description
            }
            
            if quiz.chapter.subject:
                quiz_details['subject'] = {
                    'id': quiz.chapter.subject.id,
                    'name': quiz.chapter.subject.name,
                    'description': quiz.chapter.subject.description
                }
        
        return jsonify(quiz_details), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@quiz_bp.route('/attempt/<int:score_id>', methods=['GET'])
@jwt_required()
def get_quiz_attempt(score_id):
    try:
        user_id = get_jwt_identity()
        score = Score.query.filter_by(id=score_id, user_id=user_id).first()
        
        if not score:
            return jsonify({'error': 'Quiz attempt not found'}), 404
        
        # Get questions with user's answers
        questions = Question.query.filter_by(quiz_id=score.quiz_id).all()
        
        attempt_details = {
            'score': score.to_dict(),
            'quiz': score.quiz.to_dict() if score.quiz else None,
            'questions_review': []
        }
        
        user_answers = score.answers or {}
        
        for question in questions:
            user_answer = user_answers.get(str(question.id))
            is_correct = user_answer is not None and int(user_answer) == question.correct_answer
            
            question_review = {
                'question': question.to_dict(),
                'user_answer': int(user_answer) if user_answer is not None else None,
                'is_correct': is_correct
            }
            attempt_details['questions_review'].append(question_review)
        
        return jsonify(attempt_details), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
