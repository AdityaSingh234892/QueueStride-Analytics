@echo off
REM Automated Stock Monitoring System Setup Script for Windows
REM This script sets up the complete system for development

echo 🚀 Setting up Automated Stock Monitoring System...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 16+ and try again.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed. Please install npm and try again.
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed!

REM Setup Backend
echo 🔧 Setting up Backend...
cd backend

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating .env file...
    (
        echo DATABASE_URL=sqlite:///./stock_monitor.db
        echo SECRET_KEY=your-secret-key-change-this-in-production
        echo SMTP_SERVER=smtp.gmail.com
        echo SMTP_PORT=587
        echo SMTP_USERNAME=your-email@gmail.com
        echo SMTP_PASSWORD=your-app-password
    ) > .env
    echo ⚠️  Please update the .env file with your actual configuration!
)

cd ..

REM Setup Frontend
echo 🎨 Setting up Frontend...
cd frontend

REM Install dependencies
npm install

cd ..

REM Setup CV System
echo 📹 Setting up Computer Vision System...
cd cv_system

REM Install dependencies
pip install -r requirements.txt

cd ..

echo ✅ Setup completed successfully!
echo.
echo 🚀 To start the system:
echo 1. Start the backend:
echo    cd backend && venv\Scripts\activate && uvicorn main:app --reload
echo.
echo 2. Start the frontend (in a new terminal):
echo    cd frontend && npm start
echo.
echo 3. Start the CV system (in a new terminal):
echo    cd cv_system && python enhanced_monitor.py
echo.
echo 🌐 The application will be available at:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Documentation: http://localhost:8000/docs
echo.
echo 📚 Check the README.md for more detailed instructions!
pause
