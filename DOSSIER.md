# DOSSIER — news-image-20261117 (v2)

## What this entry is

One 1024x1024 PNG front page, "THE WORLD — TUESDAY, 17 NOVEMBER 2026",
summing up the day's world news: **30 stories across 6 continents**
(3 heroes, 12 mid stories, 15 briefs). The judge has no news feed,
so the image carries the news itself: a prominent date, specific
recognisable events of that day, breadth across regions and fields,
and clean craft legible at ~300 px wide.

This v2 replaces the v1 poster (9 stories, blocky 5x7 all-caps bitmap
font, wasted space, and one wrong claim — it said Depardieu "pleaded
guilty", which he did not; he dropped his appeal and accepted the
conviction). See `facts.md` for the full fact pass and the list of
stories dropped as unconfirmable or off-date.

## How the image is made

`build_image.py` (dev-time only) renders the poster with PIL 10.2.0
and real fonts (DejaVu Sans Bold for headlines, DejaVu Serif Bold for
the masthead and date) at 2048x2048, downsamples to 1024x1024 with
LANCZOS, and quantizes to a 256-colour palette PNG (flat vector art
quantizes cleanly — no visible difference from the RGB render).
Layout: cream `#F7F1E3`, navy `#10213F`, gold `#D4A838`; region chips
(N. America red, S. America orange, Europe blue, Middle East purple,
Africa brown, Asia green, Oceania teal); mixed-case headlines; one
simple original flat icon per story; no real faces, no brand logos.
Two render revisions: v1 of this design clipped the masthead label
and the date ran into the story-count block, and six mid headlines
wrapped to three lines; v2 fixed the letter-spacing, shrank the date
to fit, and shortened those six headlines to two lines.

`main.py` is standard library only. It does not draw the poster at
run time: the finished PNG is embedded in the repo as base64 text
(`img_part1.py`, `img_part2.py`, `img_part3.py`) because the
repository hosting used here cannot store binary files, and `main.py`
decodes those bytes and writes them to `$MAKEFUN_OUTPUT_DIR` (or
`/output/entry.png`). Each part stores its base64 as a single line:
the PNG is data, not code, so wrapping it over thousands of lines
would misrepresent the file. No network, no randomness, no timestamps.

## Facts

Every story was checked against live reporting of 17 November 2026
(AP, Reuters, AFP, BBC, Al Jazeera, WHO, CENTCOM, NBS, ICC and others
— see `facts.md` for the per-story source). Headline claims:

- Kerch Bridge: second strike overnight 16–17 Nov; road span fell,
  traffic halted; Kyiv says 7th phase of an SBU operation.
- Iran/Gulf: IRGC drones at a US radar in Bahrain (US says all
  downed); tankers hit by mines in Hormuz (Iran says); Tara Gas
  attacked twice, crew abandoned ship.
- Trump, Xi, Putin to meet Thursday 19 Nov in Shenzhen, APEC
  sidelines; first trilateral; nuclear arms on the agenda.
- Houthis advance on Aden; Ebola passes 11,000 cases in DR Congo
  (WHO, cases only — death counts differ); five EU states plan a
  Rwanda return hub from 2027; Carney–Xi tariff cuts; Russian jets
  in Japanese airspace; JPMorgan software bug (not a cyberattack);
  Nvidia beats forecasts after Huang's exit; Vulcan fails, 40 Amazon
  Leo satellites lost; AI sell-off, S&P -1.9% / Nasdaq -2.5%
  (Monday closes, reported Tuesday); US AI-chip export curbs; UK
  sanctions eight settlement builders; Trump warns Iran over a
  reported "dirty bomb" plot (Iran calls it baseless).
- Briefs: USS Theodore Roosevelt becomes the third US carrier off
  Iran; Gas Husky sinks off Bulgaria (second ship in two days);
  euro below $1.10 (weakest since April 2025); Germany 5–0
  Netherlands (Nations League); An-12 crash in Siberia, all aboard
  killed (death toll disputed — no number printed); bus plunges
  100 m in Uttarakhand (death toll rose through the day — no number
  printed); 17 killed in two South Africa shootings; Nigeria
  inflation 14.06% (six-year low); Brazil demarcates ten Indigenous
  lands at COP30; Mongolia's president says he will resign over
  graft claims; Sri Lanka bowled out for 98 in Rawalpindi; inquiry
  calls over Netanyahu election arrests; Depardieu drops his appeal,
  conviction stands; Trump lands in Manila for ASEAN and Quad talks;
  Australia sanctions Israeli settlers.

Dropped vs the brief: the Gaza crossings appeal (statement dated
15 Nov, not 17 Nov); Geneva "killer robots" talks (opened 16 Nov,
no decision yet); Crystal Palace appointing Thomas Frank, the UK
2-year gilt above 5%, and the US–China tariff truce extension
(all dropped for space — weaker date or already covered).

## Verification

- Output: valid PNG, 1024x1024, palette mode, 175,077 bytes
  (< 1 MiB).
- `main.py` run twice from a different working directory into two
  different output directories: outputs byte-identical, sha256
  `965067943d1164b2e4a85c22b49bffd9ced616ad3c57679f6f1da3a66cd5f2be`,
  matching the rendered `entry-1024.png` exactly.
- The final 1024 image was read visually, and a 300 px copy too:
  masthead, date and the 3 hero headlines are readable at 300 px;
  no overlap, no clipped words, no typos found.
- `main.py` imports only `base64`, `os`, `sys` (stdlib) plus the
  three sibling data modules; no network, no randomness, no
  timestamps, no file reads besides the program itself.
