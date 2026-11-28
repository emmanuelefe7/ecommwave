# Voice-over delivery (owner's standing instructions, 2026-11-26) — applies to EVERY reel AND every video

**APPROVED by the owner ("Good 👍 save this for all my reels and videos voice overs. Match everything together"):**
the settings below, exactly as in `work_reel_demo/` (`final.mp4`), are locked for every voice-over: one-off videos,
reels in every row type, ads, anything with a voice. Use `tools/voiceover.py` with its defaults — voice `am_puck`,
`lang` en-us (simple neutral English), `speed` 1.05, flow/tighten/letters/emphasis/breaths on, no music, −13 LUFS —
and `reel.js` word-synced captions/cues. Don't change any of it unless the owner asks.

## The owner's instructions (verbatim)
VOICE-OVER DELIVERY INSTRUCTIONS

Deliver the voice-over exactly as written in the provided script. Do not rewrite, paraphrase, omit, add, or rearrange any words.

Speak naturally, like a real human narrator having a clear, confident and engaging conversation.

Strict punctuation and speech delivery rules:

1. Comma (,): When you encounter a comma, make a natural, brief pause while maintaining the flow of the sentence. Do not make the pause too long or sound disconnected.
2. Full stop (.): When you encounter a full stop, complete the sentence with a natural falling intonation. Allow a meaningful pause before starting the next sentence.
3. Question mark (?): When you encounter a question mark, deliver the sentence with a natural questioning tone, using appropriate vocal inflection that makes it sound like a genuine question.
4. Sentence flow: Understand how each sentence connects to the next. Blend related words and phrases smoothly without unnecessary pauses or robotic breaks.
5. Natural breathing: Use subtle, realistic breathing and conversational pauses where appropriate. Avoid unnatural gaps between words.
6. Emphasis: Naturally emphasize important words and phrases without exaggerating or sounding theatrical.
7. Tone and emotion: Maintain a confident, warm, professional, persuasive and slightly energetic tone. Sound knowledgeable, approachable and genuinely interested in what you are saying.
8. Consistency: Maintain consistent vocal identity, pitch, volume, accent and speaking style throughout the entire recording.

MOST IMPORTANT:

Read the script exactly as written. Respect every punctuation mark. Understand the meaning of each sentence before speaking it. Know when to pause, when to continue, when to blend words together and when to change your vocal expression.

The final delivery must sound like a real, articulate human professional speaking naturally to another person, NOT an AI reading text aloud.

Avoid robotic pronunciation, monotonous delivery, exaggerated expressions, unnatural pauses and rushed sentences.

The goal is a smooth, believable, professionally recorded commercial voice-over with excellent timing, clarity and natural human expression.

## Accent (owner, 2026-11-26, updated)
**Simple, neutral English accent** — clear and easy for everyone to understand, not a strong British or regional accent:
`"lang": "en-us"`, default voice `am_puck` (male, owner's pick). Don't use the British voices unless the owner asks again.
Plain, simple words in the script (short sentences, everyday vocabulary).

## How `tools/voiceover.py` carries this out (don't bypass it)
- **Exactly as written**: the text in `script.json` is spoken as is — the tool never adds, removes or changes words or
  punctuation (only the `*accent*` marks are stripped). So the SCRIPT must already be final: write numbers and symbols
  as words ("two weeks", not "2 wks"), and put every comma / full stop / question mark exactly where the pause belongs.
- **Comma** → brief pause (~0.16 s) inside the flowing sentence. **Full stop / question mark** → falling or questioning
  intonation from the voice model + a meaningful pause (~0.38 s) before the next sentence. A line with NO end
  punctuation blends straight into the next line (use that on purpose for one sentence split over two caption lines).
- **Flow**: each section is spoken as ONE continuous passage (never line by line), so sentences connect naturally;
  no per-line speed forcing; no gaps between words.
- **Breathing**: a soft, quiet inhale is placed inside longer sentence pauses (`"breaths": true`, default).
- **Emphasis**: words marked `*like this*` get a gentle lift (+2.5 dB, smooth ramps) and the accent colour in the captions.
  Mark only the 1–3 words per line that matter.
- **Tone**: confident, warm, slightly energetic — pace `"speed"` 1.0–1.1 (default 1.05, ~3 words/sec). Write lines the way
  a person talks; questions as real questions.
- **No dragged words**: any word spoken longer than its sounds need (e.g. "buy") is shortened automatically with
  pitch kept (`tighten_words`, owner feedback 2026-11-26).
- **Letters said as letters**: a lone capital letter is spoken as its letter name ("A" = ay, "B" = bee) with a clear,
  unhurried length; "A" is treated as a letter only when the script also uses another lone letter (A or B), otherwise it's
  the normal word "a". The caption still shows the letter (owner feedback 2026-11-26).
- **Consistency**: one voice and ONE fixed voice style for the whole video, one speed, loudness −13 LUFS.
- Limits of the engine: it can't take free-text acting directions, so tone comes from the voice choice, pace,
  punctuation and accent marks. Write the script for the ear.

## Fix bridge (owner, 2026-11-28 — every video with a problem and a fix)
Owner: "It talks about the product and continues with the fix, no pause or hold that make people understand it's talking
about the fix. Before start talking about the fix say it loud: 'Want to fix this? Here's how!'"
- Between the last problem line and the first fix line, always add the line
  `{"text": "Want to fix this? *Here's how!*", "chapter": "THE FIX", "loud": true, "hold": 0.5}`
  and set `"hold": 0.7` on the last problem line, so there is a clear pause before it and after it.
- `"loud": true` makes `voiceover.py` say that line clearly louder (+4.5 dB) than the rest. On screen it gets the big
  full-frame title card `RL.bridge` (see PLAYBOOK › REEL STYLE › FIX BRIDGE).

## ElevenLabs (owner, 2026-11-28: "Use ElevenLabs for my voice over") — PENDING, not active yet
- Wanted: ElevenLabs voice for every reel. Tested 2026-11-28 with voice "Lowell – Warm, Confident, Conversational"
  (`XxGp0QgHUscY6yYqUxAi`, American), model `eleven_v4`, 1 take: it read the script word for word (checked by
  transcription), ~420 credits per 25–30 s reel. The account is on the FREE plan (10,000 credits/month = ~20 reels).
- Pipeline is ready: `tools/el_voice.py` (text → generate → transcribe → plan timings → render silent → mix in the
  ElevenLabs sandbox). Test: `work_nln4/script_m.json`, `vo_m_el/`, `reel_m_el.html`.
- BLOCKER: this workspace can't download the ElevenLabs audio/video (elevenlabsusercontent.com is not allowed by the
  network settings, and copying it out another way is not allowed), and the sandbox output has no public URL for
  Instagram. Until the owner allows that host in the environment's network access, keep using Kokoro `am_puck` via
  `voiceover.py` and do NOT spend ElevenLabs credits in scheduled runs.
