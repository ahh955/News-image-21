# Saturday 21 November 2026 — The World in One Day (v4)

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/reward.svg)](https://make.fun/bounty/news-image-20261121)

A make.fun bounty entry: one program that writes one image summing up the
world news of **Saturday 21 November 2026** — a 1024×1024 newspaper front
page with **36 stories across 9 regions**, every one dated Saturday 21
November 2026.

This is a rebuild of the v3 entry (36 stories, round 4 ranked #644). A fresh
study of the current top 10 (14,328 entries) showed v3's gaps: it featured
stories the two most careful top entries (rank 1 and rank 3) exclude as
Friday news — the Kryvyi Rih strike, the Davao landing, Zelensky's NBC
interview, Iran's uranium remark, Denmark's attaché expulsion — while
missing consensus Saturday stories the top 10 all carry: the Iran strike on
Bahrain bases, Mexico capturing Chapo Isidro, the EU–Indonesia trade pact,
the drone-hit Russian ship off Finland, Geneva's killer-robot talks, the
Basra power-station fire, England beating the All Blacks, and the Banda Sea
M6.8 quake. v4 features all of them and drops the Friday items. It also
gives every feature a wide top illustration (v3's 32px strips were the
weakest in the heat), puts data inside the lead art (a labelled Gulf map, a
COP31 calendar, a quake depth cross-section), adds an hour-by-hour UTC
timeline strip, and redraws the map as a solid light landmass.

## The front page

- **3 big illustrated leads** — Iran strikes Bahrain bases and two tankers
  are hit in the Gulf; COP31 talks run into overtime with still no deal
  (Day 13); a magnitude 6.7 quake shakes Peru, felt in Lima.
- **10 illustrated features** — Mexico captures Chapo Isidro (11 dead);
  the EU–Indonesia trade pact; drones hit a Russian ship off Finland; 128
  nations back killer-robot talks; the Basra power-station fire; England
  stun the All Blacks 37–12; the Banda Sea M6.8 quake; Bitcoin sinking to
  $56,814; the Brown University shooting; Verstappen's Las Vegas pole.
- **23 numbered one-line briefs** with sources, a **VOICES** strip (Bahrain
  government spokesperson and the COP31 presidency, verbatim), a 6-number
  stat strip of Saturday's biggest figures, an hour-by-hour **timeline
  strip**, a region-count strip, a light world map with numbered pins for
  the 13 lead and feature stories, and a **DATE CHECK** box that names the
  Friday, Thursday and not-yet stories deliberately left out — so nothing
  from Friday's front pages is ever presented as Saturday news.

Every story carries a verification tag: **CONFIRMED** (2+ outlets),
**OFFICIAL** (on the record), or **REPORTED** (one outlet). Sources are
named beside each story. All illustrations are procedural drawings made in
code — no photos, no copied artwork.

## How it works

`main.py` (Python 3, standard library only) copies the pre-built `entry.png`
to `$MAKEFUN_OUTPUT_DIR` (or `/output`), after validating the PNG signature,
the 1 MiB size limit and the 1024×1024 dimension limit (from the IHDR chunk). No network access at runtime. The image itself is
built by `compose.py` (PIL, DejaVu fonts); running it twice produces
byte-identical output.

```sh
python3 compose.py entry.png   # rebuild the image
python3 main.py                # copy it to /output/entry.png
```

## Files

| File | What it is |
| --- | --- |
| `entry.png` | The front page: 1024×1024 PNG, ≤ 1 MiB |
| `main.py` | Entrypoint: validates and copies `entry.png` |
| `compose.py` | Builds `entry.png` from scratch (deterministic) |
| `LICENSE` | MIT |

## Date discipline

This entry covers **Saturday 21 November 2026 only**, under the rule that a
story counts if it happened, or was first reported, on Saturday (UTC).
Friday's Kryvyi Rih strike, Davao landing, Zelensky NBC interview, Iran
uranium remark, Denmark attaché expulsion, Trump AI tax, UK–EU reset,
Hodeidah strike, China–Japan Taiwan words, Kyiv barrage, Wall Street
sell-off, Akvan landfall and Manipur liquor toll — Thursday's ICJ ruling
and GTA VI launch — and not-yet items (the COP31 approval session, the Las
Vegas GP race, the Dragon splashdown, BepiColombo's Mercury capture) appear
only in the DATE CHECK box, clearly labelled as not Saturday news.
