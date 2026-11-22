#!/usr/bin/env python3
"""Compose the news-image-20261121 v5 entry: Saturday 21 November 2026.

Newspaper front page, 1024x1024, built from the #1 entry's presentation:
red header bars on leads, TALL data-carrying art on leads and features,
a real UTC timeline axis, sourced stat strip, coloured region strip,
smooth light world map, no VOICES band (none of the top 3 has one).

All 36 stories are genuinely dated Saturday 21 November 2026 (UTC).
Deterministic: no randomness, no time, no network.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 243, 232)
INK = (26, 26, 26)
GREY = (110, 108, 100)
LIGHT_LINE = (205, 198, 180)
RED = (192, 16, 46)
RED_DARK = (150, 10, 34)
GREEN = (30, 122, 52)
BLUE = (31, 95, 168)
BLACK = (20, 20, 20)
WHITE = (255, 255, 255)
CREAM2 = (238, 231, 214)
SKY = (213, 231, 240)
LAND = (232, 219, 178)
SEA = (198, 220, 232)

REGION_COLORS = {
    "Europe": (46, 111, 183),
    "Middle East": (198, 93, 33),
    "Africa": (46, 139, 87),
    "South Asia": (181, 154, 46),
    "East Asia": (184, 58, 122),
    "SE Asia": (58, 143, 184),
    "Americas": (123, 79, 168),
    "Oceania": (46, 158, 139),
    "Global": (85, 85, 85),
}

# ---------------------------------------------------------------- fonts
FD = "/usr/share/fonts/truetype/dejavu"
FL = "/usr/share/fonts/truetype/liberation"
_cache = {}


def font(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def serif_b(size):
    return font(FL + "/LiberationSerif-Bold.ttf", size)


def serif(size):
    return font(FL + "/LiberationSerif-Regular.ttf", size)


def serif_i(size):
    return font(FL + "/LiberationSerif-Italic.ttf", size)


def sans_b(size):
    return font(FL + "/LiberationSans-Bold.ttf", size)


def sans(size):
    return font(FL + "/LiberationSans-Regular.ttf", size)


def sans_i(size):
    return font(FL + "/LiberationSans-Italic.ttf", size)


# ---------------------------------------------------------------- helpers
def text_w(d, s, f):
    return d.textlength(s, font=f)


def wrap(d, text, f, max_w):
    """Greedy word wrap; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(d, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit_lines(d, text, f, max_w, max_lines):
    """Wrap text to at most max_lines; ellipsize the last line if needed."""
    lines = wrap(d, text, f, max_w)
    if len(lines) <= max_lines:
        return lines
    lines = lines[:max_lines]
    while lines and text_w(d, lines[-1] + "…", f) > max_w:
        lines[-1] = lines[-1][:-1]
    lines[-1] = lines[-1] + "…"
    return lines


def draw_wrapped(d, x, y, text, f, max_w, fill, leading=None, max_lines=None):
    if leading is None:
        leading = f.size + 2
    lines = wrap(d, text, f, max_w)
    if max_lines is not None:
        lines = fit_lines(d, text, f, max_w, max_lines)
    for i, ln in enumerate(lines):
        d.text((x, y + i * leading), ln, font=f, fill=fill)
    return y + len(lines) * leading


def badge(d, x, y, label, color):
    """Small rounded verification pill; returns width used."""
    f = sans_b(8)
    w = int(text_w(d, label, f)) + 12
    h = 12
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=color)
    d.text((x + 6, y + 1), label, font=f, fill=WHITE)
    return w


def kicker_line(d, x, y, w, number, label, verified):
    """Numbered red kicker + verification badge right-aligned."""
    f_num = sans_b(11)
    f_lab = sans_b(9)
    color = GREEN if verified == "CONFIRMED" else BLUE
    lab = "✓ " + verified
    bw = int(text_w(d, lab, sans_b(8))) + 12
    # truncate the label so it never runs under the badge
    max_lab = w - int(text_w(d, str(number), f_num)) - 5 - bw - 6
    while label and text_w(d, label, f_lab) > max_lab:
        label = label[:-1]
    if label.endswith((" ", "·", ",")):
        label = label[:-1]
    d.text((x, y), str(number), font=f_num, fill=RED)
    nx = x + int(text_w(d, str(number), f_num)) + 5
    d.text((nx, y + 1), label, font=f_lab, fill=INK)
    badge(d, x + w - bw, y, lab, color)


def shadow_box(d, box, fill, outline=None, radius=0, shadow=2):
    x0, y0, x1, y1 = box
    if shadow:
        d.rectangle([x0 + shadow, y0 + shadow, x1 + shadow, y1 + shadow],
                    fill=(225, 218, 198))
    if radius:
        d.rounded_rectangle(box, radius=radius, fill=fill,
                            outline=outline)
    else:
        d.rectangle(box, fill=fill, outline=outline)


# ---------------------------------------------------------------- data
SUB_DECK = ("Iran hits Bahrain bases  ·  a deep quake shakes Peru  ·  "
            "COP31 runs into overtime")

TIMELINE = [
    ("00:09", "Peru quake", 0.15),
    ("02:00", "Chapo held", 2.0),
    ("05:02", "F1 pole", 5.03),
    ("09:42", "Banda M6.8", 9.7),
    ("15:30", "EU pact", 15.5),
    ("18:24", "Mercury burn", 18.4),
    ("21:18", "Bahrain strike", 21.3),
]

STATS = [
    ("6.7", "Peru quake magnitude (USGS)"),
    ("2", "tankers hit off Khasab (UKMTO)"),
    ("128", "nations backing Geneva robot-arms talks"),
    ("90.4%", "tariff lines duty-free (IEU-CEPA)"),
    ("82,500", "marchers in France (ministry)"),
    ("37–12", "England over New Zealand"),
]

REGIONS = [
    ("Europe", 8), ("Middle East", 5), ("Africa", 3), ("South Asia", 3),
    ("East Asia", 2), ("SE Asia", 3), ("Americas", 5), ("Oceania", 3),
    ("Global", 4),
]

LEADS = [
    {
        "num": 1, "header": "GULF: IRAN STRIKES", "art": "gulf",
        "source": "Al Jazeera · Anadolu · Reuters · UKMTO",
        "kicker": "BAHRAIN · HORMUZ · IRAN WAR", "verified": "CONFIRMED",
        "headline": "Iran strikes Bahrain bases; tankers hit off Oman",
        "body": ("IRGC says it hit US radar at two bases; Bahrain says a "
                 "civilian plant burned. UKMTO: two tankers struck off Khasab."),
    },
    {
        "num": 2, "header": "PERU: QUAKE 6.7", "art": "quake",
        "source": "USGS · IGP · AFP · Anadolu",
        "kicker": "JUNÍN, PERU · EARTHQUAKE", "verified": "CONFIRMED",
        "headline": "Deep 6.7 earthquake shakes central Peru",
        "body": ("Centred near Ondores and felt in Lima; landslides and minor "
                 "damage, no deaths and no tsunami threat."),
    },
    {
        "num": 3, "header": "COP31: OVERTIME", "art": "cop31",
        "source": "Reuters · AFP · Anadolu",
        "kicker": "ANTALYA, TÜRKIYE · CLIMATE", "verified": "CONFIRMED",
        "headline": "COP31 climate talks run into overtime",
        "body": ("Talks in Antalya ran through Saturday over fossil fuels and "
                 "finance; approval session set for Sunday 06:00 GMT."),
    },
]

FEATURES = [
    {"num": 4, "art": "chapo", "kicker": "SINALOA · CRIME",
     "verified": "CONFIRMED",
     "headline": "Mexico captures cartel boss Chapo Isidro",
     "body": "FBI most-wanted; seized in Guasave. 11 dead in the raid.",
     "src": "AP · Al Jazeera · Mexican defence ministry"},
    {"num": 5, "art": "eucepa", "kicker": "INDONESIA–EU · TRADE",
     "verified": "OFFICIAL",
     "headline": "Indonesia and EU sign trade pact",
     "body": "Signed in Brussels; in force from 2027.",
     "src": "Ankara · Indonesian government"},
    {"num": 6, "art": "ship", "kicker": "FINLAND · SECURITY",
     "verified": "CONFIRMED",
     "headline": "Drones hit Russian ship off Finland",
     "body": "Crew evacuated; Finland suspects Ukraine.",
     "src": "Finnish MoD · Reuters · Anadolu"},
    {"num": 7, "art": "robot", "kicker": "GENEVA · ARMS",
     "verified": "CONFIRMED",
     "headline": "128 nations back killer-robot talks",
     "body": "US, Russia, Israel opposed binding rules.",
     "src": "AFP · Anadolu · Al Jazeera"},
    {"num": 8, "art": "fire", "kicker": "BASRA · DISASTER",
     "verified": "CONFIRMED",
     "headline": "Basra power-station fire kills 4",
     "body": "800 MW Hartha plant shut; 35 injured.",
     "src": "INA · Anadolu · Reuters"},
    {"num": 9, "art": "rugby", "kicker": "LONDON · RUGBY",
     "verified": "OFFICIAL",
     "headline": "England beat All Blacks 37–12",
     "body": "New Zealand's heaviest loss to England.",
     "src": "RNZ · match result"},
    {"num": 10, "art": "target", "kicker": "PAKISTAN · SECURITY",
     "verified": "OFFICIAL",
     "headline": "Pakistan says 15 militants killed",
     "body": "Balochistan raid; hideouts destroyed.",
     "src": "AFP · Al Jazeera · Dawn"},
    {"num": 11, "art": "bitcoin", "kicker": "WORLD · MARKETS",
     "verified": "CONFIRMED",
     "headline": "Bitcoin sinks to $56,814",
     "body": "A 2026 low; back over $60,000 by evening.",
     "src": "CoinGecko · Reuters"},
    {"num": 12, "art": "caf", "kicker": "ABUJA · FOOTBALL",
     "verified": "OFFICIAL",
     "headline": "All 54 CAF members back Infantino",
     "body": "FIFA vote set for March 2027 in Rabat.",
     "src": "CAF · AFP"},
    {"num": 13, "art": "f1", "kicker": "LAS VEGAS · F1",
     "verified": "OFFICIAL",
     "headline": "Verstappen takes pole in Las Vegas",
     "body": "Antonelli docked 5 places; Russell 2nd.",
     "src": "AP · Al Jazeera · F1 timing"},
]

BRIEFS = [
    (14, "BEPICOLOMBO", "37-minute burn to orbit Mercury (ESA)", "Global"),
    (15, "TAIWAN", "21 jets hold patrol; 15 cross line (Taipei)", "East Asia"),
    (16, "WELLINGTON", "Rahul 136; India 486/4 at stumps (Reuters)", "Oceania"),
    (17, "GAZA", "Drone strike on food-aid van kills 3 (AJ, Reuters)", "Middle East"),
    (18, "HORMUZ", "IRGC says it shot down 2 US drones (IRIB)", "Middle East"),
    (19, "TEHRAN", "50,000 march against the war (Reuters)", "Middle East"),
    (20, "PARIS", "82,500 march on living costs; Lisbon too (AFP)", "Europe"),
    (21, "ZAGREB", "Thousands protest over hospital death (AJ)", "Europe"),
    (22, "PAS-DE-CALAIS", "Floods swamp 850 homes (Anadolu)", "Europe"),
    (23, "NEWCASTLE", "Arsenal held 2-2 at St James' Park (AP)", "Europe"),
    (24, "DUBLIN", "Ireland beat South Africa 20-17 (Reuters)", "Europe"),
    (25, "CARDIFF", "Wallabies beat Wales 29-26 (ABC)", "Europe"),
    (26, "WASHINGTON", "Trump appears to confirm FBI breach (AP)", "Americas"),
    (27, "BRASILIA", "Bolsonaro moved to intensive care (Reuters)", "Americas"),
    (28, "MELBOURNE", "Cricket Australia backs Cummins as captain (AAP)", "Oceania"),
    (29, "MELBOURNE", "Australia beat England by 3 wickets (AP)", "Oceania"),
    (30, "BANDA SEA", "M6.8 quake felt in Darwin; no tsunami (BMKG)", "SE Asia"),
    (31, "BLUE NILE", "Sudan army says it is restoring security (SUNA)", "Africa"),
    (32, "ETHIOPIA", "700,000 displaced by conflict (UN)", "Africa"),
    (33, "DHAKA", "Five more deaths with measles symptoms (Daily Star)", "South Asia"),
    (34, "LAHORE", "Pakistan drop Rizwan, Masood from contracts (AJ)", "South Asia"),
    (35, "FUKUSHIMA", "Snow strands 1,500; 700 homes lose power (NHK)", "East Asia"),
    (36, "BALI", "Russian Interpol fugitive refused entry (Antara)", "SE Asia"),
]

DATE_CHECK = (
    "Left out (other day): Kyiv bridge barrage and missiles in Poland, the Kryvyi Rih strike, "
    "Davao landing, Zelensky's NBC interview, Iran's uranium remark, Denmark's expulsion of a Russian "
    "attaché, Trump tax cut, UK–EU reset, Hodeidah strike, China–Japan words, Wall St sell-off, Akvan "
    "landfall, Manipur toll. The TAIEX's 6% fall was all Friday 20 November (UTC). Thu 19: ICJ ruling, "
    "GTA VI launch.  Not yet known when drawn: COP31 approval session (Sun 06:00 GMT), Las Vegas GP race "
    "(Sun 04:00 UTC), Dragon splashdown, BepiColombo capture."
)


# ---------------------------------------------------------------- lead art
def art_gulf(d, x, y, w, h):
    """Gulf map: beige land, blue gulf, red strike markers."""
    d.rectangle([x, y, x + w, y + h], fill=(233, 220, 184))
    # sea: diagonal band of blue (the Gulf)
    d.polygon([(x + w * 0.34, y + h), (x + w * 0.58, y),
               (x + w * 0.80, y), (x + w * 0.56, y + h)],
              fill=(72, 130, 178))
    d.polygon([(x + w * 0.42, y + h), (x + w * 0.64, y),
               (x + w * 0.72, y), (x + w * 0.50, y + h)],
              fill=(96, 155, 200))
    # Bahrain island + labels
    bx, by = x + w * 0.42, y + h * 0.52
    d.ellipse([bx - 16, by - 9, bx + 16, by + 9], fill=(250, 244, 224),
              outline=(120, 110, 80))
    d.text((x + 8, y + 4), "2 air bases · 2 tankers hit",
           font=sans_b(11), fill=INK)
    d.text((x + w - 52, y + 4), "IRAN", font=sans_b(11), fill=(90, 70, 40))
    d.text((x + 8, y + h - 18), "SAUDI ARABIA", font=sans_b(10),
           fill=(120, 100, 60))
    d.text((bx - 30, by + 12), "BAHRAIN", font=sans_b(11), fill=INK)
    d.text((x + w * 0.66, y + h * 0.30), "HORMUZ", font=sans_b(10),
           fill=INK)
    # strike stars: two on Bahrain, two on tankers
    def star(cx, cy, r):
        pts = []
        for i in range(8):
            ang = 3.14159 * i / 4 - 3.14159 / 2
            rr = r if i % 2 == 0 else r * 0.45
            import math
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=RED, outline=(120, 0, 0))
    star(bx - 8, by - 4, 9)
    star(bx + 10, by + 2, 9)
    star(x + w * 0.55, y + h * 0.62, 9)
    star(x + w * 0.50, y + h * 0.80, 9)


def art_quake(d, x, y, w, h):
    """Quake cross-section: strata, epicentre rings, depth scale."""
    d.rectangle([x, y, x + w, y + h], fill=(58, 44, 34))
    # sky strip
    d.rectangle([x, y, x + w, y + 22], fill=(214, 200, 170))
    d.polygon([(x, y + 22), (x + w * 0.30, y + 6), (x + w * 0.55, y + 22)],
              fill=(150, 125, 90))
    d.text((x + w * 0.62, y + 4), "ONDORES", font=sans_b(10),
           fill=(90, 70, 50))
    # strata
    for i, col in enumerate([(122, 96, 66), (96, 74, 50), (74, 56, 40)]):
        yy = y + 26 + i * (h - 26) // 3
        d.rectangle([x, yy, x + w, y + 26 + (i + 1) * (h - 26) // 3],
                    fill=col)
    # epicentre rings
    ex, ey = x + w * 0.68, y + h * 0.72
    for r in (30, 21, 13):
        d.ellipse([ex - r, ey - r * 0.55, ex + r, ey + r * 0.55],
                  outline=(255, 120, 90), width=2)
    d.ellipse([ex - 5, ey - 4, ex + 5, ey + 4], fill=RED)
    # dashed depth line
    for yy in range(y + 24, int(ey), 8):
        d.line([(ex, yy), (ex, yy + 4)], fill=WHITE, width=1)
    d.text((x + 8, y + 30), "LIMA", font=sans_b(11), fill=WHITE)
    d.text((x + 8, y + 44), "shaking felt", font=sans(10),
           fill=(220, 210, 190))
    d.rectangle([x + w - 92, y + h - 22, x + w - 6, y + h - 6],
                fill=BLACK)
    d.text((x + w - 86, y + h - 21), "108–129 km", font=sans_b(11),
           fill=WHITE)
    d.text((x + 8, y + h - 21), "00:09 UTC · deep · no deaths",
           font=sans_b(10), fill=WHITE)


def art_cop31(d, x, y, w, h):
    """COP31 calendar: day grid with day 21 in red + thermometer."""
    d.rectangle([x, y, x + w, y + h], fill=(222, 238, 226))
    d.text((x + 8, y + 5), "Day 13 of a 12-day summit",
           font=sans_b(12), fill=INK)
    # thermometer
    tx = x + w - 34
    d.rectangle([tx, y + 24, tx + 10, y + h - 30], fill=WHITE,
                outline=(150, 150, 150))
    d.rectangle([tx + 2, y + 40, tx + 8, y + h - 32], fill=RED)
    d.ellipse([tx - 3, y + h - 34, tx + 13, y + h - 18], fill=RED)
    d.text((tx - 6, y + 8), "1.5°C", font=sans_b(11), fill=RED)
    # calendar grid: Nov 9-21
    gx, gy = x + 8, y + 26
    cw, ch, gap = 20, 18, 3
    d.text((gx, gy - 1), "NOV 9–20 SCHEDULED", font=sans_b(9),
           fill=GREY)
    gy += 14
    for i, day in enumerate(range(9, 22)):
        cx = gx + (i % 7) * (cw + gap)
        cy = gy + (i // 7) * (ch + gap)
        fill = RED if day == 21 else (46, 139, 87)
        d.rectangle([cx, cy, cx + cw, cy + ch], fill=fill)
        d.text((cx + 5, cy + 2), str(day), font=sans_b(11), fill=WHITE)
    d.text((gx, gy + 2 * (ch + gap) + 4), "+1 DAY",
           font=sans_b(12), fill=RED)


LEAD_ART = {"gulf": art_gulf, "quake": art_quake, "cop31": art_cop31}


# ---------------------------------------------------------------- feature art
def _art_bg(d, x, y, w, h, fill):
    d.rectangle([x, y, x + w, y + h], fill=fill)


def art_chapo(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (240, 228, 200))
    d.text((x + 8, y + 4), "$5M", font=sans_b(26), fill=INK)
    d.text((x + 8, y + 34), "REWARD", font=sans_b(10), fill=GREY)
    d.rectangle([x + 78, y + 12, x + w - 8, y + 40], outline=RED, width=3)
    d.text((x + 86, y + 16), "CAPTURED", font=sans_b(14), fill=RED)
    d.text((x + 78, y + 44), "FBI TOP TEN", font=sans_b(10), fill=INK)


def art_eucepa(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (232, 238, 244))
    # EU circle of stars
    cx, cy = x + 34, y + 30
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=(31, 95, 168))
    import math
    for i in range(12):
        a = 2 * math.pi * i / 12 - math.pi / 2
        sx, sy = cx + 14 * math.cos(a), cy + 14 * math.sin(a)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 60))
    # Indonesia flag
    d.rectangle([x + 66, y + 12, x + 106, y + 26], fill=RED)
    d.rectangle([x + 66, y + 26, x + 106, y + 40], fill=WHITE,
                outline=GREY)
    d.text((x + 112, y + 6), "90.4%", font=sans_b(24), fill=INK)
    d.text((x + 112, y + 36), "DUTY-FREE", font=sans_b(10), fill=INK)
    d.text((x + 112, y + 48), "LINES", font=sans_b(10), fill=INK)


def art_ship(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (58, 96, 138))
    # ship silhouette
    d.polygon([(x + 12, y + 44), (x + 110, y + 44), (x + 100, y + 56),
               (x + 22, y + 56)], fill=(30, 30, 30))
    d.rectangle([x + 30, y + 28, x + 48, y + 44], fill=(200, 60, 40))
    d.rectangle([x + 52, y + 32, x + 68, y + 44], fill=(220, 180, 60))
    d.rectangle([x + 72, y + 28, x + 88, y + 44], fill=(60, 160, 90))
    d.line([(x + 8, y + 56), (x + w - 8, y + 56)], fill=(180, 210, 230),
           width=2)
    d.text((x + w - 52, y + 2), "2", font=sans_b(30), fill=WHITE)
    d.text((x + w - 52, y + 36), "DRONES", font=sans_b(10), fill=WHITE)


def art_robot(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (225, 232, 238))
    # robot head
    hx, hy = x + 34, y + 32
    d.rounded_rectangle([hx - 20, hy - 16, hx + 20, hy + 14], radius=6,
                        fill=(160, 175, 190), outline=(90, 100, 110))
    d.ellipse([hx - 11, hy - 6, hx - 3, hy + 2], fill=RED)
    d.ellipse([hx + 3, hy - 6, hx + 11, hy + 2], fill=RED)
    d.line([(hx, hy - 16), (hx, hy - 24)], fill=(90, 100, 110), width=2)
    d.ellipse([hx - 3, hy - 28, hx + 3, hy - 22], fill=RED)
    d.text((x + 66, y + 4), "128", font=sans_b(28), fill=INK)
    d.text((x + 66, y + 36), "NATIONS · ROBOT ARMS",
           font=sans_b(9), fill=INK)


def art_fire(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (245, 232, 210))
    # flame bars
    for i, hh in enumerate((18, 30, 42, 34, 22)):
        bx = x + 10 + i * 16
        d.rectangle([bx, y + h - 12 - hh, bx + 12, y + h - 12],
                    fill=(220, 90, 30) if i % 2 == 0 else (240, 150, 40))
    d.text((x + 100, y + 2), "4", font=sans_b(30), fill=RED)
    d.text((x + 128, y + 10), "DEAD", font=sans_b(12), fill=INK)
    d.text((x + 128, y + 26), "IN FIRE", font=sans_b(12), fill=INK)


def art_rugby(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (24, 64, 40))
    # goalposts
    d.line([(x + 16, y + 8), (x + 16, y + 52)], fill=WHITE, width=3)
    d.line([(x + 44, y + 8), (x + 44, y + 52)], fill=WHITE, width=3)
    d.line([(x + 16, y + 20), (x + 44, y + 20)], fill=WHITE, width=3)
    d.ellipse([x + 22, y + 34, x + 38, y + 48], fill=(180, 120, 60))
    d.rectangle([x + 60, y + 8, x + w - 8, y + 34], fill=BLACK)
    d.text((x + 66, y + 11), "ENG  37–12  NZL", font=sans_b(13),
           fill=(255, 210, 60))
    d.text((x + 60, y + 40), "TWICKENHAM", font=sans_b(10),
           fill=(200, 220, 200))


def art_target(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (238, 228, 210))
    cx, cy = x + 36, y + 32
    for r, col in ((24, (120, 100, 70)), (16, WHITE), (9, RED)):
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
                  outline=(90, 75, 50))
    d.text((x + 72, y + 4), "15", font=sans_b(28), fill=INK)
    d.text((x + 72, y + 36), "MILITANTS", font=sans_b(10), fill=INK)
    d.text((x + 72, y + 48), "KILLED", font=sans_b(10), fill=INK)


def art_bitcoin(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (250, 244, 224))
    # falling-then-rising chart
    pts = [(x + 8 + i * 12, y + 14 + v) for i, v in
           enumerate((6, 12, 20, 30, 38, 34, 26, 18, 22, 16, 10))]
    d.line(pts, fill=RED, width=3)
    d.ellipse([x + w - 34, y + 6, x + w - 8, y + 32], fill=(247, 147, 26))
    d.text((x + w - 28, y + 9), "B", font=sans_b(16), fill=WHITE)
    d.text((x + 8, y + 44), "$56,814", font=sans_b(15), fill=INK)
    d.text((x + 96, y + 46), "−3.6%", font=sans_b(12), fill=RED)


def art_caf(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (226, 240, 226))
    cx, cy = x + 32, y + 32
    d.ellipse([cx - 22, cy - 22, cx + 22, cy + 22], fill=WHITE,
              outline=INK)
    d.polygon([(cx, cy - 9), (cx + 9, cy - 3), (cx + 6, cy + 8),
               (cx - 6, cy + 8), (cx - 9, cy - 3)], fill=INK)
    d.text((x + 64, y + 4), "54/54", font=sans_b(24), fill=INK)
    d.text((x + 64, y + 34), "BACK INFANTINO", font=sans_b(10),
           fill=INK)


def art_f1(d, x, y, w, h):
    _art_bg(d, x, y, w, h, (22, 24, 48))
    # checkered flag
    for r in range(3):
        for c in range(6):
            if (r + c) % 2 == 0:
                d.rectangle([x + 8 + c * 8, y + 8 + r * 8,
                             x + 16 + c * 8, y + 16 + r * 8], fill=WHITE)
    d.text((x + 8, y + 36), "P1", font=sans_b(24), fill=(255, 210, 60))
    d.text((x + 62, y + 10), "VERSTAPPEN", font=sans_b(13), fill=WHITE)
    d.text((x + 62, y + 28), "· VEGAS", font=sans_b(13), fill=WHITE)
    d.text((x + 62, y + 46), "1:34.151", font=sans_b(11),
           fill=(180, 190, 220))


FEATURE_ART = {
    "chapo": art_chapo, "eucepa": art_eucepa, "ship": art_ship,
    "robot": art_robot, "fire": art_fire, "rugby": art_rugby,
    "target": art_target, "bitcoin": art_bitcoin, "caf": art_caf,
    "f1": art_f1,
}


# ---------------------------------------------------------------- world map
# Simplified smooth continent polygons in a 336x162 box.
CONTINENTS = [
    # North America
    [(8, 28), (25, 12), (55, 8), (85, 14), (105, 26), (98, 40),
     (82, 44), (75, 58), (88, 68), (80, 84), (62, 88), (48, 80),
     (35, 72), (22, 58), (10, 45)],
    # Central America
    [(62, 88), (76, 92), (70, 102), (60, 98)],
    # Greenland
    [(112, 10), (132, 6), (140, 16), (128, 28), (114, 24)],
    # South America
    [(78, 100), (100, 94), (115, 105), (110, 128), (95, 148),
     (82, 132), (72, 115)],
    # Africa
    [(160, 62), (185, 55), (205, 64), (210, 84), (198, 105),
     (185, 122), (172, 110), (162, 88), (155, 72)],
    # Europe
    [(158, 32), (178, 26), (195, 32), (190, 46), (172, 50), (160, 44)],
    # UK
    [(150, 28), (156, 26), (158, 34), (152, 37)],
    # Asia
    [(195, 24), (240, 14), (295, 18), (318, 32), (308, 50),
     (282, 60), (255, 66), (235, 78), (218, 68), (205, 55), (198, 40)],
    # India
    [(228, 68), (242, 66), (240, 82), (232, 88), (228, 76)],
    # SE Asia
    [(248, 68), (262, 66), (266, 78), (256, 84), (248, 76)],
    # Japan
    [(308, 34), (314, 44), (310, 56), (304, 48)],
    # Indonesia
    [(258, 88), (272, 90), (286, 88), (280, 95), (264, 96)],
    # Australia
    [(272, 102), (302, 98), (314, 112), (304, 128), (280, 126),
     (268, 114)],
    # New Zealand
    [(320, 128), (324, 136), (319, 140), (316, 132)],
]

# story number -> (x, y in map box, region)
PINS = [
    (1, 205, 62, "Middle East"), (2, 88, 128, "Americas"),
    (3, 185, 48, "Middle East"), (4, 48, 78, "Americas"),
    (5, 162, 32, "Europe"), (6, 182, 20, "Europe"),
    (7, 164, 42, "Global"), (8, 198, 58, "Middle East"),
    (9, 150, 32, "Europe"), (10, 222, 62, "South Asia"),
    (12, 168, 88, "Africa"), (13, 38, 62, "Americas"),
    (15, 282, 58, "East Asia"), (16, 318, 132, "Oceania"),
    (17, 192, 54, "Middle East"), (18, 208, 60, "Middle East"),
    (19, 212, 52, "Middle East"), (20, 158, 38, "Europe"),
    (21, 174, 40, "Europe"), (22, 156, 30, "Europe"),
    (23, 148, 22, "Europe"), (24, 144, 28, "Europe"),
    (25, 146, 36, "Europe"), (26, 78, 58, "Americas"),
    (27, 100, 118, "Americas"), (28, 292, 118, "Oceania"),
    (29, 302, 128, "Oceania"), (30, 272, 88, "SE Asia"),
    (31, 188, 82, "Africa"), (32, 192, 92, "Africa"),
    (33, 232, 64, "South Asia"), (34, 220, 58, "South Asia"),
    (35, 306, 44, "East Asia"), (36, 266, 92, "SE Asia"),
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SEA, outline=LIGHT_LINE)
    sx, sy = w / 336.0, h / 162.0
    for poly in CONTINENTS:
        pts = [(x + px * sx, y + py * sy) for px, py in poly]
        d.polygon(pts, fill=LAND, outline=(190, 175, 135))
    for num, px, py, region in PINS:
        cx, cy = x + px * sx, y + py * sy
        r = 6
        col = REGION_COLORS[region]
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col,
                  outline=WHITE, width=1)
        f = sans_b(7)
        t = str(num)
        tw = text_w(d, t, f)
        d.text((cx - tw / 2, cy - 5), t, font=f, fill=WHITE)


# ---------------------------------------------------------------- sections
MX = 14            # side margin
CW = W - 2 * MX    # content width = 996


def draw_top(d, y):
    d.rectangle([0, y, W, y + 20], fill=BLACK)
    d.text((MX, y + 3), "THE WORLD IN ONE DAY", font=sans_b(11),
           fill=WHITE)
    s = "36 STORIES · 9 REGIONS · EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - MX - text_w(d, s, sans_b(10)), y + 4), s,
           font=sans_b(10), fill=(210, 205, 190))
    return y + 20


def draw_masthead(d, y):
    f = serif_b(58)
    s = "Saturday 21 November 2026"
    while text_w(d, s, f) > CW and f.size > 40:
        f = serif_b(f.size - 1)
    d.text(((W - text_w(d, s, f)) / 2, y + 2), s, font=f, fill=INK)
    d.line([(MX, y + 62), (W - MX, y + 62)], fill=INK, width=2)
    d.line([(MX, y + 65), (W - MX, y + 65)], fill=INK, width=1)
    return y + 66


def draw_subdeck(d, y):
    f = serif_i(14)
    d.text(((W - text_w(d, SUB_DECK, f)) / 2, y + 1), SUB_DECK,
           font=f, fill=INK)
    return y + 18


def draw_timeline(d, y):
    h = 52
    d.rectangle([MX, y, W - MX, y + h], fill=CREAM2)
    d.text((MX + 6, y + 4), "THE DAY", font=sans_b(11), fill=INK)
    d.text((MX + 6, y + 17), "IN UTC", font=sans_b(11), fill=INK)
    x0, x1 = MX + 72, W - MX - 6
    axis_y = y + 34
    d.line([(x0, axis_y), (x1, axis_y)], fill=(150, 140, 120), width=2)
    for hr in (0, 6, 12, 18, 24):
        hx = x0 + (x1 - x0) * hr / 24.0
        d.line([(hx, axis_y - 3), (hx, axis_y + 3)],
               fill=(150, 140, 120), width=1)
        lab = "%02d" % hr
        d.text((hx - text_w(d, lab, sans(8)) / 2, axis_y + 5), lab,
               font=sans(8), fill=GREY)
    for t, label, hr in TIMELINE:
        ex = x0 + (x1 - x0) * hr / 24.0
        d.ellipse([ex - 4, axis_y - 4, ex + 4, axis_y + 4], fill=RED,
                  outline=WHITE)
        d.text((ex - text_w(d, t, sans_b(10)) / 2, y + 4), t,
               font=sans_b(10), fill=RED)
        lw = text_w(d, label, sans(9))
        lx = min(max(ex - lw / 2, x0), x1 - lw)
        d.text((lx, y + 17), label, font=sans(9), fill=INK)
    return y + h


def draw_stats(d, y):
    h = 52
    n = len(STATS)
    cell = CW // n
    for i, (num, label) in enumerate(STATS):
        cx = MX + i * cell
        d.rectangle([cx, y, cx + cell - 4, y + h], fill=WHITE,
                    outline=LIGHT_LINE)
        d.rectangle([cx, y, cx + 3, y + h], fill=RED)
        d.text((cx + 8, y + 3), num, font=sans_b(20), fill=RED)
        draw_wrapped(d, cx + 8, y + 27, label, sans(9), cell - 14,
                     INK, leading=11, max_lines=2)
    return y + h


def draw_regions(d, y):
    h = 18
    total = sum(c for _, c in REGIONS)
    x = MX
    for name, count in REGIONS:
        w = int(CW * count / total)
        col = REGION_COLORS[name]
        d.rectangle([x, y, x + w, y + h], fill=col)
        s = "%s %d" % (name, count)
        f = sans_b(9)
        tw = text_w(d, s, f)
        if tw <= w - 4:
            d.text((x + (w - tw) / 2, y + 3), s, font=f, fill=WHITE)
        x += w
    return y + h


def draw_lead(d, x, y, w, lead):
    # red header bar
    d.rectangle([x, y, x + w, y + 24], fill=RED)
    d.text((x + 8, y + 4), lead["header"], font=sans_b(14), fill=WHITE)
    ay = y + 24
    shadow_box(d, [x, ay, x + w, ay + 110], fill=PAPER, shadow=2)
    LEAD_ART[lead["art"]](d, x, ay, w, 110)
    sy = ay + 110
    d.rectangle([x, sy, x + w, sy + 12], fill=BLACK)
    d.text((x + 6, sy + 1), lead["source"], font=sans(8),
           fill=(210, 205, 190))
    ky = sy + 12 + 3
    kicker_line(d, x, ky, w, lead["num"], lead["kicker"],
                lead["verified"])
    hy = ky + 15
    draw_wrapped(d, x, hy, lead["headline"], serif_b(24), w, INK,
                 leading=25, max_lines=2)
    by = hy + 48
    draw_wrapped(d, x, by, lead["body"], sans(11), w, INK,
                 leading=13, max_lines=3)


def draw_feature(d, x, y, w, feat):
    shadow_box(d, [x, y, x + w, y + 62], fill=PAPER, shadow=2)
    FEATURE_ART[feat["art"]](d, x, y, w, 62)
    ky = y + 64
    kicker_line(d, x, ky, w, feat["num"], feat["kicker"],
                feat["verified"])
    hy = ky + 12
    draw_wrapped(d, x, hy, feat["headline"], serif_b(15), w, INK,
                 leading=16, max_lines=2)
    by = hy + 32
    draw_wrapped(d, x, by, feat["body"], sans(9), w, INK,
                 leading=11, max_lines=2)
    d.text((x, by + 21), feat["src"], font=sans(8), fill=GREY)


def draw_map_section(d, y):
    h = 194
    # headers
    d.text((MX, y + 2), "WHERE IT HAPPENED", font=sans_b(12), fill=INK)
    d.line([(MX, y + 17), (MX + 336, y + 17)], fill=INK, width=1)
    ax = MX + 346
    aw = W - MX - ax
    d.text((ax, y + 2), "ALSO ON SATURDAY 21 NOVEMBER 2026 — 23 MORE",
           font=sans_b(12), fill=INK)
    d.line([(ax, y + 17), (W - MX, y + 17)], fill=INK, width=1)
    draw_map(d, MX, y + 22, 336, 148)
    d.text((MX, y + 174),
           "Pins carry each story's number; colour = region.",
           font=sans_i(9), fill=GREY)
    # briefs: two columns
    col_w = (aw - 12) // 2
    for i, (num, place, text, region) in enumerate(BRIEFS):
        col = 0 if i < 12 else 1
        row = i if i < 12 else i - 12
        bx = ax + col * (col_w + 12)
        by = y + 22 + row * 15
        f_n = sans_b(10)
        d.text((bx, by), str(num), font=f_n, fill=RED)
        nx = bx + int(text_w(d, str(num), f_n)) + 4
        f_p = sans_b(10)
        d.text((nx, by), place, font=f_p, fill=INK)
        tx = nx + int(text_w(d, place, f_p)) + 4
        # fit the brief text to the remaining width
        f_t = sans(10)
        avail = bx + col_w - 12 - tx
        t = text
        while t and text_w(d, t, f_t) > avail:
            t = t[:-1]
        if t != text:
            t = t[:-1] + "…"
        d.text((tx, by), t, font=f_t, fill=INK)
        # region dot at right edge
        dot_cx = bx + col_w - 4
        d.ellipse([dot_cx - 4, by + 2, dot_cx + 4, by + 10],
                  fill=REGION_COLORS[region])
    return y + h


def draw_datecheck(d, y):
    h = 46
    d.rectangle([MX, y, W - MX, y + h], outline=RED, width=2,
                fill=(255, 248, 248))
    d.text((MX + 6, y + 4), "DATE CHECK", font=sans_b(11), fill=RED)
    lx = MX + 92
    draw_wrapped(d, lx, y + 4, DATE_CHECK, sans(10), W - MX - 6 - lx,
                 INK, leading=13, max_lines=3)
    return y + h


def draw_howchecked(d, y):
    d.text((MX, y + 2), "HOW WE CHECKED", font=sans_b(10), fill=INK)
    x = MX + 108
    x += badge(d, x, y + 2, "✓ CONFIRMED", GREEN) + 4
    d.text((x, y + 2), "2+ major outlets", font=sans(9), fill=INK)
    x += int(text_w(d, "2+ major outlets", sans(9))) + 10
    x += badge(d, x, y + 2, "● OFFICIAL", BLUE) + 4
    d.text((x, y + 2), "on the record (officials, results)",
           font=sans(9), fill=INK)
    x += int(text_w(d, "on the record (officials, results)",
                    sans(9))) + 10
    x += badge(d, x, y + 2, "○ REPORTED", GREY) + 4
    d.text((x, y + 2), "one major outlet", font=sans(9), fill=INK)
    s = ("Corrections: none. Peru quake depth differs by agency: "
         "USGS 108 km, IGP 129 km.")
    d.text((W - MX - text_w(d, s, sans(9)), y + 2), s, font=sans(9),
           fill=GREY)
    return y + 18


def draw_footer(d, y):
    s = ("Every story here happened, or was first reported, on Saturday 21 November 2026 (UTC). "
         "Outlets named beside each story: Al Jazeera, Anadolu, AP, AFP, Reuters, Antara, Kyodo, RNZ, "
         "ABC, Dawn and official bodies.")
    f = sans(9)
    while text_w(d, s, f) > CW:
        s = s[:-1]
    d.text(((W - text_w(d, s, f)) / 2, y + 1), s, font=f, fill=GREY)
    return y + 14


# ---------------------------------------------------------------- main
def compose(out_path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    y = 0
    y = draw_top(d, y)          # 20
    y = draw_masthead(d, y)     # 66
    y = draw_subdeck(d, y)      # 18
    y = draw_timeline(d, y)     # 52
    y = draw_stats(d, y)        # 52
    y = draw_regions(d, y)      # 18
    # leads: 3 columns, 250 tall
    gap = 10
    lw = (CW - 2 * gap) // 3
    for i, lead in enumerate(LEADS):
        draw_lead(d, MX + i * (lw + gap), y, lw, lead)
    y += 250
    # features: 2 rows x 5 columns, 137 each
    fgap = 8
    fw = (CW - 4 * fgap) // 5
    for row in range(2):
        for i in range(5):
            feat = FEATURES[row * 5 + i]
            draw_feature(d, MX + i * (fw + fgap), y, fw, feat)
        y += 137
    y = draw_map_section(d, y)  # 194
    y = draw_datecheck(d, y)    # 46
    y = draw_howchecked(d, y)   # 18
    y = draw_footer(d, y)       # 14
    assert y <= H, "layout overflow: %d > %d" % (y, H)
    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    compose(os.path.join(here, "entry.png"))
    print("wrote entry.png")
