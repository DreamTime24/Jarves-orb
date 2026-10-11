$ErrorActionPreference = 'Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
if (Test-Path '.venv\Scripts\python.exe') {
    & '.venv\Scripts\python.exe' -m nexus @args
} else {
    py -3 -m nexus @args
}
