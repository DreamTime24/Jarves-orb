@echo off
if exist "%LOCALAPPDATA%\NEXUS\logs" (
  start "" "%LOCALAPPDATA%\NEXUS\logs"
) else (
  start "" "%~dp0START-HERE.html"
)
