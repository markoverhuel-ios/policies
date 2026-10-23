# Framing screenshots for the Overview pages

`frame_screenshots.py` turns raw simulator PNGs into framed web cards: a simple phone frame (rounded bezel,
drawn dynamic island, no Apple art) on a Navy #0B2946 to Lake Blue #168BBD gradient, caption above,
900 px wide, PNG plus WebP, each under about 250 KB. Built with Python and Pillow (no browser needed).

## Setup (once)

    python -m pip install Pillow

## Where files go

- Raw captures: `tools\raw\<slug>\`, named `01_home.png`, `02_tower.png`, ... Order is by file name
  (numbers sort naturally). Use 4 to 6 per app. Slugs: frn-dashboard, grol-trainer, ham-trainer,
  spectrum-scout, tower-roster.
- Captions (optional): `tools\captions\<slug>.json`, a list of strings in the same order as the files.
  Plain words, max 2 lines, no dashes, no emojis, no prices. Missing file means no caption.
- Output: `assets\screenshots\<slug>\shot-01.png`, `shot-01.webp`, ..., and `manifest.json`
  (files, sizes, captions, source file). Output is rebuilt on every run, and old `shot-*` files are removed.
- Inputs are never modified.
- `tools\raw\*` is git-ignored (only `.gitkeep` is kept) so raw PNGs are not committed. Remove the
  ignore lines in `tools\.gitignore` if Mark wants them in the repo.

## Run on Windows PowerShell

    cd "X:\Fresh Coast RF\Apps\_shared\policies"
    python tools\frame_screenshots.py --slug spectrum-scout --in tools\raw\spectrum-scout
    python tools\frame_screenshots.py --slug tower-roster --in tools\raw\tower-roster
    python tools\frame_screenshots.py --slug frn-dashboard --in tools\raw\frn-dashboard --preframed

## Run on the Mac

    cd ~/path/to/Fresh\ Coast\ RF/Apps/_shared/policies
    python3 -m pip install Pillow
    python3 tools/frame_screenshots.py --slug ham-trainer --in tools/raw/ham-trainer

Caption font is Segoe UI Bold on Windows, Arial Bold or Helvetica on the Mac. Output differs slightly
between machines; pass `--font <file.ttf>` to force one font.

## Options

- `--captions file.json`: use another captions file.
- `--preframed`: input is already marketing art or a framed store image (no bezel, no caption, rounded corners only).
  Never frame an already framed image; use this instead. Needed for FRN Dashboard until real raw captures exist.
- `--placeholder [--count N]`: write "Screenshot coming" cards (used for ham-trainer and grol-trainer). A real run replaces them.
- `--budget-kb N`: size target per file (default 250). The script lowers PNG colors and WebP quality to fit.

## Notes

- Take raw captures from the simulator with no price, purchase or paywall text, and no personal data.
- Output is local files only, so the site CSP (`img-src 'self'`) is fine.
- Nothing here commits, pushes or deploys.
