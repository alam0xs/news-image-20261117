#!/usr/bin/env python3
"""Render the v2 poster for make.fun news-image-20261117.

Dev-time only: renders at 2048x2048 with PIL and real fonts, then
downsamples to 1024x1024 with LANCZOS. The finished 1024 PNG is embedded
as base64 in entry_data.py (the GitHub connector cannot push binaries);
main.py decodes it at run time. See facts.md for the story list.
Every line of this file was written for this poster; no pasted art.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
S = 2  # render scale: 2048 canvas, 1024 output
W, H = 1024 * S, 1024 * S

CREAM = (247, 241, 227)
WHITE = (255, 253, 247)
NAVY = (16, 33, 63)
NAVY_SOFT = (38, 58, 92)
GOLD = (212, 168, 56)
GOLD_DARK = (176, 134, 34)
INK = (24, 28, 38)
GREY = (74, 80, 96)
BORDER = (216, 205, 178)

REGIONS = {
    "N. America": (179, 58, 58),
    "S. America": (217, 123, 41),
    "Europe": (46, 111, 176),
    "Middle East": (123, 79, 166),
    "Africa": (138, 90, 43),
    "Asia": (46, 125, 79),
    "Oceania": (31, 138, 138),
}

FONT_SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit_text(draw, text, f_path, size, max_w, max_lines, min_size):
    """Shrink font until text fits max_lines at max_w. Returns (font, lines)."""
    while size >= min_size:
        f = font(f_path, size)
        lines = wrap(draw, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        size -= 2
    f = font(f_path, min_size)
    return f, wrap(draw, text, f, max_w)


def draw_centered(draw, cx, y, s, f, fill):
    draw.text((cx - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


def letterspaced(draw, x, y, s, f, fill, spacing=6):
    """Draw text with extra space between letters, left-aligned at x.
    Returns the total width drawn (including spacing)."""
    total = 0
    for ch in s:
        w = text_w(draw, ch, f)
        draw.text((x + total, y), ch, font=f, fill=fill)
        total += w + spacing
    return total - spacing


def rounded_rect(draw, box, radius, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=radius, fill=fill, outline=outline,
                           width=width)


def chip(draw, x, y, label, color, f):
    """Small rounded region chip; returns its width."""
    pad_x, pad_y = 16, 8
    w = int(text_w(draw, label, f)) + pad_x * 2
    h = f.size + pad_y * 2
    rounded_rect(draw, [x, y, x + w, y + h], radius=h // 2, fill=color)
    draw.text((x + pad_x, y + pad_y - 2), label, font=f, fill=WHITE)
    return w

# ---------------------------------------------------------------- icons
# Each icon draws centred on (cx, cy) inside a box of half-size r.
# Flat vector style, original drawings, no logos or real faces.

def icon_bridge(draw, cx, cy, r, c):
    # broken bridge: two deck segments, sagging arc, water
    deck_y = cy - r * 0.25
    draw.rectangle([cx - r, deck_y, cx - r * 0.18, deck_y + r * 0.16], fill=c)
    draw.rectangle([cx + r * 0.18, deck_y, cx + r, deck_y + r * 0.16], fill=c)
    draw.arc([cx - r * 0.85, deck_y - r * 0.55, cx + r * 0.85,
              deck_y + r * 0.75], 200, 340, fill=c, width=max(3, r // 12))
    draw.line([cx - r, deck_y + r * 0.16, cx - r, deck_y + r * 0.75], fill=c,
              width=max(3, r // 12))
    draw.line([cx + r, deck_y + r * 0.16, cx + r, deck_y + r * 0.75], fill=c,
              width=max(3, r // 12))
    for i, yy in enumerate((cy + r * 0.55, cy + r * 0.75)):
        draw.line([cx - r, yy, cx + r, yy], fill=c, width=max(2, r // 16))
        draw.line([cx - r * 0.5, yy + r * 0.08, cx + r * 0.6, yy + r * 0.08],
                  fill=c, width=max(2, r // 16))


def icon_tanker(draw, cx, cy, r, c):
    # tanker with drones above
    hull_y = cy + r * 0.1
    draw.polygon([(cx - r, hull_y), (cx + r * 0.9, hull_y),
                  (cx + r * 0.55, hull_y + r * 0.45),
                  (cx - r * 0.75, hull_y + r * 0.45)], fill=c)
    draw.rectangle([cx - r * 0.55, hull_y - r * 0.45, cx - r * 0.05,
                    hull_y], fill=c)
    draw.rectangle([cx + r * 0.05, hull_y - r * 0.28, cx + r * 0.45,
                    hull_y], fill=(255, 255, 255))
    draw.rectangle([cx + r * 0.12, hull_y - r * 0.42, cx + r * 0.2,
                    hull_y - r * 0.28], fill=c)
    for dx, dy in ((-r * 0.55, -r * 0.8), (0, -r * 0.95), (r * 0.55, -r * 0.8)):
        draw.ellipse([cx + dx - r * 0.07, cy + dy - r * 0.07,
                      cx + dx + r * 0.07, cy + dy + r * 0.07], fill=c)
        draw.line([cx + dx - r * 0.14, cy + dy, cx + dx + r * 0.14, cy + dy],
                  fill=c, width=max(2, r // 18))
    for yy in (cy + r * 0.68, cy + r * 0.86):
        draw.line([cx - r, yy, cx + r, yy], fill=c, width=max(2, r // 16))


def icon_leaders(draw, cx, cy, r, c):
    # three people at a table
    cols = [NAVY, (46, 111, 176), (179, 58, 58)]
    for i, col in enumerate(cols):
        px = cx + (i - 1) * r * 0.62
        draw.ellipse([px - r * 0.2, cy - r * 0.75, px + r * 0.2, cy - r * 0.35],
                     fill=col)
        draw.pieslice([px - r * 0.34, cy - r * 0.28, px + r * 0.34,
                       cy + r * 0.42], 180, 360, fill=col)
    draw.rectangle([cx - r, cy + r * 0.45, cx + r, cy + r * 0.62], fill=c)
    draw.line([cx - r * 0.85, cy + r * 0.85, cx - r * 0.7, cy + r * 0.85],
              fill=c, width=max(3, r // 12))
    draw.line([cx + r * 0.7, cy + r * 0.85, cx + r * 0.85, cy + r * 0.85],
              fill=c, width=max(3, r // 12))


def icon_mountain_flag(draw, cx, cy, r, c):
    draw.polygon([(cx - r * 0.9, cy + r * 0.7), (cx - r * 0.05, cy - r * 0.7),
                  (cx + r * 0.9, cy + r * 0.7)], fill=c)
    draw.polygon([(cx - r * 0.05, cy - r * 0.7), (cx + r * 0.25, cy - r * 0.25),
                  (cx - r * 0.3, cy - r * 0.25)], fill=WHITE)
    draw.line([cx + r * 0.05, cy - r * 0.7, cx + r * 0.05, cy - r * 1.0],
              fill=c, width=max(3, r // 12))
    draw.polygon([(cx + r * 0.05, cy - r * 1.0), (cx + r * 0.5, cy - r * 0.88),
                  (cx + r * 0.05, cy - r * 0.76)], fill=(179, 58, 58))


def icon_virus(draw, cx, cy, r, c):
    for a in range(0, 360, 45):
        import math
        rad = math.radians(a)
        x1 = cx + math.cos(rad) * r * 0.55
        y1 = cy + math.sin(rad) * r * 0.55
        x2 = cx + math.cos(rad) * r * 0.95
        y2 = cy + math.sin(rad) * r * 0.95
        draw.line([x1, y1, x2, y2], fill=c, width=max(3, r // 10))
        draw.ellipse([x2 - r * 0.12, y2 - r * 0.12, x2 + r * 0.12,
                      y2 + r * 0.12], fill=c)
    draw.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                 fill=c)
    draw.ellipse([cx - r * 0.2, cy - r * 0.25, cx + r * 0.05, cy],
                 fill=WHITE)
    draw.ellipse([cx + r * 0.1, cy + r * 0.1, cx + r * 0.3, cy + r * 0.3],
                 fill=WHITE)


def icon_house_arrow(draw, cx, cy, r, c):
    draw.polygon([(cx - r * 0.75, cy + r * 0.05), (cx, cy - r * 0.7),
                  (cx + r * 0.75, cy + r * 0.05)], fill=c)
    draw.rectangle([cx - r * 0.55, cy + r * 0.05, cx + r * 0.55,
                    cy + r * 0.7], fill=c)
    draw.rectangle([cx - r * 0.14, cy + r * 0.25, cx + r * 0.14,
                    cy + r * 0.7], fill=WHITE)
    draw.line([cx + r * 0.55, cy - r * 0.15, cx + r * 0.95, cy - r * 0.15],
              fill=(179, 58, 58), width=max(4, r // 8))
    draw.polygon([(cx + r * 0.95, cy - r * 0.15), (cx + r * 0.7, cy - r * 0.4),
                  (cx + r * 0.7, cy + r * 0.1)], fill=(179, 58, 58))


def icon_exchange(draw, cx, cy, r, c):
    draw.ellipse([cx - r * 0.8, cy - r * 0.45, cx - r * 0.05, cy + r * 0.3],
                 outline=c, width=max(4, r // 8))
    draw.ellipse([cx + r * 0.05, cy - r * 0.3, cx + r * 0.8, cy + r * 0.45],
                 outline=c, width=max(4, r // 8))
    draw.polygon([(cx + r * 0.35, cy - r * 0.75), (cx + r * 0.6, cy - r * 0.45),
                  (cx + r * 0.1, cy - r * 0.45)], fill=c)
    draw.polygon([(cx - r * 0.35, cy + r * 0.75), (cx - r * 0.6, cy + r * 0.45),
                  (cx - r * 0.1, cy + r * 0.45)], fill=c)


def icon_jet(draw, cx, cy, r, c):
    draw.polygon([(cx - r * 0.9, cy + r * 0.1), (cx + r * 0.1, cy - r * 0.35),
                  (cx + r * 0.95, cy - r * 0.1), (cx + r * 0.1, cy + r * 0.35)],
                 fill=c)
    draw.polygon([(cx - r * 0.1, cy - r * 0.15), (cx - r * 0.25, cy - r * 0.75),
                  (cx + r * 0.15, cy - r * 0.2)], fill=c)
    draw.polygon([(cx - r * 0.1, cy + r * 0.15), (cx - r * 0.25, cy + r * 0.7),
                  (cx + r * 0.15, cy + r * 0.2)], fill=c)
    for i in range(4):
        x = cx - r * 0.9 + i * r * 0.28
        draw.ellipse([x, cy + r * 0.75, x + r * 0.1, cy + r * 0.85], fill=c)


def icon_bank(draw, cx, cy, r, c):
    draw.polygon([(cx - r * 0.9, cy - r * 0.15), (cx, cy - r * 0.85),
                  (cx + r * 0.9, cy - r * 0.15)], fill=c)
    for i in (-1, 0, 1):
        x = cx + i * r * 0.55
        draw.rectangle([x - r * 0.09, cy - r * 0.05, x + r * 0.09,
                        cy + r * 0.6], fill=c)
    draw.rectangle([cx - r * 0.95, cy + r * 0.6, cx + r * 0.95,
                    cy + r * 0.78], fill=c)
    draw.polygon([(cx + r * 0.45, cy - r * 0.95), (cx + r * 0.15, cy - r * 0.55),
                  (cx + r * 0.45, cy - r * 0.55), (cx + r * 0.15, cy - r * 0.15),
                  (cx + r * 0.4, cy - r * 0.15), (cx + r * 0.7, cy - r * 0.55),
                  (cx + r * 0.4, cy - r * 0.55), (cx + r * 0.7, cy - r * 0.95)],
                 fill=(212, 168, 56))


def icon_chip_up(draw, cx, cy, r, c):
    draw.rectangle([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55,
                    cy + r * 0.55], fill=c)
    draw.rectangle([cx - r * 0.25, cy - r * 0.25, cx + r * 0.25,
                    cy + r * 0.25], outline=WHITE, width=max(3, r // 10))
    for i in (-1, 0, 1):
        draw.line([cx + i * r * 0.35, cy - r * 0.55, cx + i * r * 0.35,
                   cy - r * 0.85], fill=c, width=max(3, r // 12))
        draw.line([cx + i * r * 0.35, cy + r * 0.55, cx + i * r * 0.35,
                   cy + r * 0.85], fill=c, width=max(3, r // 12))
    draw.polygon([(cx + r * 0.75, cy - r * 0.75), (cx + r * 0.55, cy - r * 0.35),
                  (cx + r * 0.95, cy - r * 0.35)], fill=(46, 125, 79))


def icon_rocket(draw, cx, cy, r, c):
    draw.polygon([(cx - r * 0.3, cy - r * 0.95), (cx + r * 0.3, cy - r * 0.95),
                  (cx, cy - r * 0.35)], fill=c)
    draw.rectangle([cx - r * 0.3, cy - r * 0.95 + r * 0.6, cx + r * 0.3,
                    cy + r * 0.15], fill=c)
    draw.ellipse([cx - r * 0.13, cy - r * 0.75, cx + r * 0.13, cy - r * 0.45],
                 fill=WHITE)
    draw.polygon([(cx - r * 0.3, cy - r * 0.1), (cx - r * 0.65, cy + r * 0.35),
                  (cx - r * 0.3, cy + r * 0.35)], fill=c)
    draw.polygon([(cx + r * 0.3, cy - r * 0.1), (cx + r * 0.65, cy + r * 0.35),
                  (cx + r * 0.3, cy + r * 0.35)], fill=c)
    draw.polygon([(cx - r * 0.16, cy + r * 0.15), (cx + r * 0.16, cy + r * 0.15),
                  (cx, cy + r * 0.75)], fill=(217, 123, 41))
    draw.line([cx - r * 0.8, cy + r * 0.6, cx - r * 0.5, cy + r * 0.6], fill=c,
              width=max(2, r // 16))
    draw.line([cx + r * 0.5, cy + r * 0.6, cx + r * 0.8, cy + r * 0.6], fill=c,
              width=max(2, r // 16))


def icon_chart_down(draw, cx, cy, r, c):
    draw.line([cx - r * 0.85, cy + r * 0.8, cx + r * 0.85, cy + r * 0.8],
              fill=c, width=max(3, r // 12))
    draw.line([cx - r * 0.85, cy - r * 0.8, cx - r * 0.85, cy + r * 0.8],
              fill=c, width=max(3, r // 12))
    pts = [(cx - r * 0.75, cy - r * 0.55), (cx - r * 0.25, cy - r * 0.2),
           (cx + r * 0.15, cy - r * 0.35), (cx + r * 0.75, cy + r * 0.55)]
    draw.line(pts, fill=(179, 58, 58), width=max(4, r // 8), joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey), (ex - r * 0.3, ey - r * 0.05),
                  (ex - r * 0.05, ey - r * 0.3)], fill=(179, 58, 58))


def icon_chip_ban(draw, cx, cy, r, c):
    draw.rectangle([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5],
                   fill=c)
    draw.rectangle([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2],
                   outline=WHITE, width=max(3, r // 10))
    for i in (-1, 0, 1):
        draw.line([cx + i * r * 0.3, cy - r * 0.5, cx + i * r * 0.3,
                   cy - r * 0.75], fill=c, width=max(3, r // 12))
        draw.line([cx + i * r * 0.3, cy + r * 0.5, cx + i * r * 0.3,
                   cy + r * 0.75], fill=c, width=max(3, r // 12))
    draw.ellipse([cx - r * 0.95, cy - r * 0.95, cx + r * 0.95, cy + r * 0.95],
                 outline=(179, 58, 58), width=max(5, r // 6))
    draw.line([cx - r * 0.67, cy + r * 0.67, cx + r * 0.67, cy - r * 0.67],
              fill=(179, 58, 58), width=max(5, r // 6))


def icon_scales(draw, cx, cy, r, c):
    draw.line([cx, cy - r * 0.8, cx, cy + r * 0.8], fill=c,
              width=max(4, r // 8))
    draw.line([cx - r * 0.75, cy - r * 0.55, cx + r * 0.75, cy - r * 0.55],
              fill=c, width=max(4, r // 8))
    draw.ellipse([cx - r * 0.1, cy - r * 0.95, cx + r * 0.1, cy - r * 0.75],
                 fill=c)
    for sx in (-r * 0.75, r * 0.75):
        draw.line([cx + sx, cy - r * 0.55, cx + sx, cy - r * 0.1], fill=c,
                  width=max(3, r // 12))
        draw.pieslice([cx + sx - r * 0.3, cy - r * 0.1, cx + sx + r * 0.3,
                       cy + r * 0.5], 0, 180, fill=c)
    draw.rectangle([cx - r * 0.6, cy + r * 0.8, cx + r * 0.6, cy + r * 0.95],
                   fill=c)


def icon_radiation(draw, cx, cy, r, c):
    import math
    draw.ellipse([cx - r * 0.16, cy - r * 0.16, cx + r * 0.16, cy + r * 0.16],
                 fill=c)
    for start in (270, 30, 150):
        draw.pieslice([cx - r * 0.85, cy - r * 0.85, cx + r * 0.85,
                       cy + r * 0.85], start, start + 60, fill=c)
    draw.ellipse([cx - r * 0.3, cy - r * 0.3, cx + r * 0.3, cy + r * 0.3],
                 fill=WHITE)
    draw.ellipse([cx - r * 0.16, cy - r * 0.16, cx + r * 0.16, cy + r * 0.16],
                 fill=c)

# ---------------------------------------------------------------- content
# Headlines were kept short on purpose so they fit in two lines at the
# required sizes. Full wording and sources: see facts.md.

HEROES = [
    ("Europe", icon_bridge, "Kerch Bridge hit again, span falls",
     "Kyiv says 7th phase of SBU operation; traffic halted"),
    ("Middle East", icon_tanker, "Iran says drones hit US radar",
     "US says drones downed; tankers hit by mines in Hormuz"),
    ("Asia", icon_leaders, "Trump, Xi, Putin to meet Thursday",
     "First trilateral talks at APEC; nuclear arms on agenda"),
]

MIDS = [
    ("Middle East", icon_mountain_flag, "Houthis push towards Aden"),
    ("Africa", icon_virus, "Ebola passes 11,000 cases in DR Congo"),
    ("Europe", icon_house_arrow, "Five EU states plan Rwanda return hub"),
    ("N. America", icon_exchange, "Carney and Xi agree tariff cuts"),
    ("Asia", icon_jet, "Russian jets enter Japanese airspace"),
    ("N. America", icon_bank, "JPMorgan blames bug for bank outage"),
    ("N. America", icon_chip_up, "Nvidia beats forecasts after Huang"),
    ("N. America", icon_rocket, "Vulcan fails; 40 satellites lost"),
    ("N. America", icon_chart_down, "AI sell-off: S&P -1.9%, Nasdaq -2.5%"),
    ("Asia", icon_chip_ban, "US tightens AI-chip export rules"),
    ("Europe", icon_scales, "UK sanctions eight settlement builders"),
    ("N. America", icon_radiation, "Trump warns Iran on 'dirty bomb'"),
]

BRIEFS = [
    ("Gulf:", "Roosevelt becomes third US carrier off Iran"),
    ("Black Sea:", "Second ship sinks off Bulgaria in two days"),
    ("Markets:", "Euro falls below $1.10, weakest since April"),
    ("Sport:", "Germany thrash Netherlands 5-0 in Nations League"),
    ("Siberia:", "Military plane crashes; all aboard killed"),
    ("India:", "Bus plunges 100m into gorge in Uttarakhand"),
    ("South Africa:", "17 killed in two mass shootings"),
    ("Nigeria:", "Inflation eases to 14.06%, a six-year low"),
    ("Brazil:", "Ten Indigenous lands demarcated at COP30"),
    ("Mongolia:", "President to resign over graft claims"),
    ("Cricket:", "Sri Lanka bowled out for 98 in Rawalpindi"),
    ("Israel:", "Inquiry calls over Netanyahu election arrests"),
    ("France:", "Depardieu drops appeal, conviction stands"),
    ("Manila:", "Trump lands for ASEAN summit and Quad talks"),
    ("Australia:", "Canberra sanctions Israeli settlers, builder"),
]

FOOTER_L1 = "Every story happened or was first reported on Tuesday 17 November 2026."
FOOTER_L2 = "Disputed claims are attributed. Sources: AP - Reuters - AFP - BBC - Al Jazeera."


def tint(color, frac=0.88):
    return tuple(int(c * (1 - frac) + 255 * frac) for c in color)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # ---- masthead
    d.rectangle([0, 0, W, 220], fill=NAVY)
    d.rectangle([0, 220, W, 228], fill=GOLD)
    letterspaced(d, 48, 30, "THE DAY IN WORLD NEWS",
                 font(FONT_SANS_B, 34), GOLD, spacing=8)
    df, dlines = fit_text(d, "TUESDAY 17 NOVEMBER 2026", FONT_SERIF_B, 116,
                          1540, 1, 88)
    d.text((48, 84), dlines[0], font=df, fill=WHITE)
    f_count = font(FONT_SANS_B, 46)
    d.text((W - 48 - text_w(d, "30 STORIES", f_count), 58), "30 STORIES",
           font=f_count, fill=GOLD)
    d.text((W - 48 - text_w(d, "6 CONTINENTS", f_count), 116), "6 CONTINENTS",
           font=f_count, fill=WHITE)

    # ---- heroes
    card_w, card_h, gap = 650, 540, 16
    hy = 244
    for i, (region, icon, headline, subline) in enumerate(HEROES):
        x = 32 + i * (card_w + gap)
        rounded_rect(d, [x, hy, x + card_w, hy + card_h], radius=18,
                     fill=WHITE, outline=NAVY, width=4)
        col = REGIONS[region]
        rounded_rect(d, [x + 16, hy + 16, x + card_w - 16, hy + 206],
                     radius=12, fill=tint(col, 0.86))
        icon(d, x + card_w // 2, hy + 111, 78, col)
        chip(d, x + 24, hy + 224, region, col, font(FONT_SANS_B, 30))
        hf, hlines = fit_text(d, headline, FONT_SANS_B, 62, card_w - 56, 2, 54)
        yy = hy + 296
        for ln in hlines:
            d.text((x + 28, yy), ln, font=hf, fill=NAVY)
            yy += int(hf.size * 1.16)
        sf, slines = fit_text(d, subline, FONT_SANS, 36, card_w - 56, 2, 32)
        yy += 6
        for ln in slines:
            d.text((x + 28, yy), ln, font=sf, fill=GREY)
            yy += int(sf.size * 1.25)

    # ---- mids: 3 columns x 4 rows
    cell_w, cell_h, cgap, rgap = 650, 150, 16, 8
    my = 800
    for i, (region, icon, headline) in enumerate(MIDS):
        col_i, row_i = i % 3, i // 3
        x = 32 + col_i * (cell_w + cgap)
        y = my + row_i * (cell_h + rgap)
        rounded_rect(d, [x, y, x + cell_w, y + cell_h], radius=12,
                     fill=WHITE, outline=BORDER, width=2)
        col = REGIONS[region]
        icon(d, x + 76, y + cell_h // 2 + 6, 46, col)
        # number badge
        bx, by, bd = x + 14, y + 10, 44
        d.ellipse([bx, by, bx + bd, by + bd], fill=NAVY)
        nf = font(FONT_SANS_B, 28)
        num = str(i + 1)
        d.text((bx + bd / 2 - text_w(d, num, nf) / 2, by + 6), num,
               font=nf, fill=WHITE)
        # region tick under the icon
        d.rectangle([x + 34, y + cell_h - 16, x + 118, y + cell_h - 10],
                    fill=col)
        hf, hlines = fit_text(d, headline, FONT_SANS_B, 44, cell_w - 176, 2,
                              40)
        block_h = len(hlines) * int(hf.size * 1.18)
        yy = y + (cell_h - block_h) // 2
        for ln in hlines:
            d.text((x + 152, yy), ln, font=hf, fill=NAVY)
            yy += int(hf.size * 1.18)

    # ---- briefs
    by = 1452
    label_w = letterspaced(d, 32, by, "ALSO TODAY", font(FONT_SANS_B, 34),
                           GOLD_DARK, spacing=8)
    lx = 32 + int(label_w) + 40
    d.line([lx, by + 20, W - 32, by + 20], fill=NAVY, width=3)
    row_h, top = 56, 1504
    for i, (lead, rest) in enumerate(BRIEFS):
        col_i, row_i = (0, i) if i < 8 else (1, i - 8)
        x = 32 + col_i * 1008
        y = top + row_i * row_h
        size = 34
        while size >= 30:
            bf = font(FONT_SANS_B, size)
            rf = font(FONT_SANS, size)
            w = text_w(d, lead + " " + rest, bf)  # upper bound, bold is wider
            w = text_w(d, lead, bf) + text_w(d, " " + rest, rf)
            if w <= 968:
                break
            size -= 1
        d.text((x, y), lead, font=bf, fill=NAVY)
        d.text((x + text_w(d, lead, bf), y), " " + rest, font=rf, fill=INK)

    # ---- footer
    d.rectangle([0, 1972, W, H], fill=NAVY)
    ff = font(FONT_SANS, 27)
    draw_centered(d, W // 2, 1984, FOOTER_L1, ff, WHITE)
    draw_centered(d, W // 2, 2016, FOOTER_L2, ff, (200, 205, 215))

    out1024 = img.resize((1024, 1024), Image.LANCZOS)
    # Flat vector art quantizes cleanly: palette PNG is ~3x smaller and
    # still byte-stable. This is the exact file main.py embeds.
    out1024 = out1024.convert("P", palette=Image.ADAPTIVE, colors=256)
    out1024.save(os.path.join(HERE, "entry-1024.png"))
    img.save(os.path.join(HERE, "entry-2048.png"))
    print("saved entry-1024.png and entry-2048.png")


if __name__ == "__main__":
    build()
