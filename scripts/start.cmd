@echo off
cd /d "%~dp0\.."
if exist .venv\Scripts\python.exe (
  .venv\Scripts\python.exe -m nexus %*
) else (
  py -3 -m nexus %*
)
