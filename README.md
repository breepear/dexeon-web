# Dexeon — landing page

Marketing site for [Dexeon](https://github.com/breepear), a free Pokédex and Pokémon TCG collection tracker for iPhone, built by Bree Pear.

Single static page, no build step.

- `index.html` — the whole page (markup, CSS, and a few lines of JS)
- `assets/cards/` — English card art (JPG)
- `assets/cards/ja/` — Japanese card art from TCGdex
- `assets/art/` — official Pokémon artwork from PokéAPI
- `assets/icon.png` — app icon

## Preview locally

```bash
python3 -m http.server 8765
```

Then open http://localhost:8765.

## Beta signup form

The form at the bottom of the page stores the visitor's email in Firestore (project `dexeontcg`, collection `beta_signups`) and then redirects to the TestFlight invite (`https://testflight.apple.com/join/awvMwjC7`). If Firestore is unreachable or refuses the write, the visitor is still redirected.

The Firebase web API key in `index.html` is a public identifier by design; access is controlled by the Firestore security rules, which live in the Dexeon app repo (`firestore.rules`). Those rules allow the public site to *create* well-formed `beta_signups` documents only. Nothing client-side can read, list, edit, or delete them.

To read the list later, open the Firebase console → Firestore → `beta_signups`, or export it with the Firebase CLI.

## Before shipping

- Deploy the Firestore rules from the Dexeon app repo (`npx firebase-tools deploy --only firestore:rules`), otherwise signups are refused and only the redirect happens.
- The site is deployed on Vercel at https://dexeontcg.com; `vercel.json` rewrites `/b/:id` to the shared-binder function in `api/b.js`.

---

Dexeon is a fan-made project and is not affiliated with Nintendo, Game Freak, Creatures Inc., or The Pokémon Company. Card data, images and pricing courtesy of Scrydex and TCGplayer.

## App Store screenshots

`assets/appstore/` holds five 1242×2688 marketing screens (iPhone 6.5" size: Full Dex, cards & prices, binders, social/leaderboard, messages) and `assets/appstore/ipad-13/` holds the same five at 2064×2752 (iPad 13" size). They are generated from the landing page's own CSS and phone mockups:

```bash
python3 marketing/build.py
```

Edit the copy or sticker positions in `marketing/build.py` and re-run to regenerate.

The same script also renders the social share image `assets/og.png` (1200×630) used by the Open Graph and Twitter card tags in `index.html`. Favicons (`assets/favicon.png`, `assets/favicon-32.png`, `assets/apple-touch-icon.png`) are downscaled from the dark D app icon (`assets/app-icon-dark.png`).

## Wordmark

`assets/logo/` holds the full DEXEON wordmark as transparent 4000×1520 PNGs in the app-icon style: `dexeon-wordmark-on-light.png` (ink outline and shadow, for light backgrounds) and `dexeon-wordmark-on-dark.png` (off-white outline and shadow, for dark backgrounds). `dexeon-wordmark-black.png` is a one-colour version for light backgrounds, with the inner rule cut out as a transparent gap (`?theme=mono`). `preview.png` shows the colour pair in place. Source: `marketing/wordmark.html`; render with

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --force-device-scale-factor=2 --window-size=2000,760 --default-background-color=00000000 --screenshot=assets/logo/dexeon-wordmark-on-light.png "file://$PWD/marketing/wordmark.html"
```

Add `?theme=dark` to the URL for the on-dark variant.

## App icon

`assets/app-icon.png` is a 1024×1024 square app icon in the site's manga style: a red Anton "D" with a hard ink shadow over faint outlined katakana (source: `marketing/icon.html`, rendered with headless Chrome). `assets/app-icon-preview.png` shows it masked at home-screen sizes. `assets/app-icon-dark.png` is the same mark in the site's dark palette (render `marketing/icon.html?theme=dark`), with its own preview in `assets/app-icon-dark-preview.png`. An earlier Pokéball variant is kept as `assets/app-icon-pokeball.png` (source: `marketing/icon-pokeball.html`). To regenerate:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --hide-scrollbars --window-size=1024,1024 --screenshot=assets/app-icon.png "file://$PWD/marketing/icon.html"
```
