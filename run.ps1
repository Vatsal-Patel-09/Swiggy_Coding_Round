# Run the Interactive Story Generator

Write-Host "🎭 Starting Interactive Story Generator..." -ForegroundColor Green
Write-Host ""

# Check if virtual environment is activated
if ($env:VIRTUAL_ENV) {
    Write-Host "✓ Virtual environment is activated" -ForegroundColor Green
} else {
    Write-Host "⚠ Virtual environment not activated" -ForegroundColor Yellow
    Write-Host "  Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
}

Write-Host ""
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan

# Check if streamlit is installed
$streamlitInstalled = pip list | Select-String "streamlit"

if (-not $streamlitInstalled) {
    Write-Host "⚠ Dependencies not found. Installing..." -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host "✓ Dependencies are installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Launching application..." -ForegroundColor Cyan
Write-Host ""

# Run the Streamlit app
streamlit run app.py
