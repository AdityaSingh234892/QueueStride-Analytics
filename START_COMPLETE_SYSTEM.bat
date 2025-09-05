@echo off
echo.
echo ============================================
echo   🚀 AUTOMATED STOCK MONITORING AI CAMERA
echo   🏪 STARTING COMPLETE SYSTEM...
echo ============================================
echo.

REM Set the project directory
set PROJECT_DIR=%~dp0
cd /d "%PROJECT_DIR%"

echo 📋 System Components Starting...
echo.

REM Start Backend Server
echo 🔧 Starting Backend Server...
start "Backend Server" /MIN cmd /k "cd /d %PROJECT_DIR%backend && echo Starting FastAPI Backend... && python main.py"

REM Wait for backend to start
echo    ⏱️ Waiting for backend to initialize...
timeout /t 5 /nobreak > nul

REM Start CV System
echo 🎥 Starting CV Monitoring System...
start "CV System" /MIN cmd /k "cd /d %PROJECT_DIR%cv_system && echo Starting OpenCV Monitoring... && python enhanced_monitor.py"

REM Wait a moment
timeout /t 2 /nobreak > nul

REM Start Original Script
echo 📹 Starting Original OpenCV Script...
start "Original Script" /MIN cmd /k "cd /d %PROJECT_DIR% && echo Starting Asm1.py... && python Asm1.py"

REM Wait a moment
timeout /t 2 /nobreak > nul

REM Open Web Interfaces
echo 🌐 Opening Web Interfaces...
start "" "%PROJECT_DIR%dashboard.html"
timeout /t 1 /nobreak > nul
start "" "http://localhost:8000/docs"

echo.
echo ============================================
echo   ✅ ALL COMPONENTS STARTED SUCCESSFULLY!
echo ============================================
echo.
echo 🎯 System URLs:
echo    • Dashboard: %PROJECT_DIR%dashboard.html
echo    • Backend API: http://localhost:8000
echo    • API Docs: http://localhost:8000/docs
echo    • Health Check: http://localhost:8000/health
echo.
echo 🎮 Running Components:
echo    • Backend Server (FastAPI) - Port 8000
echo    • CV Monitoring System (OpenCV)
echo    • Original Script (Asm1.py)
echo    • Web Dashboard (HTML)
echo.
echo 📋 To stop all components:
echo    • Close all terminal windows
echo    • Or run: taskkill /f /im python.exe
echo.
echo 🎉 YOUR AI CAMERA SYSTEM IS NOW LIVE!
echo.
pause
