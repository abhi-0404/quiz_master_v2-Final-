# Import all models to ensure they are registered with SQLAlchemy

from .user import User
from .subject import Subject, Chapter
from .quiz import Quiz, Question
from .score import Score
from .answer import UserAnswer

__all__ = ['User', 'Subject', 'Chapter', 'Quiz', 'Question', 'Score', 'UserAnswer']
