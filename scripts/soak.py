"""Real elapsed-time backend reliability test in disposable data; never labels short runs 24h."""
import argparse
import json
import os
from pathlib import Path
import platform
import queue
import re
import socket
import subprocess
import sys
import tempfile
import threading
import time
from urllib.request import Request,build_opener,ProxyHandler

ROOT=Path(__file__).resolve().parents[1]

def start(root):
    with socket.socket() as sock:sock.bind(('127.0.0.1',0));port=sock.getsockname()[1]
    env=os.environ.copy();env.update(NEXUS_DATA=str(root/'data'),NEXUS_WORKSPACE=str(root/'workspace'),NEXUS_PORT=str(port),AI_PROVIDER='disabled',PYTHONUTF8='1')
    proc=subprocess.Popen([sys.executable,'-u','-m','nexus','--no-browser'],cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,encoding='utf-8')
    lines=queue.Queue()
    def reader():
        for line in proc.stdout:lines.put(line)
    threading.Thread(target=reader,daemon=True).start();deadline=time.monotonic()+20
    while time.monotonic()<deadline:
        try:line=lines.get(timeout=.5)
        except queue.Empty:
            if proc.poll() is not None:raise RuntimeError('Backend exited during startup')
            continue
        match=re.search(r'(http://127\.0\.0\.1:\d+)/#token=([\w-]+)',line)
        if match:return proc,match.group(1),match.group(2)
    proc.kill();raise RuntimeError('Backend did not expose a session URL in 20 seconds')

def api(base,token,path,body=None):
    data=None if body is None else json.dumps(body).encode()
    req=Request(base+path,data,{'Authorization':'Bearer '+token,**({'Content-Type':'application/json'} if data else {})})
    with build_opener(ProxyHandler({})).open(req,timeout=10) as response:return json.loads(response.read())

def finish(proc):
    if proc and proc.poll() is None:
        proc.terminate()
        try:proc.wait(timeout=5)
        except subprocess.TimeoutExpired:proc.kill();proc.wait(timeout=5)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--seconds',type=int,default=86400);parser.add_argument('--interval',type=float,default=30);parser.add_argument('--output',default='docs/reliability-24h.json');args=parser.parse_args()
    if not 5<=args.seconds<=604800 or not .2<=args.interval<=60:parser.error('Use 5–604800 seconds and 0.2–60 second interval')
    report={'platform':platform.system(),'requested_seconds':args.seconds,'scope':'Disposable backend, HTTP health, SQLite, memory/task persistence, two forced process restarts; no native UI/model/microphone/speaker load',
            'samples':0,'forced_restarts':0,'errors':[],'resource_errors':[],'rss_peak_bytes':None,'24_hour_pass':False,'passed':False}
    proc=None;started=time.monotonic()
    def checkpoint(state):
        report['state']=state;report['actual_elapsed_seconds']=round(time.monotonic()-started,3)
        output=Path(args.output);output.parent.mkdir(parents=True,exist_ok=True)
        temporary=output.with_suffix('.tmp');temporary.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');temporary.replace(output)
    try:
        with tempfile.TemporaryDirectory(prefix='nexus-soak-') as directory:
            root=Path(directory);proc,base,token=start(root)
            mid=api(base,token,'/api/memory',{'content':'Reliability checkpoint fixture','category':'project'})['id']
            tid=api(base,token,'/api/tools/execute',{'tool':'game.solve','arguments':{}})['id']
            deadline=time.monotonic()+15
            while api(base,token,'/api/tasks/'+tid)['state']!='COMPLETED':
                if time.monotonic()>deadline:raise RuntimeError('Maze task failed to finish')
                time.sleep(.1)
            targets=[args.seconds/3,args.seconds*2/3]
            while time.monotonic()-started<args.seconds:
                health=api(base,token,'/api/health');d=api(base,token,'/api/diagnostics')
                if not health['worker_alive'] or d['database_integrity']!='ok':raise RuntimeError('Worker or database health failed')
                if api(base,token,'/api/tasks/'+tid)['state']!='COMPLETED':raise RuntimeError('Completed task checkpoint was lost')
                if not any(m['id']==mid for m in api(base,token,'/api/memory?q=Reliability')):raise RuntimeError('Memory checkpoint was lost')
                report['samples']+=1
                try:
                    import psutil
                    process=psutil.Process(proc.pid)
                    command=process.cmdline()
                    if '-m' not in command or 'nexus' not in command:raise RuntimeError('PID mapping is not the tested backend')
                    rss=process.memory_info().rss;report['rss_peak_bytes']=max(report['rss_peak_bytes'] or 0,rss)
                except Exception as exc:
                    note=type(exc).__name__+': '+str(exc)[:200]
                    if note not in report['resource_errors']:report['resource_errors'].append(note)
                elapsed=time.monotonic()-started
                if targets and elapsed>=targets[0]:
                    targets.pop(0);proc.kill();proc.wait(timeout=5)
                    proc,base,token=start(root);report['forced_restarts']+=1
                checkpoint('running')
                remaining=args.seconds-(time.monotonic()-started)
                if remaining>0:time.sleep(min(args.interval,remaining))
            report['passed']=report['samples']>=1 and report['forced_restarts']==2
    except KeyboardInterrupt:report['errors'].append('User stopped the test; incomplete run')
    except Exception as exc:report['errors'].append(type(exc).__name__+': '+str(exc))
    finally:
        finish(proc);report['actual_elapsed_seconds']=round(time.monotonic()-started,3)
        report['24_hour_pass']=report['passed'] and args.seconds>=86400 and report['actual_elapsed_seconds']>=86400
        checkpoint('passed' if report['passed'] else 'failed')
        print(json.dumps(report,indent=2));return 0 if report['passed'] else 1

if __name__=='__main__':sys.exit(main())
