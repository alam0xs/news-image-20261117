# Entry for make.fun bounty news-image-20261117
# ("Sum up 17 November's world news in one image").
#
# Python 3.13, STANDARD LIBRARY ONLY. Nothing is installed before the
# program runs and it has no network, so the poster is drawn here by
# this program itself: a pixel buffer, a small built-in 5x7 bitmap font,
# and a pure-stdlib PNG encoder (zlib). The program writes the finished
# front page to /output/entry.png. No randomness, no timestamps: both
# runs write the same bytes.
#
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import binascii
import os
import struct
import zlib

W, H = 1024, 1024
PAPER = (248, 244, 236)
INK = (26, 26, 26)
NAVY = (22, 50, 79)
RED = (176, 42, 32)
GREY = (90, 90, 90)
LIGHT_BLUE = (178, 205, 224)
SEA = (70, 110, 145)
WHITE = (255, 255, 255)
GOLD = (255, 200, 60)


# ---------------------------------------------------------------- pixels
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bytes(bg) * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def fill_rect(self, x0, y0, x1, y1, c):
        x0 = max(0, x0); y0 = max(0, y0)
        x1 = min(self.w, x1); y1 = min(self.h, y1)
        if x1 <= x0 or y1 <= y0:
            return
        row = bytes(c) * (x1 - x0)
        for y in range(y0, y1):
            i = (y * self.w + x0) * 3
            self.px[i:i + len(row)] = row

    def rect_outline(self, x0, y0, x1, y1, c, wdt=1):
        self.fill_rect(x0, y0, x1, y0 + wdt, c)
        self.fill_rect(x0, y1 - wdt, x1, y1, c)
        self.fill_rect(x0, y0, x0 + wdt, y1, c)
        self.fill_rect(x1 - wdt, y0, x1, y1, c)

    def line(self, x0, y0, x1, y1, c, wdt=1):
        dx = abs(x1 - x0); dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        x, y = x0, y0
        r = wdt // 2
        while True:
            self.filled_circle(x, y, r, c) if wdt > 1 else self.set(x, y, c)
            if x == x1 and y == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x += sx
            if e2 <= dx:
                err += dx; y += sy

    def filled_circle(self, cx, cy, r, c):
        if r <= 0:
            self.set(cx, cy, c)
            return
        for dy in range(-r, r + 1):
            dx = int((r * r - dy * dy) ** 0.5)
            self.fill_rect(cx - dx, cy + dy, cx + dx + 1, cy + dy + 1, c)

    def circle_outline(self, cx, cy, r, c, wdt=2):
        import math
        steps = max(24, r * 6)
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.filled_circle(cx + int(r * math.cos(a)),
                               cy + int(r * math.sin(a)), wdt // 2, c)

    def ellipse_outline(self, cx, cy, rx, ry, c, wdt=2):
        import math
        steps = max(24, rx * 6)
        for i in range(steps):
            a = 2 * math.pi * i / steps
            self.filled_circle(cx + int(rx * math.cos(a)),
                               cy + int(ry * math.sin(a)), wdt // 2, c)

    def fill_triangle(self, p1, p2, p3, c):
        pts = sorted([p1, p2, p3], key=lambda p: p[1])
        (x1, y1), (x2, y2), (x3, y3) = pts
        if y1 == y3:
            return
        def edge_xa(xa, ya, xb, yb, y):
            return xa + (xb - xa) * (y - ya) / (yb - ya) if yb != ya else xa
        for y in range(y1, y3 + 1):
            if y < y2:
                xa = edge_xa(x1, y1, x2, y2, y)
                xb = edge_xa(x1, y1, x3, y3, y)
            else:
                xa = edge_xa(x2, y2, x3, y3, y)
                xb = edge_xa(x1, y1, x3, y3, y)
            if xa > xb:
                xa, xb = xb, xa
            self.fill_rect(int(xa), y, int(xb) + 1, y + 1, c)

    def rounded_rect(self, x0, y0, x1, y1, r, c):
        self.fill_rect(x0 + r, y0, x1 - r, y1, c)
        self.fill_rect(x0, y0 + r, x1, y1 - r, c)
        for (cx, cy) in ((x0 + r, y0 + r), (x1 - r, y0 + r),
                         (x0 + r, y1 - r), (x1 - r, y1 - r)):
            self.filled_circle(cx, cy, r, c)

    def to_png_bytes(self):
        raw = bytearray()
        stride = self.w * 3
        for y in range(self.h):
            raw.append(0)
            raw += self.px[y * stride:(y + 1) * stride]
        def chunk(tag, data):
            out = struct.pack(">I", len(data)) + tag + data
            out += struct.pack(">I", binascii.crc32(tag + data) & 0xFFFFFFFF)
            return out
        ihdr = struct.pack(">IIBBBBB", self.w, self.h, 8, 2, 0, 0, 0)
        return (b"\x89PNG\r\n\x1a\n"
                + chunk(b"IHDR", ihdr)
                + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
                + chunk(b"IEND", b""))


# ---------------------------------------------------------------- font
# 5x7 bitmap font, '#' = on. Hand-drawn; verified by rendering a test
# sheet (see repo history). All poster copy is uppercase, so only
# A-Z, 0-9 and a few punctuation marks are needed.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00110", "01000", "10000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "00110", "00110"),
    ",": ("00000", "00000", "00000", "00000", "00110", "00100", "01000"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    ":": ("00000", "00110", "00110", "00000", "00110", "00110", "00000"),
}


def text_width(text, scale):
    return len(text) * 6 * scale


def draw_text(cv, x, y, text, scale, color):
    for ch in text:
        glyph = FONT.get(ch)
        if glyph is None:
            raise ValueError("no glyph for %r" % ch)
        for row in range(7):
            bits = glyph[row]
            for col in range(5):
                if bits[col] == "1":
                    cv.fill_rect(x + col * scale, y + row * scale,
                                 x + (col + 1) * scale, y + (row + 1) * scale,
                                 color)
        x += 6 * scale
    return x


def draw_text_centered(cv, cx, y, text, scale, color):
    draw_text(cv, cx - text_width(text, scale) // 2, y, text, scale, color)


def wrap_text(text, scale, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_width(t, scale) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_para(cv, x, y, text, scale, max_w, color, leading=None):
    lh = leading or int(7 * scale * 1.35)
    for ln in wrap_text(text, scale, max_w):
        draw_text(cv, x, y, ln, scale, color)
        y += lh
    return y


# ---------------------------------------------------------------- icons
def icon_globe(cv, x, y, s, bg):
    cv.rounded_rect(x, y, x + s, y + s, 10, bg)
    cx, cy = x + s // 2, y + s // 2
    r = s // 2 - 10
    cv.circle_outline(cx, cy, r, WHITE, 3)
    cv.ellipse_outline(cx, cy, r // 2, r, WHITE, 2)
    cv.line(cx - r, cy, cx + r, cy, WHITE, 2)


def icon_tanker(cv, x, y, s, bg):
    cv.rounded_rect(x, y, x + s, y + s, 10, bg)
    u = s / 84.0
    # hull
    cv.fill_rect(x + int(12 * u), y + s - int(36 * u), x + s - int(12 * u),
                 y + s - int(18 * u), WHITE)
    cv.fill_triangle((x + s - int(12 * u), y + s - int(36 * u)),
                     (x + s - int(12 * u), y + s - int(18 * u)),
                     (x + s - int(2 * u), y + s - int(27 * u)), WHITE)
    # containers
    cv.fill_rect(x + int(20 * u), y + int(20 * u), x + int(36 * u),
                 y + s - int(36 * u), WHITE)
    cv.fill_rect(x + int(42 * u), y + int(28 * u), x + int(64 * u),
                 y + s - int(36 * u), WHITE)
    # waves
    cv.fill_rect(x + 8, y + s - 12, x + s - 8, y + s - 10, WHITE)
    cv.fill_rect(x + 8, y + s - 6, x + s - 8, y + s - 4, WHITE)


def icon_bank(cv, x, y, s, bg):
    cv.rounded_rect(x, y, x + s, y + s, 10, bg)
    u = s / 64.0
    cv.fill_triangle((x + s // 2, y + int(12 * u)),
                     (x + int(12 * u), y + int(30 * u)),
                     (x + s - int(12 * u), y + int(30 * u)), WHITE)
    for i in range(4):
        cx = x + int((16 + i * 12) * u)
        cv.fill_rect(cx, y + int(36 * u), cx + int(6 * u), y + s - int(16 * u),
                     WHITE)
    cv.fill_rect(x + int(12 * u), y + s - int(14 * u), x + s - int(12 * u),
                 y + s - int(8 * u), WHITE)


def icon_chip(cv, x, y, s, bg):
    cv.rounded_rect(x, y, x + s, y + s, 10, bg)
    m = int(s * 0.30)
    cv.rect_outline(x + m, y + m, x + s - m, y + s - m, WHITE, 3)
    c = int(s * 0.42)
    cv.fill_rect(x + c, y + c, x + s - c, y + s - c, WHITE)
    for i in range(3):
        px = x + int(s * (0.32 + i * 0.18))
        cv.fill_rect(px - 1, y + int(s * 0.08), px + 2, y + m, WHITE)
        cv.fill_rect(px - 1, y + s - m, px + 2, y + int(s * 0.92), WHITE)
        py = y + int(s * (0.32 + i * 0.18))
        cv.fill_rect(x + int(s * 0.08), py - 1, x + m, py + 2, WHITE)
        cv.fill_rect(x + s - m, py - 1, x + int(s * 0.92), py + 2, WHITE)


def icon_rocket(cv, x, y, s, bg):
    cv.rounded_rect(x, y, x + s, y + s, 10, bg)
    cx = x + s // 2
    u = s / 64.0
    cv.fill_triangle((cx, y + int(10 * u)),
                     (cx + int(12 * u), y + int(34 * u)),
                     (cx - int(12 * u), y + int(34 * u)), WHITE)
    cv.fill_rect(cx - int(12 * u), y + int(34 * u), cx + int(12 * u),
                 y + s - int(26 * u), WHITE)
    cv.fill_triangle((cx - int(12 * u), y + s - int(30 * u)),
                     (cx - int(22 * u), y + s - int(14 * u)),
                     (cx - int(12 * u), y + s - int(20 * u)), WHITE)
    cv.fill_triangle((cx + int(12 * u), y + s - int(30 * u)),
                     (cx + int(22 * u), y + s - int(14 * u)),
                     (cx + int(12 * u), y + s - int(20 * u)), WHITE)
    cv.fill_triangle((cx - int(6 * u), y + s - int(26 * u)),
                     (cx + int(6 * u), y + s - int(26 * u)),
                     (cx, y + s - int(8 * u)), GOLD)


def draw_bridge(cv, x0, y0, x1, y1):
    cv.fill_rect(x0, y0, x1, y1, LIGHT_BLUE)
    cv.fill_rect(x0, y1 - 52, x1, y1, SEA)
    for wx in range(x0 + 8, x1 - 10, 26):
        cv.fill_rect(wx, y1 - 38, wx + 20, y1 - 36, (220, 235, 245))
    for tx in (x0 + 52, x1 - 76):
        cv.fill_rect(tx, y0 + 42, tx + 22, y1 - 52, INK)
    deck_y = y0 + 96
    cv.fill_rect(x0 + 10, deck_y, x0 + 150, deck_y + 10, INK)
    cv.fill_rect(x1 - 160, deck_y, x1 - 10, deck_y + 10, INK)
    # collapsed middle span, tilted down into the water
    cv.fill_triangle((x0 + 150, deck_y), (x0 + 196, deck_y + 2),
                     (x0 + 186, deck_y + 46), (120, 40, 30))
    cv.fill_triangle((x0 + 150, deck_y), (x0 + 186, deck_y + 46),
                     (x0 + 158, deck_y + 40), (120, 40, 30))
    for cx in range(x0 + 30, x0 + 150, 24):
        cv.line(cx, deck_y, x0 + 63, y0 + 42, INK, 1)
    for cx in range(x1 - 140, x1 - 20, 24):
        cv.line(cx, deck_y, x1 - 65, y0 + 42, INK, 1)
    for (sx, sy, r) in ((x0 + 172, y0 + 62, 14), (x0 + 188, y0 + 48, 18),
                        (x0 + 206, y0 + 66, 12)):
        cv.filled_circle(sx, sy, r, (235, 235, 235))
        cv.circle_outline(sx, sy, r, GREY, 1)


# ---------------------------------------------------------------- layout
def build():
    cv = Canvas(W, H, PAPER)
    cv.rect_outline(10, 10, W - 10, H - 10, INK, 3)

    # masthead
    cv.fill_rect(24, 24, W - 24, 128, NAVY)
    draw_text_centered(cv, W // 2, 34, "THE WORLD", 12, WHITE)
    # date bar
    cv.fill_rect(24, 128, W - 24, 182, RED)
    draw_text_centered(cv, W // 2, 137, "TUESDAY, 17 NOVEMBER 2026", 5, WHITE)

    # lead story
    draw_text(cv, 28, 198, "LEAD STORY - UKRAINE - RUSSIA", 3, RED)
    draw_bridge(cv, 28, 228, 420, 452)
    draw_text(cv, 448, 228, "KERCH BRIDGE", 6, INK)
    draw_text(cv, 448, 280, "SPAN COLLAPSES", 6, INK)
    draw_para(cv, 448, 344,
              "UKRAINE STRUCK THE BRIDGE LINKING RUSSIA TO OCCUPIED CRIMEA "
              "FOR A SECOND STRAIGHT DAY, AND A ROAD SPAN FELL INTO THE "
              "STRAIT BELOW. KYIV CALLED IT AN UNPRECEDENTED OPERATION. THE "
              "KREMLIN VOWED TO REBUILD.", 2, 548, INK)
    cv.fill_rect(28, 472, W - 28, 474, INK)

    # row 2
    y = 492
    icon_globe(cv, 28, y, 84, NAVY)
    draw_text(cv, 128, y - 2, "TRUMP LANDS IN MANILA", 3, INK)
    draw_para(cv, 128, y + 36,
              "THE PRESIDENT ARRIVED FOR THE ASEAN SUMMIT AND SIGNED A "
              "TRADE STATEMENT WITH THAILAND. HIS ASIA TRIP ENDS IN CHINA, "
              "WITH TALKS ALONGSIDE XI JINPING AND VLADIMIR PUTIN.",
              2, 360, INK)
    icon_tanker(cv, 528, y, 84, (120, 40, 30))
    draw_text(cv, 628, y - 2, "TANKERS HIT BY MINES", 3, INK)
    draw_para(cv, 628, y + 36,
              "IRAN'S REVOLUTIONARY GUARDS SAY TWO OIL TANKERS STRUCK MINES "
              "IN THE STRAIT OF HORMUZ. IRAN ALSO FIRED DRONES AT A U.S. "
              "RADAR BASE IN BAHRAIN.", 2, 360, INK)
    cv.fill_rect(28, 686, W - 28, 688, INK)

    # row 3
    y = 706
    cols = [
        (28, icon_bank, NAVY, "BANK BLAMES A BUG",
         "JPMORGAN CHASE SAID A SOFTWARE BUG - NOT A CYBERATTACK - SLOWED "
         "ONLINE BANKING, BRANCHES AND ZELLE PAYMENTS ON MONDAY."),
        (362, icon_chip, (60, 90, 60), "NVIDIA REPORTS",
         "THE CHIPMAKER REPORTS EARNINGS - ITS FIRST SINCE JENSEN HUANG "
         "RESIGNED AS CHIEF EXECUTIVE."),
        (696, icon_rocket, (90, 60, 110), "ROCKET FAILS",
         "A ULA VULCAN ROCKET FAILED IN FLIGHT, DESTROYING 40 AMAZON LEO "
         "INTERNET SATELLITES."),
    ]
    for (cx, icon, bg, head, body) in cols:
        icon(cv, cx, y, 56, bg)
        draw_para(cv, cx + 66, y + 2, head, 3, 224, INK)
        draw_para(cv, cx, y + 66, body, 2, 300, INK)
    cv.fill_rect(28, 890, W - 28, 892, INK)

    # also today
    draw_text(cv, 28, 904, "ALSO TODAY", 3, RED)
    draw_para(cv, 28, 930,
              "JAPAN SCRAMBLED FIGHTER JETS AFTER SUSPECTED RUSSIAN AIRCRAFT "
              "ENTERED ITS AIRSPACE - BRITAIN SANCTIONED EIGHT ISRAELI "
              "SETTLEMENT FIRMS - GERARD DEPARDIEU PLEADED GUILTY TO SEXUAL "
              "ASSAULT", 2, 968, INK)
    draw_text_centered(cv, W // 2, 990,
                       "EVENTS REPORTED ON 17 NOVEMBER 2026", 2, GREY)
    return cv


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = build().to_png_bytes()
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
