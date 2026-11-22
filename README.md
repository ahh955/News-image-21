# Saturday 21 November 2026 — The World in One Day (v3)

[![Competition](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![Rank](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard)
[![Reward](https://make.fun/badge/news-image-20261121/ahh955/News-image-21/reward.svg)](https://make.fun/bounty/news-image-20261121)

A make.fun bounty entry: one program that writes one image summing up the
world news of **Saturday 21 November 2026** — a 1024×1024 newspaper front
page with **36 stories across 7 regions and 17 fields**, every one dated
Saturday 21 November 2026.

This is a rebuild of the v2 entry (35 stories, rank #282). A fresh study of
the current top 10 showed v2's gaps: its feature cards were text-only while
every top entry illustrates all ten; its stories were unnumbered while the
winners number all of them 1–35 with the map keyed to those numbers; and it
spent vertical space on a big title above the date, where the winners make
the date itself the giant masthead. v3 fixes all three, promotes the
Verstappen pole, the Zelensky warning, the Iran uranium story, the Hormuz
drone claim and BepiColombo from briefs to features, updates Rahul to the
stumps figures (136, India 486/4), and adds a VOICES strip with two
verbatim quotes.

## The front page

- **3 big illustrated leads** — COP31 talks run into overtime with still no
  deal (Day 13); three Houthi missiles downed over Riyadh, two more over
  Jizan; a magnitude 6.7 quake shakes Peru, felt in Lima.
- **10 illustrated features** — the Kryvyi Rih double strike; the Air
  Niugini jet landing safe in Davao with 146 aboard; Bitcoin sinking to
  $56,814; the Brown University shooting; Verstappen's Las Vegas pole;
  Zelensky's Crimea-bridge warning; Iran keeping its uranium stockpile;
  Iran's Hormuz drone claim; BepiColombo reaching Mercury; Rahul's 136.
- **23 numbered one-line briefs** with sources, a **VOICES** strip (Zelenskyy
  and Trump, verbatim), a 6-number stat strip of Saturday's biggest figures,
  a region-count strip, a light dotted world map with numbered pins for the
  13 lead and feature stories, and a short **DATE CHECK** box that names the
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
story counts if it happened, or was first reported, on Saturday in at least
one time zone. Friday's Trump AI tax, UK–EU reset, Hodeidah port strike,
China–Japan Taiwan words, Kyiv barrage, Wall Street sell-off and Akvan
landfall — Thursday's ICJ Myanmar ruling and GTA VI launch — and not-yet
items (BepiColombo's Mercury capture, a final COP31 text, the Las Vegas GP
race) appear only in the DATE CHECK box, clearly labelled as not Saturday
news. The Peru quake (00:09 UTC Saturday) and the Davao landing (00:08
Saturday local time) are included with their times stated.
