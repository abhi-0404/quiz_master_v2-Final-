from app import db
from datetime import datetime

class Score(db.Model):
    __tablename__ = 'scores'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    total_scored = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    time_taken = db.Column(db.Integer)  # Time taken in seconds
    timestamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    answers = db.Column(db.JSON)  # Store user's answers as JSON
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'quiz_id': self.quiz_id,
            'quiz_title': self.quiz.title if self.quiz else None,
            'total_scored': self.total_scored,
            'total_questions': self.total_questions,
            'percentage': round((self.total_scored / self.total_questions) * 100, 2) if self.total_questions > 0 else 0,
            'time_taken': self.time_taken,
            'timestamp_of_attempt': self.timestamp_of_attempt.isoformat() if self.timestamp_of_attempt else None,
            'answers': self.answers
        }
    
    def __repr__(self):
        return f'<Score {self.user_id}-{self.quiz_id}: {self.total_scored}/{self.total_questions}>'
