# DOSSIER — news-image-20261117

## What this entry is

One 1024x1024 PNG front page, "THE WORLD — TUESDAY, 17 NOVEMBER 2026",
summing up the day's world news. The judge has no news feed, so the
image carries the news itself: a prominent date, six headline stories
with one-line summaries, and an "Also today" strip — across regions
(Europe, Asia, Middle East, US) and fields (war, diplomacy, banking,
tech, space, law).

## How the image is made

`main.py` draws it with Python's standard library only: a pixel
buffer, a hand-typed 5x7 bitmap font (verified by rendering a glyph
test sheet — every letter, digit and punctuation mark reads cleanly),
and a pure-stdlib PNG encoder (zlib + CRC32). No image file is
shipped, no library is installed, no network is used. The poster is
all-uppercase by design, matching the bitmap font.

Why not ship a PNG: the entry must run in a bare stdlib container,
and the image is drawn at run time instead, which keeps the entry
fully deterministic and self-contained.

Revisions: the layout went through four rendered revisions. v1 (PIL
draft) had three headlines clipped at the frame edge; v2 fixed the
layout; v3 was the first stdlib-drawn render and was fully legible
except the footer, which was clipped by the frame; v4 moved the
footer inside the frame. The final PNG was read and checked visually:
all text fits, nothing is cut off, layout is clean.

## Facts

Every story was checked against live reporting of 17 November 2026
(BBC, Reuters, AP, Al Jazeera, Just Security daily briefs):

- Kerch Bridge: Ukrainian strike, road span collapsed, second
  consecutive day; Zelenskyy called it "an unprecedented operation".
- Trump in Manila for the ASEAN summit; joint trade statement with
  Thailand; three-day Asia trip ending in China with Xi and Putin.
- Two tankers struck mines in the Strait of Hormuz (IRGC claim);
  Iran fired drones at a U.S. radar system at Sheikh Isa base, Bahrain.
- JPMorgan: software bug slowed online banking, branches and Zelle;
  no indication of cyberattack.
- Nvidia earnings: first since Jensen Huang's resignation.
- ULA Vulcan anomaly ~10 minutes into flight; 40 Amazon Leo
  satellites lost.
- Japan scrambled jets after two suspected Russian aircraft entered
  its airspace.
- UK sanctions on eight Israeli settlement construction firms.
- Gerard Depardieu pleaded guilty to a sexual assault charge.

## Verification

- Output: valid PNG, 1024x1024, RGB, 21,772 bytes (< 1 MiB).
- `main.py` run twice into different output directories: outputs
  byte-identical (`cmp` clean).
- `main.py` imports only `os`, `struct`, `zlib`, `binascii` (stdlib)
  plus `math` inside two small helpers; no network, no randomness,
  no timestamps, no file reads besides the program itself.
