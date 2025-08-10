@echo off
echo Starting Quiz Master V2 - Backend and Frontend
echo.

echo Checking if Python is installed...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Checking if Node.js is installed...
node --version >nul 2>&1
if errorlevel 1 (
    echo Error: Node.js is not installed or not in PATH
    echo Please install Node.js 16+ and try again
    pause
    exit /b 1
)

echo.
echo Setting up Backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing backend dependencies...
pip install -r requirements.txt

echo.
echo Starting Backend Server...
start cmd /k "title Backend Server && call venv\Scripts\activate && python run.py"

cd..

echo.
echo Setting up Frontend...
cd frontend

if not exist "node_modules" (
    echo Installing frontend dependencies...
    npm install
)

echo.
echo Starting Frontend Server...
start cmd /k "title Frontend Server && npm run serve"

cd..

echo.
echo Quiz Master V2 is starting up!
echo.
echo Backend will be available at: http://localhost:5000
echo Frontend will be available at: http://localhost:8080
echo.
echo Default Admin Login:
echo Email: admin@quizmaster.com
echo Password: admin123
echo.
echo Default User Login:
echo Email: john@student.com
echo Password: password123
echo.

pause
