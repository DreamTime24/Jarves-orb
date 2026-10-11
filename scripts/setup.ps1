$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (!(Test-Path '.venv\Scripts\python.exe')) {
    py -3 -m venv .venv
    if ($LASTEXITCODE -ne 0) { throw 'Python 3.11+ is required for source mode.' }
}
& '.venv\Scripts\python.exe' -m pip install -r requirements-source.txt
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed. Browser mode needs no external packages.' }
if (!(Test-Path '.env')) { Copy-Item '.env.example' '.env' }
Write-Host 'Source-mode dependencies installed. Start Ollama, then run scripts/start.cmd. The portable NEXUS.exe requires neither this script nor a venv.'
