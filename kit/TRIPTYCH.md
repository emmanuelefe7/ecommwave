> **Owner rule 2026-11-26:** connected sets must be SEPARATE, self-contained posts that only look connected on the grid — never one design or message split across tiles. See GRID_PLAN.md › CONNECTED-6. Where this file says otherwise, GRID_PLAN.md wins.

# Daily connected grid set (3 posts that join into one banner)

The owner LOVES the connected 3-post banner (see `profile/banner2_full.png`, template `tpl_triptych_banner.html`). Once a day you design a NEW connected set and post its 3 tiles back to back. Read `PLAYBOOK.md` first (brand rules §3, the navy look §3b, publishing §7) — everything there applies.

## Design rules
- Build ONE panorama page: an element `#pano` of exactly 3240×1350 px (copy `tpl_triptych_banner.html` and change it). Tiles are x 0–1080 (LEFT), 1080–2160 (MIDDLE), 2160–3240 (RIGHT).
- **Connected**: at least one continuous element runs across all three tiles — the mint wave lines, a glowing path/line with nodes, a gradient light beam, a row of floating UI cards, a timeline, a before→after flow. The background gradient flows across the seams.
- **Safe zones**: Instagram's grid crops 34 px off each side of every tile and adds a gap, so keep ALL text, faces, buttons and important UI ≥ 80 px from every tile edge (x = 0, 1080, 2160, 3240) — only decorative lines/gradients may cross a seam.
- **Each tile also works alone** (people see them one at a time in the feed): LEFT = brand/hook, MIDDLE = the value or the "how", RIGHT = proof or CTA (DM “GROWTH”, ecommwave.org).
- Deep navy brand look (§3b): navy gradient, mint accent, white ExtraBold headlines with one Instrument Serif italic mint phrase, realistic clean UI (phone/browser NOVA store, order cards, gauges, chips), brand photos in the mint-offset arch (`assets/woman.png`, `assets/man.png`). Clean and premium, lots of space. No 3D renders, no light-grey backgrounds.
- **Change the design every day but keep it connected.** Rotate concepts, e.g.: services wave banner · 3-step process (nodes on one mint line) · mistake → fix → result · before/after store (cluttered → clean) · problem / solution / CTA with a phone moving across · 3 quick tips joined by a timeline · "a day in your store" (visit → cart → order) · brand promise / services / free audit. Check `content-log.md` (rows with Format `TRIPTYCH`) and don't repeat the last 5 concepts.

## Render, check, post
1. `python3 tools/render_triptych.py <page>.html <out_dir> <prefix>` → `<prefix>_1.jpg` (LEFT), `_2` (MIDDLE), `_3` (RIGHT), `_full.png`, `_grid_preview.jpg`.
2. LOOK at `_grid_preview.jpg` and `_full.png` with the Read tool. Fix anything clipped at a seam, crowded, off-brand or unreadable, then re-render.
3. Save to `posts/<YYYY-MM-DD-HHMM>-triptych-<slug>/` and push (PLAYBOOK §7); verify each raw URL returns 200.
4. Post with Windsor `create_image_post` IN THIS ORDER, one after the other with nothing in between: **RIGHT (_3), then MIDDLE (_2), then LEFT (_1)** — the newest post appears at the top-left of the grid. Each with alt text and its own caption: RIGHT and MIDDLE get a short caption (2–4 lines + CTA + 3–5 hashtags); LEFT (posted last, seen first) gets the full message caption with exactly 5 hashtags.
5. Log three rows in `content-log.md` with Format `TRIPTYCH` (concept name in Topic), commit and push.
6. Finish with a short message: concept, the three media ids, and a reminder that the owner can pin the three tiles (pin RIGHT first, then MIDDLE, then LEFT) to keep today's set at the top of the profile.
