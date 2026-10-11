"""Actual source-launcher lifecycle test; does not claim Windows EXE execution."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from urllib.request import Request,urlopen

ROOT=Path(__file__).resolve().parents[1]

def call(url,token,path,body=None):
    data=json.dumps(body).encode() if body is not None else None
    request=Request(url+path,data,{'Authorization':'Bearer '+token,**({'Content-Type':'application/json'} if data is not None else {})})
    with urlopen(request,timeout=5) as response:return json.load(response)

def main():
    checks=[]
    with tempfile.TemporaryDirectory(prefix='nexus-lifecycle-') as directory:
        root=Path(directory);env=os.environ.copy();env.update(NEXUS_DATA=str(root/'data'),NEXUS_WORKSPACE=str(root/'workspace'),AI_PROVIDER='disabled',AI_MODEL='',NEXUS_AUTO_SETUP='0',PYTHONUTF8='1')
        for attempt in range(2):
            with (root/'launcher.log').open('ab') as log:
                process=subprocess.Popen([sys.executable,'-m','nexus.supervisor','--no-browser'],cwd=ROOT,env=env,stdout=log,stderr=log)
            try:
                path=root/'data'/'session.json';deadline=time.monotonic()+20;session=None
                while time.monotonic()<deadline:
                    if process.poll() is not None:raise RuntimeError('Supervisor exited: '+(root/'launcher.log').read_text())
                    try:
                        session=json.loads(path.read_text());base,token=session['url'].split('/#token=');health=call(base,token,'/api/health')
                        if health['worker_alive']:break
                    except (OSError,ValueError):pass
                    time.sleep(.1)
                else:raise RuntimeError('No authenticated live session')
                duplicate=subprocess.run([sys.executable,'-m','nexus','--no-browser'],cwd=ROOT,env=env,capture_output=True,timeout=15,text=True)
                assert duplicate.returncode==3,duplicate.stdout+duplicate.stderr
                task=call(base,token,'/api/voice/turn',{'goal':'time bolo','conversation_id':'f'*32})['id'];deadline=time.monotonic()+10
                while time.monotonic()<deadline:
                    record=call(base,token,'/api/tasks/'+task)
                    if record['state']=='COMPLETED':break
                    if record['state']=='FAILED':raise RuntimeError(record['error'])
                    time.sleep(.1)
                assert record['state']=='COMPLETED'
                evidence=json.loads(record['steps'][0]['result']);assert evidence['verified']
                call(base,token,'/api/system/shutdown',{})
                assert process.wait(timeout=20)==0
                assert not path.exists(),'Owned private session was not released'
                checks.append({'launch':attempt+1,'authenticated_health':True,'duplicate_exit':duplicate.returncode,'clock_executed':True,'normal_shutdown_exit':0,'session_removed':True})
            finally:
                if process.poll() is None:process.kill();process.wait()
    report={'platform':sys.platform,'passed':True,'checks':checks,'scope':'Real source supervisor, authenticated HTTP, single-instance lock, clock, shutdown and reopen; Windows PE/UI/hardware not executed'}
    (ROOT/'docs'/'lifecycle-measured.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))

if __name__=='__main__':main()
