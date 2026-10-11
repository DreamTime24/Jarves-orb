"""Portable entry point used by NEXUS.exe. Requires only the bundled Python."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent


def configure():
    user = Path(os.environ.get('LOCALAPPDATA', str(Path.home() / '.local' / 'share'))) / 'NEXUS'
    data = user / 'data'
    data.mkdir(parents=True, exist_ok=True)
    (user / 'logs').mkdir(exist_ok=True)
    defaults = {'NEXUS_DATA': str(data), 'NEXUS_WORKSPACE': str(ROOT / 'workspace'), 'NEXUS_RUNTIME': str(user / 'runtime'), 'STT_MODEL_DIR': str(user / 'models' / 'whisper-small'), 'STT_BENGALI_MODEL_DIR': str(user / 'models' / 'whisper-turbo'), 'TTS_MODEL_DIR': str(user / 'models' / 'piper'), 'OLLAMA_MODELS': str(user / 'models' / 'ollama'), 'OLLAMA_HOST': '127.0.0.1:11434', 'OLLAMA_NUM_PARALLEL': '1', 'AI_PROVIDER': 'auto', 'AI_TIMEOUT_SECONDS': '240', 'PYTHONUTF8': '1', 'HF_HUB_DISABLE_TELEMETRY': '1'}
    for key, value in defaults.items():
        os.environ.setdefault(key, value)
    return user, Path(os.environ['NEXUS_DATA'])


def message(text, error=False):
    if os.name == 'nt':
        ctypes.windll.user32.MessageBoxW(None, text, 'NEXUS', 0x10 if error else 0x40)
    else:
        print(text, file=sys.stderr if error else sys.stdout)


def main():
    parser = argparse.ArgumentParser()
    for flag in ['app', 'browser', 'stop', 'repair', 'shortcuts', 'no-setup']:
        parser.add_argument('--' + flag, action='store_true')
    args = parser.parse_args()
    os.chdir(ROOT)
    from nexus.shell import read_session, session_request, open_ui, create_shortcuts
    user, data = configure()
    if args.shortcuts:
        create_shortcuts(ROOT)
        message('NEXUS AI and NEXUS Web shortcuts were created on your Desktop.')
        return 0
    existing = read_session(data)
    if args.stop:
        if existing:
            session_request(existing['url'], '/api/system/shutdown', {})
        else:
            message('NEXUS is already stopped.')
        return 0
    if existing:
        if args.repair:
            session_request(existing['url'], '/api/setup/start', {})
        session_request(existing['url'],'/api/ui/open',{'mode':'browser' if args.browser else 'app'})
        return 0
    log = user / 'logs' / 'launcher.log'
    if log.exists() and log.stat().st_size > 2_000_000:
        log.replace(log.with_suffix('.previous.log'))
    env = os.environ.copy()
    env['NEXUS_AUTO_SETUP'] = '0' if args.no_setup else '1'
    with log.open('ab') as output:
        child = subprocess.Popen([sys.executable, '-m', 'nexus.supervisor', '--no-browser'], cwd=ROOT, env=env, stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    for _ in range(120):
        ready = read_session(data)
        if ready:
            session_request(ready['url'],'/api/ui/open',{'mode':'browser' if args.browser else 'app'})
            return 0
        if child.poll() is not None:
            # A simultaneous second launcher may have acquired the instance lease.
            time.sleep(.25)
            ready = read_session(data)
            if ready:
                session_request(ready['url'],'/api/ui/open',{'mode':'browser' if args.browser else 'app'})
                return 0
            break
        time.sleep(.25)
    raise RuntimeError('The local service did not become ready. Open Open-Diagnostics.cmd and inspect launcher.log. No data was deleted.')


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except Exception as exc:
        try:
            import traceback
            from nexus.security import redact
            user,_=configure()
            with (user/'logs'/'startup-error.log').open('a',encoding='utf-8') as out:out.write(redact(traceback.format_exc())+'\n')
        except Exception:pass
        message(str(exc), error=True)
        raise SystemExit(1)
