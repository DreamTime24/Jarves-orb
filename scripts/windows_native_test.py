"""Actual Windows executable/native window acceptance; no simulated devices."""
import json,os,platform,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nexus.shell import read_session,session_request
def main():
 report={'platform':platform.platform(),'scope':'Actual bundled executable, native app controls, duplicate reuse and close/reopen. No physical microphone, audible speaker or 24h test.','passed':False,'native_windows_verified':False,'checks':{},'errors':[]}
 descriptor=None
 def wait(data):
  deadline=time.monotonic()+45
  while time.monotonic()<deadline:
   item=read_session(data)
   if item and session_request(item['url'],'/api/status')['window']['native_controls']:return item
   time.sleep(.3)
  raise RuntimeError('Native app window did not become available')
 try:
  if os.name!='nt':raise RuntimeError('Requires actual Windows; native execution is not verified here')
  with tempfile.TemporaryDirectory(prefix='nexus-native-',ignore_cleanup_errors=True) as directory:
   env=os.environ.copy();env.update(LOCALAPPDATA=directory,NEXUS_DATA=str(Path(directory)/'NEXUS/data'),NEXUS_WORKSPACE=str(Path(directory)/'workspace'),NEXUS_PORT='18765',NEXUS_AUTO_SETUP='0');data=Path(env['NEXUS_DATA'])
   def launch():
    run=subprocess.run([str(ROOT/'NEXUS.exe'),'--no-setup'],cwd=ROOT,env=env,timeout=45)
    if run.returncode:raise RuntimeError('Executable returned '+str(run.returncode))
   try:
    launch();descriptor=wait(data);original=descriptor['pid'];report['checks']['portable_executable_native_window']=True
    launch();again=read_session(data)
    if not again or again['pid']!=original:raise RuntimeError('Duplicate launcher did not reuse backend')
    if not session_request(descriptor['url'],'/api/ui/open',{'mode':'app'}).get('reused_window'):raise RuntimeError('Existing native window was not reused')
    report['checks']['duplicate_reuses_backend_and_window']=True
    if not session_request(descriptor['url'],'/api/ui/window',{'action':'minimize'}).get('performed'):raise RuntimeError('Native minimize failed')
    report['checks']['native_minimize_requested']=True;session_request(descriptor['url'],'/api/ui/open',{'mode':'app'})
    if not session_request(descriptor['url'],'/api/ui/window',{'action':'topmost','value':True}).get('always_on_top'):raise RuntimeError('Native topmost failed')
    session_request(descriptor['url'],'/api/ui/window',{'action':'topmost','value':False});report['checks']['native_topmost_calls']=True
    session_request(descriptor['url'],'/api/system/shutdown',{});deadline=time.monotonic()+15
    while (data/'session.json').exists() and time.monotonic()<deadline:time.sleep(.2)
    if (data/'session.json').exists():raise RuntimeError('Closed backend retained session descriptor')
    descriptor=None;report['checks']['shutdown_cleanup']=True;launch();descriptor=wait(data);report['checks']['reopened_new_backend']=descriptor['pid']!=original
    report['passed']=all(report['checks'].values());report['native_windows_verified']=report['passed']
   finally:
    if descriptor:
     try:session_request(descriptor['url'],'/api/system/shutdown',{})
     except Exception:pass
     deadline=time.monotonic()+15
     while (data/'session.json').exists() and time.monotonic()<deadline:time.sleep(.2)
 except Exception as exc:report['errors'].append(type(exc).__name__+': '+str(exc))
 (ROOT/'docs/windows-native-acceptance.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2));return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
