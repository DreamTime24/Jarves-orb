# NEXUS 0.2 measured verification — 5 October 2026

The application code, interface and Windows bootstrap package are delivered. **Full Windows acceptance is not complete.** This build ran on Linux, Python 3.12.14 and Node 24.19.0. Measurements below describe what actually ran; they are not an AGI, universal task-success or uptime claim.

| Check | Result | Actual scope |
|---|---|---|
| Python suite | **58/58 passed**, 4.759 s | Real HTTP/SQLite/filesystem, project-test subprocesses, approval, recovery, memory, policy; model test doubles are labeled |
| JS syntax | Passed | Main UI and local microphone module |
| Microphone cancellation | Passed | Controlled permission-promise test; navigation never starts a delayed recorder |
| Interface | **9 checks passed**, all 11 pages | Real headless Chromium interactions, memory, exact environment approval, feedback, projects, maze, offline error, 390px layout; no page exceptions |
| English STT | **Passed**, 5.318 s including load | Real recorded JFK fixture, Whisper small CPU int8, binary authenticated HTTP + jobs; native mic and recorded Bengali not tested |
| English neural TTS | **Passed**, 1.418 s synthesis including load | Piper 1.7.0 LJ Speech; real 4.1-second WAV, independently transcribed by Whisper; no subjective naturalness rating |
| Voice in UI | Passed | Real Piper output through authenticated WAV route, browser media readyState 4, playback started and Stop removed the control; no Windows speaker test |
| Real model smoke | **3/3 passed** | JSON, 12×13=156 and Bengali “প্রস্তুত”; Qwen3-4B Q4_K_M through CPU llama.cpp test harness |
| Real coding repair | **Passed**, 88.299 s | Model repaired subtraction to addition, 3 independent positive/negative/zero tests passed, exactly 1 write + 1 test approval; repeated actions suppressed |
| Bengali study | **Partial / full case failed**, 43.967 s | Relevant memory retrieved and broadly correct circuit facts generated; requested two-sentence format failed and wording was awkward |
| Backend soak | **Passed**, 600.004 s | 60 health samples, 2 forced process restarts, SQLite and memory/task persistence, 0 errors; no model/native/device load |
| Resource probe | Measurement unavailable | 30-second backend probe passed, but host PID mapping prevented RSS measurement; no memory-leak/stability conclusion |
| Worker watchdog | Passed scoped fixture | Authenticated HTTP health polling detected a failed-worker fixture and terminated an owned disposable child after 3 failed checks; production interval remains 20 s |
| Windows bootstrap | Compiled; native run **not tested** | Official runtime/SDK SHA512 verified, C# compilation succeeded, Linux guard rejected unsupported platform, selected Windows Python 3.13 wheels downloaded |
| Public import | Live test **failed here** | Public/private address and HTML policy unit checks passed; real import failed with DNS unavailable in this environment |
| Full 24-hour run | **Not run** | No 24/7 reliability certification |
| Commercial gameplay | **Not implemented** | Only the owned 8×8 maze solver ran; Genshin/Roblox are not connected |

## Evidence files

- unit-measured.json / unit-measured.txt: completed suite measurement summary.
- ui-measured.json, UI-preview.png, UI-mobile.png: actual interface report and screenshots.
- voice-measured.json, tts-measured.json, voice-ui-measured.json, Speech-sample.wav: actual voice outputs and scopes.
- model-measured.json: actual final coding repair and model request timings. study-measured.json: the final study-quality limitation.
- reliability-measured.json: real ten-minute backend run. reliability-resource-measured.json: short resource probe with missing RSS. reliability-final-smoke.json: backend restart smoke after final recovery changes.
- watchdog-measured.json: real watchdog polling/termination with an explicitly controlled fixture.
- launcher-build-measured.json: official bootstrap hashes, build metadata and available Windows wheels.
- network-measured.json: actual live-import DNS failure.

## Failures retained and corrected

The first model repair used a wrong test-file path. A later run incorrectly copied the prior study answer into a coding response. Another run fixed the code but repeated completed edits/tests until the planning budget. These baselines are retained in model-baseline-measured.json, model-context-failure-measured.json and model-repetition-measured.json. Current-task context ordering, separate Conversation mode, safe observation-error replanning, real observed hash binding and duplicate-action suppression corrected the coding workflow. This was one simple repair fixture, **not an advanced repository benchmark**.

The initial neural QA environment omitted Piper's pathvalidate dependency when manually installing without dependencies. The corrected real synthesis passed. That build-only setup failure is retained in tts-initial-measured.json; the application declares Piper normally so its dependencies are installed by pip.

The current default 4B model still failed the study formatting/fluency requirement. Selecting another installed model is supported, but no larger model was benchmarked here. Model weights in the CPU harness are identified explicitly; **native Windows Ollama and its selected tag were not executed here**.

## Windows acceptance to run on the target device

Run **Test-Windows.cmd** for automated checks plus labeled human observations of native window, microphone, speaker, screen capture, Notepad and real-model task behavior. Run **Test-Reliability.cmd** for the actual 86400-second backend test, then test native UI/model/device load separately. The reliability runner uses disposable data and does not replace full-device acceptance. A short run is never marked as a 24-hour pass.

The launcher performs default dependency/model preparation, but first setup still needs network, disk space and normal OS permissions. It has not been native-tested on the user's computer. A task marked completed does not, by itself, prove that every requested fact or behavior is correct; inspect tool evidence and meaningful tests.
