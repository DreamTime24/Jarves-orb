"""Runs automatable Windows checks, then visibly records device/UI checks still requiring observation."""
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[1]
def main():
    if os.name!='nt':print('This acceptance runner requires Windows.');return 1
    os.environ['ORT_DISABLE_TELEMETRY']='1';os.environ['HF_HUB_DISABLE_TELEMETRY']='1'
    result={'platform':platform.platform(),'python':platform.python_version(),'tested_at':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'automated':{},'manual':{},'full_acceptance_passed':False}
    for name,command in [('native_imports',[sys.executable,'-c',"import onnxruntime; onnxruntime.disable_telemetry_events(); import numpy, ctranslate2, piper, av"]),('portable_exe_native_window',[sys.executable,'scripts/windows_native_test.py']),('unit',[sys.executable,'-m','unittest','discover','-s','tests','-v']),('launcher_lifecycle',[sys.executable,'scripts/lifecycle_test.py']),('restart_smoke',[sys.executable,'scripts/soak.py','--seconds','60','--interval','2','--output','docs/windows-restart.json'])]:
        run=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8',errors='replace')
        result['automated'][name]={'passed':run.returncode==0,'output':run.stdout[-16000:]}
    for check in ['Fresh full extraction -> NEXUS.exe -> compact orb; actual first setup succeeds','Windows app close/minimize/drag/topmost, no duplicate window, close and reopen work','Microphone Allow/denial/missing device -> visible error -> retry and text fallback','Bengali/English/Banglish human question, accurate transcript and contextual follow-up','Continuous and push-to-talk; own output never recaptured; Stop/mute and spoken stop while listening','Bengali/English neural reply is audible; voice choice and speed work','Clock command gives actual time; confirmed Notepad opens; failed/unsupported command never says completed','Unavailable model/service shows error and detailed log','Full 24-hour backend runner passes (does not prove native voice/model load reliability)','Test-Voice-24h.cmd: full 86400-second real ASR/model/neural-WAV report passes (no physical device proof)']:
        answer=input(check+' [pass/fail/not tested]: ').strip().lower()
        result['manual'][check]=answer if answer in {'pass','fail'} else 'not tested'
    result['full_acceptance_passed']=all(v['passed'] for v in result['automated'].values()) and all(v=='pass' for v in result['manual'].values())
    (ROOT/'docs/windows-acceptance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Saved docs/windows-acceptance.json. Manual observations are labeled and never inferred.');return 0 if result['full_acceptance_passed'] else 1

if __name__=='__main__':sys.exit(main())
