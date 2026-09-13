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
leaderboard = grab_phone('Mockup 5:')
chat = grab_phone('Mockup 6:')
trades = grab_phone('Mockup 7:')

STATUS_LIGHT = '''<div class="status"><span>9:41</span><span class="r">
<svg viewBox="0 0 14 11"><rect x="0" y="7" width="2.5" height="4"/><rect x="3.8" y="5" width="2.5" height="6"/><rect x="7.6" y="2.5" width="2.5" height="8.5"/><rect x="11.4" y="0" width="2.5" height="11"/></svg>
<svg viewBox="0 0 24 11"><rect class="bat" x="0.5" y="0.5" width="20" height="10" rx="3"/><rect x="2" y="2" width="16" height="7" rx="1.5"/><rect x="21.5" y="3.5" width="2" height="4" rx="1"/></svg>
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
  <div class="cd-price mp">
    <small class="sec">Market Price</small>
    <div class="cd-big">$178.43</div>
    <small class="sec">Holofoil · TCGplayer</small>
    <div class="cd-row"><div><small class="sec">Low</small><b>$150.00</b></div><div><small class="sec">Mid</small><b>$180.00</b></div><div><small class="sec">High</small><b>$349.99</b></div></div>
  </div>
  <div class="cd-actions">
    <span class="on g"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="currentColor"/><path d="M7.5 12.5l3 3 6-6.5" fill="none" stroke="#34C759" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Collected</span>
    <span class="b"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/></svg>Chase</span>
    <span class="on o"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.6 7 .9-5.2 4.9 1.4 7.1L12 18l-6.2 3.5 1.4-7.1L2 9.5l7-.9z"/></svg>Showcasing</span>
    <span class="k"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h13l-3-3M20 16H7l3 3"/></svg>Trade</span>
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
.cd-link{font-size:10px;font-weight:700;margin-top:2px;color:var(--is)}
'''

HEAD = ('<meta charset="utf-8"><title>Dexeon App Store screen</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">'
        '<style>' + style + SHARED_CSS + '</style>')

# Screen content, shared by every size.
SCREENS = {
    'screen-1-pokedex': dict(
        theme='light', eyebrow='Free during beta · No account needed',
        h1='Track all<br><span class="red">1025.</span>',
        p='All 1025 species across nine generations. Tap to catch, star your favorites, and pick the card that represents each one.',
        sfx=('sfx', 'GOTCHA!'), tag='<b>42%</b>431 of 1025 caught', phone=home),
    'screen-2-cards': dict(
        theme='light', eyebrow='Every printing · Live prices',
        h1='Every card.<br><span class="red">Every price.</span>',
        p='Every card ever printed for a species, with TCGplayer market pricing. Collect it, chase it, trade it, or showcase it.',
        sfx=('sfx y', 'ドン!'), tag='<b>Daily</b>TCGplayer market prices', phone=carddetail),
    'screen-3-binders': dict(
        theme='dark', eyebrow='Binders · 2×2 or 3×3',
        h1='Page like<br><span class="red">a binder.</span>',
        p='Real pocket pages for any card from any set. Tap to place, drag to swap, add pages as you grow.',
        sfx=('sfx', 'SNAP!'), tag='<b>3×3</b>drag &amp; drop pockets', phone=binder),
    'screen-4-social': dict(
        theme='light', eyebrow='Trainers · Gym Leaders · Trades',
        h1='Trade. Chat.<br><span class="red">Compete.</span>',
        p='Message other trainers with cards attached, list what you\'d trade, and climb a leaderboard of every collector on the app.',
        sfx=('sfx', 'DEAL!'), tag='<b>#7</b>of 214 trainers', phone=leaderboard),
    'screen-5-messages': dict(
        theme='light', eyebrow='Direct messages',
        h1='Send the<br><span class="red">card itself.</span>',
        p='Cards and binders travel as attachments that open in the app on tap, price and all.',
        sfx=('sfx y', 'やった!'), tag='<b>DM</b>cards &amp; binders', phone=chat),
    'screen-6-trades': dict(
        theme='light', eyebrow='Community trade board',
        h1='List it.<br><span class="red">Trade it.</span>',
        p='Tap Trade on a card you own and it\'s on the board for every trainer. Cards on your chase list wear a Wanted badge.',
        sfx=('sfx', 'DEAL!'), tag='<b>1 tap</b>messages the owner', phone=trades),
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
            'screen-4-social':  ('right:60px;top:870px;transform:rotate(7deg)', 'left:60px;top:2470px;transform:rotate(-4deg)'),
            'screen-5-messages':('right:60px;top:1010px;transform:rotate(7deg)', 'right:60px;top:2400px;transform:rotate(4deg)'),
            'screen-6-trades':  ('right:60px;top:870px;transform:rotate(7deg)', 'left:60px;top:2330px;transform:rotate(-4deg)'),
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
            'screen-4-social':  ('right:40px;top:300px;transform:rotate(7deg)', 'left:120px;top:1560px;transform:rotate(-4deg)'),
            'screen-5-messages':('left:980px;top:560px;transform:rotate(-8deg)', 'left:120px;top:1560px;transform:rotate(-3deg)'),
            'screen-6-trades':  ('right:40px;top:300px;transform:rotate(7deg)', 'left:120px;top:1560px;transform:rotate(-4deg)'),
        }),
    # Instagram 4:5 feed tiles: wordmark on top, headline, phone bleeding off the bottom, URL pill.
    'instagram-4x5': dict(
        w=1080, h=1350, out='assets/social', social=True, themes={'screen-3-binders': 'light'},
        css='''html,body{width:1080px;height:1350px}
          .kana-bg{font-size:420px;top:-30px;left:-20px}
          .tile-brand{position:absolute;top:44px;left:50%;transform:translateX(-50%);height:78px;width:auto;z-index:4}
          .head{left:64px;right:64px;top:152px;text-align:center}
          .head .eyebrow{font-size:22px;letter-spacing:.2em;gap:14px} .head .eyebrow::before{width:44px;height:5px}
          .head h1{font-size:132px;margin-top:22px;text-shadow:6px 6px 0 var(--paper),11px 11px 0 var(--ink)}
          .head p{font-size:28px;max-width:880px;margin:26px auto 0}
          .stage{left:50%;top:660px;transform:translateX(-50%) scale(2.6);transform-origin:top center}
          .speed{--cx:50%;--cy:78%}
          .sfx{font-size:62px;padding:12px 28px 8px;border-width:6px;box-shadow:10px 10px 0 var(--ink)}
          .stat-tag{font-size:26px;padding:18px 26px;border-width:6px;box-shadow:10px 10px 0 var(--ink)} .stat-tag b{font-size:66px}
          .tile-url{position:absolute;left:50%;bottom:36px;transform:translateX(-50%);z-index:6;background:var(--ink);color:var(--paper);font-weight:900;font-size:22px;letter-spacing:.08em;padding:12px 26px;border:3px solid var(--paper);white-space:nowrap}''',
        pos={
            'screen-1-pokedex': ('right:36px;top:700px;transform:rotate(8deg)', 'left:36px;top:1040px;transform:rotate(-4deg)'),
            'screen-2-cards':   ('right:36px;top:640px;transform:rotate(7deg)', 'right:36px;top:1020px;transform:rotate(4deg)'),
            'screen-3-binders': ('right:36px;top:640px;transform:rotate(7deg)', 'left:36px;top:1060px;transform:rotate(-4deg)'),
            'screen-4-social':  ('right:36px;top:640px;transform:rotate(7deg)', 'left:36px;top:590px;transform:rotate(-4deg)'),
            'screen-5-messages':('right:36px;top:700px;transform:rotate(7deg)', 'left:36px;top:1080px;transform:rotate(-4deg)'),
            'screen-6-trades':  ('left:36px;top:660px;transform:rotate(-8deg)', 'right:36px;top:1060px;transform:rotate(4deg)'),
        }),
}

# Remove only generated pages; icon.html and icon-pokeball.html are hand-written sources.
for f in glob.glob('marketing/iphone-*.html') + glob.glob('marketing/ipad-*.html') + glob.glob('marketing/instagram-*.html') + glob.glob('marketing/og.html') + glob.glob('marketing/poster.html') + glob.glob('marketing/story-*.html'):
    os.remove(f)

for sname, sz in SIZES.items():
    os.makedirs(sz['out'], exist_ok=True)
    for name, sc in SCREENS.items():
        sfx_pos, tag_pos = sz['pos'][name]
        social = sz.get('social', False)
        theme = sz.get('themes', {}).get(name, sc['theme'])
        brand = ('<img class="tile-brand" src="../assets/logo/dexeon-wordmark-nav.png" alt="">' if social and theme == 'light'
                 else '<img class="tile-brand" src="../assets/logo/dexeon-wordmark-nav-dark.png" alt="">' if social else '')
        url = '<div class="tile-url">dexeontcg.com · now in beta</div>' if social else ''
        body = (
            f'<div class="shot"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>{brand}'
            f'<div class="head"><span class="eyebrow">{sc["eyebrow"]}</span><h1>{sc["h1"]}</h1><p>{sc["p"]}</p></div>'
            f'<div class="speed"></div>'
            f'<span class="{sc["sfx"][0]}" style="{sfx_pos}">{sc["sfx"][1]}</span>'
            f'<div class="stat-tag" style="{tag_pos}">{sc["tag"]}</div>'
            f'<div class="stage">{sc["phone"]}</div>{url}</div>')
        open(f'marketing/{sname}-{name}.html', 'w').write(
            f'<!doctype html>\n<html lang="en" data-theme="{theme}"><head>{HEAD}'
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

# ── Instagram Stories: ten 1080 x 1920 frames, alternating light / dark ───────
def grab_block(start):
    """Lifts a non-phone block (fan, ticket, scan mock) from index.html by its opening tag."""
    i = src.index(start)
    depth = 0
    j = i
    for m in re.finditer(r'<div\b|</div>', src[i:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth == 0:
            j = i + m.end()
            break
    return src[i:j].replace('src="assets/', 'src="../assets/').replace(' rv d1', '').replace(' rv', '')

fan = grab_block('<div class="fan rv d1"')
ticket = grab_block('<div class="ticket rv d1"')
scanmock = grab_block('<div class="scan-mock"')

STORY_CSS = """
html,body{width:1080px;height:1920px}
.kana-bg{font-size:520px;top:-40px;left:-30px}
.tile-brand{position:absolute;top:130px;left:50%;transform:translateX(-50%);height:96px;width:auto;z-index:4}
.head{left:60px;right:60px;top:290px;text-align:center}
.head .eyebrow{font-size:24px;letter-spacing:.2em;gap:14px} .head .eyebrow::before{width:48px;height:6px}
.head h1{font-size:150px;margin-top:24px;line-height:.9;text-shadow:7px 7px 0 var(--paper),13px 13px 0 var(--ink)}
.head p{font-size:32px;max-width:900px;margin:30px auto 0}
.speed{--cx:50%;--cy:74%}
.stage{left:50%;transform-origin:top center;z-index:3}
.stage.ph{top:820px;transform:translateX(-50%) scale(3)}
.stage.fanwrap{top:860px;width:1000px;transform:translateX(-50%) scale(1.02)}
.stage.fanwrap .fan{height:900px} .stage.fanwrap .fan figure{width:300px}
.stage.fanwrap .fan .c1{left:0;top:18%} .stage.fanwrap .fan .c2{left:17%;top:6%} .stage.fanwrap .fan .c3{left:35%;top:0}
.stage.fanwrap .fan .c4{left:53%;top:4%} .stage.fanwrap .fan .c5{left:70%;top:14%} .stage.fanwrap .fan .c6{left:28%;top:44%}
.stage.fanwrap .fan .sfx{display:none}
.stage.scanwrap{top:840px;width:880px;transform:translateX(-50%)}
.stage.scanwrap .scan-mock{border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink)}
.stage.scanwrap .scan-mock i{width:56px;height:56px;border-width:8px}
.stage.scanwrap .scan-mock i:nth-child(1){top:26px;left:26px} .stage.scanwrap .scan-mock i:nth-child(2){top:26px;right:26px}
.stage.scanwrap .scan-mock i:nth-child(3){bottom:26px;left:26px} .stage.scanwrap .scan-mock i:nth-child(4){bottom:26px;right:26px}
.stage.scanwrap .scan-mock .match{font-size:30px;padding:14px 28px;bottom:34px;border-width:4px}
.stage.ticketwrap{top:880px;width:760px;transform:translateX(-50%) scale(1.15)}
.stage.ticketwrap .ticket{padding:44px 44px 40px;gap:26px} .stage.ticketwrap .ticket .lbl{font-size:15px}
.stage.ticketwrap .ticket .lbl b{font-size:28px} .stage.ticketwrap .ticket .lbl span{font-size:18px;max-width:28ch}
.stage.ticketwrap .ticket .price{font-size:96px} .stage.ticketwrap .ticket .price small{font-size:15px}
.stage.ticketwrap .ticket .never{font-size:19px} .stage.ticketwrap .ticket .sfx{display:none}
.steps-big{position:absolute;left:90px;right:90px;top:900px;display:grid;gap:26px;z-index:3}
.steps-big div{display:grid;grid-template-columns:96px 1fr;gap:26px;align-items:center;background:var(--paper-2);border:5px solid var(--ink);box-shadow:10px 10px 0 var(--ink);padding:26px 30px}
.steps-big div b{font-family:var(--display);font-weight:400;font-size:64px;line-height:1;color:var(--red);text-align:center}
.steps-big div span{font-size:34px;font-weight:900;line-height:1.2}
.steps-big div small{display:block;font-size:20px;font-weight:700;color:var(--ink-soft);margin-top:4px}
.sfx{font-size:70px;padding:14px 32px 10px;border-width:7px;box-shadow:12px 12px 0 var(--ink)}
.stat-tag{font-size:30px;padding:22px 30px;border-width:7px;box-shadow:12px 12px 0 var(--ink)} .stat-tag b{font-size:78px}
.tile-url{position:absolute;left:50%;bottom:200px;transform:translateX(-50%);z-index:6;background:var(--ink);color:var(--paper);font-weight:900;font-size:26px;letter-spacing:.08em;padding:16px 32px;border:4px solid var(--paper);white-space:nowrap}
"""

STORIES = [
    dict(theme='light', eyebrow='Now in beta · iPhone', h1='Track<br><span class="red">’Em All.</span>',
         p='Every species, every card printing, every binder. One app for the whole collection.',
         stage=f'<div class="stage ph">{home}</div>',
         sfx=('sfx', 'GOTCHA!', 'right:50px;top:900px;transform:rotate(8deg)'),
         tag=('<b>1025</b>species · Gen I–IX', 'left:50px;top:1360px;transform:rotate(-4deg)')),
    dict(theme='dark', eyebrow='Every printing · Live prices', h1='Every card.<br><span class="red">Every price.</span>',
         p='English and Japanese printings with TCGplayer market prices and 90-day trends.',
         stage=f'<div class="stage ph">{carddetail}</div>',
         sfx=('sfx y', 'ドン!', 'right:50px;top:860px;transform:rotate(7deg)'),
         tag=('<b>Daily</b>market prices', 'left:50px;top:1380px;transform:rotate(-4deg)')),
    dict(theme='light', eyebrow='Camera', h1='Point. Shoot.<br><span class="red">Matched.</span>',
         p='Snap any card and Dexeon identifies the exact printing, then opens it to collect, chase or trade.',
         stage=f'<div class="stage scanwrap">{scanmock}</div>',
         sfx=('sfx', 'SNAP!', 'right:50px;top:800px;transform:rotate(7deg)'),
         tag=('<b>1 tap</b>from photo to card page', 'left:50px;top:780px;transform:rotate(-4deg)')),
    dict(theme='dark', eyebrow='Binders · 2×2 · 3×3 · 4×3', h1='Page like<br><span class="red">a binder.</span>',
         p='Real pocket pages. Drag to swap, start from a whole set, share the link or print the PDF.',
         stage=f'<div class="stage ph">{binder}</div>',
         sfx=('sfx', 'SNAP!', 'right:50px;top:860px;transform:rotate(7deg)'),
         tag=('<b>PDF</b>print or share a link', 'left:50px;top:1380px;transform:rotate(-4deg)')),
    dict(theme='light', eyebrow='Japanese sets', h1='Every Japanese<br><span class="red">set, too.</span>',
         p='The full JA catalog beside the English one, with a JA badge on every printing.',
         stage=f'<div class="stage fanwrap">{fan}</div>',
         sfx=('sfx y', '全部!', 'right:60px;top:800px;transform:rotate(7deg)'),
         tag=('<b>EN + JA</b>one search, both catalogs', 'left:50px;top:780px;transform:rotate(-4deg)')),
    dict(theme='dark', eyebrow='Gym Leaders', h1='Climb the<br><span class="red">leaderboard.</span>',
         p='Every trainer on the app, ranked by Full Dex, sets completed, weekly catches or arcade score.',
         stage=f'<div class="stage ph">{leaderboard}</div>',
         sfx=('sfx', 'DEAL!', 'right:50px;top:860px;transform:rotate(7deg)'),
         tag=('<b>#7</b>of 214 trainers', 'left:40px;top:1400px;transform:rotate(-4deg)')),
    dict(theme='light', eyebrow='Direct messages', h1='Send the<br><span class="red">card itself.</span>',
         p='Cards and binders travel as attachments that open in the app on tap, price and all.',
         stage=f'<div class="stage ph">{chat}</div>',
         sfx=('sfx y', 'やった!', 'right:50px;top:900px;transform:rotate(7deg)'),
         tag=('<b>DM</b>cards &amp; binders', 'left:40px;top:1060px;transform:rotate(-4deg)')),
    dict(theme='dark', eyebrow='Community trade board', h1='List it.<br><span class="red">Trade it.</span>',
         p='Tap Trade on a card you own. Every trainer can see it, and one tap messages you.',
         stage=f'<div class="stage ph">{trades}</div>',
         sfx=('sfx', 'DEAL!', 'left:50px;top:860px;transform:rotate(-8deg)'),
         tag=('<b>Wanted</b>badges on your chase list', 'right:50px;top:1400px;transform:rotate(4deg)')),
    dict(theme='light', eyebrow='Pricing', h1='Free for life<br><span class="red">if you’re early.</span>',
         p='A select group of beta early adopters never pay. Everyone else: $5.99 once at launch. Never a subscription.',
         stage=f'<div class="stage ticketwrap">{ticket}</div>',
         sfx=('sfx y', 'LIMITED!', 'right:60px;top:820px;transform:rotate(7deg)'),
         tag=None),
    dict(theme='dark', eyebrow='Beta open now', h1='Get in<br><span class="red">early.</span>',
         p='The free-for-life window closes before public launch. Three taps and you’re in.',
         stage=('<div class="steps-big">'
                '<div><b>1</b><span>Tap the link in bio<small>dexeontcg.com</small></span></div>'
                '<div><b>2</b><span>Drop your email<small>One note at launch, nothing else</small></span></div>'
                '<div><b>3</b><span>TestFlight opens<small>Install the beta and start catching</small></span></div>'
                '</div>'),
         sfx=('sfx', 'GO!', 'right:70px;top:820px;transform:rotate(7deg)'),
         tag=None),
]

os.makedirs('assets/social/stories', exist_ok=True)
for f in glob.glob('marketing/story-*.html'):
    os.remove(f)
for n, st in enumerate(STORIES, 1):
    brand = '../assets/logo/dexeon-wordmark-nav.png' if st['theme'] == 'light' else '../assets/logo/dexeon-wordmark-nav-dark.png'
    sfx_cls, sfx_txt, sfx_pos = st['sfx']
    tag_html = f'<div class="stat-tag" style="{st["tag"][1]}">{st["tag"][0]}</div>' if st['tag'] else ''
    body = (
        f'<div class="shot"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>'
        f'<img class="tile-brand" src="{brand}" alt="">'
        f'<div class="head"><span class="eyebrow">{st["eyebrow"]}</span><h1>{st["h1"]}</h1><p>{st["p"]}</p></div>'
        f'<div class="speed"></div>'
        f'<span class="{sfx_cls}" style="{sfx_pos}">{sfx_txt}</span>{tag_html}'
        f'{st["stage"]}'
        f'<div class="tile-url">dexeontcg.com · link in bio</div></div>')
    open(f'marketing/story-{n:02d}.html', 'w').write(
        f'<!doctype html>\n<html lang="en" data-theme="{st["theme"]}"><head>{HEAD}<style>{STORY_CSS}</style></head><body>{body}</body></html>')

srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    for n in range(1, len(STORIES) + 1):
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1080,1920', '--virtual-time-budget=8000',
                        f'--screenshot=assets/social/stories/story-{n:02d}.png',
                        f'http://localhost:8765/marketing/story-{n:02d}.html'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('rendered story', n)
finally:
    srv.terminate()

# ── "Everything" poster: 1080 x 1080 square for Instagram ────────────────────
POSTER_CSS = """
html,body{width:1080px;height:1080px}
.kana-bg{font-size:400px;top:-30px;left:-20px}
.tile-brand{position:absolute;top:36px;left:50%;transform:translateX(-50%);height:80px;width:auto;z-index:4}
.head{left:40px;right:40px;top:136px;text-align:center}
.head .eyebrow{font-size:19px;letter-spacing:.2em;gap:14px} .head .eyebrow::before{width:44px;height:5px}
.head h1{font-size:112px;margin-top:14px;line-height:.9;text-shadow:5px 5px 0 var(--paper),10px 10px 0 var(--ink)}
.head p{font-size:23px;max-width:820px;margin:16px auto 0}
.speed{--cx:50%;--cy:84%;opacity:.26}
.chips-row{position:absolute;left:0;right:0;display:flex;justify-content:center;gap:16px;z-index:5}
.chip{display:inline-flex;align-items:center;gap:10px;background:var(--paper-2);color:var(--ink);border:4px solid var(--ink);box-shadow:5px 5px 0 var(--ink);padding:9px 16px;font-size:20px;font-weight:900;white-space:nowrap}
.chip i{width:13px;height:13px;border-radius:50%;background:var(--red);border:3px solid var(--ink);display:inline-block}
.chip.y{background:var(--yellow)} .chip.b{background:var(--blue);color:#fff} .chip.b i{background:#fff}
.stage{left:50%;transform-origin:top center;z-index:3}
.stage.mid{top:598px;transform:translateX(-50%) scale(1.62)}
.stage.l{top:660px;transform:translateX(-50%) translateX(-352px) rotate(-8deg) scale(1.28);z-index:2;filter:brightness(.96)}
.stage.r{top:660px;transform:translateX(-50%) translateX(352px) rotate(8deg) scale(1.28);z-index:2;filter:brightness(.96)}
.sfx{font-size:52px;padding:10px 22px 6px;border-width:6px;box-shadow:9px 9px 0 var(--ink)}
.tile-url{position:absolute;left:50%;bottom:28px;transform:translateX(-50%);z-index:6;background:var(--ink);color:var(--paper);font-weight:900;font-size:21px;letter-spacing:.08em;padding:12px 26px;border:3px solid var(--paper);white-space:nowrap}
.price{position:absolute;z-index:6;left:28px;bottom:120px;background:var(--paper-2);border:4px solid var(--ink);box-shadow:8px 8px 0 var(--red);padding:12px 16px;font-size:16px;font-weight:900;line-height:1.2;transform:rotate(-3deg);max-width:250px}
.price b{display:block;font-family:var(--display);font-weight:400;font-size:40px;color:var(--green);letter-spacing:.01em}
.price small{display:block;font-weight:700;color:var(--ink-soft);font-size:13px;margin-top:4px}
"""
row1 = [('', '1025 species · Full Dex', '-2deg'), ('', 'Every printing · EN + JA', '1.5deg'), ('', 'Live TCGplayer prices', '-1deg')]
row2 = [('y', 'Scan a card to identify it', '1.5deg'), ('b', 'Trade board · DMs · Gym Leaders', '-1.5deg'), ('', 'Binders · share &amp; print', '2deg')]
def chips(items):
    return ''.join(f'<span class="chip {c}" style="transform:rotate({r})"><i></i>{t}</span>' for c, t, r in items)
poster_body = (
    '<div class="shot"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>'
    '<img class="tile-brand" src="../assets/logo/dexeon-wordmark-nav.png" alt="">'
    '<div class="head"><span class="eyebrow">Now in beta · iPhone</span>'
    '<h1>Track <span class="red">’Em All.</span></h1>'
    '<p>Your Full Dex, every card printing with live prices, binders that page like binders, and a whole team of trainers to trade and talk with.</p></div>'
    '<div class="speed"></div>'
    f'<div class="chips-row" style="top:436px">{chips(row1)}</div>'
    f'<div class="chips-row" style="top:506px">{chips(row2)}</div>'
    '<span class="sfx" style="right:44px;top:900px;transform:rotate(7deg)">GOTCHA!</span>'
    f'<div class="stage l">{chat}</div><div class="stage r">{leaderboard}</div><div class="stage mid">{home}</div>'
    '<div class="price"><b>$0 for life</b>for early adopters in the beta<small>Otherwise $5.99 once at launch. Never a subscription.</small></div>'
    '<div class="tile-url">dexeontcg.com · now in beta</div></div>')
open('marketing/poster.html', 'w').write(
    f'<!doctype html>\n<html lang="en" data-theme="light"><head>{HEAD}<style>{POSTER_CSS}</style></head><body>{poster_body}</body></html>')
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                    '--window-size=1080,1080', '--virtual-time-budget=8000', '--screenshot=assets/social/dexeon-everything-1x1.png',
                    'http://localhost:8765/marketing/poster.html'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print('rendered poster 1080x1080 -> assets/social/dexeon-everything-1x1.png')
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
.head{left:72px;top:150px;width:680px;text-align:left}
.head .eyebrow{font-size:20px;letter-spacing:.2em;gap:14px} .head .eyebrow::before{width:44px;height:5px}
.head h1{font-size:172px;margin-top:22px;line-height:.86;text-shadow:7px 7px 0 var(--paper),13px 13px 0 var(--ink)}
.stage{left:745px;top:64px;transform:scale(1.5);transform-origin:top left}
.speed{--cx:83%;--cy:62%;opacity:.28}
.sfx{font-size:46px;padding:10px 22px 6px;border-width:5px;box-shadow:8px 8px 0 var(--ink)}
'''
og_body = (
    '<div class="shot"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>'
    '<div class="brand"><img src="../assets/logo-mark.png" alt=""><span><b>DEXEON</b><small>デクセオン</small></span></div>'
    '<div class="head"><span class="eyebrow">Now in beta · iPhone</span>'
    '<h1>Track<br><span class="red">\u2019Em All.</span></h1></div>'
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
