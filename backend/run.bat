@echo off

REM Backend startup script for Windows

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Create .env if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo Please update .env with your configuration
)

REM Run the application
echo Starting Tattuu API...
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
