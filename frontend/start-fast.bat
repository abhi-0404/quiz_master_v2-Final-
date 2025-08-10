@echo off
echo Starting Quiz Master Frontend (Fast Mode)...
echo.

REM Set environment variables for faster startup
set NODE_ENV=development
set GENERATE_SOURCEMAP=false
set FAST_REFRESH=true

REM Change to frontend directory
cd /d "d:\Quiz_Master_23f1003140\Quiz_Master\frontend"

REM Start development server with optimizations
npm run dev:fast
