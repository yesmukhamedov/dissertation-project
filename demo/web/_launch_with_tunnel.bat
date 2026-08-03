@echo off
rem SUPERSEDED. See demo\start-tunnel.ps1 (it locates cloudflared itself).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\start-tunnel.ps1" %*
pause
