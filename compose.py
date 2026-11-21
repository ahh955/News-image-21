#!/usr/bin/env python3
"""compose.py — builds entry.png for the make.fun bounty news-image-20261121.

A newspaper front page summing up the world news of SATURDAY 21 NOVEMBER 2026.
52 stories: 3 big illustrated leads + 13 illustrated features + 36 one-line briefs.
All artwork is procedural (PIL shapes only). No network, no randomness:
running this script twice produces byte-identical output.
"""
import hashlib
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


# ---------------------------------------------------------------- fonts
SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS = lambda s: F("DejaVuSans.ttf", s)  # noqa: E731
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)  # noqa: E731
MONO_B = lambda s: F("DejaVuSansMono-Bold.ttf", s)  # noqa: E731

# ---------------------------------------------------------------- colours
PAPER = (247, 242, 231)
INK = (20, 20, 22)
MUTED = (90, 86, 78)
RULE = (60, 58, 52)
NAVY = (12, 24, 46)
NAVY2 = (22, 38, 66)
RED = (178, 24, 28)
RED_DK = (140, 16, 20)
GOLD = (212, 160, 40)
GREEN = (26, 120, 62)
BLUE = (30, 90, 160)
CARD_BG = (255, 253, 247)
SKY_NIGHT = (8, 12, 28)

# Verification tag colours: C = CONFIRMED (2+ outlets), O = OFFICIAL (on record),
# R = REPORTED (one outlet).
TAGC = {"C": (26, 120, 62), "O": (30, 90, 160), "R": (178, 24, 28)}
TAGW = {"C": "CONFIRMED", "O": "OFFICIAL", "R": "REPORTED"}

# ---------------------------------------------------------------- F1 result
# Verified at build time from Pit Debrief + RacingNews365 (Q3 ended 05:02 UTC).
# Antonelli fastest in Q3, 1:33.893, but a 5-place grid penalty hands pole to
# Verstappen (best Q3 1:34.151); Russell 3rd, Norris 4th; both Ferraris out in Q2.
F1_POLE_DRIVER = "Verstappen"
F1_POLE_TEAM = "Red Bull"
F1_POLE_TIME = "1:34.151"

# ---------------------------------------------------------------- story data
# tag: C/O/R as above. region: EUR/ASI/MDE/AFR/AME/OCE/GLO.
LEADS = [
    dict(num=1, region="EUR", field="Politics", tag="C",
         kick="EUROPE · PROTEST", art="genz",
         head="Gen Z floods the streets in 25 countries",
         body=("Thousands rally across Europe over living costs, military spending "
               "and the climate — the largest youth protest wave of the year. "
               "(Al Jazeera, 02:49)")),
    dict(num=2, region="MDE", field="War", tag="R",
         kick="RED SEA · GULF · WAR", art="hormuz",
         head="Three missiles downed as Gulf war widens",
         body=("Saudi-led coalition downs 3 Houthi missiles; IRGC claims a US "
               "MQ-9 downed over Hormuz; Saudi jets strike Hodeidah, Sanaa, "
               "Saada, Taiz; 14+ tankers at Kharg. (Al Jazeera, 00:00)")),
    dict(num=3, region="GLO", field="Space", tag="O",
         kick="SPACE · MERCURY", art="bepi",
         head="BepiColombo burns for Mercury tonight",
         body=("After an 8-year journey, ESA's probe fires at 19:24 CET for 37 "
               "minutes — a weak-capture burn to become only the 2nd craft ever "
               "to orbit Mercury. (ESA, Sky & Telescope)")),
]

FEATURES = [
    dict(num=4, region="GLO", field="Climate", tag="C",
         kick="ANTALYA · COP31", art="cop31",
         head="COP31 in overtime as 1.5°C slips",
         body=("Plenary suspended to Sat; 3rd draft today; fossil text stripped; "
               "$120bn target dropped. (Reuters, UN News)")),
    dict(num=5, region="EUR", field="War", tag="C",
         kick="WARSAW · NATO", art="rutte",
         head="Rutte in Warsaw after incursion",
         body=("NATO chief visits today; Tusk calls Friday's crash a 'deliberate "
               "provocation'. (The Times, ISW)")),
    dict(num=6, region="EUR", field="War", tag="R",
         kick="MOSCOW · WAR", art="putin",
         head="Putin rejects any ceasefire",
         body=("Vows a 'harsh' offensive and retribution; Russia attacks Ukrainian "
               "forces today. (02:49)")),
    dict(num=7, region="ASI", field="Disaster", tag="O",
         kick="ODISHA · CYCLONE", art="akvan",
         head="Akvan weakens over Odisha",
         body=("IMD: now a low-pressure area; Patrapur 209 mm; 47 trains off; "
               "4.4 lakh evacuated. (IMD)")),
    dict(num=8, region="AME", field="Space", tag="O",
         kick="PACIFIC · NASA", art="dragon",
         head="Dragon splashes down tonight",
         body=("CRS-35 returns ~21:55 UTC off California with 6,300 lb of ISS "
               "science, incl. bioprinted vessels. (NASA)")),
    dict(num=9, region="GLO", field="Science", tag="R",
         kick="MATHS · AI · CLAIM", art="riemann",
         head="Claude 'proved Riemann' — claim",
         body=("Anthropic: Claude helped prove the 167-yr hypothesis; rival proof "
               "also out; UNVERIFIED. (AIPULSE)")),
    dict(num=10, region="AME", field="Sport", tag="C",
         kick="LAS VEGAS · F1", art="f1",
         head="Antonelli fastest, Verstappen on pole",
         body=("Antonelli fastest in Q3, 1:33.893, but a grid penalty hands "
               "pole to Verstappen. (Pit Debrief)")),
    dict(num=11, region="EUR", field="War", tag="R",
         kick="SUMY · WAR", art="himars",
         head="HIMARS kills 20 Russian commanders",
         body="Strike hits 810th Brigade HQ in Sumy; Kyiv says 20 commanders killed. (03:31)",
         ),
    dict(num=12, region="OCE", field="Sport", tag="R",
         kick="WELLINGTON · CRICKET", art="rahul",
         head="Rahul completes SENA century set",
         body=("100 off 207 balls in Wellington — a Test hundred in every SENA "
               "nation. (Daily Short)")),
    dict(num=13, region="MDE", field="War", tag="R",
         kick="GAZA · WAR", art="gaza",
         head="22,000+ children killed in Gaza",
         body="Gaza health ministry says its toll of children killed has passed 22,000. (01:14)",
         ),
    dict(num=14, region="EUR", field="Diplomacy", tag="R",
         kick="COPENHAGEN · SPY PLOT", art="denmark",
         head="Denmark expels Russian diplomat",
         body=("Over alleged plot to kill a US-Ukrainian rapper. "
               "(Al Jazeera, 01:12)")),
    dict(num=15, region="AFR", field="Diplomacy", tag="C",
         kick="MOGADISHU · DIPLOMACY", art="somalia",
         head="Somalia expels UAE ambassador",
         body="Mogadishu accuses Abu Dhabi of 'open invasion' and orders envoy out. (Africanews)",
         ),
    dict(num=16, region="ASI", field="Diplomacy", tag="R",
         kick="DANDONG · CHINA", art="kim",
         head="Kim crosses into China by new bridge",
         body=("Arrives in Dandong via the newly opened New Yalu River Bridge. "
               "(Yonhap)")),
]

# (number, text with source, tag, region, field)
BRIEFS = [
    (17, "Trump urges Nvidia to reinstate Jensen Huang (Al Jazeera)", "R", "AME", "Tech"),
    (18, "California subpoenas Nvidia over China chip deals (01:17)", "R", "AME", "Tech"),
    (19, "US defence chief restricts military ties with Canada (03:24)", "R", "AME", "Diplomacy"),
    (20, "EU Council approves \u20ac1bn military aid for Ukraine (03:29)", "C", "EUR", "War"),
    (21, "Estonia confirms border closure with Russia from 1 Dec (03:04)", "O", "EUR", "Diplomacy"),
    (22, "Nikhil Gupta jailed 19y7m over foiled Pannun plot (02:39)", "C", "AME", "Law"),
    (23, "2 Salvadoran soldiers killed in Haiti handling explosives (03:29)", "R", "AME", "War"),
    (24, "Boat capsizes in Nigeria en route to funeral, \u22654 dead (Al Jazeera)", "R", "AFR", "Disaster"),
    (25, "US declassifies more UFO footage filmed in Middle East", "R", "MDE", "Science"),
    (26, "French police sentenced for beating producer Michel Zecler", "C", "EUR", "Law"),
    (27, "Trump's team aims for Ukraine peace deal by end of January (02:39)", "R", "AME", "Diplomacy"),
    (28, "European leaders call for winter ceasefire, postwar troops", "C", "EUR", "Diplomacy"),
    (29, "China seeks 'all-encompassing' Rohingya resolution (02:49)", "R", "ASI", "Diplomacy"),
    (30, "Ebola in eastern Congo: ~100 schools affected (03:31)", "C", "AFR", "Health"),
    (31, "Record \u20b91.22 lakh crore foreign inflow into Indian shares", "O", "ASI", "Economy"),
    (32, "Africa's new credit rating agency aims to change assessments", "R", "AFR", "Economy"),
    (33, "Gaza's displaced children mark World Children's Day (Al Jazeera)", "R", "MDE", "War"),
    (34, "Israeli drones kill 7 Palestinians in central Gaza (Al Jazeera)", "R", "MDE", "War"),
    (35, "US lawmakers push tougher AI chip rules amid China crackdown", "R", "AME", "Tech"),
    (36, "Rahul Gandhi backs strong India-Israel ties despite Gaza war", "R", "ASI", "Diplomacy"),
    (37, "ANC fights to keep control of South Africa's key cities", "R", "AFR", "Politics"),
    (38, "Nearly 600 women killed in South Africa within three months", "R", "AFR", "Law"),
    (39, "Trump exits Beijing; press on plane told to give up phones (03:05)", "C", "ASI", "Diplomacy"),
    (40, "Bessent: Trump, Xi agreed humans stay in loop on military AI", "R", "ASI", "Tech"),
    (41, "Obi vows to end kidnappings, corruption in Nigeria (Punch)", "R", "AFR", "Politics"),
    (42, "Nigeria moves to end jail terms for attempted suicide (BBC)", "C", "AFR", "Law"),
    (43, "Springboks face Ireland without Erasmus: 'No-one will break us'", "R", "AFR", "Sport"),
    (44, "Bank of Japan still weighing rate hikes as yen nears 160", "R", "ASI", "Economy"),
    (45, "Nagel: AI consciousness 'just ridiculous' (WIRED, Berggruen)", "R", "AME", "Culture"),
    (46, "Japan turns to ASEAN on critical minerals as China tightens grip", "R", "ASI", "Economy"),
    (47, "Japan welcomes record 3.91m visitors in Oct; China arrivals \u221247%", "O", "ASI", "Economy"),
    (48, "Kenya judges named as court backlog nears 580,000 (Nation)", "C", "AFR", "Law"),
    (49, "Ghana MP demands account of GH\u00a2100m coder fund (GhanaWeb)", "R", "AFR", "Politics"),
    (50, "Cyclone Xavier weakens to tropical storm near Samoa (JTWC)", "O", "OCE", "Disaster"),
    (51, "Severe storms, heatwave warnings across SE Australia (BOM)", "O", "OCE", "Disaster"),
    (52, "Milky Way simulated with 5 trillion particles on 3 exascale GPUs", "R", "ASI", "Science"),
]

REGIONS = [("EUROPE", "EUR", (30, 90, 160)), ("ASIA", "ASI", (178, 24, 28)),
           ("MIDDLE EAST", "MDE", (26, 120, 62)), ("AFRICA", "AFR", (200, 130, 30)),
           ("AMERICAS", "AME", (120, 60, 150)), ("OCEANIA", "OCE", (20, 140, 160)),
           ("GLOBAL", "GLO", (90, 86, 78))]

TIMELINE = [
    ("00:00", "Saudi coalition downs 3 Houthi missiles; IRGC claims MQ-9 downed"),
    ("01:12", "Denmark expels Russian diplomat over 'assassination plot'"),
    ("01:49", "Trump: Nvidia should reinstate Jensen Huang"),
    ("02:49", "Gen Z protests sweep 25 countries; Putin rejects ceasefire"),
    ("03:31", "HIMARS kills 20 Russian commanders in Sumy"),
    ("03:49", "IMD: Cyclone Akvan weakens to low-pressure area"),
    ("18:24", "BepiColombo orbit-insertion burn begins (19:24 CET)"),
    ("21:55", "Dragon CRS-35 splashdown off California"),
]

STATS = [
    ("25", "European countries in Gen Z protests"),
    ("3", "Houthi missiles downed by coalition"),
    ("209 mm", "rain at Patrapur as Akvan weakens"),
    ("22,000+", "children killed in Gaza, ministry says"),
    ("6,300 lb", "of science aboard Dragon CRS-35"),
    ("\u20b91.22 LAKH CR", "record foreign inflow, Indian shares"),
]

# ---------------------------------------------------------------- helpers
def wrap(d, text, font, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_tag(d, x, y, tag, size=8):
    """Small coloured verification pill; returns width used."""
    col = TAGC[tag]
    word = TAGW[tag]
    f = SANS_B(size)
    tw = d.textlength(word, font=f)
    w = int(tw + 8)
    h = size + 5
    d.rounded_rectangle([x, y, x + w, y + h], radius=2, fill=col)
    d.text((x + 4, y + 1), word, font=f, fill=(255, 255, 255))
    return w


def label(d, x, y, text, size=8, fill=(255, 255, 255), bg=(0, 0, 0), font=None,
          pad=3):
    """Text on a small dark chip; returns width used."""
    f = font or SANS_B(size)
    tw = d.textlength(text, font=f)
    w = int(tw + pad * 2)
    h = size + pad + 1
    d.rectangle([x, y, x + w, y + h], fill=bg)
    d.text((x + pad, y + 1), text, font=f, fill=fill)
    return w

# ---------------------------------------------------------------- art panels
# Every panel is drawn with PIL shapes only. (d, x, y, w, h) = panel box.

def _stars(d, x, y, w, h, seed_pts):
    for (px, py, r) in seed_pts:
        d.ellipse([x + px * w, y + py * h, x + px * w + r, y + py * h + r],
                  fill=(255, 255, 255))


def art_genz(d, x, y, w, h):
    """Night street, crowd with placards, giant red 25."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 18, 30))
    # buildings
    for bx, bw, bh, col in [(0, 52, 46, (30, 30, 48)), (60, 44, 60, (26, 26, 42)),
                            (112, 58, 40, (30, 30, 48)), (178, 48, 66, (26, 26, 42)),
                            (234, 56, 44, (30, 30, 48)), (298, 34, 58, (26, 26, 42))]:
        d.rectangle([x + bx, y + h - bh - 34, x + bx + bw, y + h - 34], fill=col)
        for wy in range(0, bh - 8, 12):
            for wx in range(5, bw - 6, 12):
                if (wx + wy) % 24 == 5:
                    d.rectangle([x + bx + wx, y + h - bh - 34 + wy + 4,
                                 x + bx + wx + 5, y + h - bh - 34 + wy + 9],
                                fill=(212, 160, 40))
    # street
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(40, 38, 44))
    # crowd: rows of silhouettes
    cols = [(200, 60, 60), (60, 140, 200), (220, 180, 60), (90, 180, 90),
            (180, 90, 160), (240, 240, 240)]
    for row, (ry, sc) in enumerate([(h - 52, 1.0), (h - 40, 1.25)]):
        for i in range(16):
            px = x + 8 + i * 20 + (7 if row else 0)
            py = y + ry
            col = cols[(i + row * 3) % len(cols)]
            d.ellipse([px, py, px + 7 * sc, py + 7 * sc], fill=(12, 12, 16))
            d.polygon([(px - 2, py + 7 * sc), (px + 9 * sc, py + 7 * sc),
                       (px + 11 * sc, py + 20 * sc), (px - 4, py + 20 * sc)],
                      fill=col)
    # placards
    d.rectangle([x + 24, y + 14, x + 122, y + 32], fill=(247, 242, 231))
    d.text((x + 28, y + 17), "COST OF LIVING", font=SANS_B(9), fill=RED_DK)
    d.rectangle([x + 130, y + 6, x + 190, y + 24], fill=(247, 242, 231))
    d.text((x + 134, y + 9), "CLIMATE", font=SANS_B(9), fill=(26, 120, 62))
    d.rectangle([x + 208, y + 16, x + 260, y + 34], fill=(247, 242, 231))
    d.text((x + 212, y + 19), "NO WAR", font=SANS_B(9), fill=INK)
    # giant number
    d.text((x + w - 78, y + 40), "25", font=SANS_B(54), fill=RED)
    label(d, x + w - 82, y + h - 26, "COUNTRIES", 8, bg=RED)


def art_hormuz(d, x, y, w, h):
    """Night over the Gulf: missile trails, explosions, tankers."""
    d.rectangle([x, y, x + w, y + h], fill=(6, 10, 26))
    _stars(d, x, y, w, h, [(0.05, 0.08, 2), (0.2, 0.05, 1), (0.4, 0.12, 2),
                           (0.6, 0.06, 1), (0.8, 0.1, 2), (0.92, 0.05, 1),
                           (0.3, 0.2, 1), (0.7, 0.18, 1)])
    # moon
    d.ellipse([x + w - 46, y + 8, x + w - 22, y + 32], fill=(230, 228, 210))
    d.ellipse([x + w - 40, y + 10, x + w - 24, y + 30], fill=(6, 10, 26))
    # sea
    d.rectangle([x, y + h - 30, x + w, y + h], fill=(10, 30, 60))
    for i in range(14):
        d.line([x + 6 + i * 24, y + h - 22 + (i % 3) * 5,
                x + 20 + i * 24, y + h - 22 + (i % 3) * 5], fill=(60, 110, 170), width=2)
    # tanker silhouettes massing
    for tx, ts in [(24, 1.0), (96, 0.8), (160, 1.1), (232, 0.7)]:
        d.rectangle([x + tx, y + h - 44 * ts, x + tx + 58 * ts, y + h - 30],
                    fill=(16, 16, 20))
        d.rectangle([x + tx + 40 * ts, y + h - 54 * ts, x + tx + 50 * ts,
                     y + h - 44 * ts], fill=(16, 16, 20))
    # missile trails arcing up, intercepted: bright trails + burst
    for (sx, sy, ex, ey) in [(40, 78, 120, 22), (150, 80, 210, 18), (250, 76, 300, 26)]:
        d.line([x + sx, y + sy, x + ex, y + ey], fill=(255, 120, 40), width=4)
        d.line([x + sx, y + sy, x + ex, y + ey], fill=(255, 230, 150), width=2)
        # burst star at interception point
        for dx, dy in [(0, -7), (0, 7), (-7, 0), (7, 0), (-5, -5), (5, 5), (-5, 5), (5, -5)]:
            d.line([x + ex, y + ey, x + ex + dx, y + ey + dy],
                   fill=(255, 200, 60), width=2)
        d.ellipse([x + ex - 4, y + ey - 4, x + ex + 4, y + ey + 4],
                  fill=(255, 240, 180))
    label(d, x + 8, y + 6, "3 DOWNED", 9, bg=RED)
    label(d, x + 8, y + h - 24, "MQ-9 CLAIM", 8, bg=(0, 0, 0))
    label(d, x + w - 112, y + h - 24, "14+ TANKERS AT KHARG", 7, bg=(0, 0, 0))


def art_bepi(d, x, y, w, h):
    """Mercury looming, BepiColombo firing its engine."""
    d.rectangle([x, y, x + w, y + h], fill=(4, 4, 12))
    _stars(d, x, y, w, h, [(0.06, 0.1, 2), (0.15, 0.3, 1), (0.3, 0.06, 2),
                           (0.45, 0.2, 1), (0.55, 0.08, 2), (0.7, 0.3, 1),
                           (0.85, 0.06, 2), (0.95, 0.25, 1), (0.25, 0.45, 1)])
    # Mercury: large disc rising from the bottom-left corner
    mx, my, mr = x + 50, y + h + 60, 95
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(150, 138, 128))
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], outline=(190, 178, 165), width=2)
    for (cx, cy, cr) in [(0.25, 0.18, 9), (0.45, 0.10, 6), (0.15, 0.08, 7),
                         (0.60, 0.20, 5), (0.35, 0.05, 5), (0.70, 0.12, 8)]:
        d.ellipse([mx - mr + cx * 2 * mr - cr, my - mr + cy * 2 * mr - cr,
                   mx - mr + cx * 2 * mr + cr, my - mr + cy * 2 * mr + cr],
                  fill=(120, 110, 100))
    # trajectory arc
    d.arc([x + 60, y - 40, x + 330, y + 150], start=200, end=330,
          fill=(120, 180, 255), width=2)
    # spacecraft: body + panels, engine flame firing below
    sx, sy = x + 225, y + 30
    d.polygon([(sx - 14, sy + 26), (sx - 5, sy + 12), (sx + 5, sy + 12),
               (sx + 14, sy + 26)], fill=(255, 160, 40))
    d.polygon([(sx - 7, sy + 22), (sx - 2, sy + 12), (sx + 2, sy + 12),
               (sx + 7, sy + 22)], fill=(255, 240, 180))
    d.rectangle([sx - 32, sy - 6, sx - 11, sy + 6], fill=(40, 90, 180))
    d.rectangle([sx + 11, sy - 6, sx + 32, sy + 6], fill=(40, 90, 180))
    d.rectangle([sx - 11, sy - 8, sx + 11, sy + 12], fill=(220, 220, 225))
    d.rectangle([sx - 4, sy - 14, sx + 4, sy - 8], fill=(180, 180, 190))
    label(d, x + 8, y + 6, "BURN 19:24 CET", 9, bg=RED)
    label(d, x + 8, y + 24, "37 MIN \u00b7 4 x 20N THRUSTERS", 8, bg=(0, 0, 0))
    d.text((x + w - 118, y + h - 34), "8 YEARS", font=SANS_B(20), fill=(255, 255, 255))
    label(d, x + w - 84, y + h - 14, "2ND EVER", 8, bg=GOLD, fill=INK)


def art_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(16, 48, 38))
    # clock face, overtime
    cx, cy, r = x + 30, y + 30, 22
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(247, 242, 231))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=INK, width=2)
    d.line([cx, cy, cx, cy - 15], fill=INK, width=2)
    d.line([cx, cy, cx + 12, cy + 4], fill=INK, width=2)
    d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=RED)
    # draft document with fossil fuels struck out
    d.rectangle([x + 62, y + 8, x + w - 8, y + h - 8], fill=(247, 242, 231))
    d.rectangle([x + 68, y + 14, x + w - 14, y + 17], fill=(150, 150, 150))
    d.rectangle([x + 68, y + 21, x + w - 24, y + 24], fill=(150, 150, 150))
    d.text((x + 68, y + 27), "FOSSIL", font=SANS_B(8), fill=INK)
    d.text((x + 68, y + 37), "FUELS", font=SANS_B(8), fill=INK)
    d.line([x + 66, y + 33, x + w - 12, y + 41], fill=RED, width=3)
    label(d, x + 4, y + h - 14, "OVERTIME", 8, bg=RED)


def art_rutte(d, x, y, w, h):
    """Polish border at night: missile trail, red alert, Polish flag."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 14, 30))
    # Polish flag
    d.rectangle([x + 6, y + 6, x + 34, y + 15], fill=(255, 255, 255))
    d.rectangle([x + 6, y + 15, x + 34, y + 24], fill=(220, 20, 60))
    # border fence posts
    for px in range(6, w - 4, 14):
        d.line([x + px, y + h - 26, x + px, y + h - 12], fill=(140, 140, 150), width=2)
    d.line([x + 4, y + h - 22, x + w - 4, y + h - 22], fill=(140, 140, 150), width=1)
    d.line([x + 4, y + h - 16, x + w - 4, y + h - 16], fill=(140, 140, 150), width=1)
    # missile trail arcing over the border + burst
    d.line([x + 20, y + h - 28, x + 88, y + 12], fill=(255, 120, 40), width=3)
    d.line([x + 20, y + h - 28, x + 88, y + 12], fill=(255, 230, 150), width=1)
    for dx, dy in [(0, -6), (0, 6), (-6, 0), (6, 0), (-4, -4), (4, 4)]:
        d.line([x + 88, y + 12, x + 88 + dx, y + 12 + dy], fill=(255, 200, 60), width=2)
    d.ellipse([x + 84, y + 8, x + 92, y + 16], fill=(255, 240, 180))
    label(d, x + w - 62, y + h - 15, "PROBE OPEN", 7, bg=RED)


def art_putin(d, x, y, w, h):
    """Kremlin towers under a dark red sky."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 8, 10))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(16, 16, 20))
    # towers
    for tx, tw, th in [(10, 16, 34), (34, 20, 44), (62, 16, 34), (86, 20, 40)]:
        d.rectangle([x + tx, y + h - 18 - th, x + tx + tw, y + h - 18],
                    fill=(120, 30, 30))
        d.polygon([(x + tx - 2, y + h - 18 - th), (x + tx + tw + 2, y + h - 18 - th),
                   (x + tx + tw // 2, y + h - 18 - th - 12)], fill=(90, 20, 20))
        d.ellipse([x + tx + tw // 2 - 2, y + h - 18 - th - 17,
                   x + tx + tw // 2 + 2, y + h - 18 - th - 13], fill=GOLD)
    label(d, x + 4, y + 4, "NO CEASEFIRE", 8, bg=RED)
    label(d, x + 4, y + h - 14, "'HARSH' OFFENSIVE", 7, bg=(0, 0, 0))


def art_akvan(d, x, y, w, h):
    """Cyclone spiral over the Odisha coast, rain."""
    d.rectangle([x, y, x + w, y + h], fill=(14, 40, 66))
    # land (India east coast)
    d.polygon([(x + 78, y), (x + w, y), (x + w, y + h), (x + 96, y + h),
               (x + 84, y + 40)], fill=(90, 110, 60))
    # spiral
    cx, cy = x + 46, y + 34
    for r in (26, 20, 14, 8):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20 + r * 8, end=300 + r * 4,
              fill=(255, 255, 255), width=3)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 220, 100))
    # rain slashes
    for i in range(10):
        rx = x + 8 + i * 13
        ry = y + 4 + (i % 3) * 8
        d.line([rx, ry, rx - 3, ry + 8], fill=(140, 200, 255), width=1)
    label(d, x + w - 52, y + 4, "209 MM", 8, bg=RED)
    label(d, x + 4, y + h - 14, "47 TRAINS OFF", 7, bg=(0, 0, 0))


def art_dragon(d, x, y, w, h):
    """Capsule under three parachutes over the Pacific."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 30, 60))
    _stars(d, x, y, w, h, [(0.08, 0.1, 1), (0.85, 0.08, 2), (0.6, 0.2, 1)])
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(10, 50, 90))
    for i in range(8):
        d.line([x + 6 + i * 18, y + h - 10, x + 16 + i * 18, y + h - 10],
               fill=(80, 150, 220), width=2)
    cx = x + w // 2
    # parachutes
    for dx in (-26, 0, 26):
        d.pieslice([cx + dx - 14, y + 2, cx + dx + 14, y + 22], start=180, end=360,
                   fill=(240, 240, 240))
        d.line([cx + dx - 12, y + 20, cx + dx - 3, y + 34], fill=(240, 240, 240), width=1)
        d.line([cx + dx + 12, y + 20, cx + dx + 3, y + 34], fill=(240, 240, 240), width=1)
    # capsule
    d.polygon([(cx - 12, y + 34), (cx + 12, y + 34), (cx + 8, y + 48),
               (cx - 8, y + 48)], fill=(230, 230, 235))
    d.rectangle([cx - 12, y + 34, cx + 12, y + 38], fill=(180, 40, 40))
    label(d, x + 4, y + h - 14, "21:55 UTC", 7, bg=RED)
    label(d, x + w - 58, y + h - 14, "6,300 LB", 7, bg=(0, 0, 0))


def art_riemann(d, x, y, w, h):
    """Blackboard with the zeta function, big question mark."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 32))
    d.rectangle([x + 3, y + 3, x + w - 3, y + h - 3], outline=(160, 140, 90), width=2)
    d.text((x + 10, y + 10), "\u03b6(s) = 0", font=SERIF_B(17), fill=(255, 255, 255))
    d.text((x + 10, y + 32), "Re(s) = \u00bd ?", font=SERIF_B(13), fill=(255, 255, 255))
    d.text((x + w - 26, y + 6), "?", font=SERIF_B(30), fill=GOLD)
    label(d, x + 4, y + h - 14, "167 YRS", 7, bg=GOLD, fill=INK)
    label(d, x + w - 74, y + h - 14, "UNVERIFIED", 7, bg=RED)


def art_f1(d, x, y, w, h):
    """Las Vegas night circuit: neon, car, chequered flag."""
    d.rectangle([x, y, x + w, y + h], fill=(8, 8, 18))
    # neon strip skyline
    for bx, bh, col in [(4, 18, (255, 0, 150)), (22, 26, (0, 220, 255)),
                        (44, 14, (255, 220, 0)), (66, 22, (255, 0, 150)),
                        (88, 16, (0, 220, 255)), (110, 24, (255, 220, 0))]:
        d.rectangle([x + bx, y + 6, x + bx + 14, y + 6 + bh], fill=col)
    # track
    d.rectangle([x, y + h - 24, x + w, y + h - 8], fill=(40, 40, 46))
    for i in range(9):
        d.rectangle([x + 4 + i * 16, y + h - 17, x + 12 + i * 16, y + h - 15],
                    fill=(255, 255, 255))
    # car
    cx, cy = x + 46, y + h - 30
    d.polygon([(cx, cy + 8), (cx + 8, cy), (cx + 34, cy), (cx + 44, cy + 8)],
              fill=(220, 30, 30))
    d.rectangle([cx + 6, cy + 4, cx + 40, cy + 10], fill=(180, 20, 20))
    d.ellipse([cx + 4, cy + 6, cx + 14, cy + 16], fill=(10, 10, 10))
    d.ellipse([cx + 32, cy + 6, cx + 42, cy + 16], fill=(10, 10, 10))
    # chequered flag
    for r in range(3):
        for c in range(4):
            col = (255, 255, 255) if (r + c) % 2 == 0 else (10, 10, 10)
            d.rectangle([x + w - 24 + c * 5, y + 4 + r * 5,
                         x + w - 19 + c * 5, y + 9 + r * 5], fill=col)
    d.line([x + w - 24, y + 4, x + w - 24, y + 24], fill=(200, 200, 200), width=1)
    label(d, x + 4, y + 4, "POLE: " + F1_POLE_DRIVER.upper(), 7, bg=RED)


def art_himars(d, x, y, w, h):
    """Launcher firing, blast on the horizon."""
    d.rectangle([x, y, x + w, y + h], fill=(36, 32, 24))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(20, 18, 14))
    # launcher vehicle
    d.rectangle([x + 10, y + h - 30, x + 62, y + h - 14], fill=(70, 90, 50))
    d.rectangle([x + 44, y + h - 38, x + 58, y + h - 30], fill=(70, 90, 50))
    d.ellipse([x + 16, y + h - 18, x + 26, y + h - 8], fill=(10, 10, 10))
    d.ellipse([x + 46, y + h - 18, x + 56, y + h - 8], fill=(10, 10, 10))
    # rocket trail + blast
    d.line([x + 56, y + h - 34, x + 120, y + 8], fill=(255, 160, 40), width=3)
    d.line([x + 56, y + h - 34, x + 120, y + 8], fill=(255, 240, 180), width=1)
    for dx, dy in [(0, -10), (0, 10), (-10, 0), (10, 0), (-7, -7), (7, 7), (-7, 7), (7, -7)]:
        d.line([x + 120, y + 8, x + 120 + dx, y + 8 + dy], fill=(255, 180, 40), width=2)
    d.ellipse([x + 114, y + 2, x + 126, y + 14], fill=(255, 240, 180))
    label(d, x + 4, y + 4, "20 COMMANDERS", 7, bg=RED)


def art_rahul(d, x, y, w, h):
    """Cricket: bat, ball, stumps, big 100."""
    d.rectangle([x, y, x + w, y + h], fill=(28, 90, 44))
    d.ellipse([x + 10, y + 8, x + w - 10, y + h - 6], fill=(48, 130, 64))
    # pitch
    d.rectangle([x + 66, y + 6, x + 96, y + h - 8], fill=(210, 190, 140))
    # stumps
    for sx in (72, 80, 88):
        d.rectangle([x + sx, y + 10, x + sx + 3, y + 24], fill=(250, 220, 90))
    # bat
    d.polygon([(x + 30, y + 44), (x + 44, y + 18), (x + 54, y + 24),
               (x + 40, y + 50)], fill=(220, 190, 130))
    d.line([x + 49, y + 21, x + 58, y + 10], fill=(120, 90, 50), width=3)
    # ball
    d.ellipse([x + 112, y + 12, x + 122, y + 22], fill=(200, 30, 30))
    d.text((x + 8, y + 4), "100*", font=SANS_B(22), fill=(255, 255, 255))
    label(d, x + w - 66, y + h - 14, "207 BALLS", 7, bg=(0, 0, 0))


def art_gaza(d, x, y, w, h):
    """Sombre memorial: candles under a dark sky, oversized toll."""
    d.rectangle([x, y, x + w, y + h], fill=(12, 12, 18))
    # candles
    for i, cx in enumerate(range(14, w - 8, 18)):
        ch = 14 + (i % 3) * 5
        d.rectangle([x + cx, y + h - 10 - ch, x + cx + 6, y + h - 10],
                    fill=(240, 230, 210))
        d.ellipse([x + cx + 1, y + h - 16 - ch, x + cx + 5, y + h - 10 - ch],
                  fill=(255, 180, 40))
    d.text((x + 8, y + 4), "22,000+", font=SANS_B(21), fill=(255, 255, 255))
    label(d, x + 8, y + h - 26, "CHILDREN KILLED", 7, bg=RED)


def art_denmark(d, x, y, w, h):
    """Danish flag, departing plane."""
    d.rectangle([x, y, x + w, y + h], fill=(180, 20, 40))
    d.rectangle([x, y + h // 2 - 7, x + w, y + h // 2 + 7], fill=(255, 255, 255))
    d.rectangle([x + 34, y, x + 48, y + h], fill=(255, 255, 255))
    # plane silhouette flying out
    px, py = x + 96, y + 16
    d.polygon([(px, py), (px + 34, py + 6), (px, py + 12)], fill=(255, 255, 255))
    d.polygon([(px + 12, py + 4), (px + 20, py - 6), (px + 24, py + 4)],
              fill=(255, 255, 255))
    d.line([px - 30, py + 8, px - 2, py + 8], fill=(255, 255, 255), width=2)
    label(d, x + 4, y + h - 14, "EXPELLED", 8, bg=(0, 0, 0))


def art_somalia(d, x, y, w, h):
    """Somali flag, star, exit arrow."""
    d.rectangle([x, y, x + w, y + h], fill=(65, 137, 221))
    cx, cy, r = x + 52, y + 30, 20
    import math
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(255, 255, 255))
    # exit arrow
    d.line([x + 100, y + 30, x + 140, y + 30], fill=(255, 255, 255), width=4)
    d.polygon([(x + 140, y + 30), (x + 128, y + 22), (x + 128, y + 38)],
              fill=(255, 255, 255))
    label(d, x + 4, y + h - 14, "AMBASSADOR OUT", 7, bg=(0, 0, 0))


def art_kim(d, x, y, w, h):
    """New Yalu River Bridge, train crossing, river below."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 44, 74))
    # sky glow
    d.ellipse([x + w - 40, y + 4, x + w - 16, y + 28], fill=(255, 220, 120))
    # river
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(30, 90, 140))
    for i in range(9):
        d.line([x + 4 + i * 18, y + h - 10, x + 14 + i * 18, y + h - 10],
               fill=(120, 190, 240), width=2)
    # bridge deck + towers
    d.rectangle([x, y + h - 34, x + w, y + h - 28], fill=(200, 200, 210))
    for tx in (30, 84, 138):
        d.rectangle([x + tx, y + 10, x + tx + 6, y + h - 28], fill=(200, 200, 210))
        d.line([x + tx + 3, y + 10, x + tx - 22, y + h - 34], fill=(180, 180, 190), width=1)
        d.line([x + tx + 3, y + 10, x + tx + 28, y + h - 34], fill=(180, 180, 190), width=1)
    # train
    d.rectangle([x + 44, y + h - 46, x + 116, y + h - 34], fill=(30, 130, 70))
    for wx in range(50, 112, 12):
        d.rectangle([x + wx, y + h - 43, x + wx + 7, y + h - 38], fill=(255, 240, 160))
    label(d, x + 4, y + 4, "NEW BRIDGE", 7, bg=RED)
    label(d, x + w - 66, y + 4, "DANDONG", 7, bg=(0, 0, 0))


ARTS = {"genz": art_genz, "hormuz": art_hormuz, "bepi": art_bepi,
        "cop31": art_cop31, "rutte": art_rutte, "putin": art_putin,
        "akvan": art_akvan, "dragon": art_dragon, "riemann": art_riemann,
        "f1": art_f1, "himars": art_himars, "rahul": art_rahul,
        "gaza": art_gaza, "denmark": art_denmark, "somalia": art_somalia,
        "kim": art_kim}


def draw_art(img, art, x, y, w, h):
    """Render one art panel onto its own layer (clips overflow), then paste."""
    tmp = Image.new("RGB", (w, h), (0, 0, 0))
    td = ImageDraw.Draw(tmp)
    art(td, 0, 0, w, h)
    img.paste(tmp, (x, y))

# ---------------------------------------------------------------- world map
# Coarse land mask: row -> list of (col_start, col_end) inclusive.
# Grid is 72 cols (5 deg lon each) x 36 rows (5 deg lat each).
LAND = {
    1: [(28, 31)], 2: [(10, 20), (25, 32), (50, 55)],
    3: [(4, 10), (12, 22), (24, 32), (50, 70)],
    4: [(3, 22), (25, 31), (31, 32), (42, 71)],
    5: [(3, 24), (26, 30), (31, 33), (37, 42), (44, 71)],
    6: [(4, 24), (35, 36), (37, 43), (45, 71)],
    7: [(5, 23), (35, 36), (36, 44), (46, 71)],
    8: [(6, 23), (34, 45), (47, 70)],
    9: [(7, 23), (34, 46), (48, 64)],
    10: [(8, 22), (34, 46), (48, 63), (62, 65)],
    11: [(9, 22), (33, 46), (49, 63), (63, 64)],
    12: [(10, 20), (32, 46), (49, 56), (60, 63)],
    13: [(11, 19), (32, 46), (50, 54), (55, 57)],
    14: [(12, 19), (32, 46), (50, 53), (55, 57)],
    15: [(15, 20), (33, 46), (50, 53), (55, 57)],
    16: [(17, 20), (20, 29), (34, 46), (55, 60)],
    17: [(20, 29), (34, 45), (56, 62)],
    18: [(20, 29), (35, 44), (55, 56), (58, 66)],
    19: [(20, 29), (36, 44), (58, 65)],
    20: [(21, 28), (37, 44), (44, 45), (59, 66)],
    21: [(21, 28), (38, 43), (44, 45), (58, 66)],
    22: [(22, 27), (38, 43), (45, 45), (59, 66)],
    23: [(22, 27), (39, 43), (59, 65)],
    24: [(22, 26), (40, 42), (60, 65), (70, 71)],
    25: [(23, 26), (61, 64), (69, 71)],
    26: [(23, 25), (62, 63), (65, 65), (69, 70)],
    27: [(23, 25), (69, 70)],
    28: [(23, 24)],
}

# (story, true lon, true lat, pin lon, pin lat) — pins offset where the
# eastern Mediterranean / Europe crowd together; a leader line marks the truth.
PINS = [
    (2, -3.7, 40.4, -3.7, 40.4), (3, 56.5, 26.5, 60.0, 26.5),
    (4, 30.7, 36.9, 30.7, 36.9), (5, 21.0, 52.2, 24.0, 50.0),
    (6, 37.6, 55.7, 40.0, 58.0), (7, 85.0, 20.0, 85.0, 20.0),
    (8, -120.0, 33.0, -135.0, 32.0), (10, -115.2, 36.2, -115.2, 36.2),
    (11, 34.8, 50.9, 50.0, 45.0), (12, 174.8, -41.3, 172.0, -41.3),
    (13, 34.5, 31.5, 42.0, 26.0), (14, 12.6, 55.7, 10.0, 57.0),
    (15, 45.3, 2.0, 45.3, 2.0), (16, 124.4, 40.1, 124.4, 40.1),
]


def draw_map(d, mx, my):
    """Dark world map, 288x144, with numbered pins."""
    mw, mh, cell = 288, 144, 4
    d.rectangle([mx, my, mx + mw, my + mh], fill=(10, 20, 44))
    d.rectangle([mx, my, mx + mw, my + mh], outline=RULE, width=1)
    for r, spans in LAND.items():
        for (c0, c1) in spans:
            d.rectangle([mx + c0 * cell, my + r * cell,
                         mx + (c1 + 1) * cell, my + (r + 1) * cell],
                        fill=(206, 188, 150))
    # graticule
    for gx in range(0, 73, 12):
        d.line([mx + gx * cell, my, mx + gx * cell, my + mh],
               fill=(30, 48, 80), width=1)
    for gy in range(0, 37, 12):
        d.line([mx, my + gy * cell, mx + mw, my + gy * cell],
               fill=(30, 48, 80), width=1)

    def px(lon, lat):
        return (mx + (lon + 180.0) / 360.0 * mw,
                my + (90.0 - lat) / 180.0 * mh)

    pf = SANS_B(6)
    for (num, tlon, tlat, plon, plat) in PINS:
        tx, ty = px(tlon, tlat)
        px_, py_ = px(plon, plat)
        if (tx, ty) != (px_, py_):
            d.line([tx, ty, px_, py_], fill=(255, 255, 255), width=1)
            d.ellipse([tx - 1.5, ty - 1.5, tx + 1.5, ty + 1.5], fill=(255, 255, 255))
        d.ellipse([px_ - 5, py_ - 5, px_ + 5, py_ + 5], fill=RED,
                  outline=(255, 255, 255), width=1)
        t = str(num)
        tw = d.textlength(t, font=pf)
        d.text((px_ - tw / 2, py_ - 4), t, font=pf, fill=(255, 255, 255))


# ---------------------------------------------------------------- date check
DC_FRI = ("Kyiv barrage \u00b7 Kh-101 in Poland \u00b7 Wall St sell-off S&P \u22123.7% \u00b7 "
          "Akvan landfall \u00b7 Peru M6.8 \u00b7 Mamdani Rikers 2032 \u00b7 F1 FP2 wet, Russell fastest \u00b7 "
          "Taiex \u22126.2% \u00b7 Kospi \u22125.2% \u00b7 Nikkei \u22124.8% \u00b7 SoftBank \u221216% \u00b7 UK\u2013EU reset deal \u00b7 "
          "Nvidia \u221214% on SEC probe \u00b7 Japan inflation 2.3% \u00b7 Italy CGIL strike \u00b7 "
          "Bukele 3rd term \u00b7 China LPR held \u00b7 Seoul impeach chief justice \u00b7 "
          "Jurf al-Sakhar \u00b7 Turkana oil well \u00b7 Judge blocks Trump arch \u00b7 "
          "Argentina risk 1,070 \u00b7 Florida floods \u00b7 Trump data-centre penalties \u00b7 "
          "Panama COP31 oil cap \u00b7 WFP $12bn appeal \u00b7 Voyager 1 light-day \u00b7 "
          "Malawi fuel crisis \u00b7 Senegal boat \u00b7 Sudan gold-mine strike \u00b7 "
          "Pancreatic pill trial \u00b7 Tonga El Ni\u00f1o \u00b7 Xi\u2013Albanese \u00b7 Suneung cheating \u00b7 "
          "Kospi curb \u00b7 EU: COP31 draft unacceptable \u00b7 ATP pay reforms \u00b7 "
          "Hunger Games $21.25m \u00b7 Sheinbaum parade \u00b7 Lisa Cook rate hikes \u00b7 "
          "Myanmar: ICJ 'unfair' \u00b7 St Johns River 18.3 ft \u00b7 Lviv station strike \u00b7 "
          "US\u2013Venezuela deal \u00b7 Neuralink GTA VI video \u00b7 Binance hacker $346m \u00b7 "
          "Inkling 2 Mini \u00b7 Mlambo-Ngcuka dies \u00b7 Florida pastor guilty \u00b7 "
          "XMR1 \u221299% hack \u00b7 SEC $560m Ponzi \u00b7 MedChemBench launch \u00b7 Walliams police probe")
DC_THU = ("ICJ Myanmar ruling \u00b7 Shenzhen summit \u00b7 GTA VI launch \u00b7 Anthropic $83 IPO \u00b7 "
          "Crimean Bridge strike \u00b7 Riyadh tower attack \u00b7 Van Gogh $190.4m \u00b7 "
          "Senate Iran vote \u00b7 Denmark\u2013US Greenland pact \u00b7 Mrima Hill $60bn \u00b7 "
          "Colombia denies NYT \u00b7 Julio Iglesias probe \u00b7 Sinaloa bombing \u00b7 "
          "Hegseth Caracas jog \u00b7 US chip rule in force")
DC_EARLIER = ("Egypt $2.3bn IMF (Wed 18) \u00b7 Wong 10y (5 Nov) \u00b7 Everest collision (3 Nov) \u00b7 "
              "Haines discharged (16 Nov) \u00b7 TotalEnergies Chile (13 Nov) \u00b7 "
              "Guatemala emergency (14 Nov) \u00b7 Lula\u2013S\u00e1nchez (16 Nov) \u00b7 "
              "Gulf Cartel boss (17 Nov) \u00b7 Mexico journalist/musician (16 Nov) \u00b7 "
              "Brazil poll (13 Nov) \u00b7 Sanrio\u2013Vivant (29 Oct) \u00b7 Walliams cameo cut (17 Nov) \u00b7 "
              "SA swimming probe (17 Nov) \u00b7 Sudan cathedral (9 Nov)")
DC_NOTYET = ("ATP Finals final (Sun 22) \u00b7 Nepal PM Balen in Delhi (Sun 22) \u00b7 "
             "Las Vegas GP race (Sun 22 UTC) \u00b7 BepiColombo MPO\u2013Mio split (9\u201310 Dec)")
DC_WHY = ("Every story above happened, or was first reported, on Saturday 21 November 2026 "
          "\u2014 nothing from Friday's front pages is repeated as today's news.")

WARNINGS = []


def warn(msg):
    WARNINGS.append(msg)
    print("WARN:", msg, file=sys.stderr)


# ---------------------------------------------------------------- layout
def compose():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 8                      # side margin
    CW = W - 2 * MX             # content width = 1008

    # ---- region + field counts from the data (never hand-typed)
    all_stories = LEADS + FEATURES + [
        dict(num=n, region=r, field=f, tag=t) for (n, _, t, r, f) in BRIEFS]
    nstories = len(all_stories)
    rcount = {}
    for s in all_stories:
        rcount[s["region"]] = rcount.get(s["region"], 0) + 1
    nfields = len({s["field"] for s in all_stories})
    assert nstories == 52, nstories
    assert sum(rcount.values()) == 52

    # ---- top bar
    d.text((MX, 5), "THE WORLD IN ONE DAY", font=SANS_B(11), fill=RED)
    top_r = (f"{nstories} STORIES \u00b7 7 REGIONS \u00b7 {nfields} FIELDS \u00b7 "
             "EVERY ONE DATED SATURDAY 21 NOVEMBER 2026")
    d.text((W - MX - d.textlength(top_r, font=SANS_B(11)), 5), top_r,
           font=SANS_B(11), fill=INK)
    d.line([MX, 20, W - MX, 20], fill=RULE, width=1)

    # ---- masthead
    mast = "Saturday 21 November 2026"
    mf = SERIF_B(54)
    d.text(((W - d.textlength(mast, font=mf)) / 2, 22), mast, font=mf, fill=INK)
    d.line([MX, 78, W - MX, 78], fill=RULE, width=2)

    # ---- sub-headline strip
    d.rectangle([MX, 80, W - MX, 100], fill=NAVY)
    sub = ("Gen Z floods 25 nations' streets  \u00b7  3 missiles downed over Hormuz  "
           "\u00b7  BepiColombo burns for Mercury tonight  \u00b7  COP31 in overtime")
    sf = SANS_B(12)
    d.text(((W - d.textlength(sub, font=sf)) / 2, 84), sub, font=sf,
           fill=(255, 255, 255))

    # ---- UTC timeline
    ty = 102
    d.rectangle([MX, ty, MX + 92, ty + 40], fill=RED)
    d.text((MX + 6, ty + 5), "THE DAY", font=SANS_B(11), fill=(255, 255, 255))
    d.text((MX + 6, ty + 19), "IN UTC", font=SANS_B(11), fill=(255, 255, 255))
    cell_w = (CW - 92 - 7 * 2) / 8
    tl_items = [
        ("00:00", "3 Houthi missiles downed; IRGC claims MQ-9 hit"),
        ("01:12", "Denmark expels Russian diplomat"),
        ("01:49", "Trump: Nvidia should reinstate Huang"),
        ("02:49", "25-nation Gen Z protests; Putin: no ceasefire"),
        ("03:31", "HIMARS kills 20 Russian commanders, Sumy"),
        ("03:49", "IMD: Akvan weakens to low-pressure area"),
        ("18:24", "BepiColombo burn begins (19:24 CET)"),
        ("21:55", "Dragon CRS-35 splashdown off California"),
    ]
    for i, (t, txt) in enumerate(tl_items):
        cx = MX + 92 + 2 + i * (cell_w + 2)
        d.rectangle([cx, ty, cx + cell_w, ty + 40], outline=RULE, width=1)
        d.text((cx + 4, ty + 2), t, font=SANS_B(9), fill=RED)
        for j, ln in enumerate(wrap(d, txt, SANS(8), cell_w - 8)[:2]):
            d.text((cx + 4, ty + 13 + j * 10), ln, font=SANS(8), fill=INK)

    # ---- stat strip
    sy = 144
    sw = CW / 6
    for i, (num, lab) in enumerate(STATS):
        cx = MX + i * sw
        if i:
            d.line([cx, sy + 2, cx, sy + 30], fill=(200, 195, 180), width=1)
        d.text((cx + 6, sy), num, font=SANS_B(17), fill=RED if i in (0, 3) else NAVY)
        for j, ln in enumerate(wrap(d, lab, SANS(8), sw - 12)[:2]):
            d.text((cx + 6, sy + 20 + j * 9), ln, font=SANS(8), fill=MUTED)
    d.line([MX, sy + 32, W - MX, sy + 32], fill=RULE, width=1)

    # ---- region strip
    ry = 178
    rw = CW / 7
    for i, (name, code, col) in enumerate(REGIONS):
        cx = MX + i * rw
        d.rectangle([cx, ry, cx + rw - 2, ry + 14], fill=col)
        t = f"{name} {rcount[code]}"
        d.text((cx + (rw - 2 - d.textlength(t, font=SANS_B(8))) / 2, ry + 2),
               t, font=SANS_B(8), fill=(255, 255, 255))

    # ---- leads
    ly, lart = 194, 112
    lw = (CW - 2 * 4) // 3
    for i, s in enumerate(LEADS):
        x = MX + i * (lw + 4)
        d.rectangle([x, ly, x + lw, ly + 200], fill=CARD_BG, outline=RULE, width=1)
        draw_art(img, ARTS[s["art"]], x + 1, ly + 1, lw - 2, lart)
        ky = ly + lart + 3
        d.text((x + 5, ky), f"{s['num']}  {s['kick']}", font=SANS_B(9), fill=RED)
        tw = draw_tag(d, x + lw - 5 - 62, ky, s["tag"], 8)
        hy = ky + 13
        hlines = wrap(d, s["head"], SERIF_B(19), lw - 10)
        if len(hlines) > 2:
            warn(f"lead {s['num']} headline wraps to {len(hlines)} lines")
        for j, ln in enumerate(hlines[:2]):
            d.text((x + 5, hy + j * 20), ln, font=SERIF_B(19), fill=INK)
        by = hy + 41
        blines = wrap(d, s["body"], SANS(10), lw - 10)
        if len(blines) > 3:
            warn(f"lead {s['num']} body wraps to {len(blines)} lines")
        for j, ln in enumerate(blines[:3]):
            d.text((x + 5, by + j * 10), ln, font=SANS(10), fill=INK)

    # ---- features, two rows: 7 then 6
    def feature_row(y0, items, cols):
        cw = (CW - (cols - 1) * 4) // cols
        for i, s in enumerate(items):
            x = MX + i * (cw + 4)
            d.rectangle([x, y0, x + cw, y0 + 128], fill=CARD_BG,
                        outline=RULE, width=1)
            draw_art(img, ARTS[s["art"]], x + 1, y0 + 1, cw - 2, 52)
            ky = y0 + 55
            d.text((x + 4, ky), f"{s['num']}  {s['kick']}", font=SANS_B(7),
                   fill=RED)
            draw_tag(d, x + cw - 4 - 50, ky - 1, s["tag"], 7)
            hy = ky + 10
            hlines = wrap(d, s["head"], SANS_B(11), cw - 8)
            if len(hlines) > 2:
                warn(f"feature {s['num']} headline wraps to {len(hlines)} lines")
            for j, ln in enumerate(hlines[:2]):
                d.text((x + 4, hy + j * 12), ln, font=SANS_B(11), fill=INK)
            by = hy + 24
            blines = wrap(d, s["body"], SANS(9), cw - 8)
            if len(blines) > 4:
                warn(f"feature {s['num']} body wraps to {len(blines)} lines")
            for j, ln in enumerate(blines[:4]):
                d.text((x + 4, by + j * 9), ln, font=SANS(9), fill=INK)

    feature_row(396, FEATURES[:7], 7)
    feature_row(526, FEATURES[7:], 6)

    # ---- map + briefs
    my = 656
    d.text((MX, my), "WHERE IT HAPPENED", font=SANS_B(11), fill=RED)
    d.text((MX + 316, my), "ALSO ON SATURDAY 21 NOVEMBER \u2014 36 MORE STORIES",
           font=SANS_B(11), fill=RED)
    d.line([MX, my + 14, W - MX, my + 14], fill=RULE, width=1)
    draw_map(d, MX + 2, my + 18)
    d.text((MX + 2, my + 166), "PINS = STORIES ABOVE \u00b7 1 BepiColombo in space \u00b7",
           font=SANS(8), fill=MUTED)
    d.text((MX + 2, my + 176), "9 Riemann claim online \u00b7 pins offset where crowded",
           font=SANS(8), fill=MUTED)

    bf = SANS(9)
    bfb = SANS_B(9)
    colw = 346
    for k, (n, txt, tag, reg, fld) in enumerate(BRIEFS):
        col = k // 18
        row = k % 18
        bx = MX + 316 + col * (colw + 8)
        by = my + 16 + row * 9.5
        # tag chip
        d.rectangle([bx, by, bx + 9, by + 8], fill=TAGC[tag])
        d.text((bx + 2, by - 1), tag, font=SANS_B(7), fill=(255, 255, 255))
        num = f"{n}."
        d.text((bx + 12, by - 1), num, font=bfb, fill=INK)
        nw = d.textlength(num + " ", font=bfb)
        tw = d.textlength(txt, font=bf)
        if 12 + nw + tw > colw:
            warn(f"brief {n} too wide by {12 + nw + tw - colw:.0f}px: {txt}")
        d.text((bx + 12 + nw, by - 1), txt, font=bf, fill=INK)

    # ---- date check
    dy = 846
    d.rectangle([MX, dy, W - MX, dy + 153], fill=(255, 253, 247),
                outline=RED, width=2)
    d.rectangle([MX, dy, MX + 92, dy + 153], fill=RED)
    d.text((MX + 8, dy + 8), "DATE", font=SANS_B(15), fill=(255, 255, 255))
    d.text((MX + 8, dy + 26), "CHECK", font=SANS_B(15), fill=(255, 255, 255))
    d.text((MX + 8, dy + 48), "Left out on", font=SANS(8), fill=(255, 255, 255))
    d.text((MX + 8, dy + 58), "purpose \u2014", font=SANS(8), fill=(255, 255, 255))
    d.text((MX + 8, dy + 68), "these are NOT", font=SANS(8), fill=(255, 255, 255))
    d.text((MX + 8, dy + 78), "Saturday news.", font=SANS(8), fill=(255, 255, 255))
    tx = MX + 100
    tw_ = W - MX - tx - 6
    cy = dy + 8
    for lab, txt in [("FRI 20 NOV", DC_FRI), ("THU 19 NOV", DC_THU),
                     ("EARLIER", DC_EARLIER), ("NOT YET", DC_NOTYET),
                     ("WHY", DC_WHY)]:
        lf = SANS_B(9)
        lw_ = d.textlength(lab + "  ", font=lf)
        d.text((tx, cy), lab, font=lf, fill=RED)
        lines = wrap(d, txt, SANS(9), tw_ - lw_)
        for j, ln in enumerate(lines):
            d.text((tx + (lw_ if j == 0 else 0), cy + j * 10), ln,
                   font=SANS(9), fill=INK)
        cy += len(lines) * 10 + 3
    if cy > dy + 153:
        warn(f"date check overflows by {cy - (dy + 153)}px")

    # ---- footer
    fy = 1002
    d.text((MX, fy), "C  CONFIRMED \u00b7 2+ outlets     O  OFFICIAL \u00b7 on the record     "
                    "R  REPORTED \u00b7 one outlet",
           font=SANS_B(8), fill=INK)
    fr = "Sources named beside each story \u00b7 All drawings original, procedural"
    d.text((W - MX - d.textlength(fr, font=SANS(8)), fy), fr, font=SANS(8),
           fill=MUTED)
    foot = "Every story here happened, or was first reported, on Saturday 21 November 2026."
    ff = SANS_B(10)
    d.text(((W - d.textlength(foot, font=ff)) / 2, fy + 11), foot, font=ff,
           fill=INK)
    return img


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = compose()
    img.save(out, format="PNG")
    data = open(out, "rb").read()
    print(f"wrote {out}: {len(data)} bytes, "
          f"sha256={hashlib.sha256(data).hexdigest()}")
    print(f"warnings: {len(WARNINGS)}")


if __name__ == "__main__":
    main()
