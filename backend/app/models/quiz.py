from app import db
from datetime import datetime

class Quiz(db.Model):
    __tablename__ = 'quizzes'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id'), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # Duration in minutes
    date_of_quiz = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    scores = db.relationship('Score', backref='quiz', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'chapter_id': self.chapter_id,
            'chapter_name': self.chapter.name if self.chapter else None,
            'subject_name': self.chapter.subject.name if self.chapter and self.chapter.subject else None,
            'duration': self.duration,
            'date_of_quiz': self.date_of_quiz.isoformat() if self.date_of_quiz else None,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'questions_count': len(self.questions)
        }
    
    def __repr__(self):
        return f'<Quiz {self.title}>'

class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id'), nullable=False)
    question_statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(500), nullable=False)
    option2 = db.Column(db.String(500), nullable=False)
    option3 = db.Column(db.String(500), nullable=False)
    option4 = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(20), nullable=False)  # '1', '2', '3', '4' or '1,2' for multiple
    marks = db.Column(db.Integer, default=1)
    negative_marks = db.Column(db.Integer, default=0)
    type = db.Column(db.String(16), default='single')  # 'single' or 'multiple'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_statement': self.question_statement,
            'options': [self.option1, self.option2, self.option3, self.option4],
            'correct_answer': self.correct_answer,
            'marks': self.marks,
            'negative_marks': self.negative_marks,
            'type': self.type,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'correct_answers': [int(x) for x in self.correct_answer.split(',')] if self.type == 'multiple' else None
        }
    
    def to_dict_without_answer(self):
        """Return question without correct answer for quiz attempts"""
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question_statement': self.question_statement,
            'options': [self.option1, self.option2, self.option3, self.option4]
        }
    
    def __repr__(self):
        return f'<Question {self.id}>'
