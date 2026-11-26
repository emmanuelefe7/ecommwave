# Daily grid plan (owner's standing rule, set 2026-11-25)

Every post on every row follows PLAYBOOK §0 HOOKS & LANGUAGE (strong store-owner hook, "customers" not "buyers", plain words).

Every day the profile grid gets exactly these rows (15 posts). Every row is published as a block, back to back,
so rows always stay whole. Read `PLAYBOOK.md` (brand, NAVY look §3b, LIGHT look §3c, captions, publishing, logging) first.

| Row type | Posts | What it looks like on the grid | Made by |
|---|---|---|---|
| **CONNECTED-6** | 6 (2 rows × 3) | 6 separate, self-contained posts in one matching template, visually joined on the grid by a decorative mint line | daily connected-set task |
| **SIMILAR-3** | 3 (1 row) | 3 posts with the same template and look, each with a different message | autopilot run A |
| **N-L-N** | 3 (1 row) | navy · LIGHT · navy (one light post in the middle) | autopilot run B |
| **L-N-L** | 3 (1 row) | LIGHT · navy · LIGHT (light on both sides) | autopilot run C |

Grid reminder: the newest post shows top-left. To make a row read left→right as [A, B, C], publish **C, then B, then A**.
Keep text/faces/buttons ≥ 80 px from tile edges (the grid crops 34 px each side to 3:4); only decorative lines cross seams.

## CONNECTED-6 (2 rows) — six SEPARATE posts that connect on the grid
**Owner's rule (2026-11-26): "it should be different posts that are connected, not a single post spread over 6 — users won't
understand, and not all users see all 6 posts at once."** Never again split one design or one message across tiles.
- Make **6 independent posts**. Each one is a complete post on its own: its own hook headline, its own visual and its own
  short point, plus small logo/ecommwave.org. Someone who sees only that one post in their feed must fully understand it.
  - NO "Step 1/2/3…" numbering that needs the other posts, NO sentence or headline continued on the next tile, NO
    "follow the path", NO tile that is only a label or only a fragment of a picture.
  - Pick 6 different tips/messages on one theme (e.g. 6 ways to get repeat customers, 6 trust fixes, 6 checkout fixes);
    tile 6 can be a CTA post (free store audit, DM “GROWTH”) but it must still make sense alone.
  - A message that needs several steps in order belongs in ONE carousel post, not across the grid.
- The **connection is only visual, on the profile grid**: all 6 use the same template, palette and headline style, and a
  thin decorative mint line/wave runs along the edges (e.g. a band near the bottom of row 1 / top of row 2) so the 6 tiles
  look joined when viewed together. The line must never carry meaning (no numbered nodes, no arrows that point to "the next
  post"); each tile looks finished even with the line cut off at its edges.
- Build: one `#pano` 3240×2700 page, render with `python3 tools/render_grid6.py page.html out prefix` → `_1.._6` +
  `_grid_preview.jpg`. Tiles: row 1 = `_1 _2 _3`, row 2 = `_4 _5 _6`. **Post order: _6, _5, _4, _3, _2, _1.** Besides the
  grid preview, LOOK at each tile alone and ask "does this make sense to someone who sees only this post?" If not, fix it.
- Each post gets its OWN full caption (hook line, 3–6 lines of value about that post's tip, CTA, exactly 5 hashtags). Never
  write "see the other posts"/"swipe the grid".
- Text/faces/buttons ≥ 80 px from tile edges; only the decorative line crosses seams.
- Look: NAVY (§3b) by default; LIGHT (§3c) every other day is fine. Change the theme every day (check the last 5 CONNECTED rows).
- Log 6 rows with Format `CONNECTED-6`.
- Do NOT repeat the 2026-11-25 "4-fix path" or 2026-11-26 "comeback path" style (one story split into numbered tiles) —
  the owner rejected it.

## SIMILAR-3 (1 row)
- 3 posts built from ONE template (same layout, colors, headline style, decoration positions) so the row looks like a set,
  but each says something different (e.g. 3 quick tips, 3 services, 3 mistakes, problem/solution/result, 3 questions).
  Example the owner likes: "Before running ads" / "These 3 emails" / "Traffic & Revenue" (same light card-stack look), or the
  navy "Get a free store audit / Stores that actually sell / Get a free store audit" banners.
- Alternate the look day to day: LIGHT one day, NAVY the next. Images or carousels (cover follows the template).
- Log 3 rows with Format `SIMILAR-3`.

## N-L-N (1 row): navy · light · navy
- Left = navy GROWTH VIDEO (Reel, what store owners need to grow) · Middle = LIGHT carousel or single · Right = navy MISTAKES VIDEO (Reel).
- Publish order: right (mistakes video), middle (light), left (growth video).
- Log 3 rows with Format `N-L-N` (topic says which slot).

## L-N-L (1 row): light · navy · light
- Left = LIGHT carousel · Middle = navy Reel or navy carousel · Right = LIGHT single (different light layout from the left one).
- Publish order: right, middle, left.
- Log 3 rows with Format `L-N-L`.

## Alignment check (every run, before publishing)
Count grid posts (Windsor get_data FEED + REELS, last 7 days, no force_refresh) newer than the newest tile of the latest CONNECTED-6 (or older TRIPTYCH) set in the log.
If that count isn't a multiple of 3 (a one-off post went up), first publish 1 or 2 extra posts in the matching look to complete
that row, then publish your row. Say in the final message whether the grid is aligned.
