# Story remix: ten one-off 1080 x 1920 layouts, each its own composition.
# Executed from build.py (via exec) so it shares HEAD, the mockups and CHROME.

# Sub-blocks lifted out of the phone mockups (first occurrence in index.html).
grid2   = grab_block('<div class="grid2">')
chatblk = grab_block('<div class="chat">')
podium  = grab_block('<div class="podium">')
page1   = grab_block('<div class="page mp">')

REMIX_CSS = """
html,body{width:1080px;height:1920px}
.kana-bg{font-size:520px;top:-40px;left:-30px}
.mv{--p:#F2F3EF;--p2:#FFFFFF;--i:#121114;--is:#4A484E;--t2:#DDDFD8;--r:#AC322F;--g:#2FA44F;--b:#2E5AAC;--y:#F7C728;position:relative;color:var(--i)}
.mv.dk{--p:#131316;--p2:#1B1B1F;--i:#F1F0EA;--is:#B8B6BE;--t2:#2A2A2F;--r:#E0463F;--g:#43C06A;--b:#5B86D6}
.brand{position:absolute;top:130px;left:50%;transform:translateX(-50%);height:96px;width:auto;z-index:6}
.brand.tl{left:80px;transform:none}
.url{position:absolute;left:50%;bottom:200px;transform:translateX(-50%);z-index:8;background:var(--ink);color:var(--paper);font-weight:900;font-size:26px;letter-spacing:.08em;padding:16px 32px;border:4px solid var(--paper);white-space:nowrap}
.url.left{left:80px;transform:none}
.big{font-family:var(--display);text-transform:uppercase;line-height:.88;transform:skewX(-6deg);text-shadow:7px 7px 0 var(--paper),13px 13px 0 var(--ink);font-weight:400}
.big .red{color:var(--red)}
.eyebrow{font-size:24px;letter-spacing:.22em} .eyebrow::before{width:48px;height:6px}
.copy{font-size:31px;line-height:1.3;color:var(--ink-soft);font-weight:700;text-wrap:balance}
.sfx{font-size:70px;padding:14px 32px 10px;border-width:7px;box-shadow:12px 12px 0 var(--ink);position:absolute;z-index:9}
.stat-tag{position:absolute;left:auto;top:auto;z-index:9;font-size:30px;padding:22px 30px;border-width:7px;box-shadow:12px 12px 0 var(--ink);max-width:520px;line-height:1.15} .stat-tag b{font-size:78px}
.phone{transform-origin:top left;position:absolute}
.stg{position:absolute;transform-origin:top left;z-index:4} .stg .phone{position:relative;left:0;top:0;transform:none}

/* 01 panels */
.r1 .cell{position:absolute;overflow:hidden;background:var(--paper-2);border:7px solid var(--ink)}
.r1 .cell .phone{left:-40px;top:-140px;transform:scale(1.9)}
.r1 .cap{position:absolute;left:-7px;bottom:-7px;background:var(--ink);color:var(--paper);font-weight:900;font-size:22px;letter-spacing:.12em;text-transform:uppercase;padding:10px 18px;z-index:3}
/* 02 giant number */
.r2 .num{position:absolute;left:0;right:0;top:420px;text-align:center;font-family:var(--display);font-size:500px;line-height:.85;color:var(--red);-webkit-text-stroke:10px var(--ink);text-shadow:22px 22px 0 var(--ink);transform:skewX(-6deg)}
.r2 .strip{position:absolute;left:-60px;right:-60px;bottom:250px;display:flex;gap:26px;transform:rotate(-4deg)}
.r2 .strip img{width:250px;border-radius:14px;border:6px solid var(--ink);box-shadow:10px 10px 0 var(--ink)}
.r2 .strip img.g{filter:grayscale(1);opacity:.85}
/* 03 tilted break-out */
.r3 .list{position:absolute;left:80px;top:760px;display:grid;gap:22px;z-index:7}
.r3 .list span{display:inline-flex;align-items:center;gap:14px;background:var(--paper-2);border:5px solid var(--ink);box-shadow:8px 8px 0 var(--ink);padding:14px 22px;font-size:27px;font-weight:900;width:max-content}
.r3 .list i{width:16px;height:16px;border-radius:50%;background:var(--red);border:3px solid var(--ink)}
.r3 .stg{left:590px;top:600px;transform:rotate(-12deg) scale(2.6)}
/* 04 bubbles */
.r4 .chat{position:absolute;left:70px;right:70px;top:640px;gap:22px;padding:0}
.r4 .chat .msg{font-size:34px;padding:26px 36px;border-radius:44px;max-width:82%}
.r4 .chat .msg.them{border:4px solid var(--i)}
.r4 .chat .att{padding:24px;border-radius:36px;border-width:4px;gap:22px}
.r4 .chat .att img{width:180px;border-radius:14px}
.r4 .chat .att b{font-size:30px} .r4 .chat .att small{font-size:26px} .r4 .chat .att .sub{font-size:24px !important}
.r4 .chat .att .bth{width:90px;height:126px;border-radius:12px} .r4 .chat .att .chev{width:26px;height:26px}
.r4 .chat .when{font-size:24px}
/* 05 binder page fullscreen */
.r5 .page{position:absolute;left:60px;right:60px;top:600px;padding:34px;border-radius:44px;border-width:6px;box-shadow:16px 16px 0 var(--i)}
.r5 .slots{gap:24px} .r5 .slot{border-radius:22px} .r5 .slot img{border-radius:22px}
.r5 .slot.empty{border-width:5px} .r5 .slot.empty svg{width:60px;height:60px}
.r5 .slot.target{outline-width:8px} .r5 .slot.drag img{transform:translate(-80px,-90px) rotate(-7deg) scale(1.1)}
/* 06 podium poster */
.r6 .burst{position:absolute;inset:-20%;opacity:.16;background:repeating-conic-gradient(from 0deg at 50% 62%, var(--paper) 0deg 6deg, transparent 6deg 14deg);
  -webkit-mask:radial-gradient(circle at 50% 62%, #000 20%, transparent 62%);mask:radial-gradient(circle at 50% 62%, #000 20%, transparent 62%)}
.r6 .podium{position:absolute;left:60px;right:60px;top:780px;gap:30px;padding:0}
.r6 .pcol .av{width:150px;height:150px;font-size:56px;border-width:8px} .r6 .pcol.first .av{width:210px;height:210px;font-size:80px}
.r6 .pcol .trophy{width:44px;height:44px} .r6 .pcol.first .trophy{width:60px;height:60px}
.r6 .pcol .n{font-size:30px} .r6 .pcol .v{font-size:56px} .r6 .pcol.first .v{font-size:72px}
.r6 .ped{border-radius:26px;font-size:60px;border-width:4px} .r6 .pcol.first .ped{height:190px;font-size:84px} .r6 .pcol.second .ped{height:130px} .r6 .pcol.third .ped{height:90px}
.r6 .pill{position:absolute;left:50%;bottom:330px;transform:translateX(-50%);background:var(--red);color:#fff;font-size:34px;font-weight:900;padding:22px 44px;border-radius:99px;border:4px solid rgba(255,255,255,.4);white-space:nowrap;z-index:8}
/* 07 receipt */
.r7 .receipt{position:absolute;left:120px;right:120px;top:560px;background:var(--paper-2);border:6px solid var(--ink);box-shadow:16px 16px 0 var(--ink);padding:44px 48px;font-variant-numeric:tabular-nums}
.r7 .receipt h3{font-family:var(--display);font-weight:400;font-size:44px;letter-spacing:.06em;text-transform:uppercase;margin:0 0 8px;text-align:center}
.r7 .receipt .sub{text-align:center;font-size:22px;font-weight:800;color:var(--ink-soft);letter-spacing:.12em;text-transform:uppercase;border-bottom:4px dashed var(--tone);padding-bottom:22px;margin-bottom:22px}
.r7 .row{display:flex;justify-content:space-between;align-items:center;gap:18px;font-size:30px;font-weight:800;padding:14px 0}
.r7 .row img{width:64px;border-radius:6px;border:3px solid var(--ink)}
.r7 .row .n{flex:1} .r7 .row small{display:block;font-size:20px;font-weight:700;color:var(--ink-soft)}
.r7 .row .up{color:var(--green)} .r7 .row .dn{color:var(--red)}
.r7 .total{border-top:4px dashed var(--tone);margin-top:22px;padding-top:30px;display:flex;justify-content:space-between;align-items:flex-end}
.r7 .total b{font-family:var(--display);font-weight:400;font-size:84px;color:var(--green);line-height:1}
.r7 .total span{font-size:22px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;color:var(--ink-soft)}
/* 08 vertical katakana */
.r8 .vk{position:absolute;left:60px;top:300px;writing-mode:vertical-rl;text-orientation:upright;font-family:var(--body);font-weight:900;font-size:230px;line-height:1;letter-spacing:.06em;color:var(--red);-webkit-text-stroke:6px var(--ink);text-shadow:14px 14px 0 var(--ink)}
.r8 .fan{position:absolute;left:330px;top:640px;width:800px;height:1000px}
.r8 .fan figure{width:330px} .r8 .fan .c1{left:0;top:6%} .r8 .fan .c2{left:22%;top:0} .r8 .fan .c3{left:44%;top:6%} .r8 .fan .c4{left:6%;top:36%} .r8 .fan .c5{left:30%;top:40%} .r8 .fan .c6{left:16%;top:66%}
.r8 .fan .sfx{display:none}
/* 09 split */
.r9 .half{position:absolute;top:0;bottom:0;width:50%;overflow:hidden}
.r9 .half.l{left:0;background:#F2F3EF} .r9 .half.d{right:0;background:#131316;clip-path:polygon(12% 0,100% 0,100% 100%,0 100%)}
.r9 .half .stg{left:50%;top:720px;transform:translateX(-50%) scale(2.55);transform-origin:top center}
.r9 .seam{position:absolute;top:0;bottom:0;left:50%;width:14px;background:#C8322E;transform:skewX(-6deg);z-index:5;border-left:4px solid #121114;border-right:4px solid #121114}
.r9 .lab{position:absolute;top:590px;font-family:var(--display);font-size:64px;letter-spacing:.04em;text-transform:uppercase;padding:10px 26px 6px;border:5px solid #121114;box-shadow:8px 8px 0 #121114;z-index:6}
/* 10 speech bubble */
.r10 .bubble{position:absolute;left:70px;right:70px;top:520px;background:var(--paper-2);border:7px solid var(--ink);border-radius:80px;padding:60px 64px 54px;box-shadow:16px 16px 0 var(--ink);text-align:center}
.r10 .bubble::after{content:"";position:absolute;left:120px;bottom:-64px;width:90px;height:90px;background:var(--paper-2);border:7px solid var(--ink);border-top:0;border-left:0;transform:rotate(45deg) skew(12deg,12deg)}
.r10 .steps{position:absolute;left:70px;right:70px;top:1330px;display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.r10 .steps div{background:var(--paper-2);border:5px solid var(--ink);box-shadow:8px 8px 0 var(--ink);padding:24px 18px;text-align:center;transform:rotate(-2deg)}
.r10 .steps div:nth-child(2){transform:rotate(2deg)} .r10 .steps div:nth-child(3){transform:rotate(-1deg)}
.r10 .steps b{display:block;font-family:var(--display);font-weight:400;font-size:70px;color:var(--red);line-height:1}
.r10 .steps span{display:block;font-size:24px;font-weight:900;margin-top:8px;line-height:1.2}
"""

WM_L = '../assets/logo/dexeon-wordmark-nav.png'
WM_D = '../assets/logo/dexeon-wordmark-nav-dark.png'

def mv(inner, theme):
    return '<div class="mv %s">%s</div>' % ('dk' if theme == 'dark' else '', inner)

def head(eyebrow, h1, size, extra='', align='center', left=80, width=None):
    w = f'width:{width}px;' if width else 'right:80px;'
    return (f'<div style="position:absolute;left:{left}px;{w}top:280px;text-align:{align}">'
            f'<span class="eyebrow" style="justify-content:{"center" if align=="center" else "flex-start"}">{eyebrow}</span>'
            f'<h1 class="big" style="font-size:{size}px;margin:18px 0 0;text-align:{align}">{h1}</h1>{extra}</div>')

REMIX = [
 dict(theme='light', cls='r1', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    + head('Now in beta · iPhone', 'One app.<br><span class="red">Every panel.</span>', 120) +
    f'<div class="cell" style="left:70px;top:600px;width:470px;height:520px"><div class="phone">{home}</div><span class="cap">Full Dex</span></div>'
    f'<div class="cell" style="left:560px;top:560px;width:450px;height:560px"><div class="phone" style="top:-330px">{chat}</div><span class="cap">Messages</span></div>'
    f'<div class="cell" style="left:70px;top:1140px;width:450px;height:540px"><div class="phone" style="top:-260px">{binder}</div><span class="cap">Binders</span></div>'
    f'<div class="cell" style="left:540px;top:1140px;width:470px;height:540px"><div class="phone" style="left:-30px;top:-250px">{leaderboard}</div><span class="cap">Gym Leaders</span></div>'
    '<span class="sfx" style="right:40px;top:1080px;transform:rotate(7deg)">GOTCHA!</span>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
 dict(theme='dark', cls='r2', body=(
    f'<img class="brand" src="{WM_D}" alt="">'
    '<div style="position:absolute;left:80px;right:80px;top:280px;text-align:center"><span class="eyebrow" style="justify-content:center">The Full Dex</span></div>'
    '<div class="num">1025</div>'
    '<div style="position:absolute;left:80px;right:80px;top:940px;text-align:center">'
    '<h1 class="big" style="font-size:104px;margin:0">species.<br><span class="red">one list.</span></h1>'
    '<p class="copy" style="margin:26px auto 0;max-width:820px">Tap the ring to catch one. Star your favorites. Watch the bar climb across nine generations.</p></div>'
    '<div class="strip">'
    '<img src="../assets/cards/sv7-143.jpg" alt=""><img class="g" src="../assets/cards/base1-46.jpg" alt=""><img src="../assets/cards/sv3pt5-199.jpg" alt=""><img src="../assets/cards/sv8-238.jpg" alt=""><img class="g" src="../assets/cards/sv3pt5-150.jpg" alt=""><img src="../assets/cards/sv4pt5-232.jpg" alt="">'
    '</div>'
    '<div class="stat-tag" style="left:70px;top:1480px;transform:rotate(-4deg)"><b>42%</b>caught so far</div>'
    '<div class="url" style="bottom:100px">dexeontcg.com · link in bio</div>')),
 dict(theme='light', cls='r3', body=(
    f'<img class="brand tl" src="{WM_L}" alt="">'
    + head("What's inside", 'Built for<br><span class="red">the shelf.</span>', 118, align='left', width=620) +
    '<div class="list"><span><i></i>1025-species Full Dex</span><span><i></i>Every printing, EN + JA</span><span><i></i>Live market prices</span><span><i></i>Scan a card to match it</span><span><i></i>Binders that page like binders</span><span><i></i>Trade board + DMs</span><span><i></i>Gym Leaders leaderboard</span></div>'
    f'<div class="stg">{home}</div>'
    '<span class="sfx y" style="left:70px;top:1495px;transform:rotate(-6deg)">ドン!</span>'
    '<div class="url left">dexeontcg.com · link in bio</div>')),
 dict(theme='dark', cls='r4', body=(
    f'<img class="brand" src="{WM_D}" alt="">'
    + head('Direct messages', 'Trade<br><span class="red">talk.</span>', 124) +
    mv(chatblk, 'dark') +
    '<span class="sfx y" style="right:60px;top:560px;transform:rotate(7deg)">やった!</span>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
 dict(theme='light', cls='r5', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    + head('Binders · 3×3', 'Page one,<br><span class="red">pocket seven.</span>', 110) +
    mv(page1, 'light') +
    '<span class="sfx" style="right:40px;top:1440px;transform:rotate(7deg)">SNAP!</span>'
    '<div class="stat-tag" style="left:60px;top:1480px;transform:rotate(-4deg)"><b>Drag</b>to swap any two pockets</div>'
    '<div class="url">dexeontcg.com · link in bio</div>')),
 dict(theme='dark', cls='r6', body=(
    '<div class="burst"></div>'
    f'<img class="brand" src="{WM_D}" alt="">'
    + head('Gym Leaders · weekly seasons', '<span class="red">Climb.</span>', 190,
           extra='<p class="copy" style="margin:22px auto 0;max-width:800px">Every trainer on the app, ranked by Full Dex, sets, weekly catches or arcade score.</p>') +
    mv(podium, 'dark') +
    '<div class="pill">You\'re #7 of 214</div>'
    '<span class="sfx" style="left:60px;top:700px;transform:rotate(-8deg)">DEAL!</span>'
    '<div class="url">dexeontcg.com · link in bio</div>')),
 dict(theme='light', cls='r7', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    + head('Collection value', 'Watch it<br><span class="red">grow.</span>', 118) +
    '<div class="receipt"><h3>Collection value</h3><div class="sub">updated daily · every copy counted</div>'
    '<div class="row"><img src="../assets/cards/sv3pt5-199.jpg" alt=""><span class="n">Charizard ex<small>151 · SIR · NM</small></span><span>$178.43 <span class="up">▲</span></span></div>'
    '<div class="row"><img src="../assets/cards/sv4pt5-232.jpg" alt=""><span class="n">Mew ex<small>Paldean Fates · NM</small></span><span>$120.00 <span class="up">▲</span></span></div>'
    '<div class="row"><img src="../assets/cards/base1-4.jpg" alt=""><span class="n">Charizard<small>Base Set · LP · ×2</small></span><span>$412.00 <span class="dn">▼</span></span></div>'
    '<div class="row"><img src="../assets/cards/swsh45sv-SV107.jpg" alt=""><span class="n">Charizard VMAX<small>Shining Fates · NM</small></span><span>$96.20 <span class="up">▲</span></span></div>'
    '<div class="row"><img src="../assets/cards/ja/SV2a-208.jpg" alt=""><span class="n">Mew ex · JA<small>151 · UR · PSA 9</small></span><span>$210.00 <span class="up">▲</span></span></div>'
    '<div class="total"><span>Total · 812 cards</span><b>$2,418.60</b></div></div>'
    '<div class="stat-tag" style="right:60px;top:1560px;transform:rotate(4deg)"><b>+$212</b>this month</div>'
    '<div class="url">dexeontcg.com · link in bio</div>')),
 dict(theme='dark', cls='r8', body=(
    f'<img class="brand tl" src="{WM_D}" alt="">'
    '<div class="vk">日本語も</div>'
    + head('Japanese sets · EN + JA', 'Every<br><span class="red">printing.</span>', 104, align='left', left=330, width=680) +
    fan +
    '<span class="sfx y" style="right:50px;top:1540px;transform:rotate(7deg)">全部!</span>'
    '<div class="url">dexeontcg.com · link in bio</div>')),
 dict(theme='light', cls='r9', body=(
    f'<div class="half l"><div class="stg">{home}</div></div>'
    f'<div class="half d"><div class="stg">{binder}</div></div>'
    '<div class="seam"></div>'
    f'<img class="brand tl" src="{WM_L}" alt="">'
    '<div style="position:absolute;left:60px;right:60px;top:270px;text-align:center;z-index:7"><span class="eyebrow" style="justify-content:center;color:#121114;background:#F2F3EF;border:4px solid #121114;padding:10px 22px 8px;display:inline-flex">Appearance</span>'
    '<h1 class="big" style="font-size:116px;margin:18px 0 0;color:#121114;text-shadow:7px 7px 0 #F2F3EF,13px 13px 0 #121114">Day shift.<br><span class="red">Night shift.</span></h1></div>'
    '<span class="lab" style="left:110px;background:#fff;color:#121114">Light</span>'
    '<span class="lab" style="right:110px;background:#1B1B1F;color:#F1F0EA;border-color:#F1F0EA;box-shadow:8px 8px 0 #F1F0EA">Dark</span>'
    '<div class="url" style="background:#121114;color:#F2F3EF;border-color:#F2F3EF">dexeontcg.com · link in bio</div>')),
 dict(theme='light', cls='r10', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    '<div style="position:absolute;left:80px;right:80px;top:280px;text-align:center"><span class="eyebrow" style="justify-content:center">Beta open now</span></div>'
    '<div class="bubble"><h1 class="big" style="font-size:150px;margin:0">Get in<br><span class="red">early.</span></h1>'
    '<p class="copy" style="margin:30px auto 0;max-width:760px">A select group of early adopters gets Dexeon free for life. The window closes before public launch.</p>'
    '<p style="margin:26px 0 0;font-size:26px;font-weight:900;color:var(--ink)">Otherwise $5.99 once at launch. Never a subscription.</p></div>'
    '<div class="steps"><div><b>1</b><span>Link in bio</span></div><div><b>2</b><span>Drop your email</span></div><div><b>3</b><span>TestFlight opens</span></div></div>'
    '<span class="sfx" style="right:60px;top:440px;transform:rotate(7deg)">GO!</span>'
    '<div class="url" style="bottom:130px">dexeontcg.com · link in bio</div>')),
]

os.makedirs('assets/social/stories/remix', exist_ok=True)
for f in glob.glob('marketing/remix-*.html'):
    os.remove(f)
for n, r in enumerate(REMIX, 1):
    body = f'<div class="shot {r["cls"]}"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>{r["body"]}</div>'
    open(f'marketing/remix-{n:02d}.html', 'w').write(
        f'<!doctype html>\n<html lang="en" data-theme="{r["theme"]}"><head>{HEAD}<style>{REMIX_CSS}</style></head><body>{body}</body></html>')

srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    for n in range(1, len(REMIX) + 1):
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1080,1920', '--virtual-time-budget=8000',
                        f'--screenshot=assets/social/stories/remix/remix-{n:02d}.png',
                        f'http://localhost:8765/marketing/remix-{n:02d}.html'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('rendered remix', n)
finally:
    srv.terminate()

for f in glob.glob("marketing/remix-*.html"):
    os.remove(f)
