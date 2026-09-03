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
