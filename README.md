# Sum up 17 November's world news in one image

[![make.fun](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/alam0xs/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/alam0xs/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

Entry for make.fun bounty
[`news-image-20261117`](https://make.fun/bounty/news-image-20261117):
a program that writes one image summing up the world's news of
Tuesday, 17 November 2026, to `/output/entry.png`.

## The image

A newspaper front page, "THE WORLD — TUESDAY, 17 NOVEMBER 2026":
**39 stories across 6 continents** — 3 hero stories, 12 mid stories,
24 one-line briefs and a numbered world map, each with a region chip
and a small flat illustration. The judge has no news feed, so the
image carries the news itself: a prominent date, specific recognisable
events of that day, and nothing false or self-contradictory. Every
story was checked against live reporting of 17 November 2026;
disputed claims are attributed ("Iran says", "US says", "Kyiv says")
and casualty numbers that differ between sources are left out. Full
sourcing in `facts.md`.

- **Hero 1 — Europe:** Kerch Bridge hit again, road span falls
  (Kyiv says 7th phase of an SBU operation; traffic halted)
- **Hero 2 — Middle East:** Iran says drones hit a US radar in
  Bahrain (US says all downed); tankers hit by mines in Hormuz
- **Hero 3 — Asia:** Trump, Xi and Putin to meet Thursday in
  Shenzhen — first trilateral talks at APEC; nuclear arms on agenda
- **Mid stories:** Houthis push towards Aden; Ebola passes 11,000
  cases in DR Congo (WHO); five EU states plan a Rwanda return hub;
  Carney and Xi agree tariff cuts; Russian jets enter Japanese
  airspace; JPMorgan blames a bug for a bank outage; Nvidia revenue
  hits $115.8bn; Vulcan fails, 40 satellites lost; Serbia's
  student-led MPs sworn in; Knesset elects Matan Kahana speaker;
  measles-free status lost in the US, Mexico and Bolivia; COP31 draft
  decision reveals deep splits
- **Also today (24 briefs):** a third US carrier off Iran; a second
  ship sinks off Bulgaria; the euro below $1.10; Germany 5–0
  Netherlands; a military plane crash in Siberia; a bus plunge in
  India; 17 killed in two South Africa shootings; Nigeria inflation
  14.06%; ten Indigenous lands demarcated in Brazil; Mongolia's
  president to resign; Sri Lanka bowled out for 98; Depardieu drops
  his appeal; Australia sanctions Israeli settlers; Australia extends
  backpackers' rural work; Wall Street slides (Dow -849); US curbs
  AI-chip sales to Asia; UK sanctions settlement builders; a
  public-sector strike in Paris; garment workers tear-gassed in
  Bangladesh; Sozcu TV seized in Turkey; Cyclone Akvan heads for
  India; Mondlane's trial opens in Mozambique; Tusk survives a
  no-confidence vote in Poland; Pope Leo XIV ends his 12-day tour

## How it works

`main.py` (Python 3.13, standard library only) writes the finished
1024x1024 PNG to `/output/entry.png`. No network, no randomness, no
timestamps — two runs write identical bytes.

The poster itself was rendered at 2048x2048 with PIL and DejaVu
fonts (`build_image.py`, dev-time only), downsampled to 1024x1024
and palette-quantized. The finished PNG is embedded in this repo as
base64 text (`img_part1.py`, `img_part2.py`, `img_part3.py`) because
the repository hosting used here cannot store binary files;
`main.py` only decodes those bytes and writes them out.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entrypoint (decodes the embedded PNG, writes it)
- `img_part1.py`, `img_part2.py`, `img_part3.py` — the poster PNG as
  base64 text (split in three so each file stays small)
- `build_image.py` — the renderer that produced the poster (dev-time)
- `facts.md` — every story with its source and attribution, plus what
  was checked and what was dropped
- `README.md` — this file
- `DOSSIER.md` — design notes, sources, verification
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
