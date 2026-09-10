# GoldMeet public website (GitHub Pages)

Live site: **https://goldguideapp.com**

This public repository exists only so GitHub Pages can serve the apex domain. **Do not develop here.**

Canonical source: [mjk93447-cpu/Goldmeet](https://github.com/mjk93447-cpu/Goldmeet) → `site/`

Publish from that repo: `powershell -File scripts/publish-site.ps1`

Gold rates: `daily-gold-rates` writes IBJA 999/916/750 board rates into `rates.json` at 08:00 and 20:00 IST. GoldAPI spot is fallback only (plus 15% import duty). Source: Goldmeet `scripts/fetch-gold-rates.py`.
