# start-demo.ps1 - one-shot launcher for the defense demo (backend + frontend).
#
# Usage:  powershell -ExecutionPolicy Bypass -File start-demo.ps1
#         (or double-click start-demo.bat)
#
# Opens two extra windows: [demo backend] uvicorn and [demo frontend] CRA dev
# server. Waits for both, then opens the browser.
# Drive-letter agnostic: paths are derived from this script's own location, so it
# works wherever the traveling drive mounts (D:, E:, ...). See RUNBOOK.md.
#
# The backend runs one of two ways, picked by -Backend:
#   native  uvicorn from the Windows venv at demo\.venv (no WSL needed)
#   wsl     uvicorn in WSL2 Ubuntu, conda env dr-classifier (the original path)
#   auto    (default) native if demo\.venv exists, else wsl

param(
    [ValidateSet('orchestrate', 'backend', 'frontend')]
    [string]$Role = 'orchestrate',

    [ValidateSet('auto', 'native', 'wsl')]
    [string]$Backend = 'auto'
)

$ErrorActionPreference = 'Stop'
$demoDir = $PSScriptRoot
$webDir  = Join-Path $demoDir 'web'
$venvPy  = Join-Path $demoDir '.venv\Scripts\python.exe'

# demo dir as seen from WSL:  D:\dissertation-project\demo -> /mnt/d/dissertation-project/demo
$driveLetter = $demoDir.Substring(0, 1).ToLower()
$wslDemoDir  = "/mnt/$driveLetter" + ($demoDir.Substring(2) -replace '\\', '/')

function Resolve-BackendMode([string]$Requested) {
    if ($Requested -ne 'auto') { return $Requested }
    if (Test-Path $venvPy) { return 'native' }
    return 'wsl'
}

function Test-PortListening([int]$Port) {
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return ($null -ne $conn)
}

function Wait-ForUrl([string]$Url, [string]$What, [int]$TimeoutSec) {
    Write-Host "Waiting for $What ($Url, up to ${TimeoutSec}s)..." -NoNewline
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while ((Get-Date) -lt $deadline) {
        try {
            $null = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 3
            Write-Host " up." -ForegroundColor Green
            return $true
        } catch {
            Start-Sleep -Seconds 3
            Write-Host '.' -NoNewline
        }
    }
    Write-Host " TIMEOUT." -ForegroundColor Red
    return $false
}

# ---------------------------------------------------------------- backend role
if ($Role -eq 'backend') {
    $mode = Resolve-BackendMode $Backend
    if ($mode -eq 'native') {
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (Windows venv)'
        Set-Location $demoDir
        $env:PYTHONIOENCODING = 'utf-8'
        & $venvPy -m uvicorn server.app.main:app --host 127.0.0.1 --port 8000
    } else {
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (WSL Ubuntu)'
        $bashCmd = "cd '$wslDemoDir' && ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier uvicorn server.app.main:app --host 127.0.0.1 --port 8000"
        & wsl.exe -d Ubuntu bash -lc $bashCmd
    }
    exit $LASTEXITCODE
}

# --------------------------------------------------------------- frontend role
if ($Role -eq 'frontend') {
    $host.UI.RawUI.WindowTitle = 'demo frontend - CRA :3000'
    Set-Location $webDir
    $env:BROWSER = 'none'   # orchestrator opens the browser itself
    & npm start
    exit $LASTEXITCODE
}

# ---------------------------------------------------------------- orchestrator
Write-Host '=== DR demo launcher ===' -ForegroundColor Cyan
$backendMode = Resolve-BackendMode $Backend
Write-Host "demo dir : $demoDir"
Write-Host "backend  : $backendMode"
if ($backendMode -eq 'wsl') { Write-Host "WSL path : $wslDemoDir" }

# Sanity checks
if ($backendMode -eq 'native') {
    if (-not (Test-Path $venvPy)) {
        Write-Warning "No venv at $venvPy - create it with: python -m venv .venv; .venv\Scripts\python -m pip install -r server\requirements.txt pandas scikit-learn"
    }
} else {
    & wsl.exe --status *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Warning 'WSL is not available on this machine. Create demo\.venv and rerun (it will pick native automatically), or pass -Backend native.'
    }
}
$checkpoint = Join-Path $demoDir 'server\checkpoints\config_d_fold0.pt'
$normStats  = Join-Path $demoDir 'server\checkpoints\eyepacs_norm_stats.json'
if (-not (Test-Path $checkpoint)) {
    Write-Warning "Checkpoint missing: $checkpoint - backend will boot with random weights."
}
if (-not (Test-Path $normStats)) {
    Write-Warning "Norm stats missing: $normStats - backend falls back to ImageNet normalize (do NOT demo Config D that way)."
}
if (-not (Test-Path (Join-Path $webDir 'node_modules'))) {
    Write-Warning "demo/web/node_modules missing - run 'npm install' in demo/web first."
}

$spawnArgs = @('-NoExit', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-Backend', $backendMode, '-Role')

# Backend (:8000)
if (Test-PortListening 8000) {
    Write-Host 'Port 8000 already listening - assuming backend is running, skipping launch.' -ForegroundColor Yellow
} else {
    if ($backendMode -eq 'native') {
        Write-Host 'Starting backend window (Windows venv)...'
    } else {
        Write-Host 'Starting backend window (WSL Ubuntu / conda dr-classifier)...'
    }
    Start-Process powershell -ArgumentList ($spawnArgs + 'backend')
}
$backendOk = Wait-ForUrl 'http://127.0.0.1:8000/api/health' 'backend /api/health' 240
if ($backendOk) {
    try {
        $health = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 5
        Write-Host ("Backend: checkpoint_loaded={0}, device={1}, checkpoint={2}" -f `
            $health.checkpoint_loaded, $health.device, $health.checkpoint)
        if (-not $health.checkpoint_loaded) {
            Write-Warning 'checkpoint_loaded=false - predictions will be random-init!'
        }
    } catch {}
} else {
    Write-Warning 'Backend did not come up - check the [demo backend] window. Frontend will show "simulator (backend offline)".'
}

# Frontend (:3000)
if (Test-PortListening 3000) {
    Write-Host 'Port 3000 already listening - assuming frontend is running, skipping launch.' -ForegroundColor Yellow
} else {
    Write-Host 'Starting frontend window (npm start in demo/web)...'
    Start-Process powershell -ArgumentList ($spawnArgs + 'frontend')
}
$frontendOk = Wait-ForUrl 'http://localhost:3000' 'frontend' 300

if ($frontendOk) {
    Start-Process 'http://localhost:3000'
    Write-Host 'Demo is up: http://localhost:3000 (API: http://localhost:8000/api/health)' -ForegroundColor Green
    Write-Host 'To stop: close the [demo backend] and [demo frontend] windows, or free the ports:'
    if ($backendMode -eq 'native') {
        Write-Host '  Get-NetTCPConnection -LocalPort 8000,3000 -State Listen | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force }'
    } else {
        Write-Host "  wsl -d Ubuntu pkill -f 'uvicorn server.app.main'   and kill the PID on :3000."
    }
} else {
    Write-Warning 'Frontend did not come up - check the [demo frontend] window.'
}
