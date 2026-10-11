# NEXUS 0.4 verification — 9 October 2026

Implemented source and portable Windows package; native Windows acceptance remains open. Tests ran on Linux unless stated. A successful PE build or controlled voice fixture is not a physical Windows voice pass.

| User acceptance item | Result | Actual scope |
|---|---|---|
| Fresh installation / setuptools | Source install passed | Clean venv editable install and wheel build with explicit nexus package discovery; complete Windows fresh setup not executed |
| Core/backend | 85/85 passed, 5.083 s | HTTP auth/schema, SQLite/FTS, exact approvals, tasks/recovery, commands, voice session context, no fake provider success and redacted errors; model tests include labeled doubles |
| Source launcher startup/close/reopen | Passed twice | Actual supervisor/HTTP/session descriptor, worker health, duplicate source exit 3, real clock command, shutdown exit 0, owned session removal and reopened data |
| Default compact orb | 13 checks passed | Actual Chromium at 320×380 and 304×341 client approximation; persisted preferences, text fallback, real clock/approval, Stop/mute, continuous/PTT, errors/retry and no uncaught page errors |
| UI voice flow | Controlled-fixture pass only | Simulated microphone transcript → actual persisted clock task/command → simulated WAV rendered/played; mic-off during playback. Speech flags, device permission and WAV output were fixtures; no real ASR/Piper/LLM/device pass claimed |
| JS capture/session | Passed | Real logic for end-of-turn/idle silence, PCM resampling, greeting before capture, follow-up, stale input cancellation, interrupted greeting, late task cancellation, stable PTT/text context and unclear input never sent as command; device APIs mocked |
| Optional full web workspace | 11 checks / 13 pages passed | Actual Chromium/HTTP/SQLite, memory, approvals, environment, feedback, maze, offline model errors and mobile layout; external-open callback fixture |
| Bengali/English question/follow-up | Context/prompt logic passed; real native conversation open | Scoped stored history and provider request behavior tested with doubles. No new actual Qwen fluency or human Banglish recognition acceptance |
| Supported command | Clock actually executed | Task evidence contains actual local time; app approval/deny and failed browser request tested. Native app visibility/external page load not verified |
| Failure behavior | Passed within stated scope | Disabled model → failed task/visible error; simulated missing mic/service errors → retry/text fallback; detailed known-token redaction test |
| Windows launcher/runtime | Build/static inspection only | x64 Machine 0x8664, GUI Subsystem 2, bundled official Python and 28 pinned wheels; not executed on Windows |
| Native dependency repair | Implemented, not natively tested | PE inspection found MSVCP140/MSVCP140_1 imports; fixed real-import probe and signed Microsoft repair. No static-file check is reported as execution |
| New short reliability run | Passed: 60.004 s, 30 health/persistence samples, 2 forced restarts | Real Linux backend; psutil measurement unavailable and recorded, no mic/model/UI load; 24_hour_pass remains false |
| Full 24 hours / game play | Not verified / not implemented | Full-day backend runner supplied; no SLA, no real commercial-game adapter |

## Root causes and changes

The prior flat-layout package did not constrain setuptools discovery. It now includes only nexus and excludes launcher/workspace/runtime/tests/scripts. The prior first-run bootstrap/setup path delayed the interface and depended on package installation. The new C launcher uses bundled dependencies, starts/reuses a private local session and opens the compact orb before model download. It never reinstalls dependencies on normal launch.

Native DLL inspection found a potential Windows import failure requiring Microsoft C++ runtime libraries. Setup actually probes imports and repairs only matching DLL failures with a signed official installer. This remains a target-Windows check. UI voice error strings were normalized, errors now retain detailed redacted logs, and background jobs have bounded shutdown joining. Stop also invalidates queued backend speech before it can launch a process. Local model/session HTTP bypasses system proxies. Exact voice mappings produce observed tool evidence, with app confirmation and no speech-to-shell path.

## Evidence and historical limits

New evidence: orb-ui-measured.json, ui-measured.json, lifecycle-measured.json, unit-measured.json, portable-runtime-measured.json, native-dll-measured.json, dependency-manifest.json and launcher-portable-measured.json. Orb-preview.jpg and Orb-layout-341.jpg are real headless UI captures. They do not show a verified Windows app.

Historical model/voice/soak measurements remain under their prior scopes in TEST_REPORT_v0.3.md and TEST_REPORT_v0.2.md. Historical Bengali Piper waveform generation passed, but one generated Bengali greeting's Whisper phrase accuracy **failed** across tested model variants. Those results have not been relabeled as 0.4 passes. Banglish/code switching, factual quality, human voice naturalness and target CPU latency remain dependent on models/hardware.

## What this environment could not verify

- Fresh Windows extraction → actual NEXUS.exe, Edge/Chrome app window, single-window reuse, native drag/minimize/topmost/close matching.
- Execution/imports of bundled Windows wheels and the signed Microsoft runtime repair/UAC/restart path.
- Actual first-run Ollama/model provisioning on Windows; real Bengali/English/Banglish microphone, speaker, permissions/autoplay and contextual spoken questions.
- Human speech accuracy/naturalness, i5-13400/16 GB load/latency and a full 24-hour native voice/model endurance run.

Use Test-Windows.cmd after target-PC setup for automated plus explicitly labeled human observations. Test-Reliability.cmd is a genuine 86400-second disposable **backend-only** test. It must not be represented as a microphone/model-load endurance certificate. Own speaker output is prevented from capture by half-duplex turns; spoken “থামো” works while listening, and Stop interrupts while output is playing.
