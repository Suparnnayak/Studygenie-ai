# Quick script to run Flask backend locally (PowerShell)

Write-Host "🚀 Starting StudyGenie AI Backend locally..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"

# Install dependencies if needed
if (-not (Test-Path "venv\.installed")) {
    Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    New-Item -Path "venv\.installed" -ItemType File -Force | Out-Null
}

# Check for .env file
if (-not (Test-Path ".env")) {
    Write-Host "⚠️  .env file not found!" -ForegroundColor Yellow
    Write-Host "Creating .env from template..." -ForegroundColor Yellow
    @"
GROQ_API_KEY=your_groq_api_key_here
SECRET_KEY=dev-secret-key-change-me
CORS_ORIGINS=http://localhost:3000
GROQ_MODEL=llama-3.3-70b-versatile
"@ | Out-File -FilePath ".env" -Encoding utf8
    Write-Host "✅ Created .env file. Please update it with your API keys!" -ForegroundColor Green
}

# Run the server
Write-Host "`n🌟 Starting Flask server on http://localhost:5000" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop`n" -ForegroundColor White
python -m app.main

