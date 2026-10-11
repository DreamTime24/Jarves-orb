@echo off
cd /d "%~dp0"
"runtime\python\python.exe" "scripts\soak.py" --seconds 86400 --interval 30 --output "docs\reliability-24h.json"
pause
