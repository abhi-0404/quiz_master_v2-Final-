from app import db
from datetime import datetime
from app.utils.helpers import to_ist

class Subject(db.Model):
    __tablename__ = 'subjects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=lambda: to_ist())
    
    # Relationships
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        # Calculate total quizzes across all chapters of this subject
        quiz_count = sum(len(chapter.quizzes) for chapter in self.chapters)
        
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'chapters_count': len(self.chapters),
            'quiz_count': quiz_count
        }
    
    def __repr__(self):
        return f'<Subject {self.name}>'

class Chapter(db.Model):
    __tablename__ = 'chapters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'subject_id': self.subject_id,
            'subject_name': self.subject.name if self.subject else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'quizzes_count': len(self.quizzes)
        }
    
    def __repr__(self):
        return f'<Chapter {self.name}>'
