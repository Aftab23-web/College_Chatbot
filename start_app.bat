@echo off
echo ====================================
echo AI Chatbot Startup Script
echo ====================================
echo.
echo Testing Python...
.venv\Scripts\python.exe --version
echo.
echo Starting application...
.venv\Scripts\python.exe app.py
echo.
echo Application stopped.
pause
