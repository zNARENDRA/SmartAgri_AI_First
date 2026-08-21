@echo off
title SmartAgri AI - Stop Servers
color 0C

echo ================================================================
echo          Stopping SmartAgri AI Backend & Frontend
echo ================================================================
echo.

echo [*] Terminating Node/Vite processes (Port 5173)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5173') do (
    taskkill /F /PID %%a 2>nul
)

echo [*] Terminating Uvicorn/Python backend processes (Port 8000)...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    taskkill /F /PID %%a 2>nul
)

echo.
echo [✓] All servers stopped successfully!
echo.
pause
