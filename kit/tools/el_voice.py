"""ElevenLabs voice-over pipeline (owner, 2026-11-28: "Use ElevenLabs for my voice over").
The ElevenLabs audio can't be downloaded into this workspace (the proxy blocks elevenlabsusercontent.com), so the voice is
made and mixed INSIDE ElevenLabs (MCP tools) and only the timings come back here. See VOICE.md "ElevenLabs workflow".

1. Write script.json exactly as before (lines, *accents*, chapters, holds, "loud" fix bridge, cues).
   python3 tools/el_voice.py text script.json            -> prints the exact text to send to creative_generate_speech
2. creative_generate_speech (voice + model in VOICE.md, generations_count 1) -> creative_transcribe_audio (connect_from the
   speech node, eleven_scribe_v1, free) -> save the transcript's "words" list as vo/words.json
3. python3 tools/el_voice.py plan script.json vo/words.json vo/
   -> vo/timing.js + timing.json (same window.VO format as voiceover.py, so reel.js / RL.W work unchanged; holds are real
      pauses spliced into the audio) + vo/edit.json; checks that the spoken words match the script exactly
4. Build/render the silent video with window.DUR = VO.dur (render_video.py), push it to instagram-media.
5. python3 tools/el_voice.py sandbox vo/ > vo/sandbox.sh   (a self-contained bash command, < 30k chars)
   creative_attach_reference_file(url=<raw silent.mp4>, flow_id) ; creative_execute_sandbox(command=<vo/sandbox.sh>,
   inputs=[{node_id:<speech node>, filename:"voice.mp3"}, {node_id:<silent video node>, filename:"silent.mp4"}], flow_id)
   -> splices the holds, makes the bridge line louder, adds the sfx cues, −13 LUFS, muxes -> $OUT/final.mp4 on the flow.
   It must print "ok". Its content URL is the video_url for Windsor create_video_post (signed, valid a few hours: post
   right away). Keep the flow URL in the log.
"""
import sys, os, re, json

LEAD, TAIL, LOUD_DB = 0.25, 0.6, 4.5
norm = lambda s: re.sub(r'[^a-z0-9]', '', s.lower())
clean = lambda s: s.replace('*', '')

def hl_flags(text):
    """accent flags per word (same rule as voiceover.py): *a phrase* and "a quote" are accented."""
    out = []; inq = inst = False
    for j, t in enumerate(text.split()):
        if t.startswith(('"', '“')): inq = True
        if t.lstrip('"“').startswith('*'): inst = True
        out.append(inq or inst)
        if t.rstrip(',.?!…"”').endswith('*') or t.endswith('*'): inst = False
        if t.rstrip(',.?!…').endswith(('"', '”')) and (inq or j): inq = False
    return out

def text(script):
    spec = json.load(open(script)); out = []; para = []
    for ln in spec['lines']:
        if ln.get('loud'):
            if para: out.append(' '.join(para)); para = []
            out.append(clean(ln['text']))
        else: para.append(clean(ln['text']))
    if para: out.append(' '.join(para))
    print('\n\n'.join(out))

def plan(script, words_f, out):
    os.makedirs(out, exist_ok=True); spec = json.load(open(script)); L0 = spec['lines']
    W = [w for w in json.load(open(words_f)) if w.get('type', 'word') == 'word']
    toks = [t for ln in L0 for t in clean(ln['text']).split()]
    if len(W) != len(toks) or any(norm(a) != norm(b['text']) for a, b in zip(toks, W)):
        print('WORD MISMATCH between script and ElevenLabs transcript:')
        for i, (a, b) in enumerate(zip(toks, W)):
            if norm(a) != norm(b['text']): print(f'  #{i}: script "{a}" vs spoken "{b["text"]}"'); break
        print(f'  script {len(toks)} words, spoken {len(W)}'); sys.exit(1)
    # line word ranges
    rng, k = [], 0
    for ln in L0: n = len(ln['text'].split()); rng.append((k, k + n)); k += n
    # segments: cut after each held line (midpoint of the natural gap) and insert silence so the pause = hold
    segs, src0, shift = [], max(0.0, W[0]['start'] - 0.05), LEAD - max(0.0, W[0]['start'] - 0.05)
    offs = []   # (src_time_from, shift)
    offs.append((src0, shift))
    for i, ln in enumerate(L0):
        h = float(ln.get('hold', 0))
        if not h or i == len(L0) - 1: continue
        a, b = rng[i]; e = W[b - 1]['end']; s = W[b]['start']; cut = (e + s) / 2
        segs.append({'src0': round(src0, 3), 'src1': round(cut, 3), 'out0': round(src0 + shift, 3)})
        shift += max(0.0, h - (s - e)); src0 = cut; offs.append((cut, shift))
    endsrc = W[-1]['end'] + 0.12
    segs.append({'src0': round(src0, 3), 'src1': round(endsrc, 3), 'out0': round(src0 + shift, 3)})
    def m(t):
        sh = offs[0][1]
        for f, s in offs:
            if t >= f: sh = s
        return t + sh
    lines = []
    for i, ln in enumerate(L0):
        a, b = rng[i]; ws = W[a:b]
        words = [{'w': x, 's': round(m(w['start']), 3), 'e': round(m(w['end']), 3), 'hl': f}
                 for x, w, f in zip(clean(ln['text']).split(), ws, hl_flags(ln['text']))]
        sp = max(0.3, ws[-1]['end'] - ws[0]['start'])
        lines.append({'start': round(max(0, words[0]['s'] - 0.03), 3), 'end': round(words[-1]['e'] + 0.05, 3), 'text': clean(ln['text']),
                      'wps': round(len(ws) / sp, 2), 'words': words, 'chapter': ln.get('chapter'),
                      'hold': round(float(ln.get('hold', 0)), 2), 'loud': bool(ln.get('loud')), 'timing': 'exact'})
    dur = round(lines[-1]['end'] + TAIL, 2)
    cues = []
    for c in spec.get('cues', []):
        l = lines[c['line']]
        if 'word' in c:
            hit = [w for w in l['words'] if norm(w['w']) == norm(c['word'])]
            if not hit: print(f'WARNING: cue word "{c["word"]}" not in line {c["line"]}'); continue
            tt = hit[0]['s'] + c.get('offset', 0)
        else: tt = l['end'] + c.get('after', 0)
        cues.append({'t': round(max(0, tt), 3), 'sfx': c['sfx'], 'id': c.get('word', c['sfx'])})
    cues.sort(key=lambda c: c['t'])
    loud = [[round(l['words'][0]['s'] - 0.04, 3), round(l['words'][-1]['e'] + 0.08, 3)] for l in lines if l['loud']]
    p = {'dur': dur, 'engine': 'elevenlabs', 'voice': spec.get('el_voice'), 'music': False, 'lines': lines, 'cues': cues}
    json.dump(p, open(f'{out}/timing.json', 'w'), indent=1)
    open(f'{out}/timing.js', 'w').write('window.VO=' + json.dumps(p) + ';\n')
    json.dump({'dur': dur, 'segs': segs, 'loud': loud, 'cues': cues}, open(f'{out}/edit.json', 'w'))
    errs = []
    wsum = sum(len(l['words']) for l in lines); ssum = sum(l['words'][-1]['e'] - l['words'][0]['s'] for l in lines)
    if not 2.3 <= wsum / ssum <= 3.9: errs.append(f'overall pace {wsum/ssum:.2f} w/s')
    for i in range(1, len(lines)):
        g = lines[i]['start'] - lines[i - 1]['end']
        if not lines[i - 1]['hold'] and g > 0.6: errs.append(f'silent gap {g:.2f}s before line {i}')
    for l in lines:
        print(f"{l['start']:6.2f}-{l['end']:6.2f}s  {l['wps']:.2f} w/s  {l['text']}" + (f"  [hold {l['hold']}s]" if l['hold'] else '') + ('  [LOUD]' if l['loud'] else ''))
    for c in cues: print(f"  cue {c['sfx']:7s} {c['t']:6.2f}s  ({c['id']})")
    print(f'video length (window.DUR) = {dur}s')
    if errs: print('CHECK FAILED:', '; '.join(errs)); sys.exit(1)

SANDBOX_PY = r'''
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
    s0, s1 = max(0,int(x0*SR)), min(n,int(x1*SR)); seg = np.ones(s1-s0)*10**(%LOUD%/20); r = min(rp, len(seg)//2)
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
subprocess.run(['ffmpeg','-v','error','-y','-i','/workspace/in/silent.mp4','-i','/workspace/vo2.wav','-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',out+'/%NAME%'],check=True)
fd = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out+'/%NAME%']).decode())
print(f'ok %NAME% {fd:.2f}s, voice integrated {I:.1f} LUFS before final gain -> -13 LUFS')
'''

def sandbox(out, name='final.mp4'):
    edit = open(f'{out}/edit.json').read()
    py = SANDBOX_PY.replace('%LOUD%', str(LOUD_DB)).replace('%NAME%', name)
    print(f"cat > /workspace/edit.json <<'EOF_EDIT'\n{edit}\nEOF_EDIT\ncat > /workspace/mix.py <<'EOF_PY'\n{py}\nEOF_PY\npython3 /workspace/mix.py")

if __name__ == '__main__':
    c = sys.argv[1]
    if c == 'text': text(sys.argv[2])
    elif c == 'plan': plan(sys.argv[2], sys.argv[3], sys.argv[4])
    elif c == 'sandbox': sandbox(sys.argv[2], *(sys.argv[3:4]))
