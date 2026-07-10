# Script untuk menjalankan EyeDetect Development Server
# Double-click script ini untuk run server

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  Starting EyeDetect Server...     " -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to backend
Set-Location -Path "$PSScriptRoot\backend"

# Check if venv exists
if (-not (Test-Path ".venv")) {
    Write-Host "✗ Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first to setup the project." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Activate venv
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Check if Django is installed
Write-Host "Checking Django installation..." -ForegroundColor Yellow
$djangoCheck = python -c "import django; print(django.get_version())" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "✗ Django not found!" -ForegroundColor Red
    Write-Host "Please run setup.ps1 first to install dependencies." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host "✓ Django version: $djangoCheck" -ForegroundColor Green

# Run migrations (in case there are new ones)
Write-Host ""
Write-Host "Checking for database migrations..." -ForegroundColor Yellow
python manage.py migrate --noinput

# Start server
Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "  Server Starting...               " -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the application at:" -ForegroundColor Cyan
Write-Host "  http://localhost:8000/" -ForegroundColor White
Write-Host ""
Write-Host "Admin Login:" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Yellow
Write-Host ""

# Run server
python manage.py runserver
