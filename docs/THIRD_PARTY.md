# Third-party components — 0.5

The ZIP contains the official CPython 3.13.16 Windows x64 embedded runtime and 29 pinned wheel distributions. Original licenses, notices, package data and .dist-info records remain under runtime/python/site-packages. Exact filenames, versions and SHA256 are in docs/dependency-manifest.json and requirements-windows.lock. Python has its PSF license. The new socksio 1.0.0 wheel is MIT licensed. Dependencies are reused on normal launch.

NEXUS application code is MIT licensed except nexus/piper_runner.py, which is explicitly GPL-3.0-or-later; its license is docs/PIPER_RUNNER_LICENSE.txt. It starts the upstream Piper CLI in a separate process, sets bounded ONNX CPU threads and disables telemetry. Piper 1.7.0, eSpeak-ng and PyAV/FFmpeg notices and corresponding source/build inputs are preserved in third-party-sources. See its README and SOURCE-MANIFEST.json. Keep those materials when redistributing. No license of an aggregated component is replaced by NEXUS's MIT license.

Model weights are downloaded separately; they are not in the ZIP. The original model cards are downloaded alongside Piper voices.

| Component | Source / terms |
|---|---|
| English Ryan medium | https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/ryan/medium — MODEL_CARD identifies CC BY-NC-SA 4.0: personal noncommercial use; observe its attribution and share-alike terms. Settings offers LJ Speech as another English voice. |
| English LJ Speech medium | https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/ljspeech/medium — card identifies the public-domain LJ Speech dataset; retain its card and other included notices. |
| Bengali Google medium, 16 speakers | https://huggingface.co/rhasspy/piper-voices/tree/main/bn/bn_BD/google/medium — card attributes OpenSLR 37, CC BY-SA 4.0, and CMU Indic under its included terms. |
| Speech recognition | https://huggingface.co/Systran/faster-whisper-small and https://huggingface.co/Systran/faster-whisper-large-v3 — converted Whisper models; preserve upstream terms. |
| Default local language model | https://ollama.com/library/gemma3:4b — Google Gemma terms: https://ai.google.dev/gemma/terms and model card https://ai.google.dev/gemma/docs/core/model_card_3. Review terms for your use and redistribution. |
| Local engine | Official Ollama Windows release fetched from https://github.com/ollama/ollama with its published SHA256; Microsoft runtime repair checks the Authenticode publisher. |
| Bengali UI font | Unmodified Noto Sans Bengali from google/fonts; SIL OFL is included at nexus/web/fonts/OFL.txt. |

QA used the official Ollama Gemma3/Qwen2.5 layers, official llama.cpp b11429 CPU binary, faster-whisper's JFK fixture, and three bounded Google FLEURS Bengali dev clips (CC BY 4.0). The reports contain attribution and exact scope; those human clips and external QA model binaries are not embedded. Voice-English-05.wav and Voice-Bengali-05.wav are app-generated demonstration output, not user recordings or proof of audible playback. Historical measured reports retain their original version scopes.
