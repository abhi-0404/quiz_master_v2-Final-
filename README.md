# Quiz Master V2 - MAD II Project

## Project Overview

Quiz Master V2 is a comprehensive multi-user quiz application designed for exam preparation. It features role-based access control with admin and user roles, providing a complete learning management system for educational institutions.

## Technologies Used

### Backend
- **Flask** - Python web framework for API development
- **SQLite** - Database for data storage
- **SQLAlchemy** - ORM for database operations
- **Flask-JWT-Extended** - JWT authentication
- **Redis** - Caching and session storage
- **Celery** - Background task processing
- **Flask-Mail** - Email functionality

### Frontend
- **Vue.js 3** - Modern JavaScript framework
- **Vue Router** - Client-side routing
- **Vuex** - State management
- **Bootstrap 5** - CSS framework for responsive design
- **Axios** - HTTP client for API communication
- **Chart.js** - Data visualization

## Features

### Core Features
1. **User Authentication & Authorization**
   - JWT-based authentication
   - Role-based access (Admin/User)
   - Session management

2. **Admin Dashboard**
   - System statistics and analytics
   - User management
   - Content management (Subjects, Chapters, Quizzes)
   - Question bank management

3. **User Dashboard**
   - Personal statistics
   - Available quizzes
   - Performance tracking
   - Profile management

4. **Quiz System**
   - Timed quizzes with countdown
   - Multiple choice questions
   - Instant results and scoring
   - Detailed question review

### Advanced Features
1. **Background Jobs (Celery)**
   - Daily reminder emails
   - Monthly performance reports
   - CSV data export

2. **Caching (Redis)**
   - API response caching
   - Session storage
   - Performance optimization

3. **Email System**
   - Welcome emails
   - Quiz reminders
   - Performance reports
   - CSV exports via email

## Project Structure

```
quiz-master-v2/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── tasks/           # Celery background tasks
│   │   └── utils/           # Utility functions
│   ├── migrations/          # Database migrations
│   ├── requirements.txt     # Python dependencies
│   ├── run.py              # Application entry point
│   └── .env                # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/           # Page components
│   │   ├── store/           # Vuex store modules
│   │   ├── services/        # API service layer
│   │   └── assets/          # Static assets
│   ├── public/             # Public files
│   └── package.json        # Node.js dependencies
└── README.md
```

## Database Schema

### Users Table
- id (Primary Key)
- email (Unique)
- password_hash
- full_name
- role (admin/user)
- qualification
- dob
- created_at
- last_login

### Subjects Table
- id (Primary Key)
- name
- description
- created_at

### Chapters Table
- id (Primary Key)
- name
- description
- subject_id (Foreign Key)
- created_at

### Quizzes Table
- id (Primary Key)
- title
- description
- chapter_id (Foreign Key)
- duration (minutes)
- is_active
- created_at

### Questions Table
- id (Primary Key)
- quiz_id (Foreign Key)
- question_statement
- option1, option2, option3, option4
- correct_answer
- created_at

### Scores Table
- id (Primary Key)
- user_id (Foreign Key)
- quiz_id (Foreign Key)
- total_scored
- total_questions
- time_taken
- timestamp_of_attempt
- answers (JSON)

## API Endpoints

### Authentication
- POST `/api/auth/login` - User login
- POST `/api/auth/register` - User registration
- GET `/api/auth/me` - Get current user
- POST `/api/auth/logout` - User logout

### Admin Routes
- GET `/api/admin/dashboard` - Admin dashboard data
- CRUD `/api/admin/subjects` - Subject management
- CRUD `/api/admin/chapters` - Chapter management
- CRUD `/api/admin/quizzes` - Quiz management
- CRUD `/api/admin/questions` - Question management
- GET `/api/admin/users` - User management

### User Routes
- GET `/api/user/dashboard` - User dashboard data
- GET `/api/user/quizzes` - Available quizzes
- GET `/api/user/scores` - User quiz scores
- PUT `/api/user/profile` - Update profile

### Quiz Routes
- GET `/api/quiz/{id}/start` - Start a quiz
- POST `/api/quiz/{id}/submit` - Submit quiz answers
- GET `/api/quiz/{id}/details` - Quiz details

## Installation & Setup

### Backend Setup
1. Navigate to backend directory
2. Create virtual environment: `python -m venv venv`
3. Activate virtual environment: `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Set up environment variables in `.env`
6. Initialize database: `flask db init && flask db migrate && flask db upgrade`
7. Run application: `python run.py`

### Frontend Setup
1. Navigate to frontend directory
2. Install dependencies: `npm install`
3. Start development server: `npm run serve`

### Redis Setup
1. Install Redis server
2. Start Redis service
3. Configure Redis URL in environment variables

### Celery Setup
1. Start Celery worker: `celery -A celery_worker.celery worker --loglevel=info`
2. Start Celery beat (for scheduled tasks): `celery -A celery_worker.celery beat --loglevel=info`

## Environment Variables

```env
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret

# Database
DATABASE_URL=sqlite:///quiz_master.db

# Redis
REDIS_URL=redis://localhost:6379/0

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Admin Credentials
ADMIN_EMAIL=admin@quizmaster.com
ADMIN_PASSWORD=admin123
```

## Usage

### Admin Functions
1. Login with admin credentials
2. Create subjects and chapters
3. Design quizzes with multiple choice questions
4. Monitor user performance and activity
5. Export user data and performance reports

### User Functions
1. Register and login to the platform
2. Browse available quizzes by subject/chapter
3. Take timed quizzes with instant feedback
4. Track performance and improvement over time
5. Receive email reminders and monthly reports

## Background Jobs

### Daily Reminders
- Automatically sends email reminders to inactive users
- Notifies users about new quizzes
- Scheduled to run daily

### Monthly Reports
- Generates comprehensive performance reports
- Includes statistics, scores, and recommendations
- Sent via email as HTML reports

### Data Export
- Users can export their quiz data as CSV
- Admins can export all user performance data
- Files sent via email attachment

## Performance Optimization

### Caching Strategy
- API responses cached with Redis
- Dashboard statistics cached for 5 minutes
- User quiz data cached for 10 minutes
- Subject/chapter data cached for 15 minutes

### Database Optimization
- Proper indexing on frequently queried fields
- Optimized queries with SQLAlchemy
- Connection pooling for better performance

## Security Features

### Authentication & Authorization
- JWT tokens with expiration
- Role-based access control
- Protected API endpoints
- CORS configuration

### Data Protection
- Password hashing with Werkzeug
- SQL injection prevention with ORM
- XSS protection in frontend
- Input validation and sanitization

## Future Enhancements

1. **Advanced Analytics**
   - Detailed performance analytics
   - Learning progress tracking
   - Recommendation system

2. **Mobile Application**
   - React Native or Flutter app
   - Offline quiz capability
   - Push notifications

3. **Advanced Question Types**
   - Multiple correct answers
   - Fill in the blanks
   - Image-based questions

4. **Collaborative Features**
   - Study groups
   - Peer challenges
   - Discussion forums

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes and test thoroughly
4. Submit pull request with detailed description

## License

This project is developed for educational purposes as part of the MAD II course curriculum.
