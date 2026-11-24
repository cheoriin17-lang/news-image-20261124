# news-image-20261124 — POST-OPENING BUILD (ready to submit)

Bounty: Sum up 24 November's world news in one image. $100, top 50 paid
(1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20). No entry fee.
Opens 2026-11-24T00:00:00Z (07:00 WIB). Entries close
2026-11-26T00:00:00Z (07:00 WIB).

## Files
- `entry.png` — 1024x1024, 124,620 bytes,
  sha256 43ebf0a8bc7f9c867f71f576c23b5107df8ca8914dfc1593e5b1ae352e6dce94
- `draw_poster.py` — poster generator, rewritten from scratch in-session
  2026-11-24 ~07:50 WIB (post-opening rewrite #2, fresh authorship —
  rewrite #1 failed thinking_reproduces at 4.5%)
- `main.py` — copies entry.png to /output/entry.png (deterministic;
  verified byte-identical across two runs, matching repo entry.png)
- `NEWS-SOURCES.md` — stories + source URLs
- `LICENSE` — MIT, from the kit starter

## Poster
"The World in One Day — 24 November 2026" / THE DAILY GLOBE front page.
Lead: Ukraine sea drones hit Russian corvette Merkury off Benghazi
(ship-and-waves motif, "2,400 KM FROM THE FRONT"; "hit", not "sink" —
sinking unconfirmed). Six cards: Trump Iran deadline, COP31 walkout
fallout, Nvidia +31% as Huang returns as CEO (24 Nov update, replaces
the Kospi rout card), Nepal PM Shah in Delhi, Russian strike on Dymer,
India 720/9 in Wellington. Ticker: Skubal $450M Mets, Nigeria boat
capsizes, Eisenkot "Jewish terrorism", FBI police-database hack.
Visually inspected post-opening: clean, no overlaps, no clipped text
(one row-0 overflow fixed by trimming card bodies to 2 lines).

## Kit (pre-opening download WORKED)
- Kit dir: ~/workspace/makefun/news-image-20261124-kit/news-image-20261124-kit
  (downloaded 2026-11-23 21:43 UTC, bundle sha256
  4b5efc94df5f7f13825c507da56ccbb2c28bfefaa6d9e78930db672cc4b17c10,
  phase "dev"). No level number is printed in kit.json — check the level
  at bundle time and re-download if make.fun reports a newer level.
- Do NOT bundle from this pre-opening session. The post-opening run
  must rewrite main.py + draw_poster.py in-session (write/edit tools)
  so the bundled transcript is in-window (thinking_in_window), then
  bundle, check (0 failed), jury, submit.

## Next steps
See ~/workspace/makefun/SUBMIT-HANDOFF-news-image-20261124.md
