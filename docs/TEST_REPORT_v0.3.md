# NEXUS 0.3 verification — 6 October 2026

Voice companion is implemented and packaged. Testing ran on Linux. Native Windows microphone/speaker and human Bengali speech acceptance remain open. A human-sounding persona is a style instruction, not a claim of human understanding or emotion.

| Check | Result | Scope |
|---|---|---|
| Python suite | 68/68 passed, 4.692 s | HTTP, SQLite, tool permissions, migration-backed tasks, voice profile, session context, privacy and corrupt-transcript guards; model tests are labeled doubles |
| JS capture/session checks | Passed | End-of-turn RMS silence, idle discard, PCM WAV resampling, greeting before capture, automatic follow-up, interrupt/end, late replies/cancellation, unclear input never auto-submitted |
| Existing UI regression | 9 checks passed / 12 pages | Real Chromium, actual local HTTP/SQLite, approvals, memory, environment, feedback, maze, offline failure and 390px layout |
| Voice companion UI | 9 checks passed | Actual Bengali Piper WAV played in Chromium; preferences persisted, controlled transcript drove a real persisted wake task, automatic follow-up, interrupt/end and navigation; microphone callbacks were fixtures |
| Bengali neural output | Waveform generation passed | 16 configured speakers synthesized successfully; sample speaker 0 generated 3.19 s of 22050 Hz WAV in 0.865 s, cached replay 0.0003 s; no subjective naturalness score |
| Bengali recognition round-trip | **Phrase accuracy failed** | Small, medium and large-v3-turbo did not reproduce one generated Bengali greeting accurately. Turbo inference including load took 6.249 s. This is not a human microphone test |
| Telemetry isolation | Scoped offline test passed | An initial unisolated ASR benchmark was rejected by automatic review for an unexplained Microsoft telemetry request. Documented ONNX/HF telemetry disabling was added; the later disposable Linux ASR process denied networking at the kernel boundary and verified socket creation failed before imports |
| Native Windows | Not tested | Launcher is carried forward from the compiled 0.2 component; Python/UI are 0.3. Normal native permission/autoplay/device checks remain necessary |
| 24-hour / commercial games | Not verified / not connected | No new claim; earlier scoped backend measurements are archived |

## Evidence

voice-unit-measured.json, ui-measured.json and voice-companion-ui-measured.json contain the completed checks. Voice-preview.jpg and Voice-mobile.jpg show the current interface with the local Bengali font; UI-preview.jpg/UI-mobile.jpg are current regression captures. Voice-bengali.wav is actual generated speech from the greeting, not a human recording.

voice-bengali-measured.json preserves the original waveform and inaccurate small-model transcript. voice-speaker-measured.json preserves the unsuccessful 16-speaker round-trip. The highest character-similarity score was a repetition artifact and was **not** used to choose the default speaker. asr-bengali-offline-measured.json, asr-bengali-medium-measured.json and asr-bengali-turbo-measured.json preserve exact outputs and scopes. Recognition does not receive a pass merely for producing Bengali characters.

The normal app explicitly disables dependency telemetry. The network-denying Linux QA filter was test infrastructure, not a Windows sandbox or a claim about the user's operating system. No unidentified external telemetry payload was authorized. Source model downloads were separate public download steps.

## Behavior and limits

A session must be started explicitly. It records bounded turns (maximum 20 seconds), auto-submits in Conversation mode and speaks the result before reopening the microphone. Playback and capture do not overlap. Interrupt is a visible button; spoken stop works during listening. There is no always-on OS wake-word service or full-duplex barge-in. Leaving the page or End discards later transcripts/answers/playback.

Conversation history is scoped to the session. Disabling memory removes that history and retrieved memories from prompts. Tool mode preserves per-action approvals. Voice input is not approval. A cancellation can prevent the next step; an already-running action may finish under the existing task rules.

Invalid script, replacement characters, repetition and low model log probability trigger a repeat request. This heuristic cannot detect every incorrectly heard word. Three consecutive unclear turns end the session with manual-transcript guidance. Model reply style and Bengali factual fluency remain dependent on the selected LLM; no new real-LLM fluency benchmark passed in this release.

Use Test-Windows.cmd on the target computer for labeled human observations including Voice companion, and Test-Reliability.cmd for a real full-day backend test. Earlier 0.2 measured model/voice/reliability results are retained in TEST_REPORT_v0.2.md and associated files. Historical PNG captures belong to that prior archive; current captures are JPEG to keep this download smaller.
