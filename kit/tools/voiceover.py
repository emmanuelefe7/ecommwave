"""Voiceover-first timing for Reels. The VOICE sets the timeline; the animation follows it.

Step 1  plan:  python3 tools/voiceover.py plan script.json vo/
        script.json = {"voice":"af_heart","lines":[{"text":"..."},{"text":"...","pause_after":0.5}, ...]}
        - Synthesizes every line at a natural pace (each line auto-tuned to ~2.8 words/sec).
        - Packs lines back to back: starts at 0.30 s, 0.35 s between lines (pause_after can raise one gap, max 0.6 s),
          video ends 0.7 s after the last word.
        - Writes vo/timing.json and vo/timing.js (window.VO = {dur, lines:[{start,end,text}]}) + vo/lineN.wav.
Step 2  build the video page with <script src="vo/timing.js"></script>, set window.DUR = VO.dur, and start each
        scene's animation at VO.lines[i].start (on-screen words appear as they are spoken).
Step 3  mix:   python3 tools/voiceover.py mix vo/ silent.mp4 final.mp4
        - Places each line exactly at its planned time, adds a quiet music pad, loudness -14 LUFS.
        - QUALITY GATE: refuses to write final.mp4 if the video length doesn't match the plan (±0.15 s),
          a line is too fast/slow (outside 2.3-3.3 words/sec), a silent gap > 0.7 s, first word later than 0.5 s,
          ending silence > 1.2 s, or speech covers < 75 % of the video.
Engines: "engine":"chatterbox" (DEFAULT, natural human-sounding voice; needs `pip install --break-system-packages chatterbox-tts`
         and huggingface.co reachable; optional "voice_ref":"path/to/clip.wav" to use a specific voice; "exaggeration" 0.3-0.7)
         falls back automatically to "kokoro" (af_heart warm female / am_michael male) if Chatterbox can't load.
Model files download once (Chatterbox -> HF cache, Kokoro -> ~/.kokoro)."""
import sys, os, json, subprocess
import numpy as np, soundfile as sf

SR = 48000
TARGET_WPS = 2.8
LEAD, GAP, MAX_GAP, TAIL = 0.30, 0.35, 0.60, 0.70

def kokoro():
    d = os.path.expanduser('~/.kokoro'); os.makedirs(d, exist_ok=True)
    for f, u in [('kokoro.onnx', 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx'),
                 ('voices.bin', 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin')]:
        if not os.path.exists(f'{d}/{f}'): subprocess.run(['curl', '-sSL', '-o', f'{d}/{f}', u], check=True)
    from kokoro_onnx import Kokoro
    return Kokoro(f'{d}/kokoro.onnx', f'{d}/voices.bin')

def trim(a, sr, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0: return a
    s = max(0, idx[0] - int(0.02 * sr)); e = min(len(a), idx[-1] + int(0.05 * sr))
    return a[s:e]

def synth(k, text, voice):
    words = len(text.split()); speed = 1.0
    best = None
    for _ in range(6):
        a, sr = k.create(text, voice=voice, speed=speed, lang='en-us'); a = trim(a, sr)
        wps = words / (len(a) / sr)
        if best is None or abs(wps - TARGET_WPS) < abs(best[1] - TARGET_WPS): best = (a, wps)
        if 2.6 <= wps <= 3.0: break
        speed = float(np.clip(speed * (TARGET_WPS / wps) ** 1.3, 0.65, 1.15))
    a, wps = best
    a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    return a, wps

def chatterbox():
    import torch
    from chatterbox.tts import ChatterboxTTS
    torch.set_num_threads(os.cpu_count() or 2)
    dev = 'cuda' if torch.cuda.is_available() else 'cpu'
    return ChatterboxTTS.from_pretrained(device=dev)

def stretch(a, sr, factor):
    """time-stretch without changing pitch (factor >1 = faster)"""
    sf.write('/tmp/_st_in.wav', a.astype(np.float32), sr)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/_st_in.wav', '-af', f'atempo={factor:.4f}', '/tmp/_st_out.wav'], check=True)
    b, _ = sf.read('/tmp/_st_out.wav'); return b

def synth_cb(m, text, spec):
    import torch
    words = len(text.split()); best = None
    kw = {'exaggeration': spec.get('exaggeration', 0.55), 'cfg_weight': spec.get('cfg_weight', 0.45), 'temperature': spec.get('temperature', 0.8)}
    if spec.get('voice_ref'): kw['audio_prompt_path'] = spec['voice_ref']
    for attempt in range(3):
        torch.manual_seed(1234 + attempt * 7)
        a = m.generate(text, **kw).squeeze(0).cpu().numpy(); a = trim(a, m.sr, thr=0.015)
        wps = words / (len(a) / m.sr)
        if best is None or abs(wps - TARGET_WPS) < abs(best[1] - TARGET_WPS): best = (a, wps)
        if 2.5 <= wps <= 3.1: break
    a, wps = best
    if not 2.5 <= wps <= 3.1:   # gentle pitch-preserving tempo fix, max ±12 %
        f = float(np.clip(TARGET_WPS / wps, 0.88, 1.12)); a = stretch(a, m.sr, f); wps = words / (len(a) / m.sr)
    a = np.interp(np.arange(0, len(a), m.sr / SR), np.arange(len(a)), a)
    return a, wps

def plan(script, out):
    os.makedirs(out, exist_ok=True); spec = json.load(open(script))
    engine = spec.get('engine', 'chatterbox'); m = None
    if engine == 'chatterbox':
        try: m = chatterbox(); print('voice engine: chatterbox (natural)')
        except Exception as e:
            print(f'WARNING: Chatterbox unavailable ({type(e).__name__}: {str(e)[:120]}) -> falling back to Kokoro'); engine = 'kokoro'
    if engine == 'kokoro': k = kokoro(); print('voice engine: kokoro')
    voice = spec.get('voice', 'af_heart'); t = LEAD; lines = []
    for i, ln in enumerate(spec['lines']):
        a, wps = synth_cb(m, ln['text'], spec) if m is not None else synth(k, ln['text'], voice)
        sf.write(f'{out}/line{i}.wav', a.astype(np.float32), SR)
        L = len(a) / SR
        lines.append({'start': round(t, 3), 'end': round(t + L, 3), 'text': ln['text'], 'wps': round(wps, 2)})
        t += L + min(MAX_GAP, max(GAP, ln.get('pause_after', GAP)))
    dur = round(lines[-1]['end'] + TAIL, 2)
    plan = {'dur': dur, 'engine': engine, 'lines': lines}
    json.dump(plan, open(f'{out}/timing.json', 'w'), indent=1)
    open(f'{out}/timing.js', 'w').write('window.VO=' + json.dumps(plan) + ';\n')
    for l in lines: print(f"{l['start']:6.2f}-{l['end']:6.2f}s  {l['wps']:.2f} w/s  {l['text']}")
    print(f'video length (window.DUR) = {dur}s')

def check(p, vid_dur):
    errs = []; lines = p['lines']
    if abs(vid_dur - p['dur']) > 0.15: errs.append(f'video is {vid_dur:.2f}s but the voiceover plan is {p["dur"]}s: set window.DUR = VO.dur')
    if lines[0]['start'] > 0.5: errs.append('first word starts later than 0.5s')
    for i, l in enumerate(lines):
        if not 2.3 <= l['wps'] <= 3.3: errs.append(f'line {i} pace {l["wps"]} w/s (needs 2.3-3.3): rewrite it shorter/longer')
        if i and l['start'] - lines[i-1]['end'] > 0.7: errs.append(f'silent gap of {l["start"]-lines[i-1]["end"]:.2f}s before line {i}')
    if vid_dur - lines[-1]['end'] > 1.2: errs.append(f'{vid_dur-lines[-1]["end"]:.2f}s of silence at the end')
    cov = sum(l['end'] - l['start'] for l in lines) / vid_dur
    if cov < 0.75: errs.append(f'speech covers only {cov*100:.0f}% of the video (needs 75%+)')
    return errs, cov

def mix(out, vid, final):
    p = json.load(open(f'{out}/timing.json'))
    vd = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid]).decode())
    errs, cov = check(p, vd)
    if errs:
        print('VOICEOVER CHECK FAILED:'); [print(' -', e) for e in errs]; sys.exit(1)
    n = int(SR * vd); voice = np.zeros(n + SR)
    for i, l in enumerate(p['lines']):
        a, _ = sf.read(f'{out}/line{i}.wav'); s = int(l['start'] * SR); e = min(len(voice), s + len(a)); voice[s:e] += a[:e - s]
    voice = voice[:n]; t = np.arange(n) / SR; pad = np.zeros(n)
    for i, f in enumerate([87.31, 130.81, 174.61, 220.0, 261.63, 329.63]):
        for det in (-0.6, 0.6): pad += np.sin(2 * np.pi * (f + det) * t + i) * (0.9 if f < 200 else 0.5)
    pad *= (0.75 + 0.25 * np.sin(2 * np.pi * 0.18 * t)) * np.clip(t / 1.5, 0, 1) * np.clip((vd - t) / 1.0, 0, 1)
    pad = np.convolve(pad, np.ones(40) / 40, mode='same'); pad /= np.abs(pad).max()
    mixd = voice / max(np.abs(voice).max(), 1e-6) * 0.8 + pad * 0.8 * 10 ** (-24 / 20)
    sf.write('/tmp/vo_raw.wav', mixd.astype(np.float32), SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/vo_raw.wav', '-af', 'highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,loudnorm=I=-14:TP=-1.5:LRA=9', '-ac', '2', '-ar', '48000', '/tmp/vo.wav'], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', '/tmp/vo.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final + '.tmp.mp4'], check=True)
    os.replace(final + '.tmp.mp4', final)
    print(f'ok {final}  (speech covers {cov*100:.0f}% of {vd:.1f}s)')

if __name__ == '__main__':
    if sys.argv[1] == 'plan': plan(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'mix': mix(sys.argv[2], sys.argv[3], sys.argv[4])
    else: print(__doc__)
