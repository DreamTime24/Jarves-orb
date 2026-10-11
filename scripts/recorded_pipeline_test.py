"""Linux CPU acceptance using externally downloaded real models and recorded fixtures."""
import argparse,io,json,os,platform,re,resource,subprocess,sys,tempfile,threading,time,unicodedata,wave
from pathlib import Path
from urllib.request import Request,build_opener,ProxyHandler
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--assets',type=Path,required=True);p.add_argument('--soak-seconds',type=int,default=60);p.add_argument('--model-file',default='Qwen2.5-7B-Q4_K_M.gguf');p.add_argument('--model-label',default='Qwen2.5-7B');args=p.parse_args();A=args.assets.resolve();sys.path.insert(0,str(ROOT))
os.environ.update(STT_MODEL_DIR=str(A/'models/whisper-small'),STT_BENGALI_MODEL_DIR=str(A/'models/whisper-large-v3'),TTS_MODEL_DIR=str(A/'models/piper'),HF_HUB_OFFLINE='1')
from nexus.config import Config
from nexus.server import Application,LocalServer
from nexus.conversation import DEFAULT_PROFILE
from nexus.shell import publish_session
import numpy as np,av,onnxruntime
onnxruntime.disable_telemetry_events()
opener=build_opener(ProxyHandler({}));app=None;server=None;proc=None
report={'platform':platform.platform(),'model':args.model_label+' Q4_K_M, official Ollama layer','bengali_asr':'Systran/faster-whisper-large-v3 / CPU int8','asr_max_new_tokens':400,'cpu_only':True,'runtime':'Official llama.cpp b11429, real local HTTP provider','scope':'Prerecorded human English JFK and first three bounded FLEURS Bengali dev clips; synthetic neural question -> actual ASR -> actual model -> neural WAV; text follow-ups and clock. No provider/audio stubs. No physical mic/speaker, Windows executable or 24h acceptance.','windows_native_verified':False,'physical_devices_verified':False,'24_hour_pass':False,'cases':[],'passed':False}
def checkpoint():
 dest=ROOT/'docs/real-pipeline-05.json';tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');tmp.replace(dest)
def pcm(path):
 resampler=av.AudioResampler(format='s16',layout='mono',rate=16000);chunks=[]
 with av.open(str(path)) as c:
  for frame in c.decode(audio=0):
   for out in resampler.resample(frame):chunks.append(out.to_ndarray().tobytes())
  for out in resampler.resample(None):chunks.append(out.to_ndarray().tobytes())
 samples=np.frombuffer(b''.join(chunks),dtype='<i2');assert 1<=len(samples)<=320000
 stream=io.BytesIO()
 with wave.open(stream,'wb') as w:w.setnchannels(1);w.setsampwidth(2);w.setframerate(16000);w.writeframes(samples.tobytes())
 return stream.getvalue()
def api(path,body=None,audio=None):
 data=audio if audio is not None else json.dumps(body).encode() if body is not None else None
 with opener.open(Request(base+path,data,{'Authorization':'Bearer '+app.token,'Content-Type':'audio/wav' if audio is not None else 'application/json'}),timeout=15) as r:return json.load(r)
def wait(path):
 deadline=time.monotonic()+300
 while time.monotonic()<deadline:
  item=api(path)
  if item['state'] in {'COMPLETED','FAILED','CANCELLED','AWAITING_APPROVAL'}:
   if item['state']!='COMPLETED':raise RuntimeError(item.get('error') or item['state'])
   return item
  time.sleep(.15)
 raise RuntimeError('Operation timeout')
def job(path,body=None,audio=None):return wait('/api/jobs/'+api(path,body,audio)['job_id'])['result']
def turn(goal,session):return wait('/api/tasks/'+api('/api/voice/turn',{'goal':goal,'conversation_id':session,'mode':'answer'})['id'])
def words(text):return re.sub(r'[^\w\s\u0980-\u09ff]','',unicodedata.normalize('NFC',text)).casefold().split()
def wer(expected,observed):
 a,b=words(expected),words(observed);row=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  new=[i]
  for j,y in enumerate(b,1):new.append(min(new[-1]+1,row[j]+1,row[j-1]+(x!=y)))
  row=new
 return round(row[-1]/max(1,len(a)),4)
def case(value):report['cases'].append(value);checkpoint();print(value['case'],value['passed'],flush=True)
try:
 log=(A/'pipeline-model.log').open('w')
 proc=subprocess.Popen([str(A/'llama/llama-b11429/llama-server'),'-m',str(A/args.model_file),'--host','127.0.0.1','--port','11865','--threads','4','--threads-batch','4','--ctx-size','4096','--n-gpu-layers','0','--parallel','1','--jinja','--reasoning','off'],stdout=log,stderr=subprocess.STDOUT)
 deadline=time.monotonic()+60
 while True:
  try:
   with opener.open('http://127.0.0.1:11865/health',timeout=2) as r:assert json.load(r)['status']=='ok'
   break
  except Exception:
   if proc.poll() is not None or time.monotonic()>deadline:raise RuntimeError('Real model server did not start; inspect external model log')
   time.sleep(.2)
 with tempfile.TemporaryDirectory(prefix='nexus-recorded-') as d:
  app=Application(Config(data=Path(d)/'data',workspace=Path(d)/'workspace',provider='openai-compatible',base_url='http://127.0.0.1:11865/v1',model=args.model_label+'-real',timeout=240));app.engine.start();server=LocalServer(app,0);threading.Thread(target=server.serve_forever,daemon=True).start();base='http://127.0.0.1:'+str(server.server_port)
  app.post('/api/voice/profile',{**DEFAULT_PROFILE,'language':'en'})
  expected='And so my fellow Americans, ask not what your country can do for you, ask what you can do for your country.';stt=job('/api/voice/transcribe?language=en',audio=pcm(A/'jfk.flac'));case({'case':'human_english_ASR','expected':expected,'result':stt,'word_error_rate':wer(expected,stt['text']),'passed':wer(expected,stt['text'])==0,'source':'https://github.com/SYSTRAN/faster-whisper/blob/master/tests/data/jfk.flac'})
  fixture=job('/api/voice/speak',{'text':'What is the capital of France?','language':'en'});heard=job('/api/voice/transcribe?language=en',audio=pcm(app.voice.audio_folder/fixture['audio']));start=time.monotonic();task=turn(heard['text'],'a'*32);speech=job('/api/voice/speak',{'text':task['result'],'language':'en','conversational':True});(ROOT/'docs/Voice-English-05.wav').write_bytes((app.voice.audio_folder/speech['audio']).read_bytes());case({'case':'synthetic_question_full_real_pipeline','input_kind':'Piper input, not physical microphone','asr':heard,'answer':task['result'],'speech':speech,'seconds_after_asr':round(time.monotonic()-start,3),'passed':not task['steps'] and 'paris' in task['result'].casefold(),'engine':'real_model'})
  task=turn('Which river flows through that city? Answer briefly.','a'*32);case({'case':'real_model_english_followup','answer':task['result'],'passed':not task['steps'] and 'seine' in task['result'].casefold()})
  app.post('/api/voice/profile',DEFAULT_PROFILE)
  for goal,expected in [('বারো গুণ তেরো কত? এক বাক্যে উত্তর দাও।',('156','১৫৬','ছাপ্পান্ন')),('ওই ফলকে বারো দিয়ে ভাগ করলে কত হবে?',('13','১৩','তেরো')),('bro ami porashona korte mon dite pari na, choto ekta practical tip dao',('মিনিট','টাইমার','বিরতি','ছোট','সময়','সময়','Pomodoro'))]:
   task=turn(goal,'b'*32);case({'case':'bengali_or_banglish_answer','input':goal,'answer':task['result'],'passed':any(s in task['result'] for s in expected),'engine':'bounded_calculator' if task['steps'] and task['steps'][0]['tool']=='math.calculate' else 'real_model','scope':'Arithmetic uses the observed mapped calculator when supported; model study-tip keywords are a limited relevance check, not human naturalness acceptance'})
  for goal,markers in [('পড়ার মনোযোগের জন্য ২৫ মিনিট পড়া আর ৫ মিনিট বিরতি কীভাবে ব্যবহার করব?',('২৫','25')),('ওই বিরতিতে ফোন না দেখে আর কী করতে পারি?',('হাঁট','পানি','স্ট্রেচ','ব্যায়াম','ব্যায়াম','বিশ্রাম'))]:
   task=turn(goal,'e'*32);case({'case':'real_model_bengali_study_followup','input':goal,'answer':task['result'],'passed':not task['steps'] and any(s in task['result'] for s in markers),'scope':'Real model answer and session history. Keyword check is limited; read the stored answers to judge context and quality.'})
  labels={line.split('\t')[1]:line.split('\t')[3] for line in (A/'fleurs-bn/dev.tsv').read_text().splitlines()}
  for name in json.loads((A/'fleurs-bn/clips.json').read_text()):
   stt=job('/api/voice/transcribe?language=bn',audio=pcm(A/'fleurs-bn'/name));error=wer(labels[name],stt['text']);case({'case':'human_bengali_ASR','clip':name,'expected':labels[name],'result':stt,'word_error_rate':error,'acceptance':'WER <= 0.25 chosen before this run. Three clips do not establish general Bengali/Banglish accuracy.','source':'https://huggingface.co/datasets/google/fleurs/tree/main/data/bn_in','dataset_license':'CC BY 4.0','passed':error<=.25})
  task=turn('এখন কয়টা বাজে','c'*32);speech=job('/api/voice/speak',{'text':task['result'],'language':'bn','conversational':True});(ROOT/'docs/Voice-Bengali-05.wav').write_bytes((app.voice.audio_folder/speech['audio']).read_bytes());case({'case':'actual_clock_and_neural_bengali_audio','answer':task['result'],'speech':speech,'passed':task['steps'][0]['tool']=='system.time' and json.loads(task['steps'][0]['result'])['verified']})
  if args.soak_seconds:
   descriptor=publish_session(app.config.data,base+'/#token='+app.token);app.post('/api/voice/profile',{**DEFAULT_PROFILE,'language':'en'});run=subprocess.run([sys.executable,str(ROOT/'scripts/voice_soak.py'),'--seconds',str(args.soak_seconds),'--interval','15','--session-file',str(descriptor),'--output',str(ROOT/'docs/voice-reliability-05-smoke.json')],timeout=args.soak_seconds+360);case({'case':'real_voice_endurance_runner','passed':run.returncode==0,'report':'voice-reliability-05-smoke.json'})
  ticket=app.voice.ticket();app.voice.stop()
  try:app.voice.speak('Stopped reply','en',lambda _:None,ticket=ticket);stopped=False
  except ValueError:stopped=True
  case({'case':'actual_stale_speech_ticket_rejected_after_stop','passed':stopped})
  proc.terminate();proc.wait(timeout=10);tid=api('/api/voice/turn',{'goal':'Explain a parallel circuit briefly.','conversation_id':'d'*32,'mode':'answer'})['id'];deadline=time.monotonic()+30
  while api('/api/tasks/'+tid)['state'] not in {'FAILED','COMPLETED'} and time.monotonic()<deadline:time.sleep(.2)
  observed=api('/api/tasks/'+tid);case({'case':'real_model_service_unavailable','state':observed['state'],'error':observed['error'],'passed':observed['state']=='FAILED' and not observed['result']})
  report['model_runs']=app.store.rows('SELECT model,elapsed_seconds,success FROM model_runs');app.engine.close();app.voice.stop();app.jobs.close();server.shutdown();server.server_close();app=None;server=None
 report['passed']=all(c['passed'] for c in report['cases'])
except Exception as exc:
 import traceback
 report['error']=type(exc).__name__+': '+str(exc);report['traceback']=traceback.format_exc()
finally:
 if app:app.engine.close();app.voice.stop();app.jobs.close()
 if server:server.shutdown();server.server_close()
 if proc and proc.poll() is None:proc.terminate();proc.wait(timeout=10)
 report['self_peak_rss_bytes']=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024;report['state']='passed' if report['passed'] else 'failed';checkpoint();print('Final recorded pipeline:',report['state'],flush=True)

raise SystemExit(0 if report["passed"] else 1)
