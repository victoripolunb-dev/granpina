import json, os, sys, time
from pathlib import Path

config=json.loads(Path('.gran-ambiente.json').read_text(encoding='utf-8'))
os.environ['HF_HUB_OFFLINE']='1'
sys.path.insert(0,config['transcritor'])
from faster_whisper import WhisperModel, BatchedInferencePipeline
model=WhisperModel(config['modelo'],device='cpu',compute_type='int8',cpu_threads=4,local_files_only=True)
audio=next((Path.home()/'Downloads').glob('Planejamento Conservacionista II.mp3'))
segments, info=BatchedInferencePipeline(model=model).transcribe(str(audio),language='pt',beam_size=1,batch_size=4,chunk_length=20)
print('duration',info.duration,flush=True)
base=Path('planejamento-ii')
collected=[]
with (base/'audio-lote.ndjson').open('w',encoding='utf-8') as out:
 for s in segments:
  v=dict(inicio_segundos=s.start,fim_segundos=s.end,texto=s.text.strip(),probabilidade_sem_fala=s.no_speech_prob)
  collected.append(v)
  out.write(json.dumps(v,ensure_ascii=False)+'\n')
  out.flush()
  if len(collected)%20==0: print('progress',s.end,flush=True)
(base/'audio-lote.json').write_text(json.dumps(dict(arquivo=audio.name,duracao_segundos=info.duration,idioma=info.language,segmentos=collected),ensure_ascii=False),encoding='utf-8')
