# Dexeon — landing page

Marketing site for [Dexeon](https://github.com/breepear), a free Pokédex and Pokémon TCG collection tracker for iPhone, built by Bree Pear.

Single static page, no build step.

- `index.html` — the whole page (markup, CSS, and a few lines of JS)
- `assets/cards/` — card art from pokemontcg.io
- `assets/art/` — official Pokémon artwork from PokéAPI
- `assets/icon.png` — app icon

## Preview locally

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765.

## Before shipping

Replace the `href="#..."` placeholders marked `TODO-LINK` in `index.html` with the App Store URL.

---

Dexeon is a fan-made project and is not affiliated with Nintendo, Game Freak, Creatures Inc., or The Pokémon Company. Card data and pricing courtesy of pokemontcg.io and TCGplayer.

## App Store screenshots

`assets/appstore/` holds three 1242×2688 marketing screens (iPhone 6.5" size) and `assets/appstore/ipad-13/` holds the same three at 2064×2752 (iPad 13" size). They are generated from the landing page's own CSS and phone mockups:

```bash
python3 marketing/build.py
```

Edit the copy or sticker positions in `marketing/build.py` and re-run to regenerate.

The same script also renders the social share image `assets/og.png` (1200×630) used by the Open Graph and Twitter card tags in `index.html`. Favicons (`assets/favicon.png`, `assets/favicon-32.png`, `assets/apple-touch-icon.png`) are downscaled from the app icon.
