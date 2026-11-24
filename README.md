# news-image-20261124 — SUBMITTED (live) + v2 variant built 2026-11-24

Bounty: Sum up 24 November's world news in one image. $100, top 50 paid
(1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20). No entry fee.
Entries close 2026-11-26T00:00:00Z (07:00 WIB).
Live submission: 01a20b0c-08a9-74da-a009-9751843db131 (commit 9a5dd82).
Round 1 not yet judged at v2 build time — v2 aims to rank higher.

## Files (v2 variant, split layout, built 2026-11-24 ~19:15 WIB)
- `entry.png` — 1024x1024, 129,538 bytes,
  sha256 8f0149453d7e90f4b70ca3b3616c072104365ffeac5c4953955a8bb91f4bdf15
- `draw_poster.py` — poster generator, rewritten from scratch in-session
  2026-11-24 for the v2 resubmit (left lead column + "by the numbers"
  strip + tall dusk-sea illustration panel — same verified facts)
- `main.py` — copies entry.png to /output/entry.png (deterministic;
  verified byte-identical across two runs, matching repo entry.png)
- `NEWS-SOURCES.md` — stories + source URLs
- `LICENSE` — MIT, from the kit starter

## Poster (v2)
"The World in One Day — 24 November 2026" / THE DAILY GLOBE front page.
Lead: Ukraine sea drones hit Russian corvette Merkury off Benghazi
("hit", not "sink" — sinking unconfirmed), with a 7 / 2,400 KM / 2 ships
fact strip. Six cards: Trump Iran deadline, COP31 walkout fallout,
Nvidia +31% as Huang returns as CEO, Nepal PM Shah in Delhi, Russian
strike on Dymer, India 720/9 in Wellington. Ticker: Skubal $450M Mets,
Nigeria boat capsizes, Eisenkot "Jewish terrorism", FBI police-database
hack. Visually inspected: clean, no overlaps, no clipped text.

## Jury
- Head-to-head v2-vs-live jury prompt:
  ~/workspace/makefun/news-image-20261124-jury-prompt-v2-vs-live.txt
- Resubmit ONLY on a clear jury GO for v2; if the jury is down (503),
  do NOT resubmit blind — this is a jury-taste bounty.

## Kit
- Kit dir: ~/workspace/makefun/news-image-20261124-kit/news-image-20261124-kit
  (level 39; site at level 42 as of 2026-11-24 ~19:00 WIB — bundle/check
  step must confirm the server still accepts it, or re-download first).
- Quota (checked 2026-11-24 ~19:00 WIB): 1 entry made, 5 of 6 left today,
  hard limit 39 of 40, can submit now. This blind round's entry used;
  next round opens after 2026-11-24T12:00:00Z.

## Next steps
Bundle with the kit + --system-prompt ~/workspace/system/system_prompt.md;
kit check must be 0 failed; submit from the kit dir only on jury GO.
Save claim code + submission ID only in ~/workspace/makefun/submissions.md.
Handoff: ~/workspace/makefun/SUBMIT-HANDOFF-news-image-20261124.md (live).
