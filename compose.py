#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261121 (v3 rebuild).

A 1024x1024 newspaper front page summing up Saturday 21 November 2026:
3 illustrated leads + 10 ILLUSTRATED feature cards + 23 one-line briefs +
a light dotted world map with numbered pins + VOICES quotes + a short
DATE CHECK box. All 36 stories are numbered 1-36; the map legend is keyed
to those numbers.

v3 vs v2 (top-10 study, ~/workspace/makefun/news-image-21-v3-top10/):
- the date is the giant masthead (the big "THE WORLD IN ONE DAY" title is
  dropped to a small top line, as in the top entries);
- every feature card gets a small picture strip (v2's features were text
  only — the biggest visual gap vs the top 10);
- taller, richer lead art (thermometer on COP31, stars over Riyadh, depth
  marker on the quake);
- Verstappen pole, Zelensky, Iran uranium, Hormuz drone and BepiColombo
  promoted from briefs to features; Rahul updated to the stumps figures
  (136, India 486/4, lead 118); Brown shooting kept (the top 10 missed it).

Date discipline: every story happened, or was first reported, on Saturday
21 November 2026 in at least one time zone. Friday 20 Nov items (Trump AI
tax, UK-EU reset, Hodeidah port strike, China-Japan Taiwan words, Kyiv
barrage, Wall Street sell-off, Akvan landfall) are named in DATE CHECK and
kept out, even though several top-10 entries carry them as Saturday news.

Deterministic: no randomness, no clock, no network. Running it twice
produces byte-identical output (PIL writes no timestamps into the PNG).

Usage: python3 compose.py [output-path]   (default: entry.png)
"""

import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 14
CW = W - 2 * MARGIN  # 996, content width

# Palette: light paper, black ink, newspaper red.
PAPER = (247, 243, 234)
INK = (26, 26, 26)
RED = (179, 32, 44)
DARK = (31, 31, 31)
GREY = (110, 108, 100)
LINE = (200, 192, 172)
CARD_BG = (255, 252, 244)
MAP_BG = (239, 231, 211)
MAP_LAND = (183, 167, 126)
WHITE = (255, 255, 255)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
LIB_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def libfont(name, size):
    return ImageFont.truetype(LIB_DIR + name, size)


F_STRIP = font("DejaVuSans-Bold.ttf", 12)
F_MAST = font("DejaVuSerif-Bold.ttf", 54)
F_SUBLINE = libfont("LiberationSerif-Italic.ttf", 14)
F_STAT_NUM = font("DejaVuSans-Bold.ttf", 26)
F_STAT_LBL = font("DejaVuSans.ttf", 11)
F_REGION = font("DejaVuSans-Bold.ttf", 13)
F_KICKER = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 17)
F_LEAD_DECK = font("DejaVuSans.ttf", 12)
F_FEAT_LBL = font("DejaVuSans-Bold.ttf", 10)
F_FEAT_HEAD = font("DejaVuSans-Bold.ttf", 13)
F_FEAT_DECK = font("DejaVuSans.ttf", 11)
F_SOURCE = font("DejaVuSans.ttf", 10)
F_SECTION = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_SMALL = font("DejaVuSans.ttf", 10)
F_VOICE = libfont("LiberationSerif-Italic.ttf", 12)
F_VOICE_ATTR = font("DejaVuSans.ttf", 10)
F_DATE = font("DejaVuSans.ttf", 12)
F_DATE_BOLD = font("DejaVuSans-Bold.ttf", 12)
F_FOOT = font("DejaVuSans.ttf", 10)
F_LEGEND = font("DejaVuSans.ttf", 10)
F_PIN = font("DejaVuSans-Bold.ttf", 7)
F_PIN2 = font("DejaVuSans-Bold.ttf", 6)

# ---------------------------------------------------------------- stories
# Every story happened, or was first reported, on Saturday 21 November 2026
# in at least one time zone. Tags: CONFIRMED (2+ outlets), OFFICIAL (on the
# record), REPORTED (single-source claim).

LEADS = [
    {
        "num": 1,
        "kicker": "CLIMATE  ·  DAY 13",
        "headline": "COP31 talks run into overtime — still no deal",
        "deck": "Negotiators push past the deadline; the draft drops fossil fuels "
                "and adaptation cash stalls.",
        "tag": "OFFICIAL",
        "source": "Reuters · Guardian",
        "art": "cop31",
    },
    {
        "num": 2,
        "kicker": "WAR IN THE GULF",
        "headline": "Three missiles downed over Riyadh, two more over Jizan",
        "deck": "Saudi defences down three over the capital; two more reported "
                "over Jizan.",
        "tag": "REPORTED",
        "source": "Al Jazeera · AFP",
        "art": "riyadh",
    },
    {
        "num": 3,
        "kicker": "DISASTER  ·  00:09 UTC",
        "headline": "Magnitude 6.7 quake shakes Peru, felt in Lima",
        "deck": "108 km deep near Junín; felt across central Peru and in Lima. "
                "One injured, no deaths.",
        "tag": "CONFIRMED",
        "source": "USGS · IGP",
        "art": "quake",
    },
]

FEATURES = [
    {
        "num": 4, "label": "KRYVYI RIH", "color": (140, 47, 47),
        "headline": "Russia hits Kryvyi Rih twice overnight",
        "deck": "A boy, 7, and a paramedic, 20, killed; 47 hurt.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "kryvyi",
    },
    {
        "num": 5, "label": "DAVAO · 146 SAFE", "color": (15, 118, 110),
        "headline": "Jet lands safe in Davao, 146 aboard",
        "deck": "Air Niugini 767 diverts; all aboard slide out unhurt.",
        "tag": "CONFIRMED", "source": "AP", "art": "davao",
    },
    {
        "num": 6, "label": "BITCOIN · $56,814", "color": (180, 83, 9),
        "headline": "Bitcoin sinks to $56,814, a 2026 low",
        "deck": "Down 3.6% as $1.5bn in crypto positions liquidate.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "bitcoin",
    },
    {
        "num": 7, "label": "BROWN · 2 KILLED", "color": (49, 46, 129),
        "headline": "Gunman kills 2 students at Brown University",
        "deck": "9 wounded in the engineering building; gunman at large.",
        "tag": "CONFIRMED", "source": "AP", "art": "brown",
    },
    {
        "num": 8, "label": "LAS VEGAS · POLE", "color": (190, 24, 93),
        "headline": "Verstappen takes pole in Las Vegas",
        "deck": "Antonelli fastest but a 5-place penalty hands him pole.",
        "tag": "CONFIRMED", "source": "F1", "art": "f1",
    },
    {
        "num": 9, "label": "KYIV WARNING", "color": (30, 58, 95),
        "headline": "Zelensky: Crimea bridge 'will not stay'",
        "deck": "He warns of double-tap strikes in an NBC interview.",
        "tag": "REPORTED", "source": "NBC", "art": "bridge",
    },
    {
        "num": 10, "label": "IRAN · URANIUM", "color": (109, 40, 217),
        "headline": "Iran keeps its uranium stockpile",
        "deck": "Minister still seeks a 'fair solution' on the atom deal.",
        "tag": "OFFICIAL", "source": "Reuters", "art": "uranium",
    },
    {
        "num": 11, "label": "HORMUZ · DRONE", "color": (3, 105, 161),
        "headline": "Iran says it downed a US drone",
        "deck": "Tehran claims it; Washington has not confirmed it.",
        "tag": "REPORTED", "source": "IRIB", "art": "drone",
    },
    {
        "num": 12, "label": "MERCURY · 19:24 CET", "color": (51, 65, 85),
        "headline": "BepiColombo reaches Mercury tonight",
        "deck": "Thrusters fire at 19:24 CET; 8-year voyage ends in orbit.",
        "tag": "OFFICIAL", "source": "ESA", "art": "mercury",
    },
    {
        "num": 13, "label": "RAHUL · 136", "color": (21, 128, 61),
        "headline": "Rahul's 136 puts India 118 ahead",
        "deck": "India 486 for 4 at stumps in Wellington; Gill falls for 98.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "cricket",
    },
]

BRIEFS = [
    "WARSAW — Rutte: NATO stands with Ukraine (AP)",
    "KYIV — Russia fires 3 missiles, 148 drones overnight (UAF)",
    "BAYELSA — Funeral boat capsizes; 4+ dead (AP)",
    "GAZA — Six wounded; settler kills Palestinian (Anadolu)",
    "COPENHAGEN — Two charged over Russian murder plot (AP)",
    "BRUSSELS — EU pays €8bn to Ukraine (Reuters)",
    "MOSCOW — Trump–Putin talks held (Kremlin)",
    "BASRA — Fire at power station kills four (Reuters)",
    "KHASAB — Second tanker hit off Oman in a day (UKMTO)",
    "GENEVA — UN pledge on 'killer robots' (Reuters)",
    "HORMUZ — Pugh swims the strait for marine life (AP)",
    "LAS VEGAS — Larsen wins from 9th in F1 Academy",
    "MELBOURNE — Teen charged over 'Onepercent' ring (SMH)",
    "MOGADISHU — Somalia expels UAE ambassador (Reuters)",
    "DANDONG — Kim crosses into China (KCNA)",
    "SUMY — HIMARS strike kills 20 Russian commanders (UAF)",
    "MANIPUR — 300+ in hospital after spurious liquor (PTI)",
    "FLORIDA — Dragon capsule due back tonight (NASA)",
    "TURIN — ATP Finals semis today: Alcaraz–Shelton (ATP)",
    "DUBLIN — Springboks face Ireland tonight (AP)",
    "HAITI — Third Salvadoran soldier dies; toll now 3 (AP)",
    "COPENHAGEN — Russian attaché expelled (Al Jazeera)",
    "TEXAS — Execution of a man of 70 takes 63 minutes (ABC)",
]

VOICES = [
    ("“The Crimea bridge ‘will not stay’.”",
     "— Zelenskyy, Kyiv (NBC interview)"),
    ("“A real good chance” of a deal.",
     "— Trump, on the Putin talks (Kremlin)"),
]

STATS = [
    ("DAY 13", "COP31 — still no deal"),
    ("5", "missiles downed (reported)"),
    ("6.7", "Peru quake magnitude"),
    ("146", "safe in Davao landing"),
    ("$56,814", "Bitcoin Saturday low"),
    ("136", "Rahul, India 486/4"),
]

REGIONS = [
    ("EUROPE", 13), ("ASIA", 3), ("MIDDLE EAST", 7), ("AFRICA", 2),
    ("AMERICAS", 7), ("OCEANIA", 2), ("GLOBAL", 2),
]

DATE_CHECK = [
    "DATE CHECK — NOT SATURDAY: Trump AI tax · UK–EU reset · Hodeidah port strike · "
    "China–Japan Taiwan words (all Fri 20 Nov) · Kyiv barrage · Wall Street sell-off",
    "Akvan landfall (Fri) · ICJ ruling · GTA VI launch (Thu 19 Nov) · Starc 7/58 "
    "(2025 Ashes) · NOT YET: BepiColombo capture, COP31 text, GP race",
]

FOOTER = [
    "Every story happened, or was first reported, on Saturday 21 November 2026 in at least one time zone.",
    "Sources: Reuters, AP, AFP, BBC, USGS, UKMTO, ESA, official statements. VOICES quotes are verbatim from the reports named.",
    "Tags: CONFIRMED = verified by 2+ outlets  ·  OFFICIAL = on the record  ·  REPORTED = single-source claim.",
]


# ---------------------------------------------------------------- helpers

def wrap(d, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_one_line(d, text, fnt, small_fnt, max_w):
    """Return (text, font) that fits max_w: shrink once, then truncate."""
    if d.textlength(text, font=fnt) <= max_w:
        return text, fnt
    if d.textlength(text, font=small_fnt) <= max_w:
        return text, small_fnt
    ell = "…"
    while text and d.textlength(text + ell, font=small_fnt) > max_w:
        text = text[:-1]
    return text + ell, small_fnt


TRUNCATIONS = []


def cap_lines(d, lines, max_n, fnt, max_w, where=""):
    """Cap wrapped lines at max_n, truncating the last with an ellipsis."""
    if len(lines) <= max_n:
        return lines
    TRUNCATIONS.append("%s: %d lines capped to %d" % (where, len(lines), max_n))
    lines = lines[:max_n]
    last = lines[-1]
    while last and d.textlength(last + "…", font=fnt) > max_w:
        last = last[:-1]
    lines[-1] = last + "…"
    return lines


def hline(d, x0, x1, y, color=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- lead art
# Three procedural scenes, one per lead. All shapes are drawn in code.

def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 77, 74))
    # Globe: blue disc with green blobs.
    cx, cy, r = x + 42, y + h // 2 + 4, 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 200),
              outline=(220, 235, 225), width=2)
    d.ellipse([cx - 13, cy - 15, cx + 2, cy - 2], fill=(110, 168, 110))
    d.ellipse([cx - 2, cy + 4, cx + 15, cy + 17], fill=(110, 168, 110))
    d.ellipse([cx + 6, cy - 17, cx + 17, cy - 6], fill=(110, 168, 110))
    # Thermometer: red tube, mercury high, short label to its right.
    tx = x + 82
    d.rectangle([tx, y + 10, tx + 10, y + h - 16], fill=(247, 243, 234))
    d.rectangle([tx + 2, y + 14, tx + 8, y + h - 20], fill=(220, 60, 60))
    d.ellipse([tx - 3, y + h - 20, tx + 13, y + h - 4], fill=(220, 60, 60))
    d.text((tx + 14, y + 12), "+1.5°C", font=F_KICKER, fill=(255, 190, 190),
           anchor="la")
    d.text((tx + 14, y + 27), "AT RISK", font=F_KICKER, fill=(255, 190, 190),
           anchor="la")
    # "DAY 13 / NO DEAL" centred between thermometer and clock.
    mx = x + 205
    d.text((mx, y + 8), "DAY 13", font=F_STAT_NUM, fill=WHITE, anchor="ma")
    d.text((mx, y + 38), "NO DEAL", font=F_KICKER, fill=(255, 190, 190),
           anchor="ma")
    # Clock: white face, hands past midnight.
    qx, qy, qr = x + w - 36, y + h // 2 + 4, 20
    d.ellipse([qx - qr, qy - qr, qx + qr, qy + qr], fill=(247, 243, 234),
              outline=(220, 235, 225), width=2)
    d.line([(qx, qy), (qx, qy - 14)], fill=INK, width=3)
    d.line([(qx, qy), (qx + 11, qy + 4)], fill=INK, width=3)
    d.ellipse([qx - 3, qy - 3, qx + 3, qy + 3], fill=RED)


def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
    # Stars.
    for sx, sy in ((30, 8), (70, 14), (120, 6), (180, 12), (215, 7),
                   (260, 14), (300, 8)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(230, 230, 200))
    # Moon.
    d.ellipse([x + w - 42, y + 6, x + w - 18, y + 30], fill=(240, 230, 190))
    # Skyline silhouettes with lit windows.
    base = y + h
    towers = [(8, 34, 22), (34, 46, 18), (56, 28, 24), (84, 40, 16),
              (104, 52, 20), (128, 30, 22), (152, 44, 18), (176, 36, 20),
              (200, 50, 22), (226, 32, 18), (248, 42, 20), (272, 30, 22)]
    for tx, th, tw in towers:
        d.rectangle([x + tx, base - th, x + tx + tw, base], fill=(8, 12, 24))
        for wy in range(base - th + 5, base - 4, 8):
            for wx in range(x + tx + 4, x + tx + tw - 3, 7):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.rectangle([wx, wy, wx + 2, wy + 2], fill=(255, 214, 120))
    # Three missile arcs with interception bursts.
    for ax, apex in ((60, 12), (150, 6), (240, 12)):
        d.arc([x + ax - 45, y + apex, x + ax + 45, y + h - 6],
              start=200, end=340, fill=(255, 120, 90), width=3)
        bx, by = x + ax, y + apex + 6
        for dx, dy in ((0, -7), (0, 7), (-7, 0), (7, 0), (-5, -5), (5, -5),
                       (-5, 5), (5, 5)):
            d.line([(bx, by), (bx + dx, by + dy)], fill=(255, 220, 130),
                   width=2)
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(255, 240, 180))


def art_quake(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(74, 62, 52))
    # Seismograph paper strip.
    d.rectangle([x + 10, y + 6, x + w - 10, y + h - 24], fill=(247, 243, 234))
    # Tremor trace: calm, then a violent spike, then aftershocks.
    mid = y + 6 + (h - 30) // 2
    pts = []
    n = 52
    for i in range(n + 1):
        px = x + 10 + (w - 20) * i / n
        if i < 12:
            amp = 1
        elif i < 20:
            amp = 2 + (i - 12)
        elif i < 26:
            amp = 10 - (i - 20)
        elif i < 38:
            amp = 4
        else:
            amp = 2
        sign = 1 if i % 2 == 0 else -1
        pts.append((px, mid + sign * amp))
    d.line(pts, fill=RED, width=2, joint="curve")
    # Depth marker chip on the strip.
    d.rectangle([x + w - 96, y + 9, x + w - 13, y + 23], fill=RED)
    d.text((x + w - 54, y + 10), "108 KM DEEP", font=F_KICKER, fill=WHITE,
           anchor="ma")
    # Cracked ground + small houses below the strip.
    gy = y + h - 6
    d.line([(x + 10, gy), (x + w - 10, gy)], fill=(220, 210, 190), width=2)
    for hx in (30, 120, 250):
        d.rectangle([x + hx, gy - 10, x + hx + 26, gy], fill=(220, 210, 190))
        d.polygon([(x + hx - 3, gy - 10), (x + hx + 13, gy - 18),
                   (x + hx + 29, gy - 10)], fill=(179, 32, 44))
    d.line([(x + 190, gy), (x + 196, gy + 4), (x + 190, gy + 5)],
           fill=(220, 210, 190), width=2)


LEAD_ART = {"cop31": art_cop31, "riyadh": art_riyadh, "quake": art_quake}


# ---------------------------------------------------------------- feature art
# Ten small iconic scenes, one per feature card (strip ~193x32). All shapes
# are drawn in code; each scene reads at a glance at 300px.

def art_kryvyi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(18, 22, 40))
    for bx, bh in ((14, 20), (44, 26), (76, 18), (108, 24)):
        d.rectangle([x + bx, y + h - bh, x + bx + 24, y + h], fill=(8, 10, 20))
    # Flames over two buildings.
    for fx in (26, 56, 120):
        d.polygon([(x + fx, y + h - 20), (x + fx + 6, y + h - 30),
                   (x + fx + 12, y + h - 20)], fill=(255, 140, 40))
        d.polygon([(x + fx + 3, y + h - 20), (x + fx + 6, y + h - 26),
                   (x + fx + 9, y + h - 20)], fill=(255, 220, 120))
    for sx, sy in ((150, 6), (170, 10), (185, 5)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(230, 230, 200))


def art_davao(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(135, 190, 220))
    # Cloud puffs.
    for cx in (20, 150):
        d.ellipse([x + cx, y + 4, x + cx + 26, y + 14], fill=(255, 255, 255))
    # Plane silhouette.
    px, py = x + 66, y + 8
    d.polygon([(px, py + 6), (px + 60, py + 6), (px + 66, py + 3),
               (px + 60, py + 9), (px + 6, py + 9)], fill=(255, 255, 255))
    d.polygon([(px + 22, py), (px + 30, py), (px + 26, py + 8)],
              fill=(255, 255, 255))
    d.polygon([(px + 46, py + 9), (px + 54, py + 9), (px + 52, py + 14)],
              fill=(255, 255, 255))
    # Runway + lights.
    d.rectangle([x, y + h - 6, x + w, y + h], fill=(90, 90, 90))
    for lx in range(8, w, 24):
        d.ellipse([x + lx, y + h - 5, x + lx + 3, y + h - 2],
                  fill=(255, 220, 120))


def art_bitcoin(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 26, 20))
    # Falling chart line.
    d.line([(x + 8, y + 6), (x + 50, y + 10), (x + 90, y + 16),
            (x + 130, y + 24)], fill=(220, 60, 60), width=3)
    d.polygon([(x + 130, y + 24), (x + 122, y + 20), (x + 126, y + 28)],
              fill=(220, 60, 60))
    # Coin with B.
    cx, cy, r = x + w - 26, y + h // 2, 12
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 160, 40),
              outline=(255, 220, 140), width=2)
    d.text((cx, cy - 1), "B", font=F_FEAT_LBL, fill=(60, 40, 0), anchor="mm")


def art_brown(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 44))
    # Campus building with lit windows.
    d.rectangle([x + 30, y + 6, x + 120, y + h], fill=(60, 55, 80))
    for wy in (10, 18, 26):
        for wx in (38, 56, 74, 92, 108):
            d.rectangle([x + wx, y + wy, x + wx + 8, y + wy + 5],
                        fill=(255, 220, 120))
    # Police light glow: red + blue dots.
    d.ellipse([x + 140, y + 6, x + 152, y + 18], fill=(255, 60, 60))
    d.ellipse([x + 158, y + 6, x + 170, y + 18], fill=(80, 120, 255))
    d.rectangle([x + 138, y + 22, x + 172, y + h], fill=(40, 40, 60))


def art_f1(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 28))
    # Chequered flag, top right.
    for r in range(3):
        for c in range(4):
            fill = WHITE if (r + c) % 2 == 0 else INK
            d.rectangle([x + w - 34 + c * 7, y + 4 + r * 6,
                         x + w - 28 + c * 7, y + 9 + r * 6], fill=fill)
    # F1 car silhouette: low body, wing, two wheels.
    cx, cy = x + 30, y + h - 14
    d.polygon([(cx, cy), (cx + 90, cy), (cx + 100, cy - 6),
               (cx + 60, cy - 8), (cx + 40, cy - 12), (cx + 10, cy - 6)],
              fill=(200, 30, 50))
    d.rectangle([cx + 96, cy - 14, cx + 100, cy - 4], fill=(200, 30, 50))
    for wx in (cx + 14, cx + 78):
        d.ellipse([wx, cy - 2, wx + 14, cy + 12], fill=(10, 10, 10),
                  outline=(180, 180, 180), width=1)
    d.rectangle([x, y + h - 3, x + w, y + h], fill=(120, 120, 120))


def art_bridge(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(210, 180, 140))
    # Bridge deck + towers.
    d.rectangle([x + 6, y + 18, x + w - 40, y + 22], fill=(90, 70, 60))
    for tx in (30, 90):
        d.rectangle([x + tx, y + 6, x + tx + 6, y + 22], fill=(90, 70, 60))
    d.line([(x + 33, y + 6), (x + 60, y + 18)], fill=(90, 70, 60), width=1)
    d.line([(x + 93, y + 6), (x + 60, y + 18)], fill=(90, 70, 60), width=1)
    # Warning triangle.
    tx, ty = x + w - 34, y + 6
    d.polygon([(tx + 12, ty), (tx + 24, ty + 20), (tx, ty + 20)],
              fill=(255, 200, 0), outline=(150, 100, 0))
    d.text((tx + 12, ty + 8), "!", font=F_FEAT_LBL, fill=INK, anchor="ma")


def art_uranium(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 60, 60))
    cx, cy = x + w // 2, y + h // 2
    d.ellipse([cx - 26, cy - 9, cx + 26, cy + 9], outline=(255, 220, 120),
              width=2)
    d.ellipse([cx - 9, cy - 14, cx + 9, cy + 14], outline=(255, 220, 120),
              width=2)
    d.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 220, 120))
    d.ellipse([cx + 20, cy - 9, cx + 24, cy - 5], fill=(255, 255, 255))
    d.ellipse([cx - 9, cy + 9, cx - 5, cy + 13], fill=(255, 255, 255))


def art_drone(d, x, y, w, h):
    d.rectangle([x, y, x + 0, y + h], fill=(135, 190, 220))
    d.rectangle([x, y, x + w, y + h], fill=(135, 190, 220))
    # Sea.
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(30, 100, 160))
    for wx in range(6, w, 22):
        d.arc([x + wx, y + h - 10, x + wx + 14, y + h - 2], start=180,
              end=360, fill=(220, 240, 255), width=1)
    # Drone: body + arms + rotors.
    cx, cy = x + w // 2, y + 12
    d.rectangle([cx - 14, cy - 3, cx + 14, cy + 3], fill=(40, 40, 40))
    d.line([(cx - 20, cy - 6), (cx + 20, cy - 6)], fill=(40, 40, 40), width=2)
    for rx in (cx - 20, cx + 20):
        d.line([(rx - 7, cy - 8), (rx + 7, cy - 8)], fill=(90, 90, 90),
               width=2)
    d.line([(cx, cy + 3), (cx, cy + 8)], fill=(40, 40, 40), width=2)


def art_mercury(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 8, 18))
    for sx, sy in ((12, 6), (40, 10), (150, 5), (175, 12)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(230, 230, 200))
    # Mercury: grey cratered disc.
    cx, cy, r = x + 30, y + h // 2 + 2, 13
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(160, 155, 145))
    for ox, oy, orr in ((-5, -4, 3), (4, 3, 2), (-2, 6, 2)):
        d.ellipse([cx + ox - orr, cy + oy - orr, cx + ox + orr, cy + oy + orr],
                  fill=(120, 115, 105))
    # Spacecraft: body + solar panels.
    sx, sy = x + 110, y + 10
    d.rectangle([sx, sy, sx + 16, sy + 10], fill=(220, 220, 220))
    d.rectangle([sx - 16, sy + 2, sx, sy + 8], fill=(60, 120, 200))
    d.rectangle([sx + 16, sy + 2, sx + 32, sy + 8], fill=(60, 120, 200))
    d.line([(sx + 8, sy + 10), (sx + 8, sy + 16)], fill=(255, 180, 80),
           width=2)


def art_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 130, 70))
    # Pitch strip.
    d.rectangle([x + 60, y + 4, x + 130, y + h - 4], fill=(210, 190, 140))
    # Stumps.
    for sx in (70, 76, 82):
        d.rectangle([x + sx, y + 8, x + sx + 3, y + 20], fill=(255, 220, 120))
    # Bat (angled) + ball.
    d.line([(x + 120, y + 8), (x + 100, y + 26)], fill=(230, 200, 150),
           width=5)
    d.ellipse([x + 140, y + 8, x + 150, y + 18], fill=(180, 40, 40),
              outline=WHITE, width=1)


FEATURE_ART = {
    "kryvyi": art_kryvyi, "davao": art_davao, "bitcoin": art_bitcoin,
    "brown": art_brown, "f1": art_f1, "bridge": art_bridge,
    "uranium": art_uranium, "drone": art_drone, "mercury": art_mercury,
    "cricket": art_cricket,
}


def draw_lead(d, x, y, w, h, lead):
    art_h = 68
    LEAD_ART[lead["art"]](d, x, y, w, art_h)
    ty = y + art_h + 6
    d.text((x, ty), "%d · %s" % (lead["num"], lead["kicker"]),
           font=F_KICKER, fill=RED, anchor="la")
    ty += 15
    for line in cap_lines(d, wrap(d, lead["headline"], F_LEAD_HEAD, w),
                          2, F_LEAD_HEAD, w, "lead %d head" % lead["num"]):
        d.text((x, ty), line, font=F_LEAD_HEAD, fill=INK, anchor="la")
        ty += 20
    ty += 1
    for line in cap_lines(d, wrap(d, lead["deck"], F_LEAD_DECK, w),
                          2, F_LEAD_DECK, w, "lead %d deck" % lead["num"]):
        d.text((x, ty), line, font=F_LEAD_DECK, fill=(60, 60, 60), anchor="la")
        ty += 14
    d.text((x, y + h - 12), "%s · %s" % (lead["tag"], lead["source"]),
           font=F_SOURCE, fill=GREY, anchor="la")


def draw_feature(d, x, y, w, h, feat):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE, width=1)
    art_h = 32
    FEATURE_ART[feat["art"]](d, x + 1, y + 1, w - 2, art_h)
    # Label chip: number + short label, bottom-left over the art.
    lbl = "%d  %s" % (feat["num"], feat["label"])
    tw = d.textlength(lbl, font=F_FEAT_LBL) + 10
    d.rectangle([x + 1, y + art_h - 15, x + 1 + tw, y + art_h + 1],
                fill=feat["color"])
    d.text((x + 6, y + art_h - 14), lbl, font=F_FEAT_LBL, fill=WHITE,
           anchor="la")
    tx = x + 7
    tw2 = w - 14
    ty = y + art_h + 5
    for line in cap_lines(d, wrap(d, feat["headline"], F_FEAT_HEAD, tw2),
                          2, F_FEAT_HEAD, tw2,
                          "feat %d head" % feat["num"]):
        d.text((tx, ty), line, font=F_FEAT_HEAD, fill=INK, anchor="la")
        ty += 15
    ty += 1
    for line in cap_lines(d, wrap(d, feat["deck"], F_FEAT_DECK, tw2),
                          2, F_FEAT_DECK, tw2,
                          "feat %d deck" % feat["num"]):
        d.text((tx, ty), line, font=F_FEAT_DECK, fill=(60, 60, 60), anchor="la")
        ty += 12
    d.text((tx, y + h - 13), "%s · %s" % (feat["tag"], feat["source"]),
           font=F_SOURCE, fill=GREY, anchor="la")


# ---------------------------------------------------------------- world map
# Coarse equirectangular land mask: 60 columns of 6 degrees of longitude,
# 30 rows of 5 degrees of latitude (90N down to 60S). Each row lists the
# inclusive column ranges that hold land. Drawn as a dotted halftone map.

LAND = [
    [],
    [(15, 16), (22, 25)],
    [(10, 16), (20, 26), (31, 34), (37, 39), (45, 47)],
    [(2, 6), (9, 16), (20, 23), (40, 59)],
    [(2, 6), (7, 20), (32, 59)],
    [(2, 6), (7, 20), (26, 26), (30, 59)],
    [(4, 20), (29, 59)],
    [(9, 20), (28, 53), (56, 56)],
    [(9, 19), (29, 53)],
    [(9, 18), (29, 51), (53, 53)],
    [(9, 17), (28, 53)],
    [(10, 16), (28, 53)],
    [(11, 16), (27, 39), (41, 44), (46, 50)],
    [(11, 15), (27, 39), (41, 49)],
    [(12, 15), (27, 35), (37, 39), (42, 43), (45, 48), (50, 50)],
    [(14, 16), (27, 32), (35, 37), (42, 43), (46, 48), (50, 51)],
    [(15, 21), (27, 32), (35, 37), (46, 49), (51, 54)],
    [(17, 21), (31, 37), (45, 49), (51, 54)],
    [(16, 22), (31, 36), (46, 49), (51, 54)],
    [(16, 24), (32, 36), (47, 49), (52, 54)],
    [(17, 23), (32, 36), (51, 54)],
    [(18, 23), (32, 36), (37, 38), (50, 54)],
    [(18, 23), (32, 35), (37, 37), (49, 55)],
    [(18, 22), (32, 35), (49, 55)],
    [(18, 21), (33, 34), (49, 55), (57, 59)],
    [(17, 20), (53, 54), (57, 59)],
    [(17, 19), (57, 58)],
    [(17, 19)],
    [(17, 18)],
    [(18, 18)],
]

# Numbered pins for the lead + feature stories (numbers match the cards).
# Gulf pins are nudged apart so the numbers stay readable. No pin for 6
# (Bitcoin, global) or 12 (BepiColombo, in space) — the legend says so.
PINS = [
    (1, 36.0, 28.0),    # COP31, Antalya (nudged west)
    (2, 22.5, 41.5),    # Riyadh (nudged)
    (3, -11.0, -76.0),  # Peru quake, Junín
    (4, 46.5, 35.5),    # Kryvyi Rih (nudged east, clear of Kyiv)
    (5, 7.1, 125.6),    # Davao
    (7, 41.8, -71.4),   # Brown University, Providence
    (8, 36.1, -115.2),  # Las Vegas
    (9, 53.0, 25.0),    # Kyiv (nudged north-west, clear of Kryvyi Rih)
    (10, 35.0, 53.0),   # Tehran (nudged)
    (11, 25.0, 58.0),   # Hormuz (nudged)
    (13, -41.3, 174.8), # Wellington
]

LEGEND_LEFT = [
    "1  COP31 overtime",
    "2  Riyadh missiles",
    "3  Peru quake M6.7",
    "4  Kryvyi Rih strike",
    "5  Davao jet, 146 safe",
    "6  Bitcoin — no pin",
    "7  Brown shooting",
]
LEGEND_RIGHT = [
    "8  Verstappen pole",
    "9  Zelensky warning",
    "10  Iran uranium",
    "11  Hormuz drone",
    "12  Mercury — in space",
    "13  Rahul 136",
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG, outline=LINE, width=1)
    for r, ranges in enumerate(LAND):
        cy = y0 + (r + 0.5) / 30 * h
        for c0, c1 in ranges:
            for c in range(c0, c1 + 1):
                cx = x0 + (c + 0.5) / 60 * w
                d.ellipse([cx - 1.7, cy - 1.7, cx + 1.7, cy + 1.7],
                          fill=MAP_LAND)
    for num, lat, lon in PINS:
        px = x0 + (lon + 180) / 360 * w
        py = y0 + (90 - lat) / 150 * h
        r = 5.5
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=1)
        fnt = F_PIN if num < 10 else F_PIN2
        d.text((px, py - 1), str(num), font=fnt, fill=WHITE, anchor="mm")


# ---------------------------------------------------------------- assembly

def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Top strip: nameplate left, counts right.
    d.text((MARGIN, 8), "THE WORLD IN ONE DAY", font=F_STRIP, fill=RED,
           anchor="la")
    d.text((W - MARGIN, 8),
           "36 STORIES  ·  7 REGIONS  ·  17 FIELDS  ·  EVERY ONE DATED",
           font=F_STRIP, fill=GREY, anchor="ra")
    hline(d, MARGIN, W - MARGIN, 28, color=RED, width=2)

    # Masthead: the date IS the headline (as in the top entries).
    d.text((W // 2, 32), "Saturday 21 November 2026", font=F_MAST, fill=INK,
           anchor="ma")
    d.text((W // 2, 96),
           "COP31 talks run into overtime  ·  missiles over Riyadh  ·  "
           "a quake shakes Peru",
           font=F_SUBLINE, fill=(60, 60, 60), anchor="ma")
    hline(d, MARGIN, W - MARGIN, 118, color=INK, width=2)

    # Stat strip: 6 cells.
    sy, sh = 124, 54
    cell_w = CW // 6
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + i * cell_w
        d.rectangle([cx, sy, cx + cell_w - 1, sy + sh], fill=CARD_BG,
                    outline=LINE, width=1)
        d.text((cx + cell_w // 2, sy + 4), num, font=F_STAT_NUM, fill=RED,
               anchor="ma")
        d.text((cx + cell_w // 2, sy + 34), label, font=F_STAT_LBL,
               fill=(60, 60, 60), anchor="ma")

    # Region strip.
    ry = 184
    d.rectangle([MARGIN, ry, W - MARGIN, ry + 22], fill=DARK)
    region_text = "   ·   ".join("%s %d" % (name, n) for name, n in REGIONS)
    d.text((W // 2, ry + 4), region_text, font=F_REGION, fill=WHITE,
           anchor="ma")

    # Leads: 3 columns.
    ly, lh = 212, 168
    lead_w, lead_gap = 325, 10
    for i, lead in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + lead_gap)
        draw_lead(d, lx, ly, lead_w, lh, lead)
        if i:
            hx = lx - lead_gap // 2
            d.line([(hx, ly), (hx, ly + lh)], fill=LINE, width=1)

    # Features: 2 rows of 5, each card illustrated.
    feat_w, feat_gap, feat_h = 193, 7, 110
    for row in range(2):
        fy = 388 + row * (feat_h + 6)
        for col in range(5):
            feat = FEATURES[row * 5 + col]
            fx = MARGIN + col * (feat_w + feat_gap)
            draw_feature(d, fx, fy, feat_w, feat_h, feat)

    # VOICES: two verbatim quotes, side by side.
    vy = 620
    d.rectangle([MARGIN, vy, W - MARGIN, vy + 36], fill=CARD_BG,
                outline=LINE, width=1)
    d.text((MARGIN + 8, vy + 4), "VOICES", font=F_KICKER, fill=RED,
           anchor="la")
    d.line([(MARGIN + 62, vy + 5), (MARGIN + 62, vy + 31)], fill=LINE,
           width=1)
    vx0 = MARGIN + 72
    half = (CW - 72) // 2
    for i, (quote, attr) in enumerate(VOICES):
        qx = vx0 + i * half
        d.text((qx, vy + 3), quote, font=F_VOICE, fill=INK, anchor="la")
        d.text((qx, vy + 20), attr, font=F_VOICE_ATTR, fill=GREY, anchor="la")
        if i:
            d.line([(qx - 8, vy + 5), (qx - 8, vy + 31)], fill=LINE, width=1)

    # Lower band headers.
    hy = 664
    d.text((MARGIN, hy), "WHERE IT HAPPENED", font=F_SECTION, fill=INK,
           anchor="la")
    d.text((336, hy), "ALSO ON SATURDAY 21 NOVEMBER — 23 MORE STORIES",
           font=F_SECTION, fill=INK, anchor="la")
    hline(d, MARGIN, 326, hy + 20, color=INK, width=1)
    hline(d, 336, W - MARGIN, hy + 20, color=INK, width=1)

    # Map + legend.
    draw_map(d, MARGIN, 690, 312, 124)
    for i, item in enumerate(LEGEND_LEFT):
        d.text((MARGIN, 820 + i * 12), item, font=F_LEGEND, fill=(60, 60, 60),
               anchor="la")
    for i, item in enumerate(LEGEND_RIGHT):
        d.text((MARGIN + 160, 820 + i * 12), item, font=F_LEGEND,
               fill=(60, 60, 60), anchor="la")

    # Briefs: 2 columns (12 + 11), numbered 14-36.
    for col in range(2):
        bx = 336 + col * (329 + 16)
        rows = 12 if col == 0 else 11
        for row in range(rows):
            idx = col * 12 + row
            num = 14 + idx
            text, fnt = fit_one_line(d, "%d  %s" % (num, BRIEFS[idx]),
                                     F_BRIEF, F_BRIEF_SMALL, 329)
            if text.endswith("…"):
                TRUNCATIONS.append("brief %d truncated" % num)
            d.text((bx, 690 + row * 17), text, font=fnt, fill=INK, anchor="la")

    # DATE CHECK box.
    dy = 906
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 42], fill=(252, 240, 240),
                outline=RED, width=2)
    prefix = "DATE CHECK — "
    d.text((MARGIN + 10, dy + 4), prefix, font=F_DATE_BOLD, fill=RED,
           anchor="la")
    rest = DATE_CHECK[0][len(prefix):]
    d.text((MARGIN + 10 + d.textlength(prefix, font=F_DATE_BOLD), dy + 4),
           rest, font=F_DATE, fill=INK, anchor="la")
    d.text((MARGIN + 10, dy + 22), DATE_CHECK[1], font=F_DATE, fill=INK,
           anchor="la")

    # Footer.
    for i, line in enumerate(FOOTER):
        d.text((W // 2, 956 + i * 13), line, font=F_FOOT, fill=GREY,
               anchor="ma")

    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = build()
    img.save(out, format="PNG", optimize=True)
    import hashlib
    import os

    data = open(out, "rb").read()
    print("%s: %d bytes, sha256 %s" % (out, len(data),
                                       hashlib.sha256(data).hexdigest()))
    # Story-count sanity: 3 leads + 10 features + 23 briefs = 36.
    total = len(LEADS) + len(FEATURES) + len(BRIEFS)
    print("stories: %d (leads %d, features %d, briefs %d)"
          % (total, len(LEADS), len(FEATURES), len(BRIEFS)))
    regions_total = sum(n for _, n in REGIONS)
    print("regions sum: %d" % regions_total)
    assert total == 36 and regions_total == 36
    if TRUNCATIONS:
        print("TRUNCATIONS:")
        for t in TRUNCATIONS:
            print("  -", t)
    else:
        print("no truncations")
    # DATE CHECK fit check: both lines must fit inside the box (inner 976px).
    from PIL import ImageDraw as _ID
    _d = _ID.Draw(img)
    for i, line in enumerate(DATE_CHECK):
        wpx = _d.textlength(line, font=F_DATE)
        print("date-check line %d: %.0fpx (limit 976)" % (i + 1, wpx))
        assert wpx <= 976, "DATE CHECK line %d overflows" % (i + 1)


if __name__ == "__main__":
    main()
