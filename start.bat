@echo off
REM Chess Web App Quick Start
REM This batch file provides easy access to common commands

:menu
cls
echo ========================================
echo   Chess Web App - Quick Start
echo ========================================
echo.
echo 1. Install dependencies
echo 2. Start backend only
echo 3. Start frontend only  
echo 4. Start both (recommended)
echo 5. Run API tests
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto install
if "%choice%"=="2" goto backend
if "%choice%"=="3" goto frontend
if "%choice%"=="4" goto both
if "%choice%"=="5" goto test
if "%choice%"=="6" goto end

echo Invalid choice. Please try again.
pause
goto menu

:install
echo.
echo Installing dependencies...
echo.
cd backend
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)
call venv\Scripts\activate.bat
pip install -r requirements.txt
call deactivate
cd..

cd frontend
echo.
echo Installing frontend dependencies...
call npm install
cd..

echo.
echo Dependencies installed successfully!
pause
goto menu

:backend
echo.
echo Starting backend server...
cd backend
call venv\Scripts\activate.bat
python main.py
pause
goto menu

:frontend
echo.
echo Starting frontend server...
cd frontend
npm start
pause
goto menu

:both
echo.
echo Starting both servers...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
start "Chess Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python main.py"
timeout /t 3 /nobreak >nul
start "Chess Frontend" cmd /k "cd frontend && npm start"
echo.
echo Both servers started in separate windows!
pause
goto menu

:test
echo.
echo Running API tests...
cd backend
call venv\Scripts\activate.bat
python test_api.py
call deactivate
cd..
pause
goto menu

:end
echo.
echo Goodbye!
exit
