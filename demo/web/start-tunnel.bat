@echo off
rem SUPERSEDED. The public-demo launcher now lives one level up: demo\start-tunnel.ps1
rem (drive-letter agnostic, native-Windows or WSL backend, password gate, health +
rem CORS verification). This file only forwards to it.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0..\start-tunnel.ps1" %*
pause
