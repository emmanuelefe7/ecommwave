# Daily grid plan (owner's standing rule, set 2026-11-25)

Every post on every row follows PLAYBOOK §0 HOOKS & LANGUAGE (strong store-owner hook, "customers" not "buyers", plain words).

Every day the profile grid gets exactly these rows (15 posts). Every row is published as a block, back to back,
so rows always stay whole. Read `PLAYBOOK.md` (brand, NAVY look §3b, LIGHT look §3c, captions, publishing, logging) first.

| Row type | Posts | What it looks like on the grid | Made by |
|---|---|---|---|
| **CONNECTED-6** | 6 (2 rows × 3) | One continuous, OBVIOUS mint line / arrow path running through all 6 tiles | daily connected-set task |
| **SIMILAR-3** | 3 (1 row) | 3 posts with the same template and look, each with a different message | autopilot run A |
| **N-L-N** | 3 (1 row) | navy · LIGHT · navy (one light post in the middle) | autopilot run B |
| **L-N-L** | 3 (1 row) | LIGHT · navy · LIGHT (light on both sides) | autopilot run C |

Grid reminder: the newest post shows top-left. To make a row read left→right as [A, B, C], publish **C, then B, then A**.
Keep text/faces/buttons ≥ 80 px from tile edges (the grid crops 34 px each side to 3:4); only decorative lines cross seams.

## CONNECTED-6 (2 rows)
- One page with `#pano` 3240×2700 px; render with `python3 tools/render_grid6.py page.html out prefix` → `_1.._6` + `_grid_preview.jpg`.
  Tiles: row 1 = `_1 _2 _3`, row 2 = `_4 _5 _6`. **Post order: _6, _5, _4, _3, _2, _1.**
- The connector must be OBVIOUS: a thick (10–16 px) glowing mint line or arrow path with nodes/arrowheads that runs through
  every tile — e.g. a snake path (left→right across row 1, curving down at the right edge, right→left across row 2), a
  numbered roadmap 1→6, a journey (visit → product → cart → checkout → order → repeat), a funnel. It must cross every
  vertical seam and the horizontal seam between the rows, so the six tiles read as one picture.
- Each tile still works alone (headline or step + one visual). Tile 1 = hook, tile 6 = CTA (DM “GROWTH”, ecommwave.org).
- Look: NAVY (§3b) by default (it's what the owner's connected banners use); a LIGHT (§3c) connected set may be used every
  other day for variety. Change the concept every day (check the last 5 CONNECTED rows in the log).
- Log 6 rows with Format `CONNECTED-6`.

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
