#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261121 (v2 rebuild).

A 1024x1024 newspaper front page summing up Saturday 21 November 2026:
3 illustrated leads + 10 feature cards + 22 one-line briefs + a light
dotted world map with numbered pins + a short DATE CHECK box.

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


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


F_STRIP = font("DejaVuSans-Bold.ttf", 12)
F_TITLE = font("DejaVuSerif-Bold.ttf", 38)
F_MAST = font("DejaVuSerif-Bold.ttf", 50)
F_STAT_NUM = font("DejaVuSans-Bold.ttf", 26)
F_STAT_LBL = font("DejaVuSans.ttf", 11)
F_REGION = font("DejaVuSans-Bold.ttf", 13)
F_KICKER = font("DejaVuSans-Bold.ttf", 11)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 17)
F_LEAD_DECK = font("DejaVuSans.ttf", 12)
F_FEAT_STRIP = font("DejaVuSans-Bold.ttf", 13)
F_FEAT_HEAD = font("DejaVuSans-Bold.ttf", 13)
F_FEAT_DECK = font("DejaVuSans.ttf", 11)
F_SOURCE = font("DejaVuSans.ttf", 10)
F_SECTION = font("DejaVuSans-Bold.ttf", 13)
F_BRIEF = font("DejaVuSans.ttf", 11)
F_BRIEF_SMALL = font("DejaVuSans.ttf", 10)
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
        "kicker": "CLIMATE  ·  DAY 13",
        "headline": "COP31 talks run into overtime — still no deal",
        "deck": "Negotiators push past the deadline; the draft drops fossil fuels "
                "and adaptation cash stalls.",
        "tag": "OFFICIAL",
        "source": "Reuters · Guardian",
        "art": "cop31",
    },
    {
        "kicker": "WAR IN THE GULF",
        "headline": "Three missiles downed over Riyadh, two more over Jizan",
        "deck": "Saudi defences down three over the capital; two more reported "
                "over Jizan.",
        "tag": "REPORTED",
        "source": "Al Jazeera · AFP",
        "art": "riyadh",
    },
    {
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
        "strip": "2 KILLED · DOZENS HURT", "color": (140, 47, 47),
        "headline": "Russia hits Kryvyi Rih twice overnight",
        "deck": "A boy, 7, and a paramedic, 20, killed; injured toll climbs past 47.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
    {
        "strip": "146 SAFE", "color": (15, 118, 110),
        "headline": "Jet lands safe in Davao, 146 aboard",
        "deck": "Air Niugini 767 diverts; all 146 aboard slide out unhurt. "
                "Landed 00:08 Sat local.",
        "tag": "CONFIRMED", "source": "AP",
    },
    {
        "strip": "$56,814", "color": (180, 83, 9),
        "headline": "Bitcoin sinks to $56,814, a 2026 low",
        "deck": "Down 3.6% to a new 2026 low as $1.5bn in crypto positions "
                "liquidate in 24 hours.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
    {
        "strip": "2 KILLED · 9 WOUNDED", "color": (49, 46, 129),
        "headline": "Gunman kills 2 students at Brown University",
        "deck": "Shots in the engineering building during exams; 9 wounded, "
                "gunman at large.",
        "tag": "CONFIRMED", "source": "AP",
    },
    {
        "strip": "4 KILLED · 30 HURT", "color": (194, 65, 12),
        "headline": "Fire at Basra power station kills four",
        "deck": "Blaze at the Hartha plant spreads to nearby houses; the 800 MW "
                "station stops running.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
    {
        "strip": "2ND TANKER HIT", "color": (30, 58, 95),
        "headline": "Second tanker hit off Khasab in a day",
        "deck": "UKMTO 215-26: unknown projectile hits the stern 11 nm off Oman; "
                "no injuries.",
        "tag": "CONFIRMED", "source": "UKMTO · Reuters",
    },
    {
        "strip": "RULES BY 2028", "color": (109, 40, 217),
        "headline": "UN talks end with pledge on 'killer robots'",
        "deck": "Geneva talks end early: rules within two years; US, Russia, "
                "Israel opposed.",
        "tag": "OFFICIAL", "source": "Reuters",
    },
    {
        "strip": "15 KM SWIM", "color": (3, 105, 161),
        "headline": "Pugh swims the Strait of Hormuz",
        "deck": "UN oceans ambassador crosses the strait to show war's damage "
                "to marine life.",
        "tag": "REPORTED", "source": "AP",
    },
    {
        "strip": "WINS FROM 9TH", "color": (190, 24, 93),
        "headline": "Larsen charges from 9th to win in Las Vegas",
        "deck": "Reverse-grid race: the Swede's second win of 2026, from the "
                "lowest grid slot ever.",
        "tag": "CONFIRMED", "source": "F1 Academy",
    },
    {
        "strip": "124*", "color": (21, 128, 61),
        "headline": "Rahul's 124* puts India on top",
        "deck": "An unbeaten century anchors India's 159 for 1.",
        "tag": "CONFIRMED", "source": "Reuters",
    },
]

BRIEFS = [
    "LAS VEGAS — Verstappen on pole; Antonelli penalised (F1)",
    "WARSAW — Rutte: NATO stands with Ukraine (AP)",
    "KYIV — Zelensky: Crimea bridge 'will not stay' (Reuters)",
    "HORMUZ — Iran claims a US MQ-9 drone downed (REPORTED)",
    "TEHRAN — Iran keeps its uranium stockpile (Reuters)",
    "MERCURY — BepiColombo burn due 19:24 CET tonight (ESA)",
    "BAYELSA — Funeral boat capsizes; 4+ dead (AP)",
    "KYIV — Russia fires 3 missiles, 148 drones overnight (UAF)",
    "GAZA — Six wounded; settler kills Palestinian (Anadolu)",
    "COPENHAGEN — Two charged over Russian murder plot (AP)",
    "BRUSSELS — EU pays €8bn to Ukraine (Reuters)",
    "MOSCOW — Trump–Putin talks held (Kremlin)",
    "MELBOURNE — Teen charged over 'Onepercent' ring (SMH)",
    "HAITI — Third Salvadoran soldier dies; toll now 3 (AP)",
    "MOGADISHU — Somalia expels UAE ambassador (Reuters)",
    "DANDONG — Kim crosses into China (KCNA)",
    "SUMY — HIMARS strike kills 20 Russian commanders (UAF)",
    "MANIPUR — 300+ in hospital after spurious liquor (PTI)",
    "TECH — Claude claims Riemann proof; experts sceptical",
    "FLORIDA — Dragon capsule due to splash down tonight (NASA)",
    "TURIN — ATP Finals semis today: Alcaraz–Shelton (ATP)",
    "DUBLIN — Springboks face Ireland tonight (AP)",
]

STATS = [
    ("DAY 13", "COP31 — still no deal"),
    ("5", "missiles downed (reported)"),
    ("6.7", "Peru quake magnitude"),
    ("146", "safe in Davao landing"),
    ("$56,814", "Bitcoin Saturday low"),
    ("124*", "Rahul, unbeaten"),
]

REGIONS = [
    ("EUROPE", 9), ("ASIA", 4), ("MIDDLE EAST", 7), ("AFRICA", 2),
    ("AMERICAS", 5), ("OCEANIA", 1), ("GLOBAL", 7),
]

DATE_CHECK = [
    "DATE CHECK — NOT SATURDAY: Kyiv barrage · Wall Street sell-off · Trump AI tax · "
    "UK–EU reset · Akvan landfall · Hodeidah port strike (all Fri 20 Nov)",
    "ICJ Myanmar ruling · GTA VI launch (Thu 19 Nov) · Starc 7/58 (2025 Ashes) · "
    "NOT YET: BepiColombo capture, a final COP31 text, Las Vegas GP race (Sun)",
]

FOOTER = [
    "Every story happened, or was first reported, on Saturday 21 November 2026 in at least one time zone.",
    "Sources: Reuters, AP, AFP, BBC, USGS, UKMTO, ESA, official statements.",
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


def cap_lines(d, lines, max_n, fnt, max_w):
    """Cap wrapped lines at max_n, truncating the last with an ellipsis."""
    if len(lines) <= max_n:
        return lines
    lines = lines[:max_n]
    last = lines[-1]
    while last and d.textlength(last + "…", font=fnt) > max_w:
        last = last[:-1]
    lines[-1] = last + "…"
    return lines


def hline(d, x0, x1, y, color=INK, width=1):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


# ---------------------------------------------------------------- lead art
# Three small procedural scenes, one per lead. All shapes are drawn in code.

def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(31, 77, 74))
    # Globe: blue disc with green blobs.
    cx, cy, r = x + 52, y + h // 2 + 2, 26
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 200),
              outline=(220, 235, 225), width=2)
    d.ellipse([cx - 14, cy - 16, cx + 2, cy - 2], fill=(110, 168, 110))
    d.ellipse([cx - 2, cy + 4, cx + 16, cy + 18], fill=(110, 168, 110))
    d.ellipse([cx + 6, cy - 18, cx + 18, cy - 6], fill=(110, 168, 110))
    # Clock: white face, hands past midnight.
    qx, qy, qr = x + w - 52, y + h // 2 + 2, 22
    d.ellipse([qx - qr, qy - qr, qx + qr, qy + qr], fill=(247, 243, 234),
              outline=(220, 235, 225), width=2)
    d.line([(qx, qy), (qx, qy - 15)], fill=INK, width=3)
    d.line([(qx, qy), (qx + 12, qy + 4)], fill=INK, width=3)
    d.ellipse([qx - 3, qy - 3, qx + 3, qy + 3], fill=RED)
    # "DAY 13" between globe and clock.
    d.text((x + w // 2, y + 8), "DAY 13", font=F_STAT_NUM, fill=WHITE,
           anchor="ma")
    d.text((x + w // 2, y + 38), "NO DEAL", font=F_KICKER, fill=(255, 190, 190),
           anchor="ma")


def art_riyadh(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 24, 46))
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
    # Cracked ground + two small houses below the strip.
    gy = y + h - 6
    d.line([(x + 10, gy), (x + w - 10, gy)], fill=(220, 210, 190), width=2)
    for hx in (30, 250):
        d.rectangle([x + hx, gy - 10, x + hx + 26, gy], fill=(220, 210, 190))
        d.polygon([(x + hx - 3, gy - 10), (x + hx + 13, gy - 18),
                   (x + hx + 29, gy - 10)], fill=(179, 32, 44))
    d.line([(x + 150, gy), (x + 156, gy + 4), (x + 150, gy + 5)],
           fill=(220, 210, 190), width=2)


ART = {"cop31": art_cop31, "riyadh": art_riyadh, "quake": art_quake}


def draw_lead(d, x, y, w, h, lead):
    art_h = 56
    ART[lead["art"]](d, x, y, w, art_h)
    ty = y + art_h + 6
    d.text((x, ty), lead["kicker"], font=F_KICKER, fill=RED, anchor="la")
    ty += 15
    for line in cap_lines(d, wrap(d, lead["headline"], F_LEAD_HEAD, w),
                          2, F_LEAD_HEAD, w):
        d.text((x, ty), line, font=F_LEAD_HEAD, fill=INK, anchor="la")
        ty += 20
    ty += 1
    for line in cap_lines(d, wrap(d, lead["deck"], F_LEAD_DECK, w),
                          2, F_LEAD_DECK, w):
        d.text((x, ty), line, font=F_LEAD_DECK, fill=(60, 60, 60), anchor="la")
        ty += 14
    d.text((x, y + h - 12), "%s · %s" % (lead["tag"], lead["source"]),
           font=F_SOURCE, fill=GREY, anchor="la")


def draw_feature(d, x, y, w, h, feat):
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE, width=1)
    strip_h = 26
    d.rectangle([x, y, x + w, y + strip_h], fill=feat["color"])
    d.text((x + w // 2, y + 4), feat["strip"], font=F_FEAT_STRIP, fill=WHITE,
           anchor="ma")
    tx = x + 7
    tw = w - 14
    ty = y + strip_h + 4
    for line in cap_lines(d, wrap(d, feat["headline"], F_FEAT_HEAD, tw),
                          2, F_FEAT_HEAD, tw):
        d.text((tx, ty), line, font=F_FEAT_HEAD, fill=INK, anchor="la")
        ty += 15
    ty += 1
    for line in cap_lines(d, wrap(d, feat["deck"], F_FEAT_DECK, tw),
                          3, F_FEAT_DECK, tw):
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

# Numbered pins for the 13 lead + feature stories. Gulf pins are nudged a
# few degrees apart so the numbers stay readable. No pin for 6 (Bitcoin)
# or 11 (Pugh swim, at pin 9 in the Strait of Hormuz) — the legend says so.
PINS = [
    (1, 36.0, 28.0),    # COP31, Antalya (nudged west)
    (2, 22.5, 41.5),    # Riyadh (nudged)
    (3, -11.0, -76.0),  # Peru quake, Junín
    (4, 47.9, 33.4),    # Kryvyi Rih
    (5, 7.1, 125.6),    # Davao
    (7, 41.8, -71.4),   # Brown University, Providence
    (8, 33.0, 50.0),    # Basra (nudged)
    (9, 23.0, 59.5),    # Khasab (nudged)
    (10, 46.2, 6.1),    # Geneva
    (12, 36.1, -115.2), # Las Vegas
    (13, 21.0, 78.0),   # Rahul century, India
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
    "8  Basra fire",
    "9  Tanker off Khasab",
    "10  UN robot talks",
    "11  Pugh swim (at 9)",
    "12  F1 Academy, Vegas",
    "13  Rahul 124*",
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

    # Top strip.
    d.text((W // 2, 8),
           "35 STORIES  ·  7 REGIONS  ·  15 FIELDS  ·  EVERY ONE DATED — "
           "SATURDAY 21 NOVEMBER 2026",
           font=F_STRIP, fill=GREY, anchor="ma")
    hline(d, MARGIN, W - MARGIN, 30, color=LINE, width=1)

    # Title + masthead.
    d.text((W // 2, 34), "THE WORLD IN ONE DAY", font=F_TITLE, fill=INK,
           anchor="ma")
    d.text((W // 2, 76), "Saturday 21 November 2026", font=F_MAST, fill=INK,
           anchor="ma")
    hline(d, MARGIN, W - MARGIN, 132, color=RED, width=3)

    # Stat strip: 6 cells.
    sy, sh = 140, 56
    cell_w = CW // 6
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + i * cell_w
        d.rectangle([cx, sy, cx + cell_w - 1, sy + sh], fill=CARD_BG,
                    outline=LINE, width=1)
        d.text((cx + cell_w // 2, sy + 4), num, font=F_STAT_NUM, fill=RED,
               anchor="ma")
        d.text((cx + cell_w // 2, sy + 36), label, font=F_STAT_LBL,
               fill=(60, 60, 60), anchor="ma")

    # Region strip.
    ry = 202
    d.rectangle([MARGIN, ry, W - MARGIN, ry + 22], fill=DARK)
    region_text = "   ·   ".join("%s %d" % (name, n) for name, n in REGIONS)
    d.text((W // 2, ry + 4), region_text, font=F_REGION, fill=WHITE,
           anchor="ma")

    # Leads: 3 columns.
    ly, lh = 230, 160
    lead_w, lead_gap = 325, 10
    for i, lead in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + lead_gap)
        draw_lead(d, lx, ly, lead_w, lh, lead)
        if i:
            hx = lx - lead_gap // 2
            d.line([(hx, ly), (hx, ly + lh)], fill=LINE, width=1)

    # Features: 2 rows of 5.
    feat_w, feat_gap, feat_h = 193, 7, 118
    for row in range(2):
        fy = 398 + row * (feat_h + 8)
        for col in range(5):
            feat = FEATURES[row * 5 + col]
            fx = MARGIN + col * (feat_w + feat_gap)
            draw_feature(d, fx, fy, feat_w, feat_h, feat)

    # Lower band headers.
    hy = 650
    d.text((MARGIN, hy), "WHERE IT HAPPENED", font=F_SECTION, fill=INK,
           anchor="la")
    d.text((336, hy), "THE REST OF THE DAY — 22 MORE STORIES",
           font=F_SECTION, fill=INK, anchor="la")
    hline(d, MARGIN, 326, hy + 20, color=INK, width=1)
    hline(d, 336, W - MARGIN, hy + 20, color=INK, width=1)

    # Map + legend.
    draw_map(d, MARGIN, 676, 312, 130)
    for i, item in enumerate(LEGEND_LEFT):
        d.text((MARGIN, 812 + i * 12), item, font=F_LEGEND, fill=(60, 60, 60),
               anchor="la")
    for i, item in enumerate(LEGEND_RIGHT):
        d.text((MARGIN + 160, 812 + i * 12), item, font=F_LEGEND,
               fill=(60, 60, 60), anchor="la")

    # Briefs: 2 columns of 11.
    for col in range(2):
        bx = 336 + col * (329 + 16)
        for row in range(11):
            brief = BRIEFS[col * 11 + row]
            text, fnt = fit_one_line(d, "• " + brief, F_BRIEF,
                                     F_BRIEF_SMALL, 329)
            d.text((bx, 676 + row * 20), text, font=fnt, fill=INK, anchor="la")

    # DATE CHECK box.
    dy = 908
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
        d.text((W // 2, 958 + i * 14), line, font=F_FOOT, fill=GREY,
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


if __name__ == "__main__":
    main()
