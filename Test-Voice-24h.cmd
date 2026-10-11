@echo off
cd /d "%~dp0"
"runtime\python\python.exe" "scripts\voice_soak.py" --seconds 86400 --interval 300
echo.
echo Test finished. See the JSON report described in README.md.
pause
