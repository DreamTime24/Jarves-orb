"""Real elapsed-time ASR/model/neural-WAV endurance; no physical device claims."""
import argparse,io,json,math,os,platform,sys,time,wave
from array import array
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,build_opener,ProxyHandler
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nexus.shell import session_parts
from nexus.voice_commands import route
from nexus.storage import uid
def resample_wav(data):
 with wave.open(io.BytesIO(data),'rb') as w:
  if w.getnchannels()!=1 or w.getsampwidth()!=2:raise ValueError('Require mono 16-bit PCM voice')
  rate=w.getframerate();raw=w.readframes(w.getnframes())
 samples=array('h');samples.frombytes(raw)
 if sys.byteorder!='little':samples.byteswap()
 length=math.floor(len(samples)*16000/rate)
 if not 1<=length<=320000:raise ValueError('Fixture must be at most 20 seconds')
 pcm=array('h')
 for i in range(length):
  position=i*rate/16000;left=int(position);fraction=position-left;pcm.append(round(samples[left]*(1-fraction)+samples[min(left+1,len(samples)-1)]*fraction))
 if sys.byteorder!='little':pcm.byteswap()
 out=io.BytesIO()
 with wave.open(out,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(pcm.tobytes())
 return out.getvalue()
def main():
 parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--seconds',type=int,default=86400);parser.add_argument('--interval',type=float,default=300)
 user=Path(os.getenv('LOCALAPPDATA',str(Path.home()/'.local/share')))/'NEXUS'
 parser.add_argument('--session-file',type=Path,default=user/'data/session.json');parser.add_argument('--output',type=Path,default=user/'data/verification/voice-reliability-24h.json');args=parser.parse_args()
 if not 30<=args.seconds<=604800 or not 1<=args.interval<=3600:parser.error('Use 30–604800 seconds and 1–3600 second cycle interval')
 report={'platform':platform.platform(),'started_at':datetime.now(timezone.utc).isoformat(),'requested_seconds':args.seconds,'scope':'Running assistant: actual native imports, HTTP health/SQLite, Piper-generated capital-of-France question -> local ASR -> configured real model -> fresh neural output WAV and actual clock command. No microphone or audible speaker.','cycles':[],'health_samples':0,'max_health_gap_seconds':0,'backend_rss_peak_bytes':None,'resource_errors':[],'errors':[],'state':'starting','passed':False,'24_hour_pass':False,'windows_native_imports_verified':False,'physical_microphone_speaker_verified':False}
 opener=build_opener(ProxyHandler({}));started=None;last_health=None
 def checkpoint(state):
  report['state']=state;report['tested_elapsed_seconds']=round(time.monotonic()-started,3) if started else 0;report['updated_at']=datetime.now(timezone.utc).isoformat();args.output.parent.mkdir(parents=True,exist_ok=True);tmp=args.output.with_suffix('.tmp');tmp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(args.output)
 def api(path,body=None,audio=None,binary=False):
  data=audio if audio is not None else json.dumps(body).encode() if body is not None else None
  headers={'Authorization':'Bearer '+token,'Content-Type':'audio/wav' if audio is not None else 'application/json'}
  with opener.open(Request(base+path,data,headers),timeout=10) as r:data=r.read(20000001 if binary else 128001)
  if len(data)>(20000000 if binary else 128000):raise ValueError('Response too large')
  return data if binary else json.loads(data)
 def health():
  nonlocal last_health
  now=time.monotonic();gap=now-last_health if last_health else 0;last_health=now;report['max_health_gap_seconds']=round(max(report['max_health_gap_seconds'],gap),3)
  if gap>120:raise RuntimeError('Over 120 seconds without health observation; interrupted run cannot pass')
  d=api('/api/diagnostics')
  if not d['health']['worker_alive'] or d['database_integrity']!='ok':raise RuntimeError('Worker or SQLite integrity failed')
  try:
   import psutil
   p=psutil.Process(d['health']['pid']);cmd=p.cmdline()
   if '-m' not in cmd or 'nexus' not in cmd:raise RuntimeError('PID mapping is not the tested NEXUS backend; RSS unavailable')
   report['backend_rss_peak_bytes']=max(report['backend_rss_peak_bytes'] or 0,p.memory_info().rss)
  except Exception as exc:
   note=type(exc).__name__+': '+str(exc)[:200]
   if note not in report['resource_errors']:report['resource_errors'].append(note)
  report['health_samples']+=1
 def wait(path,timeout):
  deadline=time.monotonic()+timeout
  while time.monotonic()<deadline:
   if last_health is None or time.monotonic()-last_health>=30:health();checkpoint('running')
   item=api(path)
   if item['state'] in {'COMPLETED','FAILED','CANCELLED','PAUSED','AWAITING_APPROVAL'}:
    if item['state']!='COMPLETED':raise RuntimeError(item.get('error') or item['state'])
    return item
   time.sleep(.3)
  raise RuntimeError('Operation timed out')
 def job(path,body=None,audio=None):return wait('/api/jobs/'+api(path,body,audio)['job_id'],240)['result']
 def task(text):return wait('/api/tasks/'+api('/api/voice/turn',{'goal':text,'conversation_id':uid(),'mode':'answer'})['id'],360)
 try:
  content=json.loads(args.session_file.read_text());base,token=session_parts(content['url'])
  from nexus.native_setup import probe
  observed=probe();report['native_imports']={'passed':observed.returncode==0,'error':observed.stderr[-1600:]}
  if observed.returncode:raise RuntimeError('Native imports failed; run Retry-Setup.cmd')
  report['windows_native_imports_verified']=os.name=='nt';status=api('/api/status');report['model']=status['model'];report['provider']=status['provider']
  if status['provider']=='disabled' or not status['model']:raise RuntimeError('Prepare a real AI model first')
  fixture=job('/api/voice/speak',{'text':'What is the capital of France?','language':'en'})
  if not fixture.get('audio'):raise RuntimeError('Prepare the local English neural voice first')
  wav=resample_wav(api('/api/audio/'+fixture['audio'],binary=True));started=time.monotonic();last_health=None;next_cycle=0
  print('Actual voice backend test running. Keep NEXUS open and the PC awake. Ctrl+C stops without claiming full-day completion.',flush=True)
  while time.monotonic()-started<args.seconds:
   health();elapsed=time.monotonic()-started
   if elapsed>=next_cycle:
    begin=time.monotonic();stt=job('/api/voice/transcribe?language=en',audio=wav)
    if stt.get('needs_review') or not stt.get('text') or route(stt['text']):raise RuntimeError('Unclear/unexpected knowledge-question transcript; no action executed')
    answer=task(stt['text'])
    if answer['steps'] or not any(name in answer['result'].casefold() for name in ['paris','প্যারিস']):raise RuntimeError('Actual model answer incorrect or replaced by a mapped tool')
    text='Cycle '+str(len(report['cycles'])+1)+'. '+answer['result']
    tts=job('/api/voice/speak',{'text':text,'language':'auto','conversational':True})
    if tts.get('cached') or not tts.get('audio') or not api('/api/audio/'+tts['audio'],binary=True).startswith(b'RIFF'):raise RuntimeError('No fresh valid neural output WAV')
    clock=task('what time is it')
    if not clock['steps'] or clock['steps'][0]['tool']!='system.time' or not json.loads(clock['steps'][0]['result'])['verified']:raise RuntimeError('Actual clock command failed')
    report['cycles'].append({'elapsed':round(elapsed,3),'seconds':round(time.monotonic()-begin,3),'asr_seconds':stt.get('seconds'),'tts_seconds':tts.get('seconds'),'tts_cached':bool(tts.get('cached')),'output_seconds':tts['duration_seconds']});next_cycle=elapsed+args.interval
   checkpoint('running');remaining=args.seconds-(time.monotonic()-started)
   if remaining>0:time.sleep(min(30,remaining,max(.1,next_cycle-(time.monotonic()-started))))
  report['passed']=bool(report['cycles']);report['24_hour_pass']=report['passed'] and args.seconds>=86400 and time.monotonic()-started>=86400
 except KeyboardInterrupt:report['errors'].append('User stopped test; incomplete run')
 except Exception as exc:report['errors'].append(type(exc).__name__+': '+str(exc))
 finally:checkpoint('passed' if report['passed'] else 'failed');print('Report: '+str(args.output),flush=True)
 return 0 if report['passed'] else 1
if __name__=='__main__':raise SystemExit(main())
