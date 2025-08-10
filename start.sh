#!/bin/bash

echo "Starting Quiz Master V2 - Backend and Frontend"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    echo "Please install Node.js 16+ and try again"
    exit 1
fi

echo "Setting up Backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo
echo "Starting Backend Server..."
gnome-terminal --title="Backend Server" -- bash -c "source venv/bin/activate && python run.py; exec bash" 2>/dev/null || \
xterm -title "Backend Server" -e "source venv/bin/activate && python run.py; bash" 2>/dev/null || \
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && source venv/bin/activate && python run.py"' 2>/dev/null || \
echo "Please manually run: cd backend && source venv/bin/activate && python run.py"

cd ..

echo
echo "Setting up Frontend..."
cd frontend

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo
echo "Starting Frontend Server..."
gnome-terminal --title="Frontend Server" -- bash -c "npm run serve; exec bash" 2>/dev/null || \
xterm -title "Frontend Server" -e "npm run serve; bash" 2>/dev/null || \
osascript -e 'tell application "Terminal" to do script "cd \"'$(pwd)'\" && npm run serve"' 2>/dev/null || \
echo "Please manually run: cd frontend && npm run serve"

cd ..

echo
echo "Quiz Master V2 is starting up!"
echo
echo "Backend will be available at: http://localhost:5000"
echo "Frontend will be available at: http://localhost:8080"
echo
echo "Default Admin Login:"
echo "Email: admin@quizmaster.com"
echo "Password: admin123"
echo
echo "Default User Login:"
echo "Email: john@student.com"
echo "Password: password123"
echo
