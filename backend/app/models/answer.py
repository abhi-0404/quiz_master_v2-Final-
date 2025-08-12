from app import db
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint
from app.utils.helpers import to_ist

class UserAnswer(db.Model):
    __tablename__ = 'user_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    selected_option = db.Column(db.Integer, nullable=False) # Stores 1, 2, 3, or 4
    attempt_timestamp = db.Column(db.DateTime(timezone=True), default=lambda: to_ist())

    # Relationships
    user = db.relationship('User', backref=db.backref('answers', lazy=True))
    quiz = db.relationship('Quiz', backref=db.backref('answers', lazy=True))
    question = db.relationship('Question', backref=db.backref('answers', lazy=True))

    # Ensures a user can only answer a specific question in a quiz once
    __table_args__ = (UniqueConstraint('user_id', 'quiz_id', 'question_id', name='_user_quiz_question_uc'),)

    def __repr__(self):
        return f'<UserAnswer User:{self.user_id} Quiz:{self.quiz_id} Q:{self.question_id} Opt:{self.selected_option}>'

    def as_dict(self):
        return {c.key: getattr(self, c.key) for c in self.__table__.columns}
