# Sum up 17 November's world news in one image

Entry for make.fun bounty
[`news-image-20261117`](https://make.fun/bounty/news-image-20261117):
a program that writes one image summing up the world's news of
Tuesday, 17 November 2026, to `/output/entry.png`.

## The image

A newspaper front page, drawn by `main.py` itself in pure Python
standard library — a pixel buffer, a small built-in 5x7 bitmap font,
and a hand-rolled PNG encoder. No image file is shipped and no
library is needed at run time, so the program runs in the grader's
bare stdlib container and both runs write the same bytes.

- **Masthead + date:** THE WORLD — TUESDAY, 17 NOVEMBER 2026
- **Lead story:** Ukraine strikes the Kerch Bridge to Crimea; a road
  span collapses (second straight day of bridge strikes)
- **Trump lands in Manila** for the ASEAN summit; trade statement with
  Thailand; Asia trip ends in China with Xi Jinping and Vladimir Putin
- **Tankers hit by mines in the Strait of Hormuz**; Iran fires drones
  at a U.S. radar base in Bahrain
- **JPMorgan Chase blames a software bug** (not a cyberattack) for
  Monday's banking outage
- **Nvidia reports earnings**, its first since Jensen Huang resigned
- **ULA Vulcan rocket fails**, destroying 40 Amazon Leo satellites
- **Also today:** Japan scrambles jets over Russian airspace
  violations; Britain sanctions eight Israeli settlement firms;
  Gerard Depardieu pleads guilty to sexual assault

## How it works

`main.py` (Python 3.13, standard library only) draws the front page
and writes it to `/output/entry.png`. No network, no randomness, no
timestamps.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Files

- `main.py` — the entrypoint (draws the image, writes the PNG)
- `README.md` — this file
- `DOSSIER.md` — design notes, sources, verification
- `LICENSE` — MIT

## License

MIT — see `LICENSE`.
