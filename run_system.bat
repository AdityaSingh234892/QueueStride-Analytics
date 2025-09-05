@echo off
echo Starting Automated Stock Monitoring AI Camera System...
echo.

REM Create new terminal windows for each component
echo Starting Backend Server...
start "Backend Server" cmd /k "cd /d %~dp0backend && python main.py"

timeout /t 3 /nobreak > nul

echo Starting CV System...
start "CV System" cmd /k "cd /d %~dp0cv_system && python enhanced_monitor.py"

timeout /t 2 /nobreak > nul

echo.
echo All components started!
echo.
echo - Backend Server: http://localhost:8000
echo - Simple Client: Open simple-client.html in browser
echo - CV System: Running in separate window
echo.
echo Press any key to continue...
pause > nul
