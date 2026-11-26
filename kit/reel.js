/* reel.js — word-synced Reel engine (owner's reference style, 2026-11-26).
   Everything is a pure function of t (seconds) so render_video.py can step frame by frame.
   Needs vo/timing.js (window.VO from tools/voiceover.py plan: lines[].words[{w,s,e,hl}], lines[].chapter, cues[]).

   RL.W('word', line)           -> start time of that spoken word (exact, from the voice model)
   RL.L(line)                   -> {start,end,...} of a line
   RL.caption(el, t)            -> word-by-word caption: each word rises in with a blur exactly when it is spoken,
                                   accent words (*word* / "quotes" in the script) in the accent colour
   RL.chapter(el, t)            -> small black pill label ("THE SETUP") that pops when the chapter changes
   RL.cam(t, keys)              -> continuous camera: keys [{t, s, x, y, d}] (scale, offset px, move duration d)
   RL.pop(t, t0, d)             -> 0..1 with overshoot (labels / pins popping in on their word)
   RL.ease(t, t0, d, fn)        -> 0..1 eased progress
   RL.draw(t, t0, d)            -> 0..1 for drawing a highlight box (use with stroke-dashoffset)
   RL.ripple(el, t, t0)         -> tap ripple
   RL.scribble(el, t, t0, d)    -> reveal handwritten note left->right
   RL.countdown(el, t, t0, n)   -> OPTIONAL "A or B?" ring countdown (only when the topic is a real comparison)
*/
(function () {
  const C = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
  const E = {
    out: x => 1 - Math.pow(1 - x, 3),
    inout: x => (x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2),
    back: x => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); },
    expo: x => (x >= 1 ? 1 : 1 - Math.pow(2, -10 * x)),
  };
  const norm = s => s.toLowerCase().replace(/[^a-z0-9]/g, '');
  const RL = {
    E,
    ease(t, t0, d = .5, fn = 'out') { return E[fn](C((t - t0) / d)); },
    pop(t, t0, d = .38) { const p = C((t - t0) / d); return p <= 0 ? 0 : E.back(p); },
    draw(t, t0, d = .35) { return E.out(C((t - t0) / d)); },
    L(i) { return VO.lines[i]; },
    W(word, line) {
      const ls = line == null ? VO.lines : [VO.lines[line]];
      for (const l of ls) for (const w of l.words) if (norm(w.w) === norm(word)) return w.s;
      console.warn('RL.W: word not found', word, line); return line == null ? 0 : VO.lines[line].start;
    },
    lineAt(t) { let k = -1; VO.lines.forEach((l, i) => { if (t >= l.start - 0.06) k = i; }); return k; },

    /* ---------- captions ---------- */
    _capKey: null,
    caption(el, t, o = {}) {
      const i = this.lineAt(t);
      if (i < 0) { el.innerHTML = ''; this._capKey = null; return; }
      const l = VO.lines[i], next = VO.lines[i + 1];
      // hide the line shortly after it ends if a hold / long gap follows (e.g. countdown), else keep until next line
      const until = next ? (l.hold ? l.end + (o.holdShow ?? 0.5) : next.start - 0.06) : 1e9;
      if (this._capKey !== i) {
        el.innerHTML = l.words.map(w => `<span class="rw${w.hl ? ' hl' : ''}">${w.w}</span>`).join(' ');
        this._capKey = i;
      }
      const spans = el.children; const fadeOut = C((t - until) / 0.12);
      l.words.forEach((w, j) => {
        const p = E.out(C((t - w.s + 0.03) / (o.rise ?? 0.2)));
        const sp = spans[j];
        sp.style.opacity = (p * (1 - fadeOut)).toFixed(3);
        sp.style.transform = `translateY(${((1 - p) * (o.dy ?? 26)).toFixed(1)}px) scale(${(0.96 + 0.04 * p).toFixed(3)})`;
        sp.style.filter = p < 1 ? `blur(${((1 - p) * (o.blur ?? 9)).toFixed(1)}px)` : 'none';
      });
    },

    /* ---------- chapter pill ---------- */
    _chap: null,
    chapter(el, t) {
      let name = null, t0 = 0;
      VO.lines.forEach(l => { if (l.chapter && t >= l.start - 0.25) { name = l.chapter; t0 = l.start - 0.25; } });
      if (!name) { el.style.opacity = 0; return; }
      if (this._chap !== name) { el.textContent = name; this._chap = name; }
      const p = this.pop(t, t0, .4);
      el.style.opacity = C(p * 1.5); el.style.transform = `translateX(-50%) scale(${(0.6 + 0.4 * p).toFixed(3)})`;
    },

    /* ---------- camera ---------- */
    cam(t, keys) {
      let s = keys[0].s ?? 1, x = keys[0].x ?? 0, y = keys[0].y ?? 0, r = keys[0].r ?? 0;
      for (let i = 1; i < keys.length; i++) {
        const k = keys[i]; const p = E.inout(C((t - k.t) / (k.d ?? .6)));
        if (p <= 0) break;
        const ns = k.s ?? s, nx = k.x ?? x, ny = k.y ?? y, nr = k.r ?? r;
        s += (ns - s) * p; x += (nx - x) * p; y += (ny - y) * p; r += (nr - r) * p;
      }
      return { s, x, y, r, css: `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) scale(${s.toFixed(4)}) rotate(${r.toFixed(2)}deg)` };
    },

    /* ---------- small effects ---------- */
    ripple(el, t, t0) {
      const p = C((t - t0) / .55);
      el.style.opacity = p <= 0 || p >= 1 ? 0 : (1 - p).toFixed(3);
      el.style.transform = `translate(-50%,-50%) scale(${(0.3 + 1.2 * E.out(p)).toFixed(3)})`;
    },
    scribble(el, t, t0, d = .45) {
      const p = E.out(C((t - t0) / d));
      el.style.clipPath = `inset(-20% ${((1 - p) * 100).toFixed(1)}% -20% 0)`; el.style.opacity = p > 0 ? 1 : 0;
    },
    countdown(el, t, t0, n = 3, step = 0.8) {
      const k = Math.floor((t - t0) / step); const on = t >= t0 && k < n;
      el.style.opacity = on ? 1 : 0; if (!on) return;
      const f = ((t - t0) % step) / step;
      el.querySelector('.cd-n').textContent = n - k;
      el.querySelector('.cd-n').style.transform = `scale(${(0.7 + 0.3 * E.back(C(f / .35))).toFixed(3)})`;
      const ring = el.querySelector('.cd-ring'); const L = 2 * Math.PI * 120;
      ring.style.strokeDasharray = L; ring.style.strokeDashoffset = (L * f).toFixed(1);
    },
  };
  window.RL = RL;
})();
