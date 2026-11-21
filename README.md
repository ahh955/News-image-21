# Saturday 21 November 2026 — The World in One Day

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/reward.svg)](https://make.fun/bounty/news-image-20261121)

A make.fun bounty entry: one program that writes one image summing up the
world news of **Saturday 21 November 2026** — a 1024×1024 newspaper front
page with **52 stories across 7 regions and 13 fields**, every one dated
Saturday 21 November 2026.

## The front page

- **3 big illustrated leads** — Gen Z protests flood the streets in 25
  European countries; the Saudi-led coalition downs 3 Houthi missiles as the
  Gulf war widens; BepiColombo fires its engine tonight for Mercury orbit
  after an 8-year journey.
- **13 illustrated features** — COP31 in overtime, Rutte in Warsaw after the
  Poland incursion, Putin rejecting any ceasefire, Cyclone Akvan's aftermath,
  Dragon's splashdown tonight, Anthropic's Riemann-hypothesis claim (marked
  UNVERIFIED), F1 Las Vegas qualifying, the HIMARS strike in Sumy, KL Rahul's
  SENA century set, Gaza's child toll passing 22,000, Denmark and Somalia
  expelling diplomats, Kim Jong Un crossing into China by a new bridge.
- **36 one-line briefs** with sources, a UTC timeline of the day, a stat
  strip of Saturday's biggest numbers, a dark world map with numbered pins,
  and a prominent **DATE CHECK** box that names the Friday, Thursday and
  earlier stories deliberately left out — so nothing from Friday's front
  pages is ever presented as Saturday news.

Every story carries a verification tag: **CONFIRMED** (2+ outlets),
**OFFICIAL** (on the record), or **REPORTED** (one outlet). Sources are
named beside each story. All illustrations are procedural drawings made in
code — no photos, no copied artwork.

## How it works

`main.ts` (Node 22, standard library only) copies the pre-built `entry.png`
to `$MAKEFUN_OUTPUT_DIR` (or `/output`), after validating the PNG signature,
the 1 MiB size limit, and the 1024×1024 dimension limit. No network access
at runtime. The image itself is built by `compose.py` (PIL, DejaVu fonts);
running it twice produces byte-identical output.

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
| `.makefun/owner.json` | Payout wallet |

## Date discipline

This entry covers **Saturday 21 November 2026 only**. Friday's Kyiv barrage,
the Kh-101 crash in Poland, the market sell-off, Cyclone Akvan's landfall and
the Peru quake — and Thursday's ICJ ruling, Shenzhen summit, GTA VI launch and
Crimean Bridge strike — appear only in the DATE CHECK box, clearly labelled
as not Saturday news.
