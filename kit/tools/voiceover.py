"""Make a voiceover track and mux it onto a silent video.
Usage: python3 tools/voiceover.py script.json silent.mp4 out.mp4
script.json: {"voice":"af_heart","lines":[{"start":0.25,"text":"..."}, ...]}
Voices: af_heart (warm female, default), am_michael (male). Model files download once to ~/.kokoro.
Each line must finish before the next starts: ~2.6 words/sec at speed 1.08."""
import sys, os, json, subprocess, numpy as np, soundfile as sf
D=os.path.expanduser('~/.kokoro'); os.makedirs(D,exist_ok=True)
for f,u in [('kokoro.onnx','https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx'),
            ('voices.bin','https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin')]:
    if not os.path.exists(f'{D}/{f}'): subprocess.run(['curl','-sSL','-o',f'{D}/{f}',u],check=True)
from kokoro_onnx import Kokoro
spec=json.load(open(sys.argv[1])); vid=sys.argv[2]; out=sys.argv[3]
dur=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',vid]).decode())
k=Kokoro(f'{D}/kokoro.onnx',f'{D}/voices.bin'); SR=48000
mix=np.zeros(int(SR*dur)+SR)
for ln in spec['lines']:
    a,sr=k.create(ln['text'],voice=spec.get('voice','af_heart'),speed=spec.get('speed',1.08),lang='en-us')
    a=np.interp(np.arange(0,len(a),sr/SR),np.arange(len(a)),a)
    s=int(ln['start']*SR); e=min(len(mix),s+len(a)); mix[s:e]+=a[:e-s]
    end=ln['start']+len(a)/SR
    if end>dur: print(f'WARNING line ends at {end:.2f}s after video end {dur:.2f}s: {ln["text"]}')
    print(f"{ln['start']:.2f}-{end:.2f}s  {ln['text']}")
t=np.arange(len(mix))/SR; pad=np.zeros(len(mix))
for i,f in enumerate([87.31,130.81,174.61,220.0,261.63,329.63]):
    for det in (-0.6,0.6): pad+=np.sin(2*np.pi*(f+det)*t+i)*(0.9 if f<200 else 0.5)
pad*=(0.75+0.25*np.sin(2*np.pi*0.18*t))*np.clip(t/2.5,0,1)*np.clip((dur-t)/1.5,0,1)
pad=np.convolve(pad,np.ones(40)/40,mode='same'); pad/=np.abs(pad).max()
mix=mix/max(np.abs(mix).max(),1e-6)*0.8+pad*0.8*10**(-25/20)
sf.write('/tmp/vo_raw.wav',mix[:int(SR*dur)].astype(np.float32),SR)
subprocess.run(['ffmpeg','-v','error','-y','-i','/tmp/vo_raw.wav','-af','highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9','-ac','2','-ar','48000','/tmp/vo.wav'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-i',vid,'-i','/tmp/vo.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out+'.tmp.mp4'],check=True)
os.replace(out+'.tmp.mp4',out); print('ok',out)
