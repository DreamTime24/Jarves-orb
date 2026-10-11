@echo off
cd /d "%~dp0"
"runtime\python\python.exe" "scripts\windows_native_test.py"
echo.
echo Test finished. See the JSON report described in README.md.
pause
