# DOSSIER — news-image-20261117 (v3, Palette A)

## What this entry is

One 1024x1024 PNG front page, "THE WORLD — TUESDAY, 17 NOVEMBER 2026",
summing up the day's world news: **39 stories across 6 continents**
(3 heroes, 12 mid stories, 24 briefs) plus a numbered world map.
The judge has no news feed, so the image carries the news itself: a
prominent date, specific recognisable events of that day, breadth
across regions and fields, and clean craft legible at ~300 px wide.

This v3 replaces the v2 poster (30 stories, no map). It adds nine
stories, a hand-drawn world map with numbered dots for stories 1–15
and small dots for the briefs, full drawn scenes in the three hero
cards, and a corrected Wall Street brief: v2 used Monday's closes
(S&P -1.9%, Nasdaq -2.5%) as reported on Tuesday; v3 uses Tuesday's
own session (Dow -849, S&P -1.0%). See `facts.md` for the full fact
pass, the stories dropped as unconfirmable or off-date, and the
number conflicts that were resolved.

## How the image is made

`build_image.py` (dev-time only) renders the poster with PIL 10.2.0
and real fonts at 2048x2048, downsamples to 1024x1024 with LANCZOS,
and quantizes to a 256-colour palette PNG (flat vector art quantizes
cleanly — no visible difference from the RGB render). Layout: cream
`#F7F1E3`, navy `#10213F`, gold `#D4A838` (Palette A — all colours live
in a `PALETTE` dict so a later palette can be swapped in); region
colours (Europe blue, Middle East orange, Asia red, Africa green,
Americas purple, Oceania teal, Global grey) with darker chip variants
so white text on the chips clears 4.5:1 contrast; mixed-case
headlines; one simple original flat icon per story; no real faces, no
brand logos.

Two details worth recording. First, the date font: the brief asked
for DejaVu Serif Bold at >= 66 px on one line, but that font measures
1153 px at 66 px — it cannot fit inside 1024 minus margins. The date
therefore uses Liberation Serif Bold (a real serif on this machine,
943 px at 66 px), set at 68 px; hero headlines keep DejaVu Serif
Bold. Second, the masthead is 120 px tall, not 104: a 66+ px date
plus the required 24 px clear space below the top row does not fit in
104 px, so the masthead grew and the heroes start at y128.

Three render revisions: the first build failed its own asserts twice
(a mid subline and a mid headline wrapped past their line limits and
were reworded); the first visual pass found the hero chips hiding the
CRIMEA label and sitting on the summit banner, so the chips moved to
the top-left inside the art; the second pass deepened the map tints,
added drones to the Gulf scene, and redrew the gavel icon with
rotated heads.

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
(AP, Reuters, AFP, BBC, Al Jazeera, WHO, CENTCOM, NBS, ICC, PAHO,
IMD and others — see `facts.md` for the per-story source). Headline
claims:

- Kerch Bridge: second strike overnight 16–17 Nov; road span fell,
  traffic halted; Kyiv says 7th phase of an SBU operation.
- Iran/Gulf: IRGC drones at a US radar in Bahrain (Bahrain says all
  downed); US strikes Qeshm Island (Iran confirms); tankers hit by
  mines in Hormuz (Iran says); Tara Gas attacked twice, crew
  abandoned ship.
- Trump, Xi, Putin to meet Thursday 19 Nov in Shenzhen, APEC
  sidelines; first trilateral; nuclear arms on the agenda. Trump
  landed in Manila Tuesday 17 Nov for the ASEAN summit and Quad talks.
- Houthis advance on Aden; Ebola passes 11,000 cases in DR Congo
  (WHO, cases only — death counts differ); five EU states plan a
  Rwanda return hub from 2027; Carney–Xi tariff cuts; Russian jets
  in Japanese airspace; JPMorgan software bug (not a cyberattack);
  Nvidia revenue $115.8bn, beating ~$109bn forecasts; Vulcan fails,
  40 Amazon Leo satellites lost; Serbia's student-led MPs sworn in,
  ending 14 years of Vucic rule; Knesset elects Matan Kahana speaker
  66–52; the US, Mexico and Bolivia lose measles elimination status
  (PAHO); COP31 publishes its first draft decision in Antalya.
- Briefs: USS Theodore Roosevelt becomes the third US carrier off
  Iran; Gas Husky sinks off Bulgaria (second ship in two days);
  euro below $1.10 (19-month low); Germany 5–0 Netherlands (Nations
  League); An-12 crash in Siberia, all aboard killed (death toll
  disputed — no number printed); bus plunges 100 m in Uttarakhand
  (death toll rose through the day — no number printed); 17 killed in
  two South Africa shootings; Nigeria inflation 14.06% (six-year
  low); Brazil demarcates ten Indigenous lands at COP30; Mongolia's
  president says he will resign over graft claims; Sri Lanka bowled
  out for 98 in Rawalpindi; Depardieu drops his appeal, conviction
  stands; Australia sanctions Israeli settlers and extends
  backpackers' rural work to four months; Wall Street slides on
  Tuesday's own session (Dow -849, S&P -1.0%); US AI-chip export
  curbs; UK sanctions West Bank settlement builders; French
  public-sector strike; Bangladesh garment workers tear-gassed;
  Turkey seizes Sozcu TV; Cyclone Akvan heads for India; Mondlane's
  trial opens in Maputo; Tusk survives a no-confidence vote in
  Poland, 242–200; Pope Leo XIV ends his 12-day tour in Rome.

Dropped vs the brief: the Gaza crossings appeal (statement dated
15 Nov, not 17 Nov); Geneva "killer robots" talks (opened 16 Nov,
no decision yet); the US–China tariff truce extension (instruments
9–10 Nov); Voyager 1's one-light-day crossing (it happens Wed 18
Nov, not 17 Nov in any time zone); Crystal Palace appointing Thomas
Frank (announced Mon 16 Nov); PNG/Australia visa (no dated 17 Nov
news event found); and, for space, Netanyahu inquiry calls, Syria
returns, Moldova airspace, Prague trains, the Moscow drone attack,
Oman–Iran talks, Pakistan mediation, Brazil 7–0 Singapore, Canada
4–1 Guatemala, the Guinea gold crackdown, twin quasars, the UK gilt
yield, and Trump's "dirty bomb" warning (folded into the Gulf hero).

## Verification

- Output: valid PNG, 1024x1024, palette mode, 202,670 bytes
  (< 1 MiB).
- `main.py` run twice from a different working directory into two
  different output directories: outputs byte-identical, sha256
  `cb5096c0a7197f165b1924fa309776ea8285020e1d78db26a40d7133b83cd26e`,
  matching the rendered `entry-1024.png` exactly.
- Build asserts all passed: 39 stories (masthead count matches);
  date 68 px on one line with >= 24 px clear of the top row; hero
  headlines <= 2 lines at >= 26 px, sublines <= 2 lines at >= 13.5 px;
  mid headlines <= 3 lines at >= 17 px, sublines <= 2 lines at >= 12 px;
  every brief fits one line at 13.5 px; no map dots touch or overlap.
- The final 1024 image was read visually (top 120 px, four quadrants
  at 100%, and a 300 px copy): masthead, date and the 3 hero
  headlines are readable at 300 px; no overlap, no clipped words, no
  typos found. Two design revisions were made after the visual pass
  (chip position, map tints, Gulf drones, gavel icon).
- `main.py` imports only `base64`, `os`, `sys` (stdlib) plus the
  three sibling data modules; no network, no randomness, no
  timestamps, no file reads besides the program itself.
