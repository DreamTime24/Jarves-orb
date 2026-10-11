# Setup — 0.5

Extract the full archive to a writable local folder and double-click **NEXUS.exe**. Intended target is Windows x64, Windows 10 22H2/Windows 11, Edge or Chrome, i5-13400 class CPU and 16 GB RAM. Native Windows operation has not been verified on those devices.

The portable package bundles official Python 3.13.16 embedded x64 and 29 installed Windows wheel packages. It needs neither a preinstalled Python/.NET runtime nor pip on normal launch. `launcher/portable.c` is the source of the included GUI PE executable; `desktop_launcher.py` runs the authenticated local service and reuses an existing session.

The small orb opens before model setup completes. First setup downloads the official Ollama Windows engine after validating its published SHA256, pulls Gemma3:4B, checks actual native speech imports, and prepares multilingual Whisper small, Bengali/auto large-v3, and Bengali/English Piper voices. Several GB of models are not embedded in the ZIP. Allow at least 20 GB of free user-data space, plus project space. Preparation may fail on restricted/offline machines; progress and logs are visible and Retry uses cached downloads where the upstream downloader supports them.

Static PE inspection found speech components needing MSVCP140/MSVCP140_1. If the real import probe detects a DLL error, setup downloads the fixed official Microsoft Visual C++ x64 redistributable, validates Windows Authenticode trust and Microsoft publisher, then runs its standard installer. A Windows/UAC permission prompt or restart may be necessary. This repair path has not been executed on Windows here. Setup never changes execution policy or disables Windows protections.

| Data | Location |
|---|---|
| Bundled Python/dependencies | NEXUS/runtime/python |
| SQLite tasks/settings/session descriptor | %LOCALAPPDATA%/NEXUS/data |
| Downloaded Ollama and runtime repair | %LOCALAPPDATA%/NEXUS/runtime |
| Model weights/cache | %LOCALAPPDATA%/NEXUS/models |
| Launcher/Ollama/error logs | %LOCALAPPDATA%/NEXUS/logs |
| Default approved project files | NEXUS/workspace |

Local inference uses CPU explicitly: Model context 4096, 6 threads, GPU layers 0, short voice replies up to 320 output tokens; Whisper uses int8/4 threads/one worker and retains one speech model. Latency and available memory depend on the PC and other applications; this is not a benchmark of the user's i5.

The native app uses Edge/Chrome app mode with a separate profile, approximately 320×380 outer window. Full workspace is optional at `/dashboard`. It falls back to a normal browser when app mode is unavailable. Minimize/drag/topmost address only this session's app window. Closing the native window after it is detected shuts down the backend. In browser mode use the orb Close button or Stop-NEXUS.cmd; closing a tab alone is not a reliable backend shutdown signal.

NEXUS-Web.cmd, Retry-Setup.cmd, Open-Without-Downloads.cmd and Create-Desktop-Shortcuts.cmd use fixed launcher options. Open-Without-Downloads skips automatic setup only when creating a new session; it does not cancel existing downloads. Normal launch never reinstalls dependencies.

For optional source development, use a normal Python 3.11+ venv and `pip install -r requirements-source.txt`; run Ollama first. `AI_PROVIDER` supports auto, disabled, ollama and openai-compatible. Remote API is optional and requires HTTPS; credentials remain backend environment variables, are not returned by status or saved to SQLite. Do not put credentials in memory or source control. The portable default needs no credential configuration. SCREEN_ACCESS_ENABLED sets the initial approved-screen preference; full-workspace Settings can change it.

Test-Windows.cmd labels native/device observations. Test-Reliability.cmd runs a real full-day *backend* test in disposable data; this does not verify a full day of microphone, model or native UI load. This app is not a Windows service and cannot run while the PC sleeps.

Jarvis preset selects Ryan male English voice, with its personal/noncommercial terms displayed in Settings and THIRD_PARTY.md. Device check ties human observations to completed production jobs and a valid WAV; it does not independently certify physical devices or Windows execution. Test-Native-Windows.cmd exercises the actual portable executable/window on Windows. Test-Voice-24h.cmd measures full-day real ASR/model/WAV load against the running app without recording the microphone or proving audible output.
