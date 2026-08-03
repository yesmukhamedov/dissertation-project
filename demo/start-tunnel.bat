@echo off
rem Double-click launcher for the PUBLIC demo (backend + frontend + 2 Cloudflare tunnels).
rem Add a password gate by editing the line below, e.g.  -Password "defense2026"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start-tunnel.ps1"
pause
