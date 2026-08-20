@echo off
title KrishiKalyan AI - One Click Launcher
color 0A

echo ================================================================
echo               KRISHIKALYAN AI (कृषिकल्याण AI)
echo      Production AI Decision Platform for Indian Farmers
echo ================================================================
echo.

set "ROOT_DIR=%~dp0"
cd /d "%ROOT_DIR%"

echo [1/4] Checking Backend Environment...
if not exist "backend\.venv\Scripts\uvicorn.exe" (
    if not exist "backend\.venv\Scripts\activate.bat" (
        echo [*] Creating Python virtual environment in backend\.venv ...
        python -m venv backend\.venv
    )
    echo [*] Installing backend Python dependencies...
    call backend\.venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
    echo [*] Training ML Models and Ingesting Datasets...
    python backend\scripts\download_and_process_data.py
    python backend\scripts\seed_sqlite_db.py
    python backend\scripts\train_crop_recommendation.py
    python backend\scripts\train_yield_prediction.py
    python backend\scripts\setup_disease_model.py
)

if not exist "backend\data\krishi_kalyan.db" (
    echo [*] Seeding SQLite database krishi_kalyan.db ...
    call backend\.venv\Scripts\activate.bat
    python backend\scripts\seed_sqlite_db.py
)

echo [2/4] Checking Frontend Dependencies...
if not exist "frontend\node_modules" (
    echo [*] Installing frontend npm packages...
    cd /d "%ROOT_DIR%frontend"
    call npm install
    cd /d "%ROOT_DIR%"
)

echo [3/4] Starting FastAPI Backend Server on http://127.0.0.1:8000 ...
start "KrishiKalyan AI - Backend Server (Port 8000)" cmd /k "cd /d %ROOT_DIR%backend && call .venv\Scripts\activate.bat && uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload"

echo [4/4] Starting React + Vite Frontend on http://127.0.0.1:5173 ...
start "KrishiKalyan AI - Frontend (Port 5173)" cmd /k "cd /d %ROOT_DIR%frontend && npm run dev -- --host 127.0.0.1 --port 5173"

echo.
echo ================================================================
echo      KrishiKalyan AI is now running successfully!
echo.
echo      - Web Application:  http://127.0.0.1:5173
echo      - Backend API Docs: http://127.0.0.1:8000/docs
echo.
echo      Opening browser in 3 seconds...
echo ================================================================

timeout /t 3 /nobreak >nul 2>&1
start http://127.0.0.1:5173

echo.
echo Press any key to exit this launcher window (servers will continue running in background).
pause >nul 2>&1
