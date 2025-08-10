# Getting Started with Quiz Master V2

This guide will help you set up and run the Quiz Master V2 application on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (for backend)
- **Node.js 16+** (for frontend)
- **Redis Server** (for caching and background jobs)
- **Git** (for version control)

## Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd perplexity
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
copy .env.example .env  # Windows
cp .env.example .env    # macOS/Linux

# Initialize database
python run.py
```

The backend will start on `http://localhost:5000`

### 3. Frontend Setup

Open a new terminal window:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run serve
```

The frontend will start on `http://localhost:8080`

### 4. Redis Setup

#### Windows
1. Download Redis from https://github.com/microsoftarchive/redis/releases
2. Extract and run `redis-server.exe`

#### macOS
```bash
brew install redis
brew services start redis
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

### 5. Celery Setup (Optional - for background jobs)

Open a new terminal window:

```bash
# Navigate to backend directory
cd backend

# Activate virtual environment
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start Celery worker
celery -A app.tasks.celery_tasks worker --loglevel=info

# In another terminal, start Celery beat (for scheduled tasks)
celery -A app.tasks.celery_tasks beat --loglevel=info
```

## Default Login Credentials

### Admin Account
- **Email:** admin@quizmaster.com
- **Password:** admin123

### Test User Account
- **Email:** john@student.com
- **Password:** password123

## Project Structure Overview

```
perplexity/
├── backend/                 # Flask API backend
│   ├── app/
│   │   ├── models/         # Database models
│   │   ├── routes/         # API routes
│   │   ├── tasks/          # Background tasks
│   │   └── utils/          # Utility functions
│   ├── requirements.txt    # Python dependencies
│   ├── run.py             # Application entry point
│   └── .env               # Environment variables
├── frontend/               # Vue.js frontend
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── views/         # Page components
│   │   ├── store/         # Vuex state management
│   │   └── services/      # API service layer
│   ├── package.json       # Node.js dependencies
│   └── public/            # Static files
└── README.md              # Project documentation
```

## Available Scripts

### Backend Scripts
```bash
# Run development server
python run.py

# Run with debug mode
FLASK_ENV=development python run.py

# Database operations
flask db init      # Initialize migrations
flask db migrate   # Create migration
flask db upgrade   # Apply migrations
```

### Frontend Scripts
```bash
# Development server
npm run serve

# Production build
npm run build

# Lint code
npm run lint
```

## Environment Configuration

The `.env` file in the backend directory contains important configuration:

```env
# Basic Configuration
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here

# Database
DATABASE_URL=sqlite:///quiz_master.db

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/2

# Email Configuration (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Admin Credentials
ADMIN_EMAIL=admin@quizmaster.com
ADMIN_PASSWORD=admin123

# Frontend URL
FRONTEND_URL=http://localhost:8080
```

## Testing the Application

1. **Access the Application:**
   - Open your browser and go to `http://localhost:8080`
   - You'll see the Quiz Master V2 login page

2. **Login as Admin:**
   - Use admin credentials to access the admin panel
   - Create subjects, chapters, and quizzes
   - Add questions to quizzes

3. **Login as User:**
   - Register a new user or use the test user credentials
   - Browse available quizzes
   - Take quizzes and view results

4. **Test API Endpoints:**
   - Backend API is available at `http://localhost:5000/api`
   - Use tools like Postman to test endpoints
   - API documentation available in the main README

## Common Issues and Solutions

### Issue: Port Already in Use
```bash
# Find process using port
netstat -ano | findstr :5000    # Windows
lsof -ti:5000                   # macOS/Linux

# Kill process and restart
```

### Issue: Redis Connection Error
- Ensure Redis server is running
- Check Redis URL in `.env` file
- Verify Redis is accessible on `localhost:6379`

### Issue: Database Errors
```bash
# Reset database
rm instance/quiz_master.db  # Delete existing database
python run.py               # Restart application
```

### Issue: Module Not Found
```bash
# Ensure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: CORS Errors
- Ensure backend is running on `http://localhost:5000`
- Check CORS configuration in backend
- Verify `FRONTEND_URL` in `.env` file

## Development Tips

1. **Hot Reload:**
   - Backend: Flask development server auto-reloads on file changes
   - Frontend: Vue CLI provides hot module replacement

2. **Debugging:**
   - Use browser developer tools for frontend debugging
   - Add `import pdb; pdb.set_trace()` for Python debugging

3. **Database Inspection:**
   - Use SQLite browser tools to inspect the database
   - Access database at `backend/instance/quiz_master.db`

4. **API Testing:**
   - Use Postman or curl to test API endpoints
   - JWT token required for protected routes

## Next Steps

Once you have the application running:

1. Explore the admin panel to understand the content management system
2. Create sample subjects, chapters, and quizzes
3. Test the user experience by taking quizzes
4. Review the code structure to understand the architecture
5. Customize the application according to your requirements

## Getting Help

If you encounter issues:

1. Check the console for error messages
2. Review the logs in both frontend and backend terminals
3. Ensure all prerequisites are properly installed
4. Verify environment configuration
5. Check network connectivity for Redis and database

For additional support, refer to the main README.md file for detailed documentation and troubleshooting guides.
