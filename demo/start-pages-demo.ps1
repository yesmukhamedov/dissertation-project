# start-pages-demo.ps1 - the defense demo on a PERMANENT free URL (Cloudflare Pages).
#
# Usage:  powershell -ExecutionPolicy Bypass -File start-pages-demo.ps1 -Password "<secret>"
#
# Costs nothing and needs no domain. Split hosting:
#
#   https://<project>.pages.dev   dashboard - static build on Cloudflare Pages (PERMANENT)
#   https://<random>.trycloudflare.com   API - quick tunnel to the local GPU backend
#
# The dashboard URL never changes, so it can go on a slide. The backend URL is
# random per launch, so the frontend is REBUILT with it baked into
# REACT_APP_API_URL and redeployed each time (~1-2 min; only changed files
# upload after the first deploy). The payoff: CORS_ORIGINS is now a CONSTANT
# (the pages.dev origin), so the backend never needs restarting for a new tunnel.
#
# Prerequisites (one time):
#   1. cloudflared:  winget install --id Cloudflare.cloudflared -e
#   2. Node/npm:     winget install --id OpenJS.NodeJS.LTS -e
#   3. npx wrangler login      <- interactive, opens a browser
#      With more than one Cloudflare account, also pass -AccountId <id> (the hex
#      string in the dashboard URL) or wrangler cannot pick one on its own.
#
# Params:
#   -Project <name>     Pages project (default dr-classification) => <name>.pages.dev
#   -AccountId <hex>    Cloudflare account id; required if the login has several
#   -Backend auto|native|wsl   as in start-demo.ps1 (default auto)
#   -Password <str>     sets DEMO_PASSWORD on the backend (access gate)
#   -SkipBuild          redeploy the existing build/ instead of rebuilding. ONLY
#                       valid if the backend tunnel URL has not changed.
#   -Http2              force cloudflared --protocol http2 (blocked QUIC/UDP 7844)
#   -Stop               kill the tunnel + backend and exit (the Pages site stays up,
#                       serving a dashboard whose backend is gone => simulator mode)

param(
    [ValidateSet('orchestrate', 'backend')]
    [string]$Role = 'orchestrate',

    [string]$Project = 'dr-classification',
    [string]$AccountId = '',

    [ValidateSet('auto', 'native', 'wsl')]
    [string]$Backend = 'auto',

    [string]$CorsOrigins = '',
    [string]$Password = '',

    [switch]$SkipBuild,
    [switch]$Http2,
    [switch]$Stop
)

$ErrorActionPreference = 'Stop'
$demoDir  = $PSScriptRoot
$webDir   = Join-Path $demoDir 'web'
$buildDir = Join-Path $webDir 'build'
$venvPy   = Join-Path $demoDir '.venv\Scripts\python.exe'

$driveLetter = $demoDir.Substring(0, 1).ToLower()
$wslDemoDir  = "/mnt/$driveLetter" + ($demoDir.Substring(2) -replace '\\', '/')

# Access password: -Password wins, else demo/.demo-password (gitignored). Having a
# default on disk means a launch never has to stop and ask for one.
$passwordFile = Join-Path $demoDir '.demo-password'
if (-not $Password -and (Test-Path $passwordFile)) {
    $Password = (Get-Content $passwordFile -Raw).Trim()
}

# Asset trees copied into build/ by CRA that nothing in src/ or public/*.md ever
# references - 367 MB of the 1.1 GB build, most of it a stale duplicate of
# pipeline/ under images/. Pruned before upload; verified unreferenced 2026-08-03.
$UnusedAssetDirs = @('images', 'fundus-examples', 'camera', 'webApp')

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

function Find-Npx {
    $cmd = Get-Command npx.cmd -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($c in @("${env:ProgramFiles}\nodejs\npx.cmd", "${env:ProgramFiles(x86)}\nodejs\npx.cmd")) {
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
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (Windows venv) [PAGES]'
        Set-Location $demoDir
        $env:PYTHONIOENCODING = 'utf-8'
        $env:CORS_ORIGINS = $CorsOrigins
        if ($Password) { $env:DEMO_PASSWORD = $Password }
        & $venvPy -m uvicorn server.app.main:app --host 127.0.0.1 --port 8000
    } else {
        $host.UI.RawUI.WindowTitle = 'demo backend - uvicorn :8000 (WSL Ubuntu) [PAGES]'
        $exports = "export CORS_ORIGINS='$CorsOrigins'"
        if ($Password) { $exports += " && export DEMO_PASSWORD='$Password'" }
        $bashCmd = "cd '$wslDemoDir' && $exports && ~/miniconda3/bin/conda run --no-capture-output -n dr-classifier uvicorn server.app.main:app --host 127.0.0.1 --port 8000"
        & wsl.exe -d Ubuntu bash -lc $bashCmd
    }
    exit $LASTEXITCODE
}

# ---------------------------------------------------------------- orchestrator
Write-Host '=== DR demo launcher (Cloudflare Pages + quick tunnel, no domain) ===' -ForegroundColor Cyan

$cloudflared = Find-Cloudflared
$npm = Find-Npm
$npx = Find-Npx

if ($Stop) {
    Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force
    Stop-Port 8000
    Stop-Port 3000
    & wsl.exe --status *> $null
    if ($LASTEXITCODE -eq 0) {
        & wsl.exe -d Ubuntu bash -lc "pkill -f 'uvicorn server.app.main' >/dev/null 2>&1; exit 0"
    }
    Write-Host 'Stopped: cloudflared, :8000, :3000.' -ForegroundColor Yellow
    Write-Host "The Pages site stays online at https://$Project.pages.dev (it will show 'simulator (backend offline)')."
    exit 0
}

if (-not $cloudflared) { Write-Error 'cloudflared not found. Install it: winget install --id Cloudflare.cloudflared -e'; exit 1 }
if (-not $npm -or -not $npx) { Write-Error 'npm/npx not found. Install Node: winget install --id OpenJS.NodeJS.LTS -e'; exit 1 }

$pagesUrl = "https://$Project.pages.dev"

# wrangler is run through npx (cached after the first download) and must never
# block on a prompt.
$env:WRANGLER_SEND_METRICS = 'false'
if ($AccountId) { $env:CLOUDFLARE_ACCOUNT_ID = $AccountId }

function Invoke-Wrangler([string[]]$WranglerArgs) {
    $prev = $env:CI
    $env:CI = '1'   # non-interactive for wrangler ONLY - CRA treats CI=1 warnings as errors
    try {
        $out = & $npx --yes wrangler @WranglerArgs 2>&1
        return @{ Code = $LASTEXITCODE; Text = ($out | Out-String) }
    } finally {
        if ($null -eq $prev) { Remove-Item Env:CI -ErrorAction SilentlyContinue } else { $env:CI = $prev }
    }
}

# --- wrangler auth ----------------------------------------------------------
Write-Host 'Checking the Cloudflare login (first run downloads wrangler, ~30s)...'
$who = Invoke-Wrangler @('whoami')
if ($who.Code -ne 0 -or $who.Text -match 'not authenticated|You are not logged in') {
    Write-Error @"
Not logged in to Cloudflare. Run this once, in an interactive shell:

    npx wrangler login

It opens a browser - authorise the account you want to host the dashboard on,
then rerun this script. With several accounts on the login, also pass
-AccountId <hex from the dashboard URL>.
"@
    exit 1
}
Write-Host '  logged in.' -ForegroundColor Green

# --- Pages project ----------------------------------------------------------
$projects = Invoke-Wrangler @('pages', 'project', 'list')
if ($projects.Text -notmatch [regex]::Escape($Project)) {
    Write-Host "Creating Pages project '$Project'..."
    $created = Invoke-Wrangler @('pages', 'project', 'create', $Project, '--production-branch', 'main')
    if ($created.Code -ne 0) {
        Write-Error "Failed to create the Pages project:`n$($created.Text)"
        exit 1
    }
    Write-Host "  created - $pagesUrl" -ForegroundColor Green
} else {
    Write-Host "Pages project '$Project' already exists - $pagesUrl"
}

$backendMode = Resolve-BackendMode $Backend
Write-Host "demo dir    : $demoDir"
Write-Host "backend     : $backendMode"
if (-not $Password) {
    Write-Warning 'No -Password given: the public URL will be OPEN to anyone. Pass -Password "<secret>" to enable the DEMO_PASSWORD gate.'
}
$checkpoint = Join-Path $demoDir 'server\checkpoints\config_d_fold0.pt'
$normStats  = Join-Path $demoDir 'server\checkpoints\eyepacs_norm_stats.json'
if (-not (Test-Path $checkpoint)) { Write-Warning "Checkpoint missing: $checkpoint - backend will boot with random weights." }
if (-not (Test-Path $normStats))  { Write-Warning "Norm stats missing: $normStats - backend falls back to ImageNet normalize (do NOT demo Config D that way)." }
if (-not (Test-Path (Join-Path $webDir 'node_modules'))) { Write-Warning "demo/web/node_modules missing - run 'npm install' in demo/web first." }

# --- backend + its tunnel ---------------------------------------------------
# CORS_ORIGINS is the CONSTANT pages.dev origin, so the backend survives any
# number of tunnel restarts.
$corsOrigins = "http://localhost:3000,$pagesUrl"

if (Test-PortListening 8000) {
    Write-Host 'Restarting the backend on :8000 so it carries the Pages origin...' -ForegroundColor Yellow
    Stop-Port 8000
    if ($backendMode -eq 'wsl') {
        & wsl.exe -d Ubuntu bash -lc "pkill -f 'uvicorn server.app.main' >/dev/null 2>&1; exit 0"
    }
    Start-Sleep -Seconds 2
}
Write-Host 'Starting backend window...'
$spawn = @('-NoExit', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-Backend', $backendMode, '-Role', 'backend',
           '-CorsOrigins', "`"$corsOrigins`"")
if ($Password) { $spawn += @('-Password', "`"$Password`"") }
Start-Process powershell -ArgumentList $spawn

Get-Process cloudflared -ErrorAction SilentlyContinue | Stop-Process -Force
$logB = Join-Path $env:TEMP 'cf_pages_backend.log'
Remove-Item $logB -ErrorAction SilentlyContinue
$cfArgs = @('tunnel', '--no-autoupdate')
if ($Http2) { $cfArgs += @('--protocol', 'http2') }
$cfArgs += @('--url', 'http://localhost:8000', '--logfile', $logB)
Write-Host 'Starting the backend quick tunnel...'
Start-Process -FilePath $cloudflared -ArgumentList $cfArgs -WindowStyle Minimized | Out-Null

$urlB = $null
$deadline = (Get-Date).AddSeconds(60)
while ((Get-Date) -lt $deadline -and -not $urlB) {
    if (Test-Path $logB) {
        $m = Select-String -Path $logB -Pattern 'https://[a-z0-9-]+\.trycloudflare\.com' -ErrorAction SilentlyContinue
        if ($m) { $urlB = ($m | Select-Object -First 1).Matches[0].Value }
    }
    if (-not $urlB) { Start-Sleep -Milliseconds 700; Write-Host '.' -NoNewline }
}
if (-not $urlB) { Write-Error "Timed out waiting for the backend tunnel URL. Log: $logB"; exit 1 }
Write-Host "  backend tunnel: $urlB" -ForegroundColor Green

$backendOk = Wait-ForUrl 'http://127.0.0.1:8000/api/health' 'backend /api/health' 240
if ($backendOk) {
    try {
        $health = Invoke-RestMethod -Uri 'http://127.0.0.1:8000/api/health' -TimeoutSec 5
        Write-Host ("Backend: checkpoint_loaded={0}, device={1}, checkpoint={2}" -f `
            $health.checkpoint_loaded, $health.device, $health.checkpoint)
        if (-not $health.checkpoint_loaded) { Write-Warning 'checkpoint_loaded=false - predictions will be random-init!' }
    } catch {}
} else {
    Write-Warning 'Backend did not come up - the deployed dashboard will fall back to the simulator.'
}

# --- build the dashboard against this tunnel --------------------------------
if ($SkipBuild) {
    Write-Host 'Skipping the build (-SkipBuild) - the existing build/ must already target this tunnel URL.' -ForegroundColor Yellow
    if (-not (Test-Path $buildDir)) { Write-Error "No build at $buildDir - rerun without -SkipBuild."; exit 1 }
} else {
    Write-Host "Building the dashboard against $urlB (this takes a minute)..."
    Push-Location $webDir
    try {
        $env:REACT_APP_API_URL = $urlB      # overrides the empty value in .env.production
        $env:GENERATE_SOURCEMAP = 'false'
        & $npm run build
        if ($LASTEXITCODE -ne 0) { Write-Error 'npm run build failed.'; exit 1 }
    } finally {
        Pop-Location
        Remove-Item Env:GENERATE_SOURCEMAP -ErrorAction SilentlyContinue
    }
    Write-Host '  build done.' -ForegroundColor Green
}

# CRA copies all of public/ into build/; drop what the app never requests so the
# upload is ~730 MB instead of 1.1 GB.
foreach ($d in $UnusedAssetDirs) {
    $p = Join-Path $buildDir $d
    if (Test-Path $p) {
        Write-Host "  pruning unused asset tree: build\$d"
        Remove-Item $p -Recurse -Force
    }
}

# --- deploy -----------------------------------------------------------------
Write-Host 'Deploying to Cloudflare Pages (the FIRST deploy uploads ~730 MB and can take a while;'
Write-Host 'later ones only send changed files)...'
$deploy = Invoke-Wrangler @('pages', 'deploy', $buildDir, '--project-name', $Project, '--branch', 'main', '--commit-dirty=true')
Write-Host $deploy.Text
if ($deploy.Code -ne 0) {
    Write-Error 'wrangler pages deploy failed - see the output above.'
    exit 1
}

# --- verify the public path -------------------------------------------------
Write-Host 'Verifying...'
$pagesOk  = Wait-ForUrl $pagesUrl 'Pages site' 120
$tunnelOk = Wait-ForUrl "$urlB/api/health" 'backend tunnel' 90

$corsOk = $false
if ($tunnelOk) {
    try {
        $pre = Invoke-WebRequest -Uri "$urlB/api/predict" -Method Options -UseBasicParsing -TimeoutSec 20 -Headers @{
            'Origin'                         = $pagesUrl
            'Access-Control-Request-Method'  = 'POST'
            'Access-Control-Request-Headers' = 'content-type'
        }
        $allow = $pre.Headers['Access-Control-Allow-Origin']
        $corsOk = ($pre.StatusCode -eq 200 -and $allow -eq $pagesUrl)
        Write-Host ("CORS preflight: {0}, Access-Control-Allow-Origin={1}" -f $pre.StatusCode, $allow)
    } catch {
        Write-Warning "CORS preflight failed: $($_.Exception.Message)"
    }
}

Write-Host ''
Write-Host '  PUBLIC DEMO' -ForegroundColor Cyan
Write-Host "  share this (PERMANENT) : $pagesUrl"
Write-Host "  API this session       : $urlB"
Write-Host "  local                  : http://localhost:8000/api/health"
if ($Password) { Write-Host '  password gate          : ON (DEMO_PASSWORD)' }
else           { Write-Host '  password gate          : OFF - anyone with the URL can use the GPU' -ForegroundColor Yellow }
Write-Host ''

if ($backendOk -and $pagesOk -and $tunnelOk -and $corsOk) {
    Write-Host 'All checks passed - the dashboard will report "real model".' -ForegroundColor Green
    Start-Process $pagesUrl
} else {
    Write-Warning 'Some checks failed - the dashboard may fall back to the simulator.'
    if (-not $tunnelOk -and -not $Http2) {
        Write-Host 'If the tunnel never answers, the venue network may block QUIC/UDP 7844 - rerun with -Http2.' -ForegroundColor Yellow
    }
}
Write-Host 'To stop the GPU backend: .\start-pages-demo.ps1 -Stop   (the Pages site stays online)'
Write-Host 'Rerun this script for every session - the tunnel URL changes and must be rebuilt in.'
