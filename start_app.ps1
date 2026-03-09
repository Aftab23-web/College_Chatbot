# AI Chatbot Startup Script (PowerShell)
Write-Host "====================================" -ForegroundColor Cyan
Write-Host "   AI Chatbot Startup" -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Checking Python..." -ForegroundColor Yellow
& ".\.venv\Scripts\python.exe" --version
Write-Host ""

# Start the application
Write-Host "Starting Flask application..." -ForegroundColor Green
Write-Host "The browser will open automatically..." -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Open browser after a short delay
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:5000"
} | Out-Null

& ".\.venv\Scripts\python.exe" "app.py"

Write-Host ""
Write-Host "Application stopped." -ForegroundColor Red
Read-Host "Press Enter to close"
