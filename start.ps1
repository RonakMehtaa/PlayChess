# Chess Web App - Quick Start Script for Windows
# This script helps set up and run both backend and frontend

Write-Host "🎯 Chess Web App - Quick Start" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if Node is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "✓ Found Node: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ Node.js not found! Please install Node.js 14+" -ForegroundColor Red
    exit 1
}

# Check if Stockfish is available
Write-Host "Checking Stockfish installation..." -ForegroundColor Yellow
try {
    $stockfishTest = stockfish.exe 2>&1 | Select-Object -First 1
    Write-Host "✓ Stockfish found in PATH" -ForegroundColor Green
} catch {
    Write-Host "⚠ Stockfish not found in PATH" -ForegroundColor Yellow
    Write-Host "  Please install Stockfish and set STOCKFISH_PATH environment variable" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host "1. Install dependencies (first time setup)" -ForegroundColor White
Write-Host "2. Run backend only" -ForegroundColor White
Write-Host "3. Run frontend only" -ForegroundColor White
Write-Host "4. Run both (recommended)" -ForegroundColor White
Write-Host "5. Exit" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-5)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "📦 Installing dependencies..." -ForegroundColor Cyan
        
        # Backend dependencies
        Write-Host ""
        Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
        Set-Location -Path ".\backend"
        
        # Create venv if it doesn't exist
        if (-not (Test-Path "venv")) {
            Write-Host "Creating virtual environment..." -ForegroundColor Yellow
            python -m venv venv
        }
        
        # Activate venv and install
        .\venv\Scripts\Activate.ps1
        pip install -r requirements.txt
        deactivate
        
        Write-Host "✓ Backend dependencies installed" -ForegroundColor Green
        
        # Frontend dependencies
        Write-Host ""
        Write-Host "Installing frontend dependencies..." -ForegroundColor Yellow
        Set-Location -Path "..\frontend"
        npm install
        
        Write-Host "✓ Frontend dependencies installed" -ForegroundColor Green
        Set-Location -Path ".."
        
        Write-Host ""
        Write-Host "✓ All dependencies installed successfully!" -ForegroundColor Green
        Write-Host "Run this script again and choose option 4 to start the app" -ForegroundColor Cyan
    }
    
    "2" {
        Write-Host ""
        Write-Host "🚀 Starting backend..." -ForegroundColor Cyan
        Set-Location -Path ".\backend"
        .\venv\Scripts\Activate.ps1
        Write-Host "Backend running at http://localhost:8000" -ForegroundColor Green
        python main.py
    }
    
    "3" {
        Write-Host ""
        Write-Host "🚀 Starting frontend..." -ForegroundColor Cyan
        Set-Location -Path ".\frontend"
        Write-Host "Frontend will open at http://localhost:3000" -ForegroundColor Green
        npm start
    }
    
    "4" {
        Write-Host ""
        Write-Host "🚀 Starting backend and frontend..." -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Backend will run at: http://localhost:8000" -ForegroundColor Green
        Write-Host "Frontend will open at: http://localhost:3000" -ForegroundColor Green
        Write-Host ""
        Write-Host "Press Ctrl+C in each window to stop the servers" -ForegroundColor Yellow
        Write-Host ""
        
        # Start backend in new window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; python main.py"
        
        # Wait a moment for backend to start
        Start-Sleep -Seconds 3
        
        # Start frontend in new window
        Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm start"
        
        Write-Host "✓ Both servers started in separate windows!" -ForegroundColor Green
    }
    
    "5" {
        Write-Host "Goodbye! 👋" -ForegroundColor Cyan
        exit 0
    }
    
    default {
        Write-Host "Invalid choice. Please run the script again." -ForegroundColor Red
    }
}
