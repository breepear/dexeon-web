"""Builds the App Store marketing screens from the landing page's own CSS and
phone mockups, then renders them to 1242x2688 PNGs with headless Chrome.
Run from the repo root:  python3 marketing/build.py
"""
import re, subprocess, time, os, sys
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
src=open('index.html').read()
style=re.search(r'<style>(.*?)</style>',src,re.S).group(1)

def grab_phone(marker):
    i=src.index(marker); i=src.index('<div class="phone',i)
    depth=0; j=i
    for m in re.finditer(r'<div\b|</div>',src[i:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth==0: j=i+m.end(); break
    return (src[i:j].replace('src="assets/','src="../assets/').replace(' id="heroPhone"','')
            .replace('class="phone back"','class="phone"').replace('class="phone front"','class="phone"'))

home=grab_phone('Mockup 1:')
binder=grab_phone('Mockup 3:')

status_light='''<div class="status"><span>9:41</span><span class="r">
<svg viewBox="0 0 14 11"><rect x="0" y="7" width="2.5" height="4" fill="#121114"/><rect x="3.8" y="5" width="2.5" height="6" fill="#121114"/><rect x="7.6" y="2.5" width="2.5" height="8.5" fill="#121114"/><rect x="11.4" y="0" width="2.5" height="11" fill="#121114"/></svg>
<svg viewBox="0 0 24 11"><rect x="0.5" y="0.5" width="20" height="10" rx="3" fill="none" stroke="#121114"/><rect x="2" y="2" width="16" height="7" rx="1.5" fill="#121114"/><rect x="21.5" y="3.5" width="2" height="4" rx="1" fill="#121114"/></svg>
</span></div>'''

carddetail=f'''<div class="phone">
<div class="island"></div>
<div class="screen">
{status_light}
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

extra_css='''
html,body{margin:0;width:1242px;height:2688px;overflow:hidden}
body{background:var(--paper);position:relative;font-family:var(--body)}
.shot{position:absolute;inset:0;overflow:hidden}
.halft{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.4px, transparent 3px);background-size:18px 18px;opacity:.9}
.kana-bg{position:absolute;top:-40px;left:-30px;font-size:560px;line-height:1;color:transparent;-webkit-text-stroke:4px var(--tone);opacity:.5;white-space:nowrap;letter-spacing:.02em;font-weight:900}
.head{position:absolute;left:80px;right:80px;top:170px;text-align:center;z-index:3}
.head .eyebrow{font-size:34px;letter-spacing:.22em;gap:22px}
.head .eyebrow::before{width:70px;height:8px}
.head h1{font-family:var(--display);font-weight:400;text-transform:uppercase;font-size:196px;line-height:.9;margin:40px 0 0;transform:skewX(-6deg);text-shadow:10px 10px 0 var(--paper),18px 18px 0 var(--ink)}
.head h1 .red{color:var(--red)}
.head p{font-size:46px;line-height:1.3;color:var(--ink-soft);font-weight:700;margin:56px auto 0;max-width:1000px}
.stage{position:absolute;left:50%;transform-origin:top center;z-index:2}
.speed{position:absolute;inset:0;pointer-events:none;background:repeating-conic-gradient(from 0deg at 50% var(--cy), var(--ink) 0deg .35deg, transparent .35deg 3deg);-webkit-mask:radial-gradient(ellipse 70% 40% at 50% var(--cy), transparent 40%, #000 62%, transparent 100%);mask:radial-gradient(ellipse 70% 40% at 50% var(--cy), transparent 40%, #000 62%, transparent 100%);opacity:.3;z-index:1}
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

head=('<meta charset="utf-8"><title>Dexeon App Store screen</title>'
 '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">'
 '<style>'+style+extra_css+'</style>')

screens={
 'screen-1-pokedex': ('light', '''
  <div class="head"><span class="eyebrow">Free · No account needed</span>
    <h1>Track all<br><span class="red">1025.</span></h1>
    <p>Every species from Kanto to Paldea. Tap to catch, star your favorites, and pick the card that represents each one.</p></div>
  <div class="speed" style="--cy:70%"></div>
  <span class="sfx" style="right:60px;top:1010px;transform:rotate(8deg)">GOTCHA!</span>
  <div class="stat-tag" style="left:60px;top:2200px;transform:rotate(-4deg)"><b>42%</b>431 of 1025 caught</div>
  <div class="stage" style="top:900px;transform:translateX(-50%) scale(3)">'''+home+'</div>'),
 'screen-2-cards': ('light', '''
  <div class="head"><span class="eyebrow">Every printing · Live prices</span>
    <h1>Every card.<br><span class="red">Every price.</span></h1>
    <p>Open any species to see each card ever printed, with TCGplayer market pricing. Collect it, chase it, or make it your showcase.</p></div>
  <div class="speed" style="--cy:72%"></div>
  <span class="sfx y" style="left:60px;top:1130px;transform:rotate(-8deg)">ドン!</span>
  <div class="stat-tag" style="right:60px;top:1320px;transform:rotate(4deg)"><b>Daily</b>TCGplayer market prices</div>
  <div class="stage" style="top:940px;transform:translateX(-50%) scale(3)">'''+carddetail+'</div>'),
 'screen-3-binders': ('dark', '''
  <div class="head"><span class="eyebrow">Binders · 2×2 or 3×3</span>
    <h1>Page like<br><span class="red">a binder.</span></h1>
    <p>Real pocket pages for any card from any set. Tap to place, drag to swap, add pages as you grow.</p></div>
  <div class="speed" style="--cy:70%"></div>
  <span class="sfx" style="right:60px;top:870px;transform:rotate(7deg)">SNAP!</span>
  <div class="stat-tag" style="left:60px;top:2330px;transform:rotate(-4deg)"><b>3×3</b>drag &amp; drop pockets</div>
  <div class="stage" style="top:900px;transform:translateX(-50%) scale(3)">'''+binder+'</div>'),
}
for name,(theme,body) in screens.items():
    open(f'marketing/{name}.html','w').write(
      f'<!doctype html>\n<html lang="en" data-theme="{theme}"><head>{head}</head><body><div class="shot">'
      f'<div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>{body}</div></body></html>')
print("built html:", ", ".join(screens))

if '--no-render' in sys.argv: sys.exit()
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
srv=subprocess.Popen([sys.executable,'-m','http.server','8765'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL); time.sleep(1)
try:
    os.makedirs('assets/appstore',exist_ok=True)
    for name in screens:
        subprocess.run([CHROME,'--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1',
            '--window-size=1242,2688','--virtual-time-budget=8000',f'--screenshot=assets/appstore/{name}.png',
            f'http://localhost:8765/marketing/{name}.html'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        print("rendered", name)
finally:
    srv.terminate()
