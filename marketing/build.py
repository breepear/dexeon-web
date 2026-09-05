"""Builds the App Store marketing screens from the landing page's own CSS and
phone mockups, then renders them with headless Chrome.

Sizes:
  iphone-6.5  1242 x 2688  ->  assets/appstore/
  ipad-13     2064 x 2752  ->  assets/appstore/ipad-13/

Run from the repo root:  python3 marketing/build.py   (add --no-render to only write HTML)
"""
import re, subprocess, time, os, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
src = open('index.html').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)


def grab_phone(marker):
    """Returns the phone mockup that follows a `Mockup N:` comment in index.html."""
    i = src.index(marker)
    i = src.index('<div class="phone', i)
    depth = 0
    j = i
    for m in re.finditer(r'<div\b|</div>', src[i:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth == 0:
            j = i + m.end()
            break
    return (src[i:j]
            .replace('src="assets/', 'src="../assets/')
            .replace(' id="heroPhone"', '')
            .replace('class="phone back"', 'class="phone"')
            .replace('class="phone front"', 'class="phone"'))


home = grab_phone('Mockup 1:')
binder = grab_phone('Mockup 3:')

STATUS_LIGHT = '''<div class="status"><span>9:41</span><span class="r">
<svg viewBox="0 0 14 11"><rect x="0" y="7" width="2.5" height="4" fill="#121114"/><rect x="3.8" y="5" width="2.5" height="6" fill="#121114"/><rect x="7.6" y="2.5" width="2.5" height="8.5" fill="#121114"/><rect x="11.4" y="0" width="2.5" height="11" fill="#121114"/></svg>
<svg viewBox="0 0 24 11"><rect x="0.5" y="0.5" width="20" height="10" rx="3" fill="none" stroke="#121114"/><rect x="2" y="2" width="16" height="7" rx="1.5" fill="#121114"/><rect x="21.5" y="3.5" width="2" height="4" rx="1" fill="#121114"/></svg>
</span></div>'''

# The card detail sheet isn't on the landing page, so it's built here.
carddetail = f'''<div class="phone">
<div class="island"></div>
<div class="screen">
{STATUS_LIGHT}
<div class="navbar"><span class="acc">Done</span><span class="t">Charizard ex</span><span style="width:26px"></span></div>
<div class="pad cd">
  <div class="cd-img"><img src="../assets/cards/sv3pt5-199.jpg" alt=""></div>
  <div class="cd-title"><b>151</b><div class="cd-tags"><span>Special Illustration Rare</span><span>#199</span></div></div>
  <div class="cd-price surface">
    <small class="sec">Market Price</small>
    <div class="cd-big">$178.43</div>
    <small class="sec">Holofoil · TCGplayer</small>
    <div class="cd-row"><div><small class="sec">Low</small><b>$150.00</b></div><div><small class="sec">Mid</small><b>$180.00</b></div><div><small class="sec">High</small><b>$349.99</b></div></div>
  </div>
  <div class="cd-actions">
    <span class="on g"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="currentColor"/><path d="M7.5 12.5l3 3 6-6.5" fill="none" stroke="#34C759" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Collected</span>
    <span class="b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/></svg>Chase</span>
    <span class="on o"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.6 7 .9-5.2 4.9 1.4 7.1L12 18l-6.2 3.5 1.4-7.1L2 9.5l7-.9z"/></svg>Showcasing</span>
  </div>
  <div class="cd-link sec">↗ View on TCGplayer</div>
</div>
<div class="home-bar"></div>
</div>
</div>'''

# Shared marketing-screen CSS. Canvas size, headline placement, and phone
# placement are set per size below.
SHARED_CSS = '''
html,body{margin:0;overflow:hidden}
body{background:var(--paper);position:relative;font-family:var(--body)}
.shot{position:absolute;inset:0;overflow:hidden}
.halft{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.4px, transparent 3px);background-size:18px 18px;opacity:.9}
.kana-bg{position:absolute;line-height:1;color:transparent;-webkit-text-stroke:4px var(--tone);opacity:.5;white-space:nowrap;letter-spacing:.02em;font-weight:900}
.head{position:absolute;z-index:3}
.head .eyebrow{font-size:34px;letter-spacing:.22em;gap:22px}
.head .eyebrow::before{width:70px;height:8px}
.head h1{font-family:var(--display);font-weight:400;text-transform:uppercase;line-height:.9;margin:40px 0 0;transform:skewX(-6deg);text-shadow:10px 10px 0 var(--paper),18px 18px 0 var(--ink)}
.head h1 .red{color:var(--red)}
.head p{font-size:46px;line-height:1.3;color:var(--ink-soft);font-weight:700}
.stage{position:absolute;z-index:2}
.speed{position:absolute;inset:0;pointer-events:none;z-index:1;opacity:.3;
  background:repeating-conic-gradient(from 0deg at var(--cx) var(--cy), var(--ink) 0deg .35deg, transparent .35deg 3deg);
  -webkit-mask:radial-gradient(ellipse 70% 40% at var(--cx) var(--cy), transparent 40%, #000 62%, transparent 100%);
          mask:radial-gradient(ellipse 70% 40% at var(--cx) var(--cy), transparent 40%, #000 62%, transparent 100%)}
.sfx{position:absolute;z-index:4;font-size:96px;padding:18px 42px 12px;border-width:8px;box-shadow:14px 14px 0 var(--ink)}
.stat-tag{position:absolute;left:auto;top:auto;z-index:4;background:var(--paper-2);border:8px solid var(--ink);box-shadow:14px 14px 0 var(--ink);padding:26px 38px;font-weight:900;font-size:36px;line-height:1.1}
.stat-tag b{display:block;font-family:var(--display);font-weight:400;font-size:96px;color:var(--red)}
.phone{box-shadow:0 14px 30px -10px rgba(0,0,0,.5),0 0 0 2px #2b2b30 inset,0 0 0 3px #121114}
.cd{display:flex;flex-direction:column;align-items:center;gap:9px}
.cd-img{width:176px;border-radius:13px;overflow:hidden;box-shadow:0 12px 22px rgba(0,0,0,.25)}
.cd-title{text-align:center}
.cd-title b{font-size:12px;font-weight:800;display:block}
.cd-tags{display:flex;gap:5px;justify-content:center;margin-top:4px}
.cd-tags span{font-size:8.5px;font-weight:700;color:#6e6e73;background:rgba(0,0,0,.06);padding:2px 8px;border-radius:99px}
.cd-price{width:100%;border-radius:15px;padding:10px 12px;text-align:center}
.cd-price small{font-size:8.5px;font-weight:700;display:block}
.cd-big{font-size:26px;font-weight:900;color:#34C759;line-height:1.1;font-variant-numeric:tabular-nums}
.cd-row{display:flex;justify-content:space-around;margin-top:8px}
.cd-row b{display:block;font-size:11px;font-weight:800;font-variant-numeric:tabular-nums}
.cd-actions{display:flex;gap:7px;width:100%}
.cd-actions span{flex:1;display:flex;flex-direction:column;align-items:center;gap:3px;font-size:8.5px;font-weight:800;padding:8px 2px;border-radius:9px}
.cd-actions svg{width:15px;height:15px}
.cd-actions .g{color:#34C759;background:rgba(52,199,89,.12)} .cd-actions .g.on{background:#34C759;color:#fff}
.cd-actions .b{color:#2E5AAC;background:rgba(46,90,172,.12)}
.cd-actions .o{color:#F08A24;background:rgba(240,138,36,.12)} .cd-actions .o.on{background:#F08A24;color:#fff}
.cd-link{font-size:10px;font-weight:700;margin-top:2px}
'''

HEAD = ('<meta charset="utf-8"><title>Dexeon App Store screen</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">'
        '<style>' + style + SHARED_CSS + '</style>')

# Screen content, shared by every size.
SCREENS = {
    'screen-1-pokedex': dict(
        theme='light', eyebrow='Free · No account needed',
        h1='Track all<br><span class="red">1025.</span>',
        p='Every species from Kanto to Paldea. Tap to catch, star your favorites, and pick the card that represents each one.',
        sfx=('sfx', 'GOTCHA!'), tag='<b>42%</b>431 of 1025 caught', phone=home),
    'screen-2-cards': dict(
        theme='light', eyebrow='Every printing · Live prices',
        h1='Every card.<br><span class="red">Every price.</span>',
        p='Every card ever printed for a species, with TCGplayer market pricing. Collect it, chase it, or showcase it.',
        sfx=('sfx y', 'ドン!'), tag='<b>Daily</b>TCGplayer market prices', phone=carddetail),
    'screen-3-binders': dict(
        theme='dark', eyebrow='Binders · 2×2 or 3×3',
        h1='Page like<br><span class="red">a binder.</span>',
        p='Real pocket pages for any card from any set. Tap to place, drag to swap, add pages as you grow.',
        sfx=('sfx', 'SNAP!'), tag='<b>3×3</b>drag &amp; drop pockets', phone=binder),
}

# Per-size layout: canvas CSS plus (sticker, tag) positions for each screen.
SIZES = {
    'iphone-6.5': dict(
        w=1242, h=2688, out='assets/appstore',
        css='''html,body{width:1242px;height:2688px}
          .kana-bg{font-size:560px;top:-40px;left:-30px}
          .head{left:80px;right:80px;top:170px;text-align:center}
          .head h1{font-size:196px} .head p{max-width:1000px;margin:56px auto 0}
          .stage{left:50%;top:900px;transform:translateX(-50%) scale(3);transform-origin:top center}
          .speed{--cx:50%;--cy:70%}''',
        pos={
            'screen-1-pokedex': ('right:60px;top:1010px;transform:rotate(8deg)', 'left:60px;top:2200px;transform:rotate(-4deg)'),
            'screen-2-cards':   ('left:60px;top:1130px;transform:rotate(-8deg)', 'right:60px;top:1320px;transform:rotate(4deg)'),
            'screen-3-binders': ('right:60px;top:870px;transform:rotate(7deg)', 'left:60px;top:2330px;transform:rotate(-4deg)'),
        }),
    'ipad-13': dict(
        w=2064, h=2752, out='assets/appstore/ipad-13',
        css='''html,body{width:2064px;height:2752px}
          .kana-bg{font-size:720px;top:-70px;left:-40px}
          .head{left:120px;top:520px;width:940px;text-align:left}
          .head h1{font-size:172px;margin-top:44px} .head p{max-width:860px;margin:60px 0 0}
          .stage{left:1090px;top:404px;transform:scale(3);transform-origin:top left}
          .speed{--cx:75%;--cy:50%}
          .stat-tag{font-size:40px} .stat-tag b{font-size:110px}''',
        pos={
            'screen-1-pokedex': ('right:40px;top:300px;transform:rotate(8deg)', 'left:120px;top:1560px;transform:rotate(-4deg)'),
            'screen-2-cards':   ('left:980px;top:560px;transform:rotate(-8deg)', 'left:120px;top:1560px;transform:rotate(-3deg)'),
            'screen-3-binders': ('right:40px;top:300px;transform:rotate(7deg)', 'left:120px;top:1560px;transform:rotate(-4deg)'),
        }),
}

for f in glob.glob('marketing/*.html'):
    os.remove(f)

for sname, sz in SIZES.items():
    os.makedirs(sz['out'], exist_ok=True)
    for name, sc in SCREENS.items():
        sfx_pos, tag_pos = sz['pos'][name]
        body = (
            f'<div class="shot"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>'
            f'<div class="head"><span class="eyebrow">{sc["eyebrow"]}</span><h1>{sc["h1"]}</h1><p>{sc["p"]}</p></div>'
            f'<div class="speed"></div>'
            f'<span class="{sc["sfx"][0]}" style="{sfx_pos}">{sc["sfx"][1]}</span>'
            f'<div class="stat-tag" style="{tag_pos}">{sc["tag"]}</div>'
            f'<div class="stage">{sc["phone"]}</div></div>')
        open(f'marketing/{sname}-{name}.html', 'w').write(
            f'<!doctype html>\n<html lang="en" data-theme="{sc["theme"]}"><head>{HEAD}'
            f'<style>{sz["css"]}</style></head><body>{body}</body></html>')
print('built html for', ', '.join(SIZES))

if '--no-render' in sys.argv:
    sys.exit()

CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    for sname, sz in SIZES.items():
        for name in SCREENS:
            subprocess.run([
                CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                f'--window-size={sz["w"]},{sz["h"]}', '--virtual-time-budget=8000',
                f'--screenshot={sz["out"]}/{name}.png',
                f'http://localhost:8765/marketing/{sname}-{name}.html',
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print('rendered', sname, name)
finally:
    srv.terminate()

# ── Social share image (Open Graph / Twitter card), 1200 x 630 ──────────────
OG_CSS = '''
html,body{width:1200px;height:630px}
.kana-bg{font-size:360px;top:-30px;left:-20px;-webkit-text-stroke:2.5px var(--tone)}
.brand{position:absolute;left:72px;top:54px;z-index:3;display:flex;align-items:center;gap:16px}
.brand img{width:60px;height:60px;border-radius:15px;border:3px solid var(--ink)}
.brand b{font-family:var(--display);font-weight:400;font-size:46px;letter-spacing:.02em;line-height:1;display:block}
.brand small{display:block;font-size:14px;font-weight:900;letter-spacing:.3em;color:var(--red);line-height:1;margin-top:4px}
.head{left:72px;top:176px;width:680px;text-align:left}
.head .eyebrow{font-size:20px;letter-spacing:.2em;gap:14px} .head .eyebrow::before{width:44px;height:5px}
.head h1{font-size:80px;margin-top:24px;text-shadow:5px 5px 0 var(--paper),9px 9px 0 var(--ink)}
.head p{font-size:26px;line-height:1.35;margin:30px 0 0;max-width:600px}
.stage{left:745px;top:64px;transform:scale(1.5);transform-origin:top left}
.speed{--cx:83%;--cy:62%;opacity:.28}
.sfx{font-size:46px;padding:10px 22px 6px;border-width:5px;box-shadow:8px 8px 0 var(--ink)}
'''
og_body = (
    '<div class="shot"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>'
    '<div class="brand"><img src="../assets/icon.png" alt=""><span><b>DEXEON</b><small>デクセオン</small></span></div>'
    '<div class="head"><span class="eyebrow">Free on iPhone</span>'
    '<h1>Track all 1025.<br><span class="red">Sleeve every card.</span></h1>'
    '<p>A free Pokédex, card and binder tracker with live market prices. No account needed.</p></div>'
    '<div class="speed"></div>'
    '<span class="sfx" style="right:44px;top:40px;transform:rotate(7deg)">GOTCHA!</span>'
    f'<div class="stage">{home}</div></div>')
open('marketing/og.html', 'w').write(
    f'<!doctype html>\n<html lang="en" data-theme="light"><head>{HEAD}<style>{OG_CSS}</style></head><body>{og_body}</body></html>')
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--window-size=1200,630', '--virtual-time-budget=8000', '--screenshot=assets/og.png',
                    'http://localhost:8765/marketing/og.html'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('rendered og 1200x630 -> assets/og.png')
finally:
    srv.terminate()
