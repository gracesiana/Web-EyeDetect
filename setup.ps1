# Setup Script untuk EyeDetect Project
# Run script ini untuk setup project otomatis

Write-Host "====================================" -ForegroundColor Cyan
Write-Host "  EyeDetect Project Setup Script  " -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "[1/8] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = py --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python first." -ForegroundColor Red
    Write-Host "Download from: https://www.python.org/downloads/" -ForegroundColor Red
    exit 1
}

# Navigate to backend
Write-Host ""
Write-Host "[2/8] Navigating to backend folder..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\backend"
Write-Host "✓ Current directory: $(Get-Location)" -ForegroundColor Green

# Remove old venv if exists
Write-Host ""
Write-Host "[3/8] Checking for old virtual environment..." -ForegroundColor Yellow
if (Test-Path ".venv") {
    Write-Host "Found old .venv, removing..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .venv
    Write-Host "✓ Old virtual environment removed" -ForegroundColor Green
} else {
    Write-Host "✓ No old virtual environment found" -ForegroundColor Green
}

# Create virtual environment
Write-Host ""
Write-Host "[4/8] Creating virtual environment..." -ForegroundColor Yellow
py -m venv .venv
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Virtual environment created successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to create virtual environment" -ForegroundColor Red
    exit 1
}

# Activate virtual environment
Write-Host ""
Write-Host "[5/8] Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Upgrade pip
Write-Host ""
Write-Host "[6/8] Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet
Write-Host "✓ pip upgraded" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[7/8] Installing dependencies (this may take a while)..." -ForegroundColor Yellow
Write-Host "Installing Django..." -ForegroundColor Cyan
pip install Django==6.0.7 --quiet

Write-Host "Installing image processing libraries..." -ForegroundColor Cyan
pip install Pillow==11.2.1 --quiet
pip install opencv-python-headless --quiet

Write-Host "Installing TensorFlow (this is a large file ~350MB)..." -ForegroundColor Cyan
pip install tensorflow --quiet

Write-Host "Installing other dependencies..." -ForegroundColor Cyan
pip install whitenoise==6.12.0 --quiet
pip install numpy --quiet
pip install cloudinary==1.41.0 --quiet
pip install django-cloudinary-storage==0.3.0 --quiet
pip install psycopg[binary]==3.2.1 --quiet
pip install gunicorn==23.0.0 --quiet

Write-Host "✓ All dependencies installed" -ForegroundColor Green

# Run migrations
Write-Host ""
Write-Host "[8/8] Setting up database..." -ForegroundColor Yellow
python manage.py migrate
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Database migrations completed" -ForegroundColor Green
} else {
    Write-Host "✗ Database migration failed" -ForegroundColor Red
    exit 1
}

# Create default admin
Write-Host ""
Write-Host "Creating default admin user..." -ForegroundColor Yellow
python manage.py ensure_default_admin
Write-Host "✓ Default admin user created" -ForegroundColor Green

# Done
Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "  Setup Complete! 🎉" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Default Admin Credentials:" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "To start the server, run:" -ForegroundColor Yellow
Write-Host "  python manage.py runserver" -ForegroundColor White
Write-Host ""
Write-Host "Then open your browser to:" -ForegroundColor Yellow
Write-Host "  http://localhost:8000/" -ForegroundColor White
Write-Host ""
