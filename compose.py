#!/usr/bin/env python3
"""Build entry.png for make.fun news-image-20261121 (v4 rebuild, round 5).

A 1024x1024 newspaper front page summing up Saturday 21 November 2026:
3 illustrated leads + 10 features with WIDE TOP art + 23 one-line briefs +
an hour-by-hour UTC timeline strip + a light world map with numbered pins +
VOICES quotes + a DATE CHECK box with a "not yet known" section. All 36
stories are numbered 1-36; the map legend is keyed to those numbers.

v4 vs v3 (top-10 study, 14,328 entries; v3 round 4 ranked #644, 982,336,
bar #50 = 988,803):
- STORY SELECTION was v3's biggest gap. v3 featured stories the two most
  careful top entries (rank 1, rank 3) exclude as Friday — Kryvyi Rih,
  the Davao landing, Zelensky's NBC interview, Iran's uranium remark,
  Denmark's attaché expulsion — while MISSING consensus Saturday stories
  the top 10 all carry: the Iran strike on Bahrain bases (rank 1's lead),
  Mexico capturing Chapo Isidro, the EU-Indonesia trade pact, the
  drone-hit Russian ship off Finland, Geneva's killer-robot talks, the
  Basra power-station fire, England beating the All Blacks, the Banda
  Sea M6.8 quake. v4 features all of them and drops the Friday items.
- FEATURE ART: v3's 32px art strips were the weakest in the heat. v4
  gives every feature a 46px WIDE TOP illustration (the news-22 v5
  lesson: small side panels lose, wide top art wins).
- LEAD ART carries data in the picture now: the Gulf lead is a labelled
  map (Bahrain, Hormuz, 2 bases hit, 2 tankers hit); COP31 is a calendar
  strip (days 9-21, Day 13, +1 day); Peru is a depth cross-section.
- NEW: an hour-by-hour "THE DAY IN UTC" timeline strip (ranks 1, 3, 5
  all have one; v3 had none).
- MAP: solid light-tan landmass instead of the dotted halftone that read
  as noise; 9 regions (Asia split into South / East / SE, as rank 1).
- DATE CHECK gains a "Not yet known when drawn" section.

Date discipline: every story happened, or was first reported, on Saturday
21 November 2026 (UTC). Friday 20 Nov items — Kryvyi Rih strike, Davao
landing, Zelensky NBC interview, Iran uranium remark, Denmark's attaché
expulsion, Trump AI tax, UK-EU reset, Hodeidah port strike, China-Japan
Taiwan words, Kyiv barrage, Wall Street sell-off, Akvan landfall, Manipur
liquor toll — are named in DATE CHECK and kept out, even though several
top-10 entries carry them as Saturday news. The user chose honest.

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
MAP_BG = (240, 233, 214)
MAP_LAND = (201, 184, 138)
MAP_SEA = (214, 228, 232)
WHITE = (255, 255, 255)
SHADOW = (222, 214, 196)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
LIB_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


def libfont(name, size):
    return ImageFont.truetype(LIB_DIR + name, size)


F_STRIP = font("DejaVuSans-Bold.ttf", 12)
F_MAST = font("DejaVuSerif-Bold.ttf", 50)
F_SUBLINE = libfont("LiberationSerif-Italic.ttf", 14)
F_TIME_LBL = font("DejaVuSans-Bold.ttf", 11)
F_TIME_TXT = font("DejaVuSans.ttf", 10)
F_TIME_TM = font("DejaVuSans-Bold.ttf", 10)
F_STAT_NUM = font("DejaVuSans-Bold.ttf", 24)
F_STAT_LBL = font("DejaVuSans.ttf", 11)
F_REGION = font("DejaVuSans-Bold.ttf", 12)
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
F_ART_LBL = font("DejaVuSans-Bold.ttf", 9)
F_ART_NUM = font("DejaVuSans-Bold.ttf", 16)

# ---------------------------------------------------------------- stories
# Every story happened, or was first reported, on Saturday 21 November 2026
# (UTC). Tags: CONFIRMED (2+ outlets), OFFICIAL (on the record), REPORTED
# (single-source claim). Sources are the outlets that carried each story.

LEADS = [
    {
        "num": 1,
        "kicker": "WAR IN THE GULF  ·  21:18 UTC",
        "headline": "Iran strikes Bahrain bases; two tankers hit",
        "deck": "Bahrain says a site was set on fire; US jets answer; "
                "oil jumps 9% as the Gulf war widens.",
        "tag": "CONFIRMED",
        "source": "Reuters · AP · UKMTO",
        "art": "gulf",
    },
    {
        "num": 2,
        "kicker": "CLIMATE  ·  DAY 13",
        "headline": "COP31 talks run into overtime — still no deal",
        "deck": "Negotiators push past the deadline; the draft drops fossil "
                "fuels and adaptation cash stalls.",
        "tag": "OFFICIAL",
        "source": "Reuters · Guardian",
        "art": "cop31",
    },
    {
        "num": 3,
        "kicker": "DISASTER  ·  00:09 UTC",
        "headline": "Magnitude 6.7 quake shakes Peru, felt in Lima",
        "deck": "108 km deep near Junín; felt across central Peru and in "
                "Lima. One injured, no deaths.",
        "tag": "CONFIRMED",
        "source": "USGS · IGP",
        "art": "quake",
    },
]

FEATURES = [
    {
        "num": 4, "label": "MEXICO · 11 DEAD", "color": (140, 47, 47),
        "headline": "Mexico captures Chapo Isidro; 11 dead",
        "deck": "Dawn raid seizes the cartel boss; gunmen torch trucks.",
        "tag": "CONFIRMED", "source": "AP · Reuters", "art": "chapo",
    },
    {
        "num": 5, "label": "TRADE · €17.4BN", "color": (15, 118, 110),
        "headline": "EU and Indonesia sign trade pact",
        "deck": "Deal signed in Jakarta; tariffs fall on 90% of goods.",
        "tag": "OFFICIAL", "source": "Reuters · AFP", "art": "trade",
    },
    {
        "num": 6, "label": "FINLAND · SHIP HIT", "color": (3, 105, 161),
        "headline": "Drones hit Russian ship off Finland",
        "deck": "Fire aboard in the Gulf; crew rescued by Helsinki.",
        "tag": "CONFIRMED", "source": "Reuters · Yle", "art": "ship",
    },
    {
        "num": 7, "label": "GENEVA · 128 NATIONS", "color": (109, 40, 217),
        "headline": "128 nations back killer-robot talks",
        "deck": "First UN talks on autonomous weapons start in March.",
        "tag": "OFFICIAL", "source": "UN · AP", "art": "robots",
    },
    {
        "num": 8, "label": "BASRA · 4 KILLED", "color": (180, 83, 9),
        "headline": "Fire at Basra power station kills 4",
        "deck": "Blaze knocks out power for 200,000 homes.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "basra",
    },
    {
        "num": 9, "label": "RUGBY · 37–12", "color": (21, 128, 61),
        "headline": "England stun All Blacks 37–12",
        "deck": "Six tries at Twickenham; first home win in a decade.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "rugby",
    },
    {
        "num": 10, "label": "BANDA SEA · M6.8", "color": (153, 27, 27),
        "headline": "M6.8 quake off East Timor rattles Darwin",
        "deck": "Deep quake, no tsunami; tremors felt in Darwin.",
        "tag": "CONFIRMED", "source": "USGS · BMKG", "art": "banda",
    },
    {
        "num": 11, "label": "BITCOIN · $56,814", "color": (180, 83, 9),
        "headline": "Bitcoin sinks to $56,814, a 2026 low",
        "deck": "Down 3.6%, then back over $60,000 by evening.",
        "tag": "CONFIRMED", "source": "Reuters", "art": "bitcoin",
    },
    {
        "num": 12, "label": "BROWN · 2 KILLED", "color": (49, 46, 129),
        "headline": "Gunman kills 2 students at Brown University",
        "deck": "9 wounded in the engineering building; gunman at large.",
        "tag": "CONFIRMED", "source": "AP", "art": "brown",
    },
    {
        "num": 13, "label": "LAS VEGAS · POLE", "color": (190, 24, 93),
        "headline": "Verstappen takes pole in Las Vegas",
        "deck": "Antonelli fastest but a 5-place penalty hands him pole.",
        "tag": "CONFIRMED", "source": "F1", "art": "f1",
    },
]

BRIEFS = [
    "BepiColombo fires its 37-minute burn to orbit Mercury (ESA)",
    "TAIWAN — 21 Chinese jets cross the median line (Taipei)",
    "WELLINGTON — Rahul 136; India 486/4 at stumps (Reuters)",
    "GAZA — Drone strike kills 3 in Gaza City (Al Jazeera)",
    "HORMUZ — IRGC says it shot down 2 US drones (IRIB)",
    "TEHRAN — 50,000 march against the war (Reuters)",
    "PARIS — 82,500 march on the cost of living (AFP)",
    "ZAGREB — Floods swamp homes after days of rain (AP)",
    "TURIN — Alcaraz meets Shelton in ATP Finals semis (ATP)",
    "NEWCASTLE — Arsenal held 2–2 at St James' Park (AP)",
    "DUBLIN — Ireland beat South Africa 20–17 (Reuters)",
    "CARDIFF — Wales lose 26–9 to New Zealand (BBC)",
    "WASHINGTON — Trump appears to confirm FBI breach (AP)",
    "BRASÍLIA — Bolsonaro moved to intensive care (Reuters)",
    "MELBOURNE — Cricket Australia backs Cummins (AAP)",
    "MELBOURNE — Australia beat England by 3 wickets (AP)",
    "TEXAS — Execution takes over an hour (01:08 UTC) (ABC)",
    "BLUE NILE — Sudan army says it is restoring security (SUNA)",
    "ETHIOPIA — 700,000 displaced by conflict (UN)",
    "DHAKA — Measles kills 7 children in a week (UNICEF)",
    "LAHORE — Pakistan drop Rizwan, Masood for Tests (PCB)",
    "FUKUSHIMA — Snow strands 1,500 on mountain roads (NHK)",
    "BALI — Russian Interpol fugitive arrested (Police)",
]

VOICES = [
    ("“The situation is tense but under control.”",
     "— Bahrain government spokesperson"),
    ("“We have a text. Now we need a decision.”",
     "— COP31 presidency"),
]

TIMELINE = [
    ("00:09", "Peru quake M6.7"),
    ("02:00", "Riyadh: 3 downed"),
    ("05:02", "F1 pole decided"),
    ("09:42", "Banda Sea M6.8"),
    ("18:24", "BepiColombo burn"),
    ("21:18", "Bahrain strike"),
]

STATS = [
    ("6.7", "Peru quake magnitude"),
    ("128", "nations back robot talks"),
    ("11", "dead in Chapo Isidro raid"),
    ("$56,814", "Bitcoin Saturday low"),
    ("82,500", "marchers in France"),
    ("37–12", "England over All Blacks"),
]

REGIONS = [
    ("EUROPE", 11), ("MIDDLE EAST", 5), ("AFRICA", 2),
    ("SOUTH ASIA", 2), ("EAST ASIA", 2), ("SE ASIA", 2),
    ("AMERICAS", 7), ("OCEANIA", 3), ("GLOBAL", 2),
]

DATE_CHECK = [
    "DATE CHECK — Left out (Friday 20 Nov): Kryvyi Rih strike · Davao landing · "
    "Zelensky's NBC interview · Iran uranium remark · Denmark's attaché expulsion",
    "Trump AI tax · UK–EU reset · Hodeidah strike · China–Japan words · "
    "Kyiv barrage · Wall St sell-off · Akvan landfall · Manipur toll · Thu 19: ICJ ruling · GTA VI launch",
    "Not yet known when drawn: COP31 approval session (Sun 06:00 GMT) · Las Vegas "
    "GP race (Sun 04:00 UTC) · Dragon splashdown · BepiColombo capture",
]

FOOTER = [
    "Every story happened, or was first reported, on Saturday 21 November 2026 (UTC).",
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


def chip(d, x, y, text, fnt, bg, fg=WHITE):
    """Small rounded-ish label chip; returns its width."""
    tw = d.textlength(text, font=fnt) + 10
    d.rectangle([x, y, x + tw, y + 14], fill=bg)
    d.text((x + 5, y + 1), text, font=fnt, fill=fg, anchor="la")
    return tw


# ---------------------------------------------------------------- lead art
# Three data-rich scenes, one per lead. All shapes are drawn in code.

def art_gulf(d, x, y, w, h):
    """Labelled Gulf map: Bahrain, Hormuz, 2 bases hit, 2 tankers hit."""
    d.rectangle([x, y, x + w, y + h], fill=MAP_SEA)
    # Arabian peninsula landmass (stylised polygon, left/bottom).
    d.polygon([(x, y + h), (x, y + 22), (x + 52, y + 10), (x + 110, y + 18),
               (x + 150, y + 34), (x + 168, y + 56), (x + 150, y + h)],
              fill=MAP_LAND)
    # Iran landmass (top right).
    d.polygon([(x + 190, y), (x + w, y), (x + w, y + 26),
               (x + 240, y + 18), (x + 205, y + 10)], fill=MAP_LAND)
    # Qatar bump.
    d.polygon([(x + 168, y + 40), (x + 190, y + 34), (x + 196, y + 44),
               (x + 180, y + 52)], fill=MAP_LAND)
    d.text((x + 14, y + h - 16), "SAUDI ARABIA", font=F_ART_LBL,
           fill=(120, 100, 60), anchor="la")
    d.text((x + 240, y + 2), "IRAN", font=F_ART_LBL, fill=(120, 100, 60),
           anchor="la")
    d.text((x + 205, y + 30), "GULF", font=F_ART_LBL, fill=(70, 110, 140),
           anchor="la")
    # Bahrain: red dot + label + hit chip.
    bx, by = x + 172, y + 30
    d.ellipse([bx - 5, by - 5, bx + 5, by + 5], fill=RED, outline=WHITE,
              width=1)
    d.text((bx + 8, by - 11), "BAHRAIN", font=F_ART_LBL, fill=INK,
           anchor="la")
    chip(d, bx + 8, by + 2, "2 BASES HIT", F_ART_LBL, RED)
    # Hormuz: strait marker at the far right, label left of it.
    hx, hy = x + 302, y + 28
    d.ellipse([hx - 4, hy - 4, hx + 4, hy + 4], fill=RED, outline=WHITE,
              width=1)
    d.text((x + 248, y + 20), "HORMUZ", font=F_ART_LBL, fill=INK,
           anchor="la")
    # Two tanker icons in the Gulf.
    for tx, ty in ((x + 205, y + 40), (x + 225, y + 48)):
        d.rectangle([tx, ty, tx + 22, ty + 6], fill=(40, 60, 80))
        d.rectangle([tx + 15, ty - 4, tx + 19, ty], fill=(40, 60, 80))
        d.line([(tx, ty + 8), (tx + 22, ty + 8)], fill=(255, 255, 255),
               width=1)
    chip(d, x + 200, y + h - 16, "2 TANKERS HIT", F_ART_LBL, (40, 60, 80))
    # Oil chip top-left.
    chip(d, x + 6, y + 6, "OIL +9%", F_ART_LBL, (31, 77, 74))


def art_cop31(d, x, y, w, h):
    """COP31 calendar strip: days 9-21, Day 13, +1 day; globe + thermometer."""
    d.rectangle([x, y, x + w, y + h], fill=(31, 77, 74))
    # Globe left.
    cx, cy, r = x + 30, y + h // 2 + 2, 20
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(96, 165, 200),
              outline=(220, 235, 225), width=2)
    d.ellipse([cx - 11, cy - 12, cx + 2, cy - 2], fill=(110, 168, 110))
    d.ellipse([cx - 2, cy + 3, cx + 12, cy + 14], fill=(110, 168, 110))
    # Thermometer.
    tx = x + 58
    d.rectangle([tx, y + 8, tx + 8, y + h - 14], fill=(247, 243, 234))
    d.rectangle([tx + 2, y + 12, tx + 6, y + h - 18], fill=(220, 60, 60))
    d.ellipse([tx - 2, y + h - 18, tx + 10, y + h - 6], fill=(220, 60, 60))
    d.text((tx + 12, y + 8), "+1.5°C", font=F_ART_LBL, fill=(255, 190, 190),
           anchor="la")
    d.text((tx + 12, y + 20), "AT RISK", font=F_ART_LBL, fill=(255, 190, 190),
           anchor="la")
    # Calendar: 13 day cells, days 9..21, in two rows (7 + 6).
    cal_x, cal_y = x + 118, y + 6
    cell = 20
    for i, day in enumerate(range(9, 22)):
        row, col = divmod(i, 7)
        px = cal_x + col * (cell + 2)
        py = cal_y + row * (cell + 2)
        if day == 21:
            fill, fg = RED, WHITE
        elif day == 13:
            fill, fg = (255, 220, 120), INK
        else:
            fill, fg = (247, 243, 234), (60, 60, 60)
        d.rectangle([px, py, px + cell, py + cell], fill=fill)
        d.text((px + cell // 2, py + 3), str(day), font=F_ART_LBL, fill=fg,
               anchor="ma")
    d.text((cal_x, cal_y + 46), "NOV · DAY 13 OF 13 · +1 DAY",
           font=F_ART_LBL, fill=(255, 220, 120), anchor="la")


def art_quake(d, x, y, w, h):
    """Peru quake: depth cross-section + seismograph trace."""
    d.rectangle([x, y, x + w, y + h], fill=(74, 62, 52))
    # Seismograph strip top.
    d.rectangle([x + 8, y + 6, x + w - 8, y + 28], fill=(247, 243, 234))
    mid = y + 17
    pts = []
    n = 44
    for i in range(n + 1):
        px = x + 8 + (w - 16) * i / n
        if i < 10:
            amp = 1
        elif i < 16:
            amp = 1 + (i - 10)
        elif i < 22:
            amp = 7 - (i - 16)
        elif i < 32:
            amp = 3
        else:
            amp = 1
        sign = 1 if i % 2 == 0 else -1
        pts.append((px, mid + sign * amp))
    d.line(pts, fill=RED, width=2, joint="curve")
    # Cross-section: ground layers with the hypocentre.
    gy = y + 34
    d.rectangle([x + 8, gy, x + w - 8, y + h - 6], fill=(120, 100, 80))
    d.line([(x + 8, gy + 10), (x + w - 8, gy + 10)], fill=(90, 75, 60),
           width=1)
    # Hypocentre star at 108 km depth.
    hx, hy = x + w // 2, y + h - 12
    for dx, dy in ((0, -6), (0, 6), (-6, 0), (6, 0), (-4, -4), (4, -4),
                   (-4, 4), (4, 4)):
        d.line([(hx, hy), (hx + dx, hy + dy)], fill=(255, 220, 120), width=2)
    d.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=(255, 240, 180))
    # Depth arrow + labels.
    d.line([(x + w - 18, gy + 2), (x + w - 18, y + h - 12)], fill=WHITE,
           width=1)
    d.text((x + w - 60, gy + 2), "108 KM", font=F_ART_LBL, fill=WHITE,
           anchor="la")
    d.text((x + 12, gy + 2), "JUNÍN", font=F_ART_LBL, fill=(255, 220, 120),
           anchor="la")
    d.text((x + 12, y + h - 16), "FELT IN LIMA", font=F_ART_LBL,
           fill=(255, 220, 120), anchor="la")


LEAD_ART = {"gulf": art_gulf, "cop31": art_cop31, "quake": art_quake}


# ---------------------------------------------------------------- feature art
# Ten WIDE TOP illustrations (strip ~193x46), one per feature card. All
# shapes are drawn in code; each scene reads at a glance at 300px.

def art_chapo(d, x, y, w, h):
    """Night raid: house, police lights, helicopter, burning truck."""
    d.rectangle([x, y, x + w, y + h], fill=(14, 18, 34))
    for sx, sy in ((10, 6), (50, 10), (150, 5), (180, 9)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(230, 230, 200))
    # Helicopter with searchlight.
    hx, hy = x + 130, y + 6
    d.ellipse([hx, hy, hx + 26, hy + 9], fill=(20, 20, 20))
    d.line([(hx - 6, hy + 1), (hx + 32, hy + 1)], fill=(180, 180, 180),
           width=2)
    d.polygon([(hx + 6, hy + 9), (hx + 20, hy + 9), (hx + 26, y + h - 8),
               (hx, y + h - 8)], fill=(255, 240, 160))
    # House with lit windows.
    d.rectangle([x + 12, y + 16, x + 70, y + h - 4], fill=(50, 45, 70))
    d.polygon([(x + 8, y + 16), (x + 41, y + 4), (x + 74, y + 16)],
              fill=(120, 30, 30))
    for wx in (20, 36, 52):
        d.rectangle([x + wx, y + 24, x + wx + 8, y + 32],
                    fill=(255, 220, 120))
    # Police lights.
    d.ellipse([x + 82, y + 26, x + 92, y + 36], fill=(255, 60, 60))
    d.ellipse([x + 96, y + 26, x + 106, y + 36], fill=(80, 120, 255))
    # Burning truck (right).
    d.rectangle([x + 160, y + 30, x + 186, y + h - 4], fill=(60, 60, 60))
    d.polygon([(x + 164, y + 30), (x + 170, y + 18), (x + 176, y + 30)],
              fill=(255, 140, 40))
    d.polygon([(x + 167, y + 30), (x + 170, y + 24), (x + 173, y + 30)],
              fill=(255, 220, 120))


def art_trade(d, x, y, w, h):
    """EU + Indonesia flags over a container ship."""
    d.rectangle([x, y, x + w, y + h], fill=(135, 190, 220))
    # EU flag.
    d.rectangle([x + 10, y + 6, x + 58, y + 22], fill=(0, 51, 153))
    for i in range(12):
        import math
        a = 2 * math.pi * i / 12
        sx = x + 34 + int(7 * math.cos(a))
        sy = y + 14 + int(5 * math.sin(a))
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 204, 0))
    # Indonesia flag.
    d.rectangle([x + 66, y + 6, x + 114, y + 14], fill=(200, 30, 40))
    d.rectangle([x + 66, y + 14, x + 114, y + 22], fill=(255, 255, 255))
    # "90% cut" chip in the empty sky, top right.
    chip(d, x + 118, y + 8, "90% CUT", F_ART_LBL, (15, 118, 110))
    # Sea + container ship.
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(30, 100, 160))
    sx, sy = x + 40, y + h - 12
    d.rectangle([sx, sy - 12, sx + 110, sy], fill=(40, 40, 40))
    for cx, cc in ((sx + 8, (200, 60, 60)), (sx + 30, (60, 160, 60)),
                   (sx + 52, (230, 180, 40)), (sx + 74, (60, 120, 200))):
        d.rectangle([cx, sy - 22, cx + 20, sy - 12], fill=cc)
    d.rectangle([sx + 96, sy - 26, sx + 106, sy - 12], fill=(220, 220, 220))


def art_ship(d, x, y, w, h):
    """Ship on fire in the Gulf of Finland, drones overhead."""
    d.rectangle([x, y, x + w, y + h], fill=(180, 205, 220))
    # Sky + drones.
    for dx, dy in ((30, 8), (150, 6)):
        d.rectangle([x + dx, y + dy, x + dx + 16, y + dy + 3],
                    fill=(40, 40, 40))
        d.line([(x + dx - 4, y + dy - 2), (x + dx + 20, y + dy - 2)],
               fill=(90, 90, 90), width=1)
    # Sea.
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(40, 110, 170))
    for wx in range(6, w, 24):
        d.arc([x + wx, y + h - 12, x + wx + 14, y + h - 4], start=180,
              end=360, fill=(220, 240, 255), width=1)
    # Ship hull + bridge, listing slightly.
    sx, sy = x + 45, y + h - 12
    d.polygon([(sx, sy - 14), (sx + 100, sy - 14), (sx + 92, sy),
               (sx + 8, sy)], fill=(90, 40, 40))
    d.rectangle([sx + 70, sy - 26, sx + 86, sy - 14], fill=(220, 220, 220))
    # Flames + smoke.
    for fx in (sx + 20, sx + 40):
        d.polygon([(fx, sy - 14), (fx + 7, sy - 30), (fx + 14, sy - 14)],
                  fill=(255, 140, 40))
        d.polygon([(fx + 4, sy - 14), (fx + 7, sy - 24), (fx + 10, sy - 14)],
                  fill=(255, 220, 120))
    for ox, oy, orr in ((sx + 30, sy - 34, 5), (sx + 38, sy - 40, 4)):
        d.ellipse([ox - orr, oy - orr, ox + orr, oy + orr],
                  fill=(120, 120, 120))


def art_robots(d, x, y, w, h):
    """UN hall: robot figure + dove + 128-nation chip."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 50, 90))
    # Flags row (UN-style blue banners).
    for fx in range(8, w - 8, 18):
        d.rectangle([x + fx, y + 4, x + fx + 10, y + 16],
                    fill=(100, 160, 220))
    # Robot figure.
    rx, ry = x + 30, y + 14
    d.rectangle([rx, ry, rx + 26, ry + 12], fill=(180, 180, 180))
    d.rectangle([rx + 4, ry + 14, rx + 22, ry + 28], fill=(140, 140, 140))
    d.ellipse([rx + 6, ry + 4, rx + 10, ry + 8], fill=(255, 60, 60))
    d.ellipse([rx + 16, ry + 4, rx + 20, ry + 8], fill=(255, 60, 60))
    d.line([(rx - 6, ry + 16), (rx + 4, ry + 16)], fill=(180, 180, 180),
           width=3)
    d.line([(rx + 22, ry + 16), (rx + 32, ry + 16)], fill=(180, 180, 180),
           width=3)
    # Dove (white bird shape).
    dx, dy = x + 120, y + 16
    d.polygon([(dx, dy + 8), (dx + 18, dy), (dx + 36, dy + 8),
               (dx + 18, dy + 14)], fill=(255, 255, 255))
    d.ellipse([dx + 14, dy + 6, dx + 22, dy + 12], fill=(255, 255, 255))


def art_basra(d, x, y, w, h):
    """Power station on fire, transmission tower, smoke."""
    d.rectangle([x, y, x + w, y + h], fill=(40, 30, 26))
    # Cooling towers.
    for tx in (14, 52):
        d.polygon([(x + tx, y + h - 6), (x + tx + 6, y + 12),
                   (x + tx + 26, y + 12), (x + tx + 32, y + h - 6)],
                  fill=(120, 110, 100))
    # Flames between towers.
    for fx in (36, 84):
        d.polygon([(x + fx, y + h - 6), (x + fx + 8, y + 10),
                   (x + fx + 16, y + h - 6)], fill=(255, 140, 40))
        d.polygon([(x + fx + 5, y + h - 6), (x + fx + 8, y + 20),
                   (x + fx + 11, y + h - 6)], fill=(255, 220, 120))
    # Smoke.
    for ox, oy, orr in ((60, 8, 6), (72, 4, 5), (100, 8, 6)):
        d.ellipse([x + ox - orr, y + oy - orr, x + ox + orr, y + oy + orr],
                  fill=(90, 90, 90))
    # Transmission tower (right).
    tx = x + 150
    d.line([(tx, y + 6), (tx + 8, y + h - 6)], fill=(180, 180, 180), width=2)
    d.line([(tx + 16, y + 6), (tx + 8, y + h - 6)], fill=(180, 180, 180),
           width=2)
    d.line([(tx - 4, y + 10), (tx + 20, y + 10)], fill=(180, 180, 180),
           width=2)
    d.line([(tx - 2, y + 18), (tx + 18, y + 18)], fill=(180, 180, 180),
           width=2)
    # Sparks.
    for sx, sy in ((120, 14), (132, 20), (140, 10)):
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2],
                  fill=(255, 220, 120))


def art_rugby(d, x, y, w, h):
    """Rugby pitch, ball, posts, 37-12 scoreboard."""
    d.rectangle([x, y, x + w, y + h], fill=(40, 130, 70))
    # Pitch lines.
    d.line([(x + 10, y + 8), (x + w - 10, y + 8)], fill=(255, 255, 255),
           width=1)
    d.line([(x + 10, y + h - 8), (x + w - 10, y + h - 8)],
           fill=(255, 255, 255), width=1)
    # Goal posts.
    px = x + 24
    d.line([(px, y + 6), (px, y + 30)], fill=(255, 255, 255), width=2)
    d.line([(px + 16, y + 6), (px + 16, y + 30)], fill=(255, 255, 255),
           width=2)
    d.line([(px, y + 22), (px + 16, y + 22)], fill=(255, 255, 255), width=2)
    # Rugby ball (oval) mid-pitch.
    bx, by = x + 96, y + h // 2 + 2
    d.ellipse([bx - 20, by - 10, bx + 20, by + 10], fill=(160, 90, 40),
              outline=(255, 255, 255), width=1)
    d.line([(bx - 12, by), (bx + 12, by)], fill=(255, 255, 255), width=1)
    # Scoreboard chip.
    chip(d, x + w - 62, y + 6, "37–12", F_ART_NUM, (21, 128, 61))
    d.text((x + w - 62, y + 28), "6 TRIES", font=F_ART_LBL, fill=WHITE,
           anchor="la")


def art_banda(d, x, y, w, h):
    """Banda Sea quake: seismograph + ocean wave + M6.8 chip."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 50, 80))
    # Seismograph trace.
    mid = y + 14
    pts = []
    n = 40
    for i in range(n + 1):
        px = x + 8 + (w - 16) * i / n
        if i < 8:
            amp = 1
        elif i < 14:
            amp = 1 + (i - 8)
        elif i < 20:
            amp = 7 - (i - 14)
        elif i < 30:
            amp = 3
        else:
            amp = 1
        sign = 1 if i % 2 == 0 else -1
        pts.append((px, mid + sign * amp))
    d.line(pts, fill=(255, 220, 120), width=2, joint="curve")
    # Ocean wave.
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(40, 110, 170))
    for wx in range(4, w, 20):
        d.arc([x + wx, y + h - 14, x + wx + 16, y + h - 2], start=180,
              end=360, fill=(220, 240, 255), width=2)
    chip(d, x + 8, y + h - 30, "M6.8", F_ART_NUM, RED)
    d.text((x + 62, y + h - 28), "NO TSUNAMI", font=F_ART_LBL,
           fill=(220, 240, 255), anchor="la")


def art_bitcoin(d, x, y, w, h):
    """Bitcoin: chart falls to the low, then rebounds; coin."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 26, 20))
    # Falling-then-rising chart line.
    d.line([(x + 8, y + 8), (x + 45, y + 14), (x + 80, y + 30),
            (x + 115, y + 24), (x + 140, y + 14)], fill=(220, 60, 60),
           width=3)
    d.line([(x + 80, y + 30), (x + 115, y + 24), (x + 140, y + 14)],
           fill=(60, 200, 100), width=3)
    d.polygon([(x + 140, y + 14), (x + 132, y + 10), (x + 136, y + 18)],
              fill=(60, 200, 100))
    # Low marker.
    d.text((x + 66, y + 32), "LOW", font=F_ART_LBL, fill=(255, 190, 190),
           anchor="la")
    # Coin with B.
    cx, cy, r = x + w - 24, y + h // 2, 13
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 160, 40),
              outline=(255, 220, 140), width=2)
    d.text((cx, cy - 1), "B", font=F_FEAT_LBL, fill=(60, 40, 0), anchor="mm")


def art_brown(d, x, y, w, h):
    """Brown campus building at night, police lights."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 44))
    # Campus building with lit windows.
    d.rectangle([x + 24, y + 8, x + 120, y + h - 2], fill=(60, 55, 80))
    d.polygon([(x + 20, y + 8), (x + 72, y - 2), (x + 124, y + 8)],
              fill=(90, 40, 40))
    for wy in (14, 24, 34):
        for wx in (32, 50, 68, 86, 104):
            d.rectangle([x + wx, y + wy, x + wx + 9, y + wy + 6],
                        fill=(255, 220, 120))
    # Police light glow: red + blue.
    d.ellipse([x + 140, y + 8, x + 154, y + 22], fill=(255, 60, 60))
    d.ellipse([x + 160, y + 8, x + 174, y + 22], fill=(80, 120, 255))
    d.rectangle([x + 138, y + 28, x + 176, y + h - 2], fill=(40, 40, 60))
    d.rectangle([x + 144, y + 32, x + 170, y + 38], fill=(200, 200, 220))


def art_f1(d, x, y, w, h):
    """Las Vegas night: chequered flag, F1 car, strip lights."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 20, 28))
    # Strip lights.
    for lx, lc in ((10, (255, 60, 120)), (30, (60, 200, 255)),
                   (150, (255, 220, 60)), (170, (255, 60, 120))):
        d.ellipse([x + lx, y + 5, x + lx + 4, y + 9], fill=lc)
    # Chequered flag, top right.
    for r in range(3):
        for c in range(4):
            fill = WHITE if (r + c) % 2 == 0 else INK
            d.rectangle([x + w - 36 + c * 7, y + 4 + r * 6,
                         x + w - 30 + c * 7, y + 9 + r * 6], fill=fill)
    # F1 car silhouette: low body, wing, two wheels.
    cx, cy = x + 28, y + h - 14
    d.polygon([(cx, cy), (cx + 95, cy), (cx + 105, cy - 6),
               (cx + 62, cy - 8), (cx + 42, cy - 13), (cx + 10, cy - 6)],
              fill=(200, 30, 50))
    d.rectangle([cx + 101, cy - 15, cx + 105, cy - 4], fill=(200, 30, 50))
    for wx in (cx + 14, cx + 82):
        d.ellipse([wx, cy - 2, wx + 15, cy + 13], fill=(10, 10, 10),
                  outline=(180, 180, 180), width=1)
    d.rectangle([x, y + h - 3, x + w, y + h], fill=(120, 120, 120))
    chip(d, x + 6, y + h - 26, "POLE", F_ART_LBL, (190, 24, 93))


FEATURE_ART = {
    "chapo": art_chapo, "trade": art_trade, "ship": art_ship,
    "robots": art_robots, "basra": art_basra, "rugby": art_rugby,
    "banda": art_banda, "bitcoin": art_bitcoin, "brown": art_brown,
    "f1": art_f1,
}


# ---------------------------------------------------------------- card drawing

def draw_lead(d, x, y, w, h, lead):
    # 4D depth: soft shadow under the art panel.
    d.rectangle([x + 2, y + 2, x + w + 2, y + 68], fill=SHADOW)
    art_h = 64
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
    # 4D depth: soft shadow under the card.
    d.rectangle([x + 2, y + 2, x + w + 2, y + h + 2], fill=SHADOW)
    d.rectangle([x, y, x + w, y + h], fill=CARD_BG, outline=LINE, width=1)
    art_h = 46
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
# inclusive column ranges that hold land. Drawn as a solid light landmass
# (the dotted halftone read as noise at 300px).

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
# Gulf pins are nudged apart so the numbers stay readable. No pin for 11
# (Bitcoin, global) — the legend says so.
PINS = [
    (1, 22.5, 53.0),    # Bahrain (nudged south-east, clear of Basra)
    (2, 36.9, 30.7),    # COP31, Antalya
    (3, -11.0, -76.0),  # Peru quake, Junín
    (4, 24.8, -107.4),  # Chapo Isidro, Sinaloa
    (5, -6.2, 106.8),   # EU-Indonesia pact, Jakarta
    (6, 59.9, 23.0),    # Ship hit, Gulf of Finland
    (7, 45.0, 8.0),     # Geneva (nudged south-east, clear of London)
    (8, 32.5, 44.5),    # Basra (nudged north-west, clear of Bahrain)
    (9, 52.5, -2.0),    # Twickenham (nudged north-west, clear of Geneva)
    (10, -6.0, 129.0),  # Banda Sea quake
    (12, 41.8, -71.4),  # Brown University, Providence
    (13, 36.1, -115.2), # Las Vegas
]

LEGEND_LEFT = [
    "1  Gulf strike",
    "2  COP31 overtime",
    "3  Peru quake M6.7",
    "4  Chapo captured",
    "5  EU–Indonesia pact",
    "6  Ship hit off Finland",
    "7  Geneva robot talks",
]
LEGEND_RIGHT = [
    "8  Basra fire",
    "9  England 37–12",
    "10  Banda Sea M6.8",
    "11  Bitcoin — no pin",
    "12  Brown shooting",
    "13  Verstappen pole",
]


def draw_map(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=MAP_BG, outline=LINE, width=1)
    cell_w, cell_h = w / 60, h / 30
    for r, ranges in enumerate(LAND):
        for c0, c1 in ranges:
            d.rectangle([x0 + c0 * cell_w, y0 + r * cell_h,
                         x0 + (c1 + 1) * cell_w, y0 + (r + 1) * cell_h],
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
    d.text((MARGIN, 6), "THE WORLD IN ONE DAY", font=F_STRIP, fill=RED,
           anchor="la")
    d.text((W - MARGIN, 6),
           "36 STORIES  ·  9 REGIONS  ·  EVERY ONE DATED",
           font=F_STRIP, fill=GREY, anchor="ra")
    hline(d, MARGIN, W - MARGIN, 26, color=RED, width=2)

    # Masthead: the date IS the headline (as in the top entries).
    d.text((W // 2, 30), "Saturday 21 November 2026", font=F_MAST, fill=INK,
           anchor="ma")
    d.text((W // 2, 88),
           "Iran hits Bahrain bases  ·  a deep quake shakes Peru  ·  "
           "COP31 runs into overtime",
           font=F_SUBLINE, fill=(60, 60, 60), anchor="ma")
    hline(d, MARGIN, W - MARGIN, 108, color=INK, width=2)

    # Timeline strip: the day in UTC (NEW in v4).
    ty0, th = 112, 24
    d.rectangle([MARGIN, ty0, W - MARGIN, ty0 + th], fill=(232, 226, 208),
                outline=LINE, width=1)
    d.text((MARGIN + 8, ty0 + 5), "THE DAY IN UTC", font=F_TIME_LBL,
           fill=RED, anchor="la")
    tx = MARGIN + 122
    avail = CW - 122 - 8
    slot = avail // len(TIMELINE)
    for i, (tm, txt) in enumerate(TIMELINE):
        cx = tx + i * slot
        d.text((cx, ty0 + 5), tm, font=F_TIME_TM, fill=RED, anchor="la")
        tw = d.textlength(tm + " ", font=F_TIME_TM)
        label, lfnt = fit_one_line(d, txt, F_TIME_TXT, F_TIME_TXT,
                                   slot - tw - 4)
        d.text((cx + tw, ty0 + 5), label, font=lfnt, fill=INK, anchor="la")
        if i:
            d.line([(cx - 5, ty0 + 4), (cx - 5, ty0 + th - 4)], fill=LINE,
                   width=1)

    # Stat strip: 6 cells.
    sy, sh = 140, 52
    cell_w = CW // 6
    for i, (num, label) in enumerate(STATS):
        cx = MARGIN + i * cell_w
        d.rectangle([cx + 1, sy + 1, cx + cell_w, sy + sh + 1], fill=SHADOW)
        d.rectangle([cx, sy, cx + cell_w - 1, sy + sh], fill=CARD_BG,
                    outline=LINE, width=1)
        d.text((cx + cell_w // 2, sy + 3), num, font=F_STAT_NUM, fill=RED,
               anchor="ma")
        d.text((cx + cell_w // 2, sy + 32), label, font=F_STAT_LBL,
               fill=(60, 60, 60), anchor="ma")

    # Region strip.
    ry = 196
    d.rectangle([MARGIN, ry, W - MARGIN, ry + 20], fill=DARK)
    region_text = "   ·   ".join("%s %d" % (name, n) for name, n in REGIONS)
    d.text((W // 2, ry + 3), region_text, font=F_REGION, fill=WHITE,
           anchor="ma")

    # Leads: 3 columns.
    ly, lh = 220, 164
    lead_w, lead_gap = 325, 10
    for i, lead in enumerate(LEADS):
        lx = MARGIN + i * (lead_w + lead_gap)
        draw_lead(d, lx, ly, lead_w, lh, lead)
        if i:
            hx = lx - lead_gap // 2
            d.line([(hx, ly), (hx, ly + lh)], fill=LINE, width=1)

    # Features: 2 rows of 5, each card with WIDE TOP art.
    feat_w, feat_gap, feat_h = 193, 7, 117
    for row in range(2):
        fy = 390 + row * (feat_h + 6)
        for col in range(5):
            feat = FEATURES[row * 5 + col]
            fx = MARGIN + col * (feat_w + feat_gap)
            draw_feature(d, fx, fy, feat_w, feat_h, feat)

    # VOICES: two verbatim quotes, side by side.
    vy = 636
    d.rectangle([MARGIN + 1, vy + 1, W - MARGIN + 1, vy + 35], fill=SHADOW)
    d.rectangle([MARGIN, vy, W - MARGIN, vy + 34], fill=CARD_BG,
                outline=LINE, width=1)
    d.text((MARGIN + 8, vy + 3), "VOICES", font=F_KICKER, fill=RED,
           anchor="la")
    d.line([(MARGIN + 62, vy + 4), (MARGIN + 62, vy + 30)], fill=LINE,
           width=1)
    vx0 = MARGIN + 72
    half = (CW - 72) // 2
    for i, (quote, attr) in enumerate(VOICES):
        qx = vx0 + i * half
        d.text((qx, vy + 2), quote, font=F_VOICE, fill=INK, anchor="la")
        d.text((qx, vy + 19), attr, font=F_VOICE_ATTR, fill=GREY, anchor="la")
        if i:
            d.line([(qx - 8, vy + 4), (qx - 8, vy + 30)], fill=LINE, width=1)

    # Lower band headers.
    hy = 676
    d.text((MARGIN, hy), "WHERE IT HAPPENED", font=F_SECTION, fill=INK,
           anchor="la")
    d.text((336, hy), "ALSO ON SATURDAY 21 NOVEMBER — 23 MORE STORIES",
           font=F_SECTION, fill=INK, anchor="la")
    hline(d, MARGIN, 326, hy + 20, color=INK, width=1)
    hline(d, 336, W - MARGIN, hy + 20, color=INK, width=1)

    # Map + legend.
    draw_map(d, MARGIN, 700, 312, 114)
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
            d.text((bx, 700 + row * 17), text, font=fnt, fill=INK, anchor="la")

    # DATE CHECK box (3 lines: Friday exclusions + Thu + not-yet-known).
    dy = 908
    d.rectangle([MARGIN + 1, dy + 1, W - MARGIN + 1, dy + 55], fill=SHADOW)
    d.rectangle([MARGIN, dy, W - MARGIN, dy + 54], fill=(252, 240, 240),
                outline=RED, width=2)
    for i, line in enumerate(DATE_CHECK):
        if i == 0:
            prefix = "DATE CHECK — "
            d.text((MARGIN + 10, dy + 3), prefix, font=F_DATE_BOLD, fill=RED,
                   anchor="la")
            rest = line[len(prefix):]
            d.text((MARGIN + 10 + d.textlength(prefix, font=F_DATE_BOLD),
                    dy + 3), rest, font=F_DATE, fill=INK, anchor="la")
        else:
            d.text((MARGIN + 10, dy + 3 + i * 17), line, font=F_DATE,
                   fill=INK, anchor="la")

    # Footer.
    for i, line in enumerate(FOOTER):
        d.text((W // 2, 970 + i * 13), line, font=F_FOOT, fill=GREY,
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
    # DATE CHECK fit check: all lines must fit inside the box (inner 976px).
    from PIL import ImageDraw as _ID
    _d = _ID.Draw(img)
    for i, line in enumerate(DATE_CHECK):
        wpx = _d.textlength(line, font=F_DATE)
        print("date-check line %d: %.0fpx (limit 976)" % (i + 1, wpx))
        assert wpx <= 976, "DATE CHECK line %d overflows" % (i + 1)
    # Region strip fit check.
    region_text = "   ·   ".join("%s %d" % (name, n) for name, n in REGIONS)
    rw = _d.textlength(region_text, font=F_REGION)
    print("region strip: %.0fpx (limit 996)" % rw)
    assert rw <= 996, "region strip overflows"
    # Timeline fit check.
    slot = (CW - 122 - 8) // len(TIMELINE)
    for tm, txt in TIMELINE:
        tw = _d.textlength(tm + " " + txt, font=F_TIME_TXT)
        if tw > slot - 4:
            print("timeline tight: %s %s (%.0fpx vs slot %d)" % (tm, txt, tw,
                                                                slot - 4))


if __name__ == "__main__":
    main()
