# start-named-tunnel.ps1 - the defense demo on a PERMANENT hostname (Cloudflare named tunnel).
#
# Unlike start-tunnel.ps1 (quick tunnels, random *.trycloudflare.com URLs that die
# with the window), this serves the demo at a stable hostname of your own zone and
# can run as a Windows service, surviving reboots.
#
# ONE hostname, path-routed - the whole API lives under /api/ and every frontend
# call is `${API}/api/...`, so both halves fit behind one name:
#
#   https://<hostname>/api/*  --> localhost:8000  (FastAPI)
#   https://<hostname>/*      --> localhost:3000  (CRA)
#
# Same origin => no CORS preflight, no mixed-content block, one URL to hand out.
#
# Prerequisites (one time):
#   1. cloudflared installed:  winget install --id Cloudflare.cloudflared -e
#   2. an ACTIVE zone in your Cloudflare account, on FULL DNS setup (the zone's
#      nameservers delegated to Cloudflare) - a partial/CNAME zone cannot hold the
#      CNAME to <uuid>.cfargotunnel.com that routing needs.
#   3. cloudflared tunnel login      <- opens a browser, pick the zone; writes cert.pem
#
# Then:
#   .\start-named-tunnel.ps1 -Hostname dr-classification.example.com -Setup
#   .\start-named-tunnel.ps1 -Hostname dr-classification.example.com -Password "<secret>"
#
# Params:
#   -Hostname <fqdn>        required; the public name to serve on
#   -TunnelName <name>      cloudflared tunnel name (default dr-demo)
#   -Setup                  create the tunnel + config + DNS route, then exit
#   -Backend auto|native|wsl  as in start-demo.ps1 (default auto)
#   -Password <str>         sets DEMO_PASSWORD on the backend (access gate)
#   -InstallService         install the tunnel as a Windows service (needs an
#                           elevated shell); the servers are NOT services - see
#                           the note at the bottom of RUNBOOK.md
#   -Stop                   kill the tunnel + servers and exit

param(
    [ValidateSet('orchestrate', 'backend', 'frontend')]
    [string]$Role = 'orchestrate',

    [string]$Hostname = '',
    [string]$TunnelName = 'dr-demo',

    [ValidateSet('auto', 'native', 'wsl')]
    [string]$Backend = 'auto',

    [string]$ApiUrl = '',
    [string]$CorsOrigins = '',
    [string]$Password = '',

    [switch]$Setup,
    [switch]$InstallService,
    [switch]$Stop
)

$ErrorActionPreference = 'Stop'
$demoDir = $PSScriptRoot
$webDir  = Join-Path $demoDir 'web'
$venvPy  = Join-Path $demoDir '.venv\Scripts\python.exe'

$driveLetter = $demoDir.Substring(0, 1).ToLower()
$wslDemoDir  = "/mnt/$driveLetter" + ($demoDir.Substring(2) -replace '\\', '/')

# Access password: -Password wins, else demo/.demo-password (gitignored). Having a
# default on disk means a launch never has to stop and ask for one.
$passwordFile = Join-Path $demoDir '.demo-password'
if (-not $Password -and (Test-Path $passwordFile)) {
    $Password = (Get-Content $passwordFile -Raw).Trim()
}

$cfDir      = Join-Path $env:USERPROFILE '.cloudflared'
$cfConfig   = Join-Path $cfDir 'config.yml'
$repoCfgDir = Join-Path $demoDir 'cloudflared'

function Sync-PathFromRegistry {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user    = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = (@($machine, $user) | Where-Object { $_ } ) -join ';'
}
Sync-PathFromRegistry

function Resolve-BackendMode([string]$Requested) {
    if ($Requested -ne 'auto') { return $Requested }
    if (Test-Path $venvPy) { return 'native' }
    return 'wsl'
}

function Find-Npm {
    $cmd = Get-Command npm.cmd -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($c in @("${env:ProgramFiles}\nodejs\npm.cmd", "${env:ProgramFiles(x86)}\nodejs\npm.cmd")) {
        if (Test-Path $c) { return $c }
    }
    return $null
}

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
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (Windows venv) [NAMED TUNNEL]'
        Set-Location $demoDir
        $env:PYTHONIOENCODING = 'utf-8'
        $env:CORS_ORIGINS = $CorsOrigins
        if ($Password) { $env:DEMO_PASSWORD = $Password }
        & $venvPy -m uvicorn server.app.main:app --host 127.0.0.1 --port 8000
    } else {
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (WSL Ubuntu) [NAMED TUNNEL]'
        $exports = "export CORS_ORIGINS='$CorsOrigins'"
        if ($Password) { $exports += " && export DEMO_PASSWORD='$Password'" }
        $bashCmd = "cd '$wslDemoDir' && $exports && ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier uvicorn server.app.main:app --host 127.0.0.1 --port 8000"
        & wsl.exe -d Ubuntu bash -lc $bashCmd
    }
    exit $LASTEXITCODE
}

# --------------------------------------------------------------- frontend role
if ($Role -eq 'frontend') {
    $host.UI.RawUI.WindowTitle = 'demo frontend - CRA :3000 [NAMED TUNNEL]'
    Set-Location $webDir
    $env:BROWSER = 'none'
    $env:REACT_APP_API_URL = $ApiUrl              # same origin as the page
    $env:WDS_SOCKET_PORT = '0'                    # HMR socket follows the page port (443)
    $env:DANGEROUSLY_DISABLE_HOST_CHECK = 'true'  # accept the custom Host header
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
Write-Host '=== DR demo launcher (PERMANENT hostname / Cloudflare named tunnel) ===' -ForegroundColor Cyan

$cloudflared = Find-Cloudflared
if (-not $cloudflared) {
    Write-Error 'cloudflared not found. Install it: winget install --id Cloudflare.cloudflared -e'
    exit 1
}

if ($Stop) {
    Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force
    Stop-Port 3000
    Stop-Port 8000
    & wsl.exe --status *> $null
    if ($LASTEXITCODE -eq 0) {
        & wsl.exe -d Ubuntu bash -lc "pkill -f 'uvicorn server.app.main' >/dev/null 2>&1; exit 0"
    }
    Write-Host 'Stopped: cloudflared, :3000, :8000.' -ForegroundColor Yellow
    Write-Host 'If the tunnel is installed as a service, stop it with: Stop-Service cloudflared'
    exit 0
}

if (-not $Hostname) {
    Write-Error 'Pass -Hostname <fqdn>, e.g. -Hostname dr-classification.example.com'
    exit 1
}
$publicUrl = "https://$Hostname"

# --- login state ------------------------------------------------------------
if (-not (Test-Path (Join-Path $cfDir 'cert.pem'))) {
    Write-Error @"
Not logged in to Cloudflare. Run this once, in an interactive shell:

    cloudflared tunnel login

It opens a browser; pick the zone that owns $Hostname. The zone must be ACTIVE
and on full DNS setup (nameservers delegated to Cloudflare). It writes
$cfDir\cert.pem, after which rerun this script with -Setup.
"@
    exit 1
}

# --- tunnel: create if missing ----------------------------------------------
function Get-TunnelId([string]$Name) {
    $raw = & $cloudflared tunnel list --output json 2>$null
    if ($LASTEXITCODE -ne 0 -or -not $raw) { return $null }
    $list = $raw | ConvertFrom-Json
    $t = $list | Where-Object { $_.name -eq $Name -and -not $_.deleted_at } | Select-Object -First 1
    if ($t) { return $t.id }
    return $null
}

$tunnelId = Get-TunnelId $TunnelName
if (-not $tunnelId) {
    Write-Host "Creating tunnel '$TunnelName'..."
    & $cloudflared tunnel create $TunnelName
    if ($LASTEXITCODE -ne 0) { Write-Error "cloudflared tunnel create failed."; exit 1 }
    $tunnelId = Get-TunnelId $TunnelName
    if (-not $tunnelId) { Write-Error "Tunnel created but not found in 'tunnel list'."; exit 1 }
}
Write-Host "tunnel      : $TunnelName ($tunnelId)"
Write-Host "hostname    : $publicUrl"
Write-Host "cloudflared : $cloudflared"

$credFile = Join-Path $cfDir "$tunnelId.json"
if (-not (Test-Path $credFile)) {
    Write-Warning "Credentials file not found at $credFile - the tunnel may have been created on another machine. Recreate it there or copy the JSON across."
}

# --- config.yml (single hostname, /api/* split off to the backend) ----------
$configYaml = @"
# Generated by demo/start-named-tunnel.ps1 - regenerate rather than hand-editing.
tunnel: $tunnelId
credentials-file: '$credFile'

ingress:
  # The whole API lives under /api/ (see server/app/main.py); path is a regex.
  - hostname: $Hostname
    path: ^/api/
    service: http://localhost:8000
  # Everything else is the dashboard (CRA dev server, websockets included).
  - hostname: $Hostname
    service: http://localhost:3000
  - service: http_status:404
"@

if (-not (Test-Path $cfDir)) { New-Item -ItemType Directory -Path $cfDir | Out-Null }
Set-Content -Path $cfConfig -Value $configYaml -Encoding ascii
Write-Host "config      : $cfConfig"

# Repo copy so the setup travels with the drive (credentials themselves do not).
if (-not (Test-Path $repoCfgDir)) { New-Item -ItemType Directory -Path $repoCfgDir | Out-Null }
Set-Content -Path (Join-Path $repoCfgDir 'config.yml.example') -Value $configYaml -Encoding ascii

# --- DNS route --------------------------------------------------------------
Write-Host "Routing DNS $Hostname -> $tunnelId.cfargotunnel.com ..."
$routeOut = & $cloudflared tunnel route dns $TunnelName $Hostname 2>&1
$routeText = ($routeOut | Out-String).Trim()
if ($LASTEXITCODE -ne 0) {
    if ($routeText -match 'already exists|record with that host') {
        Write-Host '  DNS record already present - keeping it.' -ForegroundColor Yellow
    } else {
        Write-Warning "DNS routing failed: $routeText"
        Write-Warning 'If the zone is on partial (CNAME) setup, move it to full setup - a tunnel route needs Cloudflare-managed DNS.'
    }
} else {
    Write-Host "  $routeText"
}

if ($InstallService) {
    Write-Host 'Installing cloudflared as a Windows service (requires elevation)...'
    & $cloudflared service install
    if ($LASTEXITCODE -eq 0) {
        Write-Host 'Service installed. It runs the tunnel only - start the demo servers separately.' -ForegroundColor Green
        Write-Host '  Start-Service cloudflared / Stop-Service cloudflared'
    } else {
        Write-Warning 'Service install failed - rerun this script from an elevated PowerShell.'
    }
}

if ($Setup) {
    Write-Host ''
    Write-Host 'Setup done. Start the demo with:' -ForegroundColor Green
    Write-Host "  .\start-named-tunnel.ps1 -Hostname $Hostname -Password `"<secret>`""
    exit 0
}

# --- sanity checks ----------------------------------------------------------
$backendMode = Resolve-BackendMode $Backend
Write-Host "backend     : $backendMode"
if (-not $Password) {
    Write-Warning 'No -Password given: the hostname will be OPEN to anyone. Pass -Password "<secret>" to enable the DEMO_PASSWORD gate.'
}
$checkpoint = Join-Path $demoDir 'server\checkpoints\config_d_fold0.pt'
$normStats  = Join-Path $demoDir 'server\checkpoints\eyepacs_norm_stats.json'
if (-not (Test-Path $checkpoint)) { Write-Warning "Checkpoint missing: $checkpoint - backend will boot with random weights." }
if (-not (Test-Path $normStats))  { Write-Warning "Norm stats missing: $normStats - backend falls back to ImageNet normalize (do NOT demo Config D that way)." }
if (-not (Test-Path (Join-Path $webDir 'node_modules'))) { Write-Warning "demo/web/node_modules missing - run 'npm install' in demo/web first." }
if (-not (Find-Npm)) { Write-Warning 'npm not found - the frontend will not start. Install Node: winget install --id OpenJS.NodeJS.LTS -e' }

# The hostname is fixed, but REACT_APP_API_URL / CORS_ORIGINS are still read at
# process start, so restart the servers to be sure they carry this hostname.
if ((Test-PortListening 3000) -or (Test-PortListening 8000)) {
    Write-Host 'Restarting the servers already on :3000/:8000 so they carry this hostname...' -ForegroundColor Yellow
    Stop-Port 3000
    Stop-Port 8000
    if ($backendMode -eq 'wsl') {
        & wsl.exe -d Ubuntu bash -lc "pkill -f 'uvicorn server.app.main' >/dev/null 2>&1; exit 0"
    }
    Start-Sleep -Seconds 2
}

$spawn = @('-NoExit', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-Backend', $backendMode)

# Same origin, so CORS is not exercised by the browser; the allowlist is kept
# accurate anyway for direct API callers and for local :3000 development.
$corsOrigins = "http://localhost:3000,$publicUrl"
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
        if (-not $health.checkpoint_loaded) { Write-Warning 'checkpoint_loaded=false - predictions will be random-init!' }
    } catch {}
}

Write-Host 'Starting frontend window...'
Start-Process powershell -ArgumentList ($spawn + @('-Role', 'frontend', '-ApiUrl', "`"$publicUrl`""))
$frontendOk = Wait-ForUrl 'http://localhost:3000' 'frontend' 300

# --- the tunnel itself ------------------------------------------------------
$svc = Get-Service cloudflared -ErrorAction SilentlyContinue
if ($svc -and $svc.Status -eq 'Running') {
    Write-Host 'cloudflared service is already running - not starting a second connector.' -ForegroundColor Yellow
} else {
    Write-Host 'Starting the tunnel connector...'
    Start-Process -FilePath $cloudflared -ArgumentList @('--config', $cfConfig, 'tunnel', 'run', $TunnelName) -WindowStyle Minimized | Out-Null
}

$publicOk  = Wait-ForUrl "$publicUrl/api/health" 'public /api/health' 120
$publicApp = Wait-ForUrl $publicUrl 'public dashboard' 120

Write-Host ''
Write-Host '  PUBLIC DEMO (permanent hostname)' -ForegroundColor Cyan
Write-Host "  share this : $publicUrl"
Write-Host "  API        : $publicUrl/api/health"
Write-Host "  local      : http://localhost:3000 / http://localhost:8000/api/health"
if ($Password) { Write-Host '  password gate : ON (DEMO_PASSWORD)' }
else           { Write-Host '  password gate : OFF - anyone with the URL can use the GPU' -ForegroundColor Yellow }
Write-Host ''

if ($backendOk -and $frontendOk -and $publicOk -and $publicApp) {
    Write-Host 'All checks passed - the dashboard will report "real model".' -ForegroundColor Green
    Start-Process $publicUrl
} else {
    Write-Warning 'Some checks failed. If the public checks time out, verify: the zone is ACTIVE on full DNS setup, the CNAME to <uuid>.cfargotunnel.com exists and is proxied (orange cloud), and the connector window shows registered connections.'
}
Write-Host 'To stop: .\start-named-tunnel.ps1 -Stop     (plus Stop-Service cloudflared if installed as a service)'
