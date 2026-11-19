import json
import re
from pathlib import Path

from difflib import SequenceMatcher

def tokens(text):
    return re.findall(r'[^\W_]+',text.casefold())

def seconds(stamp):
    hours, minutes, tail = stamp.replace(',', '.').split(':')
    return int(hours)*3600+int(minutes)*60+float(tail)

base=Path(__file__).parent
raw=(base/'legenda.txt').read_text(encoding='utf-8')
parts=re.split(r'(?m)^(\d\d:\d\d:\d\d,\d+) --> (\d\d:\d\d:\d\d,\d+)\s*',raw)
cues=[]
for start,end,text in zip(parts[1::3],parts[2::3],parts[3::3]):
    text=re.split(r'\n\s*(?:\d+\s*$|===|Powered by)',text,flags=re.M)[0]
    text=re.sub(r'(?m)^\s*\d+ / 33\s*$','',text)
    cues.append((seconds(start),seconds(end),' '.join(text.split())))
asr=json.loads((base/'audio.json').read_text(encoding='utf-8'))
segments=asr['segmentos']
print('duracao',asr['duracao_segundos'],'legenda',len(cues),cues[-1][:2],'asr',len(segments),segments[-1])
for start in range(0,int(asr['duracao_segundos']),300):
    end=min(start+300,asr['duracao_segundos'])
    caption=' '.join(c for a,b,c in cues if start<=a<end)
    audio=' '.join(s['texto'] for s in segments if start<=s['inicio_segundos']<end)
    ratio=SequenceMatcher(None,tokens(caption),tokens(audio),autojunk=False).ratio()
    print(f'{start/60:02.0f}–{end/60:.2f}: {len(tokens(caption))} / {len(tokens(audio))} palavras; correspondência lexical {ratio:.1%}')
for i,s in enumerate(segments):
    if i>0 and s['inicio_segundos']-segments[i-1]['fim_segundos']>2.5:
        print('lacuna ASR',segments[i-1]['fim_segundos'],s['inicio_segundos'])
    print(f"{s['inicio_segundos']:07.2f}–{s['fim_segundos']:07.2f}: {s['texto']}")
