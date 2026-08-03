# start-tunnel.ps1 - one-shot launcher for the PUBLIC demo (real model over Cloudflare).
#
# Usage:  powershell -ExecutionPolicy Bypass -File start-tunnel.ps1
#         (or double-click start-tunnel.bat)
#
# Opens four windows: two cloudflared quick tunnels (frontend :3000, backend
# :8000), the uvicorn backend and the CRA frontend, wired to each other:
#
#   remote browser --HTTPS--> [tunnel F] --> :3000 CRA  (REACT_APP_API_URL = tunnel B)
#                  --HTTPS--> [tunnel B] --> :8000 API  (CORS_ORIGINS      = tunnel F)
#
# Why two tunnels: an HTTPS page cannot call http://localhost:8000 from a remote
# machine (mixed-content block), so the dashboard would silently fall back to the
# in-browser simulator. The backend needs its own HTTPS origin.
#
# Quick-tunnel URLs are random per launch, so the tunnels are created FIRST and
# the servers are started already pointing at them. Any backend/frontend already
# running is therefore restarted - their URLs are baked in at process start.
#
# Local-only launch (no tunnels): start-demo.ps1. See RUNBOOK.md.
#
# Params:
#   -Backend auto|native|wsl  same meaning as in start-demo.ps1 (default auto)
#   -Password <str>           sets DEMO_PASSWORD on the backend (access gate).
#                             STRONGLY recommended: a quick tunnel is public.
#   -Http2                    force --protocol http2 (use when QUIC/UDP 7844 is
#                             blocked by the venue network and tunnels stall)
#   -Stop                     kill tunnels + servers and exit

param(
    [ValidateSet('orchestrate', 'backend', 'frontend')]
    [string]$Role = 'orchestrate',

    [ValidateSet('auto', 'native', 'wsl')]
    [string]$Backend = 'auto',

    [string]$ApiUrl = '',
    [string]$CorsOrigins = '',
    [string]$Password = '',

    [switch]$Http2,
    [switch]$Stop
)

$ErrorActionPreference = 'Stop'
$demoDir = $PSScriptRoot
$webDir  = Join-Path $demoDir 'web'
$venvPy  = Join-Path $demoDir '.venv\Scripts\python.exe'

# demo dir as seen from WSL:  D:\dissertation-project\demo -> /mnt/d/dissertation-project/demo
$driveLetter = $demoDir.Substring(0, 1).ToLower()
$wslDemoDir  = "/mnt/$driveLetter" + ($demoDir.Substring(2) -replace '\\', '/')

# Access password: -Password wins, else demo/.demo-password (gitignored). Having a
# default on disk means a launch never has to stop and ask for one.
$passwordFile = Join-Path $demoDir '.demo-password'
if (-not $Password -and (Test-Path $passwordFile)) {
    $Password = (Get-Content $passwordFile -Raw).Trim()
}

function Resolve-BackendMode([string]$Requested) {
    if ($Requested -ne 'auto') { return $Requested }
    if (Test-Path $venvPy) { return 'native' }
    return 'wsl'
}

# A shell started before node/cloudflared were installed carries a stale PATH, and
# passes it to every window it spawns. Rebuild PATH from the registry so tools
# installed since this session began (npm, cloudflared) are found.
function Sync-PathFromRegistry {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user    = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = (@($machine, $user) | Where-Object { $_ } ) -join ';'
}
Sync-PathFromRegistry

function Find-Npm {
    $cmd = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($c in @("${env:ProgramFiles}\nodejs\npm.cmd", "${env:ProgramFiles(x86)}\nodejs\npm.cmd")) {
        if (Test-Path $c) { return $c }
    }
    return $null
}

function Test-PortListening([int]$Port) {
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    return ($null -ne $conn)
}

function Stop-Port([int]$Port) {
    $conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    foreach ($c in $conns) {
        try { Stop-Process -Id $c.OwningProcess -Force -ErrorAction Stop } catch {}
    }
}

function Wait-ForUrl([string]$Url, [string]$What, [int]$TimeoutSec) {
    Write-Host "Waiting for $What ($Url, up to ${TimeoutSec}s)..." -NoNewline
    $deadline = (Get-Date).AddSeconds($TimeoutSec)
    while ((Get-Date) -lt $deadline) {
        try {
            $null = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
            Write-Host ' up.' -ForegroundColor Green
            return $true
        } catch {
            Start-Sleep -Seconds 3
            Write-Host '.' -NoNewline
        }
    }
    Write-Host ' TIMEOUT.' -ForegroundColor Red
    return $false
}

# ---------------------------------------------------------------- backend role
if ($Role -eq 'backend') {
    $mode = Resolve-BackendMode $Backend
    if ($mode -eq 'native') {
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (Windows venv) [TUNNELLED]'
        Set-Location $demoDir
        $env:PYTHONIOENCODING = 'utf-8'
        $env:CORS_ORIGINS = $CorsOrigins
        if ($Password) { $env:DEMO_PASSWORD = $Password }
        & $venvPy -m uvicorn server.app.main:app --host 127.0.0.1 --port 8000
    } else {
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (WSL Ubuntu) [TUNNELLED]'
        $exports = "export CORS_ORIGINS='$CorsOrigins'"
        if ($Password) { $exports += " && export DEMO_PASSWORD='$Password'" }
        $bashCmd = "cd '$wslDemoDir' && $exports && ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier uvicorn server.app.main:app --host 127.0.0.1 --port 8000"
        & wsl.exe -d Ubuntu bash -lc $bashCmd
    }
    exit $LASTEXITCODE
}

# --------------------------------------------------------------- frontend role
if ($Role -eq 'frontend') {
    $host.UI.RawUI.WindowTitle = 'demo frontend - CRA :3000 [TUNNELLED]'
    Set-Location $webDir
    $env:BROWSER = 'none'                        # orchestrator opens the browser itself
    $env:REACT_APP_API_URL = $ApiUrl             # overrides .env.development
    $env:WDS_SOCKET_PORT = '0'                   # HMR socket follows the page port (443)
    $env:DANGEROUSLY_DISABLE_HOST_CHECK = 'true' # accept the *.trycloudflare.com Host header
    $npm = Find-Npm
    if (-not $npm) {
        Write-Error 'npm not found. Install Node: winget install --id OpenJS.NodeJS.LTS -e'
        Read-Host 'Press Enter to close'
        exit 1
    }
    & $npm start
    exit $LASTEXITCODE
}

# ---------------------------------------------------------------- orchestrator

function Find-Cloudflared {
    $cmd = Get-Command cloudflared.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    $candidates = @(
        "${env:ProgramFiles(x86)}\cloudflared\cloudflared.exe",
        "${env:ProgramFiles}\cloudflared\cloudflared.exe",
        "C:\Program Files (x86)\cloudflared\cloudflared.exe",
        "$env:LOCALAPPDATA\Microsoft\WinGet\Links\cloudflared.exe"
    )
    foreach ($c in $candidates) { if (Test-Path $c) { return $c } }
    return $null
}

function Start-QuickTunnel([string]$Exe, [int]$Port, [string]$Label, [string]$LogFile) {
    Remove-Item $LogFile -ErrorAction SilentlyContinue
    $cfArgs = @('tunnel', '--no-autoupdate')
    if ($Http2) { $cfArgs += @('--protocol', 'http2') }
    $cfArgs += @('--url', "http://localhost:$Port", '--logfile', $LogFile)
    Write-Host "Starting Cloudflare quick tunnel for $Label (:$Port)..."
    Start-Process -FilePath $Exe -ArgumentList $cfArgs -WindowStyle Minimized | Out-Null

    $deadline = (Get-Date).AddSeconds(60)
    while ((Get-Date) -lt $deadline) {
        if (Test-Path $LogFile) {
            $m = Select-String -Path $LogFile -Pattern 'https://[a-z0-9-]+\.trycloudflare\.com' -ErrorAction SilentlyContinue
            if ($m) {
                $url = ($m | Select-Object -First 1).Matches[0].Value
                Write-Host "  $Label tunnel: $url" -ForegroundColor Green
                return $url
            }
        }
        Start-Sleep -Milliseconds 700
        Write-Host '.' -NoNewline
    }
    Write-Host ''
    throw "Timed out waiting for the $Label tunnel URL. Log: $LogFile"
}

Write-Host '=== DR demo launcher (PUBLIC / Cloudflare quick tunnels) ===' -ForegroundColor Cyan

$logF = Join-Path $env:TEMP 'cf_demo_frontend.log'
$logB = Join-Path $env:TEMP 'cf_demo_backend.log'

# -Stop: tear everything down and exit.
if ($Stop) {
    Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force
    Stop-Port 3000
    Stop-Port 8000
    & wsl.exe --status *> $null
    if ($LASTEXITCODE -eq 0) {
        & wsl.exe -d Ubuntu bash -lc "pkill -f 'uvicorn server.app.main' >/dev/null 2>&1; exit 0"
    }
    Write-Host 'Stopped: cloudflared, :3000, :8000.' -ForegroundColor Yellow
    exit 0
}

$cloudflared = Find-Cloudflared
if (-not $cloudflared) {
    Write-Error @'
cloudflared not found. Install it, then rerun:
    winget install --id Cloudflare.cloudflared -e
(or download cloudflared-windows-amd64.exe from
 https://github.com/cloudflare/cloudflared/releases and put it on PATH)
'@
    exit 1
}

$backendMode = Resolve-BackendMode $Backend
Write-Host "demo dir    : $demoDir"
Write-Host "backend     : $backendMode"
Write-Host "cloudflared : $cloudflared"
if ($backendMode -eq 'wsl') { Write-Host "WSL path    : $wslDemoDir" }

if (-not $Password) {
    Write-Warning 'No -Password given: the public URL will be OPEN to anyone who has it. Pass -Password "<secret>" to enable the DEMO_PASSWORD gate.'
}

# Sanity checks (same set as start-demo.ps1).
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
if (-not (Find-Npm)) {
    Write-Warning 'npm not found - the frontend will not start. Install Node: winget install --id OpenJS.NodeJS.LTS -e'
}

# Servers must be (re)started with the tunnel URLs in their environment, so any
# instance already listening is torn down first.
if ((Test-PortListening 3000) -or (Test-PortListening 8000)) {
    Write-Host 'Stopping the servers already on :3000/:8000 (they need the tunnel URLs baked in)...' -ForegroundColor Yellow
    Stop-Port 3000
    Stop-Port 8000
    if ($backendMode -eq 'wsl') {
        & wsl.exe -d Ubuntu bash -lc "pkill -f 'uvicorn server.app.main' >/dev/null 2>&1; exit 0"
    }
    Start-Sleep -Seconds 2
}
Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force

# 1-2. Tunnels first - their URLs are the servers' configuration.
$urlF = Start-QuickTunnel $cloudflared 3000 'FRONTEND' $logF
$urlB = Start-QuickTunnel $cloudflared 8000 'BACKEND'  $logB

$corsOrigins = "http://localhost:3000,$urlF"
$spawn = @('-NoExit', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-Backend', $backendMode)

# 3. Backend, allowing the frontend tunnel origin.
Write-Host 'Starting backend window...'
$backendArgs = $spawn + @('-Role', 'backend', '-CorsOrigins', "`"$corsOrigins`"")
if ($Password) { $backendArgs += @('-Password', "`"$Password`"") }
Start-Process powershell -ArgumentList $backendArgs

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
    Write-Warning 'Backend did not come up - check the [demo backend] window. Remote users would see "simulator (backend offline)".'
}

# 4. Frontend, calling the backend tunnel.
Write-Host 'Starting frontend window...'
Start-Process powershell -ArgumentList ($spawn + @('-Role', 'frontend', '-ApiUrl', "`"$urlB`""))
$frontendOk = Wait-ForUrl 'http://localhost:3000' 'frontend' 300

# 5. Verify the public path end to end: tunnels reachable + CORS preflight.
Write-Host 'Verifying the public path...'
$tunnelBackendOk = Wait-ForUrl "$urlB/api/health" 'backend tunnel' 90
$tunnelFrontOk   = Wait-ForUrl $urlF 'frontend tunnel' 90

$corsOk = $false
if ($tunnelBackendOk) {
    try {
        $pre = Invoke-WebRequest -Uri "$urlB/api/predict" -Method Options -UseBasicParsing -TimeoutSec 20 -Headers @{
            'Origin'                         = $urlF
            'Access-Control-Request-Method'  = 'POST'
            'Access-Control-Request-Headers' = 'content-type'
        }
        $allow = $pre.Headers['Access-Control-Allow-Origin']
        $corsOk = ($pre.StatusCode -eq 200 -and $allow -eq $urlF)
        Write-Host ("CORS preflight: {0}, Access-Control-Allow-Origin={1}" -f $pre.StatusCode, $allow)
    } catch {
        Write-Warning "CORS preflight failed: $($_.Exception.Message)"
    }
}

Write-Host ''
Write-Host '  PUBLIC DEMO' -ForegroundColor Cyan
Write-Host  "  frontend (share this) : $urlF"
Write-Host  "  backend  (API)        : $urlB"
Write-Host  "  local                 : http://localhost:3000 / http://localhost:8000/api/health"
if ($Password) { Write-Host "  password gate         : ON (DEMO_PASSWORD)" }
else           { Write-Host "  password gate         : OFF - anyone with the URL can use the GPU" -ForegroundColor Yellow }
Write-Host ''

if ($backendOk -and $frontendOk -and $tunnelBackendOk -and $tunnelFrontOk -and $corsOk) {
    Write-Host 'All checks passed - the dashboard will report "real model".' -ForegroundColor Green
    Start-Process $urlF
} else {
    Write-Warning 'Some checks failed - the dashboard may fall back to the simulator. See the windows above.'
    Write-Host "cloudflared logs: $logF | $logB"
    if (-not $tunnelBackendOk -and -not $Http2) {
        Write-Host 'If the tunnels never answer, the venue network may block QUIC/UDP 7844 - rerun with -Http2.' -ForegroundColor Yellow
    }
}
Write-Host 'To stop everything: powershell -ExecutionPolicy Bypass -File start-tunnel.ps1 -Stop'
Write-Host 'Tunnel URLs are random per launch and die with these windows.'
