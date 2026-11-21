# Saturday 21 November 2026 — The World in One Day (v2)

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/reward.svg)](https://make.fun/bounty/news-image-20261121)

A make.fun bounty entry: one program that writes one image summing up the
world news of **Saturday 21 November 2026** — a 1024×1024 newspaper front
page with **35 stories across 7 regions and 15 fields**, every one dated
Saturday 21 November 2026.

This is a rebuild of the v1 entry (52 stories, rank #640). A study of the
top-10 entries showed the winners all use the same skeleton — 3 illustrated
leads, 10 feature cards, ~20 one-line briefs, a light map and a short DATE
CHECK — at 32–36 stories, in larger type. v2 follows that skeleton and
carries the consensus stories v1 missed: the Peru quake, the Kryvyi Rih
strike, the Davao landing, Bitcoin's Saturday low, and the evening's Brown
University shooting.

## The front page

- **3 big illustrated leads** — COP31 talks run into overtime with still no
  deal (Day 13); three Houthi missiles downed over Riyadh, two more over
  Jizan; a magnitude 6.7 quake shakes Peru, felt in Lima.
- **10 illustrated features** — the Kryvyi Rih double strike; the Air
  Niugini jet landing safe in Davao with 146 aboard; Bitcoin sinking to
  $56,814; the Brown University shooting; the Basra power-station fire; a
  second tanker hit off Khasab; the UN "killer robots" talks; Lewis Pugh's
  Hormuz swim; Alba Larsen's F1 Academy win from 9th; Rahul's 124*.
- **22 one-line briefs** with sources, a 6-number stat strip of Saturday's
  biggest figures, a region-count strip, a light dotted world map with
  numbered pins for the 13 lead and feature stories, and a short **DATE
  CHECK** box that names the Friday, Thursday and not-yet stories
  deliberately left out — so nothing from Friday's front pages is ever
  presented as Saturday news.

Every story carries a verification tag: **CONFIRMED** (2+ outlets),
**OFFICIAL** (on the record), or **REPORTED** (one outlet). Sources are
named beside each story. All illustrations are procedural drawings made in
code — no photos, no copied artwork.

## How it works

`main.ts` (Node 22, standard library only) copies the pre-built `entry.png`
to `$MAKEFUN_OUTPUT_DIR` (or `/output`), after validating the PNG signature,
the 1 MiB size limit and the 1024×1024 dimension limit (from the IHDR chunk). No network access at runtime. The image itself is
built by `compose.py` (PIL, DejaVu fonts); running it twice produces
byte-identical output.

```sh
python3 compose.py entry.png   # rebuild the image
node main.ts                   # copy it to /output/entry.png
```

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The front page: 1024×1024 PNG, ≤ 1 MiB |
| `main.ts` | Entrypoint: validates and copies `entry.png` |
| `compose.py` | Builds `entry.png` from scratch (deterministic) |
| `LICENSE` | MIT |

## Date discipline

This entry covers **Saturday 21 November 2026 only**, under the rule that a
story counts if it happened, or was first reported, on Saturday in at least
one time zone. Friday's Kyiv barrage, Wall Street sell-off, Trump AI tax,
UK–EU reset, Akvan landfall and Hodeidah port strike — Thursday's ICJ
Myanmar ruling and GTA VI launch — and not-yet items (BepiColombo's Mercury
capture, a final COP31 text, the Las Vegas GP race) appear only in the DATE
CHECK box, clearly labelled as not Saturday news. The Peru quake (00:09 UTC
Saturday) and the Davao landing (00:08 Saturday local time) are included
with their times stated.
