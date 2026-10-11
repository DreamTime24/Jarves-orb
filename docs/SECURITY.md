# Security boundaries

The HTTP server binds to 127.0.0.1. Each launch uses a random bearer session token; Host and Origin are checked and a restrictive local-content policy applies. Do not share the private session URL. This does not protect against another malicious process with your own account privileges.

The model cannot grant approvals, install arbitrary tools, execute arbitrary shell commands or choose a filesystem root. Workspace paths reject traversal, excluded private paths, links and junctions. Existing-file edits require observed SHA256 and read-back verification. A local hostile process racing filesystem changes is outside the boundary; these controls are not an OS sandbox.

All project test execution requires exact approval and runs with your user privileges. Only predefined python_tests and git_status commands exist. Untrusted code may still access your account's files/network. No package manager or generated function is silently registered as a privileged tool.

Screen capture is opt-in and per-use approved. Microphone input is explicit push-to-talk or an explicitly started Voice companion session. Audio stays local in the implemented STT path, manual transcripts are editable; continuous mode auto-submits clear turns and recordings are not persistently stored by the backend. Bengali/English neural synthesis runs locally through a separate Piper process. Other output uses Windows voices or browser voices marked local. Generated output audio retains only the 32 most recent app-created WAVs. Source text and tool results are untrusted data and never permissions.

Public import permits HTTPS text only, resolves every address as public, pins the chosen IP for TLS with the original hostname, rejects redirects and caps content. DNS/TLS failures are surfaced. Imports require an approval and memory access. Credentials should not be stored in memory; heuristic redaction is not a guarantee of perfect secret detection.

Installer code is separate from model tools. The bundled Python archive was checked against its official published checksum. Setup verifies the official Ollama asset SHA256 and Microsoft runtime Authenticode trust/publisher. It does not modify execution policy or disable OS protections. Application binaries are not publisher-signed by this project. Bundled Python and wheel distributions preserve supplied licenses/notices; downloaded models retain their own licenses.

No security audit certification, encrypted database, continuous surveillance, account access, anti-cheat bypass or commercial-game adapter is claimed.

Voice preferences do not authorize tools. Voice sessions are scoped by random IDs; ending or navigating cancels late playback. Dubious script, corruption, repetition and low log probability trigger a retry, but the guard cannot identify every misrecognition. ONNX Runtime telemetry and Hugging Face telemetry are explicitly disabled. The Linux QA ASR process additionally denied networking at the kernel boundary; native Windows isolation was not tested.

Exact voice mappings never become arbitrary shell strings. App arguments and website URLs are allowlisted. Window control is restricted to this session title and installed browser executable. Detailed logs redact known configured credentials/session tokens; no perfect-redaction claim is made.
