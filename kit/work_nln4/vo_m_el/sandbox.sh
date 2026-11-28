cat > /workspace/edit.json <<'EOF_EDIT'
{"dur": 28.94, "segs": [{"src0": 0.0, "src1": 13.26, "out0": 0.25}, {"src0": 13.26, "src1": 15.16, "out0": 14.01}, {"src0": 15.16, "src1": 27.56, "out0": 16.01}], "loud": [[14.07, 15.79]], "cues": [{"t": 0.15, "sfx": "swoosh", "id": "Got"}, {"t": 0.57, "sfx": "tick", "id": "countdown"}, {"t": 2.13, "sfx": "whoosh", "id": "Picture"}, {"t": 4.41, "sfx": "tick", "id": "ten"}, {"t": 6.41, "sfx": "swoosh", "id": "tomorrow"}, {"t": 9.61, "sfx": "error", "id": "Again"}, {"t": 11.25, "sfx": "pop", "id": "trust"}, {"t": 12.73, "sfx": "error", "id": "prices"}, {"t": 14.11, "sfx": "whoosh", "id": "Want"}, {"t": 15.51, "sfx": "ding", "id": "how"}, {"t": 18.21, "sfx": "pop", "id": "real"}, {"t": 19.85, "sfx": "ding", "id": "date"}, {"t": 23.01, "sfx": "pop", "id": "back"}, {"t": 24.93, "sfx": "ding", "id": "trust"}, {"t": 27.57, "sfx": "pop", "id": "GROWTH"}]}
EOF_EDIT
cat > /workspace/mix.py <<'EOF_PY'

import json, subprocess, re, numpy as np, soundfile as sf
SR = 48000; E = json.loads(open('/workspace/edit.json').read())
subprocess.run(['ffmpeg','-v','error','-y','-i','/workspace/in/voice.mp3','-ac','1','-ar',str(SR),'/workspace/v.wav'],check=True)
a, _ = sf.read('/workspace/v.wav'); a = a.astype(np.float64)
vd = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','/workspace/in/silent.mp4']).decode())
assert abs(vd - E['dur']) < 0.15, f'silent video is {vd:.2f}s but the plan is {E["dur"]}s'
n = int(vd * SR); v = np.zeros(n + SR)
for s in E['segs']:
    seg = a[int(s['src0']*SR):int(s['src1']*SR)].copy(); r = min(int(0.012*SR), len(seg)//2)
    if r: seg[:r] *= np.linspace(0,1,r); seg[-r:] *= np.linspace(1,0,r)
    o = int(s['out0']*SR); e = min(len(v), o+len(seg)); v[o:e] += seg[:e-o]
v = v[:n]
g = np.ones(n); rp = int(0.04*SR)
for x0, x1 in E['loud']:
    s0, s1 = max(0,int(x0*SR)), min(n,int(x1*SR)); seg = np.ones(s1-s0)*10**(4.5/20); r = min(rp, len(seg)//2)
    if r: seg[:r] = np.linspace(1,seg[0],r); seg[-r:] = np.linspace(seg[0],1,r)
    g[s0:s1] = seg
v = v*g; mixd = v/max(np.abs(v).max(),1e-6)*0.8
def sfx(kind):
    r = np.random.default_rng(7)
    def env(d,a=0.003,k=30): tt=np.arange(int(d*SR))/SR; return tt, np.clip(tt/a,0,1)*np.exp(-k*tt)
    if kind=='tick': tt,e=env(0.06,0.001,70); y=np.sin(2*np.pi*2600*tt)*e*0.55
    elif kind=='pop': tt,e=env(0.12,0.002,38); f=520+500*np.exp(-30*tt); y=np.sin(2*np.pi*np.cumsum(f)/SR)*e*0.45
    elif kind=='tap': tt,e=env(0.05,0.001,90); y=(np.sin(2*np.pi*1500*tt)*0.5+r.normal(0,.3,len(tt)))*e*0.5
    elif kind=='whoosh':
        tt=np.arange(int(0.45*SR))/SR; nz=np.convolve(r.normal(0,1,len(tt)),np.ones(30)/30,'same'); y=nz*np.sin(np.pi*tt/0.45)**2*0.35
    elif kind=='swoosh':
        tt=np.arange(int(0.25*SR))/SR; nz=np.convolve(r.normal(0,1,len(tt)),np.ones(12)/12,'same'); y=nz*np.sin(np.pi*tt/0.25)**2*0.28
    elif kind=='ding': tt,e=env(0.6,0.003,6); y=(np.sin(2*np.pi*1318.5*tt)+.5*np.sin(2*np.pi*1975.5*tt))*e*0.3
    elif kind=='error': tt,e=env(0.28,0.003,9); y=np.sign(np.sin(2*np.pi*170*tt))*e*0.12
    elif kind=='type': y=np.concatenate([sfx('tap')*0.4,np.zeros(int(0.06*SR))]*3)
    return y
fx = np.zeros(n)
for c in E['cues']:
    y = sfx(c['sfx']); s0 = int(c['t']*SR); e = min(n, s0+len(y))
    if 0 <= s0 < n: fx[s0:e] += y[:e-s0]
mixd += fx*0.6
sf.write('/workspace/raw.wav', mixd.astype(np.float32), SR)
subprocess.run(['ffmpeg','-v','error','-y','-i','/workspace/raw.wav','-af','highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,loudnorm=I=-13.5:TP=-1.0:LRA=8','-ac','2','-ar','48000','/workspace/vo.wav'],check=True)
meas = subprocess.run(['ffmpeg','-i','/workspace/vo.wav','-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr
I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', meas)[-1])
subprocess.run(['ffmpeg','-v','error','-y','-i','/workspace/vo.wav','-af',f'volume={-13.0-I:.2f}dB,alimiter=limit=0.93:level=false','/workspace/vo2.wav'],check=True)
import os; out = os.environ['OUT']
subprocess.run(['ffmpeg','-v','error','-y','-i','/workspace/in/silent.mp4','-i','/workspace/vo2.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out+'/ecommwave_reel_fake_timer_el.mp4'],check=True)
fd = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out+'/ecommwave_reel_fake_timer_el.mp4']).decode())
print(f'ok ecommwave_reel_fake_timer_el.mp4 {fd:.2f}s, voice integrated {I:.1f} LUFS before final gain -> -13 LUFS')

EOF_PY
python3 /workspace/mix.py
