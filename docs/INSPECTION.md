# What was inspected and corrected — 0.5

The existing 0.3 project, launcher source, packaging, configuration, dependency metadata and archived logs/reports were inspected. Existing reports did not establish native Windows acceptance. No missing Windows error log was invented.

- Prior setuptools discovery used a flat project directory with nexus, launcher and workspace. Explicit include/exclude rules now package only nexus; a clean source editable install and wheel build succeed.
- The prior bootstrap depended on first-launch Python/venv/package installation before showing a large interface. The new fixed C launcher uses bundled embedded Python/dependencies, opens the small orb first and provisions models visibly in background. Stale .NET binaries are removed from this release.
- PE imports exposed MSVCP140/MSVCP140_1 dependencies absent from the bundled Python. A real native-import probe and signed Microsoft runtime repair were added. Static inspection is not a Windows execution pass.
- Voice errors passed as strings were mishandled by the orb error handler; errors now normalize to a visible message and client log. Cleanup of asynchronous jobs was made bounded and tracked.
- Source launch/duplicate prevention, authenticated session reuse, normal shutdown and reopen were tested. Startup exceptions retain a visible message and detailed redacted trace.
- The default UI is compact; transcript/full workspace are optional. Worker/model/network work runs outside the UI thread. Mic/audio sessions use generation counters and half-duplex capture to prevent stale restarts and self-audio commands.
- Exact voice mappings run the actual clock/fixed browser/app tools and only report their observed result. App launch requires confirmation. No arbitrary speech-to-shell path, delete/message sender or unimplemented commercial-game control was added.

Windows PE execution, real native imports, hardware microphone/speaker, Windows window matching/size, actual fresh model provisioning and 24-hour acceptance remain target-PC checks. See TEST_REPORT.md and START-HERE.html.

0.5 continuation inspected the recovered project and actual logs. It fixed a missing SOCKS transport dependency, incomplete v3 speech model readiness, English persona contamination, adjacent user messages rejected by an alternating chat template, queued greeting/output races, a Piper subprocess module import path, unbounded ONNX thread defaults and device-check WAV validation/filename matching. Real Bengali model arithmetic failures led to a bounded Decimal calculator, not a fake corrected LLM result. Full observed model/ASR failures remain in current reports.
