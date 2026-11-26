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
Engines: "engine":"kokoro" (DEFAULT: exact word timings from the model). "chatterbox" (natural voice, NO exact word timings; needs `pip install --break-system-packages chatterbox-tts`
         and huggingface.co reachable; optional "voice_ref":"path/to/clip.wav" to use a specific voice; "exaggeration" 0.3-0.7)
         falls back automatically to "kokoro" (af_heart warm female / am_michael male) if Chatterbox can't load.
Model files download once (Chatterbox -> HF cache, Kokoro -> ~/.kokoro)."""
import sys, os, json, subprocess
import numpy as np, soundfile as sf

SR = 48000
TARGET_WPS = 3.0                     # brisk, conversational (owner's reference reel ~3 words/sec)
LEAD, GAP, MAX_GAP, TAIL = 0.25, 0.15, 0.45, 0.60   # lines almost back to back
MAX_HOLD = 3.6
LANG = 'en-us'   # owner, 2026-11-26: simple, neutral English accent (clear, easy to understand); MAX_HOLD above = optional countdown pause

def kokoro():
    d = os.path.expanduser('~/.kokoro'); os.makedirs(d, exist_ok=True)
    for f, u in [('kokoro.onnx', 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx'),
                 ('voices.bin', 'https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin')]:
        if not os.path.exists(f'{d}/{f}'): subprocess.run(['curl', '-sSL', '-o', f'{d}/{f}', u], check=True)
    if not os.path.exists(f'{d}/kokoro_timed.onnx'):   # expose the model's own phoneme durations -> exact word timings
        import onnx
        from onnx import helper, TensorProto
        mm = onnx.load(f'{d}/kokoro.onnx')
        mm.graph.node.append(helper.make_node('Identity', ['/encoder/Round_output_0'], ['duration'], name='expose_duration'))
        mm.graph.output.append(helper.make_tensor_value_info('duration', TensorProto.FLOAT, None))
        onnx.save(mm, f'{d}/kokoro_timed.onnx')
    from kokoro_onnx import Kokoro
    return Kokoro(f'{d}/kokoro_timed.onnx', f'{d}/voices.bin')

def trim(a, sr, thr=0.01):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0: return a
    s = max(0, idx[0] - int(0.02 * sr)); e = min(len(a), idx[-1] + int(0.05 * sr))
    return a[s:e]

def synth(k, text, voice):
    """Kokoro line + EXACT word timings from the model's phoneme durations (kokoro_timed.onnx)."""
    words = len(text.split()); speed = 1.0
    best = None
    for _ in range(6):
        a, sr, sp = k.create_timed(text, voice=voice, speed=speed, lang=LANG)
        idx = np.where(np.abs(a) > 0.01)[0]; head = max(0, idx[0] - int(0.02 * sr)) if len(idx) else 0
        tail = min(len(a), idx[-1] + int(0.05 * sr)) if len(idx) else len(a)
        a = a[head:tail]; off = head / sr
        wps = words / (len(a) / sr)
        wt = []; cur = None
        for ph in sp:                       # group phonemes into words at spaces
            if ph.phoneme == ' ':
                if cur: wt.append(cur); cur = None
                continue
            if ph.phoneme in ',.!?;:…"“”': continue
            cur = [ph.start - off, ph.end - off] if cur is None else [cur[0], ph.end - off]
        if cur: wt.append(cur)
        wt = [[max(0, x), max(0, y)] for x, y in wt] if len(wt) == words else None
        if best is None or abs(wps - TARGET_WPS) < abs(best[1] - TARGET_WPS): best = (a, wps, wt)
        if 2.8 <= wps <= 3.2: break
        speed = float(np.clip(speed * (TARGET_WPS / wps) ** 1.3, 0.65, 1.25))
    a, wps, wt = best
    a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
    return a, wps, wt

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
        if 2.7 <= wps <= 3.3: break
    a, wps = best
    if not 2.7 <= wps <= 3.3:   # gentle pitch-preserving tempo fix, max ±12 %
        f = float(np.clip(TARGET_WPS / wps, 0.88, 1.12)); a = stretch(a, m.sr, f); wps = words / (len(a) / m.sr)
    a = np.interp(np.arange(0, len(a), m.sr / SR), np.arange(len(a)), a)
    return a, wps, None

import re
def clean(text):
    """script markup: *word* = accent word (caption colour), "..." quotes are accented too. TTS gets plain text."""
    return re.sub(r'\*', '', text)

def syl(w):
    w = re.sub(r'[^a-z0-9]', '', w.lower())
    if not w: return 0.5
    if w.isdigit(): return 1.5 * len(w)
    n = len(re.findall(r'[aeiouy]+', w)) - (1 if w.endswith('e') and len(w) > 3 else 0)
    return max(1, n)

PHON = None   # set to a word -> phoneme-count function when Kokoro is loaded (much better duration weights)
def weight(t):
    w = re.sub(r'[^A-Za-z0-9\']', '', t)
    if PHON and w:
        try: return max(1.0, float(PHON(w)))
        except Exception: pass
    return syl(t) * 2.6 + 0.5

def align(a, text):
    """Word timestamps inside one synthesized line. 1) find the real pauses in the audio (runs of >= 60 ms near-silence),
    2) pin the boundary after every punctuated word to its pause, 3) split the rest by phoneme count, 4) snap each
    boundary to the quietest frame within ±50 ms. Typically within ~40 ms of the true word onset."""
    toks = text.split(); fr = int(0.01 * SR); L = len(a) / SR
    env = np.array([np.sqrt((a[i:i + fr] ** 2).mean()) for i in range(0, max(1, len(a) - fr), fr)]) + 1e-6
    env = np.convolve(env, np.ones(3) / 3, mode='same')
    thr = np.median(env[env > np.percentile(env, 40)]) * 0.12
    quiet = env < thr; pauses = []; j = 0
    while j < len(quiet):
        if quiet[j]:
            k = j
            while k < len(quiet) and quiet[k]: k += 1
            if k - j >= 6 and j > 3 and k < len(quiet) - 3: pauses.append(((j + k) / 2) * 0.01)
            j = k
        else: j += 1
    wts = [weight(t) for t in toks]
    cum = np.cumsum([0] + wts) / sum(wts) * L; b = list(cum)
    punct = [bool(re.search(r'[,.;:?!…]["”*]*$', t)) for t in toks]
    anchors = {0: 0.0, len(toks): L}
    for j in range(len(toks) - 1):
        if punct[j] and pauses:
            c = min(pauses, key=lambda x: abs(x - b[j + 1]))
            if abs(c - b[j + 1]) < 0.35: anchors[j + 1] = c
    keys = sorted(anchors)
    for x, y in zip(keys, keys[1:]):       # re-split by weight between anchors
        tot = sum(wts[x:y]); acc = anchors[x]
        for j in range(x, y):
            b[j] = acc; acc += (anchors[y] - anchors[x]) * wts[j] / tot
        b[y] = anchors[y]
    for j in range(1, len(b) - 1):
        if j in anchors: continue
        c = int(b[j] / 0.01); lo, hi = max(1, c - 5), min(len(env) - 1, c + 6)
        if hi > lo: b[j] = (lo + int(np.argmin(env[lo:hi]))) * 0.01
    for j in range(1, len(b)): b[j] = max(b[j], b[j - 1] + 0.08)
    out = []; inq = False; inst = False
    for j, t in enumerate(toks):            # *a phrase* and "a quote" are accent spans (can cover several words)
        if t.startswith(('"', '“')): inq = True
        if t.lstrip('"“').startswith('*'): inst = True
        hl = inq or inst
        if t.rstrip(',.?!…"”').endswith('*') or t.endswith('*'): inst = False
        if t.rstrip(',.?!…').endswith(('"', '”')) and (inq or j): inq = False
        out.append({'w': t.replace('*', ''), 's': round(b[j], 3), 'e': round(b[j + 1], 3), 'hl': hl})
    return out

def rb_stretch(a, sr, factor):
    """pitch- and formant-preserving tempo change (Rubber Band, high quality). factor > 1 = shorter."""
    sf.write('/tmp/_rb_in.wav', a.astype(np.float32), sr)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/_rb_in.wav', '-af',
                    f'rubberband=tempo={factor:.4f}:pitchq=quality:formant=preserved:transients=mixed', '/tmp/_rb_out.wav'], check=True)
    b, _ = sf.read('/tmp/_rb_out.wav'); return b

def tighten_words(k, a, sr, wt, toks):
    """Owner feedback: some words come out dragged ("buy" too long). The model has no per-word duration control, so
    every word whose spoken length is well over what its sounds need is shortened (pitch kept), and all later
    timings move with it. Expected length = 0.052 s per phoneme + 0.045 s (sentence-final words may be 45 % longer)."""
    if not wt: return a, wt
    out = [a[:int(wt[0][0] * sr)]]; new = []; pos = wt[0][0]
    for j, ((s0, e0), tok) in enumerate(zip(wt, toks)):
        w = re.sub(r"[^A-Za-z0-9']", '', tok)
        try: n = len(re.sub(r'[^\w]|[ˈˌːˑ]', '', k.tokenizer.phonemize(w, LANG))) if w else 3
        except Exception: n = max(2, len(w))
        final = bool(re.search(r'[.?!]["”*]*$', tok))
        exp = (0.052 * n + 0.045) * (1.45 if final else 1.0)
        piece = a[int(s0 * sr):int(e0 * sr)]; d = e0 - s0
        if d > exp * 1.12 and len(piece) > int(0.06 * sr):
            f = min(1.7, d / (exp * 1.05)); piece = rb_stretch(piece, sr, f)
        new.append([pos, pos + len(piece) / sr]); out.append(piece); pos += len(piece) / sr
        nxt = wt[j + 1][0] if j + 1 < len(wt) else len(a) / sr
        gap = a[int(e0 * sr):int(nxt * sr)]; out.append(gap); pos += len(gap) / sr
    b = np.concatenate(out)
    return b, new

def hl_flags(text):
    """accent flags per word from the script markup: *a phrase* and "a quote" are accented."""
    out = []; inq = inst = False
    for j, t in enumerate(text.split()):
        if t.startswith(('"', '“')): inq = True
        if t.lstrip('"“').startswith('*'): inst = True
        out.append(inq or inst)
        if t.rstrip(',.?!…"”').endswith('*') or t.endswith('*'): inst = False
        if t.rstrip(',.?!…').endswith(('"', '”')) and (inq or j): inq = False
    return out

def breath(sr, dur=0.24):
    """a soft, short inhale (band-limited noise, rise/fall) used only in sentence pauses."""
    r = np.random.default_rng(11); n = int(dur * sr); tt = np.arange(n) / sr
    nz = r.normal(0, 1, n + 400)
    nz = np.convolve(nz, np.ones(6) / 6, 'same') - np.convolve(nz, np.ones(60) / 60, 'same')   # ~band-pass 400-4k
    env = np.sin(np.pi * np.clip(tt / dur, 0, 1)) ** 1.6 * (0.6 + 0.4 * tt / dur)
    return nz[200:200 + n] * env

# VOICE DELIVERY (owner's instructions, kit/VOICE.md): pauses follow punctuation exactly.
COMMA_PAUSE, STOP_PAUSE = 0.16, 0.38    # brief pause at "," ; meaningful pause after "." "?" "!"

def plan_flow(k, spec, out, voice):
    """NATURAL FLOW (default): speak each section (lines up to the next "hold") as ONE continuous passage, exactly as
    written (no words or punctuation added/removed), then cut it into lines at the exact word times.
    - commas: brief pause, full stops / question marks: meaningful pause (sizes above), set via the model's timings
    - one fixed voice style for the whole video (consistent pitch, tone, identity), one speed, continuous prosody
    - accent words (*...*) get a gentle +2.5 dB lift = natural emphasis; soft breath in sentence pauses
    "speed" (default 1.05) sets the overall pace (~3 words/sec)."""
    speed = float(spec.get('speed', 1.05)); L0 = spec['lines']; groups = [[]]
    for i, ln in enumerate(L0):
        groups[-1].append(i)
        if ln.get('hold') and i < len(L0) - 1: groups.append([])
    vs = k.get_voice_style(voice) if isinstance(voice, str) else voice
    style = np.repeat(vs[int(spec.get('style_row', 160)):int(spec.get('style_row', 160)) + 1], len(vs), axis=0)  # constant identity
    t = LEAD; lines = [None] * len(L0)
    for g in groups:
        text = ' '.join(clean(L0[i]['text']).strip() for i in g)
        try: a, sr, ph = k.create_timed(text, voice=style, speed=speed, lang=LANG, sentence_pause=STOP_PAUSE, clause_pause=COMMA_PAUSE, continuous=True)
        except Exception: a, sr, ph = k.create_timed(text, voice=style, speed=speed, lang=LANG, sentence_pause=STOP_PAUSE, clause_pause=COMMA_PAUSE)
        wt = []; cur = None
        for p in ph:
            if p.phoneme == ' ':
                if cur: wt.append(cur); cur = None
                continue
            if p.phoneme in ',.!?;:…"“”': continue
            cur = [p.start, p.end] if cur is None else [cur[0], p.end]
        if cur: wt.append(cur)
        counts = [len(L0[i]['text'].split()) for i in g]
        if len(wt) != sum(counts): raise RuntimeError(f'word/phoneme mismatch in section starting line {g[0]} ({len(wt)} vs {sum(counts)}): write numbers/symbols as words')
        flags = [f for i in g for f in hl_flags(L0[i]['text'])]
        toks = [x for i in g for x in clean(L0[i]['text']).split()]
        a = a.astype(np.float64)
        if spec.get('tighten', True): a, wt = tighten_words(k, a, sr, wt, toks)
        if spec.get('emphasis', True):          # gentle lift on accent words (with 25 ms ramps)
            gain = np.ones(len(a)); rp = int(0.025 * sr)
            for (x0, x1), f in zip(wt, flags):
                if not f: continue
                s0, s1 = int(x0 * sr), int(x1 * sr); seg = np.ones(s1 - s0) * 10 ** (2.5 / 20)
                r = min(rp, len(seg) // 2)
                if r: seg[:r] = np.linspace(1, seg[0], r); seg[-r:] = np.linspace(seg[0], 1, r)
                gain[s0:s1] = np.maximum(gain[s0:s1], seg)
            a = a * gain
        if spec.get('breaths', True):           # soft breath before a new sentence when the pause is long enough
            pk = np.abs(a).max(); br = breath(sr)
            for j in range(1, len(wt)):
                if re.search(r'[.?!]["”]?$', toks[j - 1]) and wt[j][0] - wt[j - 1][1] >= 0.3:
                    e0 = int((wt[j][0] - 0.05) * sr); s0 = e0 - len(br)
                    if s0 > int(wt[j - 1][1] * sr): a[s0:e0] += br / np.abs(br).max() * pk * 10 ** (-34 / 20)
        a = np.interp(np.arange(0, len(a), sr / SR), np.arange(len(a)), a)
        head = max(0.0, wt[0][0] - 0.03); gend = min(len(a) / SR, wt[-1][1] + 0.08)
        pos = 0
        for n, i in enumerate(g):
            w = wt[pos:pos + counts[n]]; pos += counts[n]
            seg_s = max(head, w[0][0] - 0.03) if n == 0 else lines[g[n - 1]]['_cut']
            seg_e = (wt[pos][0] - 0.30 if n < len(g) - 1 else gend)
            if n < len(g) - 1: seg_e = max(seg_e, w[-1][1] + 0.02)
            seg = a[int(seg_s * SR):int(seg_e * SR)]
            sf.write(f'{out}/line{i}.wav', seg.astype(np.float32), SR)
            off = t + seg_s - head
            words = [{'w': x.replace('*', ''), 's': round(t + y0 - head, 3), 'e': round(t + y1 - head, 3), 'hl': f}
                     for x, (y0, y1), f in zip(L0[i]['text'].split(), w, hl_flags(L0[i]['text']))]
            spoken = w[-1][1] - w[0][0]
            lines[i] = {'start': round(off, 3), 'end': round(off + len(seg) / SR, 3), 'text': clean(L0[i]['text']),
                        'wps': round(counts[n] / max(spoken, 0.3), 2), 'words': words, 'chapter': L0[i].get('chapter'),
                        'hold': round(min(MAX_HOLD, float(L0[i].get('hold', 0))), 2), 'timing': 'exact', '_cut': seg_e}
        t += (gend - head) + (lines[g[-1]]['hold'] or GAP)
    for l in lines: l.pop('_cut', None)
    return lines, t

def plan(script, out):
    os.makedirs(out, exist_ok=True); spec = json.load(open(script))
    engine = spec.get('engine', 'kokoro'); m = None   # kokoro = exact word timings
    if engine == 'chatterbox':
        try: m = chatterbox(); print('voice engine: chatterbox (natural)')
        except Exception as e:
            print(f'WARNING: Chatterbox unavailable ({type(e).__name__}: {str(e)[:120]}) -> falling back to Kokoro'); engine = 'kokoro'
    if engine == 'kokoro':
        global PHON
        k = kokoro(); print('voice engine: kokoro')
        try: PHON = lambda w: len(re.sub(r'[^\w]', '', k.tokenizer.phonemize(w, LANG)))
        except Exception: PHON = None
    global LANG
    LANG = spec.get('lang', 'en-us'); voice = spec.get('voice', 'am_puck'); t = LEAD; lines = []
    if engine == 'kokoro' and spec.get('flow', True):
        lines, t = plan_flow(k, spec, out, voice)
    else:
      for i, ln in enumerate(spec['lines']):
        txt = clean(ln['text'])
        a, wps, wt = synth_cb(m, txt, spec) if m is not None else synth(k, txt, voice)
        sf.write(f'{out}/line{i}.wav', a.astype(np.float32), SR)
        L = len(a) / SR
        al = align(a, ln['text'])
        if wt: al = [dict(w, s=round(x, 3), e=round(y, 3)) for w, (x, y) in zip(al, wt)]; src = 'exact'
        else: src = 'estimated'
        words = [dict(w, s=round(t + w['s'], 3), e=round(t + w['e'], 3)) for w in al]
        hold = min(MAX_HOLD, float(ln.get('hold', 0)))
        lines.append({'start': round(t, 3), 'end': round(t + L, 3), 'text': txt, 'wps': round(wps, 2), 'words': words,
                      'chapter': ln.get('chapter'), 'hold': round(hold, 2), 'timing': src})
        t += L + (hold if hold else min(MAX_GAP, max(GAP, ln.get('pause_after', GAP))))
    dur = round(lines[-1]['end'] + TAIL, 2)
    cues = []
    for c in spec.get('cues', []):   # {"sfx":"pop","line":3,"word":"clutter"} | {"sfx":"tick","line":2,"after":0.0} (after = s past line end)
        l = lines[c['line']]
        if 'word' in c:
            hit = [w for w in l['words'] if re.sub(r'[^a-z0-9]', '', w['w'].lower()) == re.sub(r'[^a-z0-9]', '', c['word'].lower())]
            if not hit: print(f'WARNING: cue word "{c["word"]}" not in line {c["line"]}'); continue
            tt = hit[0]['s'] + c.get('offset', 0)
        else: tt = l['end'] + c.get('after', 0)
        cues.append({'t': round(tt, 3), 'sfx': c['sfx'], 'id': c.get('id', c.get('word', c['sfx']))})
    plan = {'dur': dur, 'engine': engine, 'music': bool(spec.get('music', False)), 'lines': lines, 'cues': sorted(cues, key=lambda c: c['t'])}
    json.dump(plan, open(f'{out}/timing.json', 'w'), indent=1)
    open(f'{out}/timing.js', 'w').write('window.VO=' + json.dumps(plan) + ';\n')
    for l in lines:
        print(f"{l['start']:6.2f}-{l['end']:6.2f}s  {l['wps']:.2f} w/s  {l['text']}" + (f"  [hold {l['hold']}s]" if l['hold'] else ''))
        print(f"        [{l['timing']}] " + ' '.join(f"{w['w']}@{w['s']:.2f}" for w in l['words']))
    for c in plan['cues']: print(f"  cue {c['sfx']:7s} {c['t']:6.2f}s  ({c['id']})")
    print(f'video length (window.DUR) = {dur}s')

def check(p, vid_dur):
    errs = []; lines = p['lines']
    if abs(vid_dur - p['dur']) > 0.15: errs.append(f'video is {vid_dur:.2f}s but the voiceover plan is {p["dur"]}s: set window.DUR = VO.dur')
    if lines[0]['start'] > 0.5: errs.append('first word starts later than 0.5s')
    words = sum(len(l['words']) for l in lines); spoken = sum(l['words'][-1]['e'] - l['words'][0]['s'] for l in lines)
    flow = all(l.get('timing') == 'exact' for l in lines)
    if flow and not 2.6 <= words / spoken <= 3.8: errs.append(f'overall pace {words/spoken:.2f} w/s (needs 2.6-3.8): adjust "speed"')
    for i, l in enumerate(lines):
        if flow: pass
        elif not 2.5 <= l['wps'] <= 3.5: errs.append(f'line {i} pace {l["wps"]} w/s (needs 2.5-3.5): rewrite it shorter/longer')
        if i and not lines[i-1].get('hold') and l['start'] - lines[i-1]['end'] > 0.5: errs.append(f'silent gap of {l["start"]-lines[i-1]["end"]:.2f}s before line {i}')
    if vid_dur - lines[-1]['end'] > 1.2: errs.append(f'{vid_dur-lines[-1]["end"]:.2f}s of silence at the end')
    cov = sum(l['end'] - l['start'] for l in lines) / (vid_dur - sum(l.get('hold', 0) for l in lines))
    if cov < 0.75: errs.append(f'speech covers only {cov*100:.0f}% of the video (needs 75%+)')
    return errs, cov

def sfx(kind):
    """Small, clean UI sound effects (synthesized, royalty-free). Levels are relative to the voice."""
    r = np.random.default_rng(7)
    def env(d, a=0.003, k=30): tt = np.arange(int(d * SR)) / SR; return tt, np.clip(tt / a, 0, 1) * np.exp(-k * tt)
    if kind == 'tick':   tt, e = env(0.06, 0.001, 70); y = np.sin(2*np.pi*2600*tt) * e * 0.55
    elif kind == 'pop':  tt, e = env(0.12, 0.002, 38); f = 520 + 500 * np.exp(-30 * tt); y = np.sin(2*np.pi*np.cumsum(f)/SR) * e * 0.45
    elif kind == 'tap':  tt, e = env(0.05, 0.001, 90); y = (np.sin(2*np.pi*1500*tt) * 0.5 + r.normal(0, .3, len(tt))) * e * 0.5
    elif kind == 'whoosh':
        tt = np.arange(int(0.45 * SR)) / SR; nz = np.convolve(r.normal(0, 1, len(tt)), np.ones(30) / 30, 'same')
        y = nz * np.sin(np.pi * tt / 0.45) ** 2 * 0.35
    elif kind == 'swoosh':   # short UI slide
        tt = np.arange(int(0.25 * SR)) / SR; nz = np.convolve(r.normal(0, 1, len(tt)), np.ones(12) / 12, 'same')
        y = nz * np.sin(np.pi * tt / 0.25) ** 2 * 0.28
    elif kind == 'ding':  tt, e = env(0.6, 0.003, 6); y = (np.sin(2*np.pi*1318.5*tt) + .5*np.sin(2*np.pi*1975.5*tt)) * e * 0.3
    elif kind == 'error': tt, e = env(0.28, 0.003, 9); y = np.sign(np.sin(2*np.pi*170*tt)) * e * 0.12
    elif kind == 'type':  y = np.concatenate([sfx('tap') * 0.4, np.zeros(int(0.06 * SR))] * 3)
    else: raise ValueError(f'unknown sfx {kind}: use tick pop tap whoosh swoosh ding error type')
    return y

def mix(out, vid, final):
    p = json.load(open(f'{out}/timing.json'))
    vd = float(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', vid]).decode())
    errs, cov = check(p, vd)
    if errs:
        print('VOICEOVER CHECK FAILED:'); [print(' -', e) for e in errs]; sys.exit(1)
    n = int(SR * vd); voice = np.zeros(n + SR)
    for i, l in enumerate(p['lines']):
        a, _ = sf.read(f'{out}/line{i}.wav'); s = int(l['start'] * SR); e = min(len(voice), s + len(a)); voice[s:e] += a[:e - s]
    voice = voice[:n]; t = np.arange(n) / SR
    mixd = voice / max(np.abs(voice).max(), 1e-6) * 0.8
    if p.get('music'):   # off by default: the reference style is voice + sound effects only
        pad = np.zeros(n)
        for i, f in enumerate([87.31, 130.81, 174.61, 220.0, 261.63, 329.63]):
            for det in (-0.6, 0.6): pad += np.sin(2 * np.pi * (f + det) * t + i) * (0.9 if f < 200 else 0.5)
        pad *= (0.75 + 0.25 * np.sin(2 * np.pi * 0.18 * t)) * np.clip(t / 1.5, 0, 1) * np.clip((vd - t) / 1.0, 0, 1)
        pad = np.convolve(pad, np.ones(40) / 40, mode='same'); pad /= np.abs(pad).max(); mixd += pad * 0.8 * 10 ** (-24 / 20)
    fx = np.zeros(n)
    for c in p.get('cues', []):
        a = sfx(c['sfx']); s0 = int(c['t'] * SR); e = min(n, s0 + len(a))
        if 0 <= s0 < n: fx[s0:e] += a[:e - s0]
    mixd += fx * 0.6
    sf.write('/tmp/vo_raw.wav', mixd.astype(np.float32), SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/vo_raw.wav', '-af', 'highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,loudnorm=I=-13.5:TP=-1.0:LRA=8', '-ac', '2', '-ar', '48000', '/tmp/vo.wav'], check=True)
    meas = subprocess.run(['ffmpeg', '-i', '/tmp/vo.wav', '-af', 'ebur128', '-f', 'null', '-'], capture_output=True, text=True).stderr
    I = float(re.findall(r'I:\s+(-?[\d.]+) LUFS', meas)[-1]); gain = -13.0 - I   # second pass: land on -13 LUFS (reference ~-14)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', '/tmp/vo.wav', '-af', f'volume={gain:.2f}dB,alimiter=limit=0.93:level=false', '/tmp/vo2.wav'], check=True)
    os.replace('/tmp/vo2.wav', '/tmp/vo.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', vid, '-i', '/tmp/vo.wav', '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', final + '.tmp.mp4'], check=True)
    os.replace(final + '.tmp.mp4', final)
    print(f'ok {final}  (speech covers {cov*100:.0f}% of {vd:.1f}s)')

if __name__ == '__main__':
    if sys.argv[1] == 'plan': plan(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'mix': mix(sys.argv[2], sys.argv[3], sys.argv[4])
    else: print(__doc__)
