@echo off
cls
echo ================================================
echo    AI CAMERA SYSTEM - COMPLETE PROJECT RUNNER
echo ================================================
echo.

cd /d "%~dp0"

echo 🚀 Starting Automated Stock Monitoring AI Camera System...
echo.

echo 📍 Current Directory: %CD%
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python and try again
    pause
    exit /b 1
)

echo ✅ Python is available
echo.

REM Check if OpenCV is available
python -c "import cv2; print('✅ OpenCV version:', cv2.__version__)" 2>nul
if errorlevel 1 (
    echo ⚠️  OpenCV might not be installed
    echo Installing OpenCV...
    pip install opencv-python
)

echo.
echo ================================================
echo           COMPONENT SELECTION MENU
echo ================================================
echo.
echo 1. Run Original OpenCV Script (Asm.py)
echo 2. Start Backend Server
echo 3. Start Enhanced CV System
echo 4. Open Web Interfaces
echo 5. Run Complete System (ALL)
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto run_original
if "%choice%"=="2" goto run_backend
if "%choice%"=="3" goto run_cv_system
if "%choice%"=="4" goto open_web
if "%choice%"=="5" goto run_complete
if "%choice%"=="6" goto exit
goto invalid_choice

:run_original
echo.
echo 🔍 Running Original OpenCV Script...
echo ================================================
python Asm.py
pause
goto menu

:run_backend
echo.
echo 🚀 Starting Backend Server...
echo ================================================
cd backend
echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop the server
python main.py
cd ..
pause
goto menu

:run_cv_system
echo.
echo 📹 Starting Enhanced CV System...
echo ================================================
cd cv_system
echo Starting enhanced monitoring system...
echo Press 'q' in the video window to quit
python enhanced_monitor.py
cd ..
pause
goto menu

:open_web
echo.
echo 🌐 Opening Web Interfaces...
echo ================================================
echo Opening dashboard...
start "" "dashboard.html"
timeout /t 2 /nobreak >nul
echo Opening API documentation...
start "" "http://localhost:8000/docs"
timeout /t 1 /nobreak >nul
echo Opening simple client...
start "" "simple-client.html"
echo ✅ Web interfaces opened in browser
pause
goto menu

:run_complete
echo.
echo 🎉 RUNNING COMPLETE SYSTEM
echo ================================================
echo.
echo Starting all components...
echo.

REM Start backend in background
echo 1. Starting Backend Server...
start "Backend Server" cmd /c "cd /d %CD%\backend && python main.py && pause"
timeout /t 3 /nobreak >nul

REM Start CV system in background
echo 2. Starting CV System...
start "CV System" cmd /c "cd /d %CD%\cv_system && python enhanced_monitor.py && pause"
timeout /t 2 /nobreak >nul

REM Run original script in background
echo 3. Starting Original Script...
start "Original OpenCV" cmd /c "cd /d %CD% && python Asm.py && pause"
timeout /t 2 /nobreak >nul

REM Open web interfaces
echo 4. Opening Web Interfaces...
start "" "dashboard.html"
timeout /t 1 /nobreak >nul
start "" "http://localhost:8000/docs"
timeout /t 1 /nobreak >nul
start "" "simple-client.html"

echo.
echo ================================================
echo 🎉 COMPLETE SYSTEM IS NOW RUNNING!
echo ================================================
echo.
echo ✅ Backend Server: http://localhost:8000
echo ✅ API Documentation: http://localhost:8000/docs  
echo ✅ Dashboard: dashboard.html
echo ✅ CV System: Running in separate window
echo ✅ Original Script: Monitoring shelves
echo.
echo 📱 Check the opened windows and browser tabs
echo 🎯 Your AI Camera System is fully operational!
echo.
echo Press any key to return to menu...
pause >nul
goto menu

:invalid_choice
echo.
echo ❌ Invalid choice. Please try again.
echo.
goto menu

:menu
cls
echo ================================================
echo    AI CAMERA SYSTEM - COMPLETE PROJECT RUNNER
echo ================================================
echo.
echo 📍 Current Directory: %CD%
echo.
echo ================================================
echo           COMPONENT SELECTION MENU
echo ================================================
echo.
echo 1. Run Original OpenCV Script (Asm.py)
echo 2. Start Backend Server
echo 3. Start Enhanced CV System
echo 4. Open Web Interfaces
echo 5. Run Complete System (ALL)
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto run_original
if "%choice%"=="2" goto run_backend
if "%choice%"=="3" goto run_cv_system
if "%choice%"=="4" goto open_web
if "%choice%"=="5" goto run_complete
if "%choice%"=="6" goto exit
goto invalid_choice

:exit
echo.
echo 👋 Thank you for using the AI Camera System!
echo Goodbye!
pause
exit /b 0
