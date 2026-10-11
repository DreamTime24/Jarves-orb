@echo off
cd /d "%~dp0"
"runtime\python\python.exe" "scripts\windows_acceptance.py"
pause
