# saasisdead (GitHub catalog)

- Public catalog of open-source alternatives to paid SaaS, mirroring https://saasisdead.si. Repo: https://github.com/tonyzedginidze/saasisdead.
- `README.md` is the source of truth and is edited by hand through pull requests. There is no sync with the website in either direction.
- `scripts/seed-readme.py` made the first README from the website catalog on 2026-11-04. Don't rerun it: it would overwrite manual entries.
- Art: generated PNGs in `lfs/art/raw`, trimmed in `lfs/art/prep`, Recraft vectors in `lfs/art/svg`. `scripts/compose-art.py` (run with `uv run --with fonttools python scripts/compose-art.py`) builds `assets/art`, `assets/tiles` and `assets/buttons`, with text as outlines in the site's Archivo and Geist fonts (`lfs/fonts`).
- Product logos in `assets/logos` come from the website's `public/logos`; `-dark` copies are inverted for black logos.
- Entry rules are in `CONTRIBUTING.md` and match the website's editorial bar.
