# Troubleshooting

| Problem | Action |
|---|---|
| Double-click does not open | Extract ALL files; keep NEXUS.exe, desktop_launcher.py and runtime together. Check Open-Diagnostics.cmd → launcher.log/startup-error.log. |
| Multiple top-level packages discovered | Fixed explicit `nexus` package discovery in pyproject.toml. Portable mode does not invoke setuptools/pip. For source mode install this corrected project in a fresh venv. |
| DLL/native import failure | Settings → Prepare/retry setup. It probes imports and can run the signed official Microsoft runtime repair. Inspect errors.log; allow the normal Windows permission prompt if you choose to install it. Restart Windows if requested. |
| Brain not ready | Setup needs Ollama and an installed model. Retry setup. A selected model is not proof that inference works; connection checks and actual task failures are shown. |
| Mic denied/unavailable | Check Windows microphone privacy and Edge/Chrome permissions for localhost. Retry Mic. Text input works independently of the microphone. |
| Bengali/Banglish misheard | Use short clear turns, correct language and a quiet mic. Review Transcript; use Text input for commands when uncertain. Recognition accuracy is not guaranteed. |
| No spoken audio | Unmute, check output device/volume, prepare voices and press visible Play if browser autoplay blocks playback. Stop still cancels output. |
| Reply is slow | CPU models take time. Close other heavy apps, keep short turns and use text fallback. No GPU is assumed. |
| App window controls unavailable | Use the Windows title bar or NEXUS-Web.cmd. Native title/process matching may need target-PC inspection; it has not been verified here. |
| Close left a browser service running | Closing a browser tab alone cannot signal shutdown reliably. Use the orb × or Stop-NEXUS.cmd. |
| Approval pending | Review exact action and arguments; Approve once or Deny. Voice is not approval. |
| UNCERTAIN after a crash | Inspect whether the side effect happened, acknowledge/cancel and create a new task if needed. It does not blindly replay it. |
| Unsupported delete/message/game request | No such voice command or commercial-game adapter is installed. It reports unsupported rather than successful. |
| Web source import failed | Public HTTPS text only; private addresses, redirects and nontext data are rejected. DNS/TLS failures are surfaced. |
| Shortcut points to old folder | Stop the old instance and run Create-Desktop-Shortcuts.cmd from the new extracted folder. |

Errors appear in the orb and in redacted logs. `launcher.log` records startup/supervisor output, `startup-error.log` records bootstrap exceptions, `errors.log` contains background/API/task/client traces and `ollama.log` records the owned engine. Known session tokens/API credentials are redacted, but review logs before sharing them.
