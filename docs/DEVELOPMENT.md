# Development — 0.5

## Source mode

Use a normal Python 3.11+ venv, not the bundled Windows runtime on Linux.

```sh
python -m pip install -r requirements-source.txt
python -m nexus --no-browser
python -m unittest discover -s tests -v
node --check nexus/web/orb.js
node tests/voice_capture.cjs
node tests/voice_session.cjs
python scripts/lifecycle_test.py
```

Start Ollama for real questions/model tasks. Tests use isolated data and clearly labeled model doubles; those doubles are never production fallback replies. Empty/disabled providers raise actual errors. The core source tests do not need voice weights.

## UI checks

Install Playwright/Chromium in a development environment, then run `python scripts/ui_test.py --orb` and `python scripts/ui_test.py`. Optional NEXUS_PLAYWRIGHT_PATH, NEXUS_BROWSER_EXECUTABLE and NEXUS_BROWSER_ARGS select a QA browser. Node/Playwright are not needed by the shipped app. Orb checks use actual HTTP/SQLite/clock execution and explicitly simulated microphone/voice flags/WAV output. Dashboard tests use real local tasks and an open-window callback fixture. These are not Windows hardware tests.

## Portable runtime reproduction

Download the official Python 3.13.16 win-amd64 embedded archive and verify the published SHA256 recorded in docs/portable-runtime-measured.json. Extract into runtime/python. Using a development Python/pip, download the pinned wheels:

```sh
python -m pip download --only-binary=:all: --platform win_amd64 --python-version 313 --implementation cp --abi cp313 --require-hashes -r requirements-windows.lock -d wheels
python -m pip install --no-deps --no-compile --only-binary=:all: --platform win_amd64 --python-version 313 --implementation cp --abi cp313 --target runtime/python/site-packages --no-index --find-links wheels --require-hashes -r requirements-windows.lock
```

Set runtime/python/python313._pth to lines `python313.zip`, `.`, `site-packages`, `../..`, `import site`. Keep dependency licenses/metadata. Compare wheel hashes with docs/dependency-manifest.json. Do not overwrite a user's model/data directories. Model weights are provisioned separately by SetupService.

## Launcher build

Compile launcher/portable.c with an x64 Windows compiler. This release used Zig 0.13.0:

```sh
zig cc -target x86_64-windows-gnu -O2 -municode -Wl,--subsystem,windows launcher/portable.c -o NEXUS.exe -luser32
```

Verify x64 Machine 0x8664 and GUI Subsystem 2, then **execute it on Windows** for native acceptance. Building/inspecting PE is not an execution test. The project does not publisher-sign NEXUS.exe. The old C#/.NET launcher is not used in 0.5.

## Reliability and retained evidence

`python scripts/soak.py --seconds 86400 --interval 30 --output docs/reliability-24h.json` measures real elapsed backend health/persistence and two forced restarts. It does not exercise microphone or model load. Earlier actual model/voice benchmarks and failed Bengali recognition are retained with their historical scope in TEST_REPORT_v0.3.md and TEST_REPORT_v0.2.md. Large model/QA tools are not shipped.
