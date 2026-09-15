# Writes marketing/live-story.html: a 14-second, one-continuous-shot Instagram
# Story (1080x1920) that looks like someone using Dexeon. One phone, the landing
# page's real screens stacked inside it, iOS-style pushes between them, tap
# rings, a scroll, a card being dragged into a binder pocket, a DM arriving.
# Run from the repo root, then render with:
#   python3 marketing/live-story.py && python3 marketing/logo-story.py --page live-story --dur 14
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
src = open('index.html').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)

def block(text, start_tag, from_index=0):
    i = text.index(start_tag, from_index); depth = 0; j = i
    for m in re.finditer(r'<div\b|</div>', text[i:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth == 0:
            j = i + m.end(); break
    return text[i:j]

def screen(marker, cls):
    i = src.index(marker)
    s = block(src, '<div class="screen', i)
    s = s.replace('src="assets/', 'src="../assets/').replace('class="screen dark"', 'class="screen"')
    return s.replace('class="screen"', f'class="screen {cls}"', 1)

s_home, s_profile, s_binder, s_chat = (screen(f'Mockup {n}:', c) for n, c in ((1, 's1'), (2, 's3'), (3, 's4'), (6, 's5')))

STATUS = '''<div class="status"><span>9:41</span><span class="r">
<svg viewBox="0 0 14 11"><rect x="0" y="7" width="2.5" height="4"/><rect x="3.8" y="5" width="2.5" height="6"/><rect x="7.6" y="2.5" width="2.5" height="8.5"/><rect x="11.4" y="0" width="2.5" height="11"/></svg>
<svg viewBox="0 0 24 11"><rect class="bat" x="0.5" y="0.5" width="20" height="10" rx="3"/><rect x="2" y="2" width="16" height="7" rx="1.5"/><rect x="21.5" y="3.5" width="2" height="4" rx="1"/></svg>
</span></div>'''
s_card = f'''<div class="screen s2">
{STATUS}
<div class="navbar"><span class="acc">Done</span><span class="t">Charizard ex</span><span style="width:26px"></span></div>
<div class="pad cd">
  <div class="cd-img"><img src="../assets/cards/sv3pt5-199.jpg" alt=""></div>
  <div class="cd-title"><b>151</b><div class="cd-tags"><span>Special Illustration Rare</span><span>#199</span></div></div>
  <div class="cd-price mp">
    <small class="sec">Market Price</small>
    <div class="cd-big">$178.43</div>
    <small class="sec">Holofoil · Market</small>
    <div class="cd-row"><div><small class="sec">Low</small><b>$150.00</b></div><div><small class="sec">Mid</small><b>$180.00</b></div><div><small class="sec">High</small><b>$349.99</b></div></div>
  </div>
  <div class="cd-actions">
    <span class="on g"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10" fill="currentColor"/><path d="M7.5 12.5l3 3 6-6.5" fill="none" stroke="#34C759" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>Collected</span>
    <span class="b chase"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.2" fill="currentColor"/></svg>Chase</span>
    <span class="on o"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3 6.6 7 .9-5.2 4.9 1.4 7.1L12 18l-6.2 3.5 1.4-7.1L2 9.5l7-.9z"/></svg>Showcasing</span>
    <span class="k"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M4 8h13l-3-3M20 16H7l3 3"/></svg>Trade</span>
  </div>
  <div class="cd-link sec">↗ Price history · 90 days</div>
</div>
<div class="home-bar"></div>
</div>'''

# The DM that "arrives" during the shot, and the reply typed after it.
s_chat = s_chat.replace('<div class="msg them">deal 🤝 the Gengar too and we\'re square</div>',
                        '<div class="msg them arrive">deal 🤝 the Gengar too and we\'re square</div>'
                        '<div class="msg me reply">DEAL. Shipping tomorrow 📦</div>')
# Notification banner that drops into the binder screen when Maple replies.
s_binder = s_binder.replace('<div class="status">',
    '<div class="notif"><div class="av" style="background:#2FA44F">M</div><div><b>Maple</b><small>deal 🤝 the Gengar too and we\'re square</small></div><span class="now">now</span></div>'
    '<div class="tap" style="left:150px;top:60px;animation-delay:9.55s"></div><div class="status">', 1)

TAPS = {  # screen-space taps: (class, x, y, time)
    's1': [(79, 320, 2.05), (277, 70, 5.35)],
    's2': [(30, 64, 4.55), (128, 488, 3.75)],
    's3': [(82, 455, 6.45)],
    's5': [(150, 590, 11.15)],
}
def taps(cls):
    return ''.join(f'<div class="tap" style="left:{x}px;top:{y}px;animation-delay:{t}s"></div>' for x, y, t in TAPS.get(cls, []))
def with_taps(s, cls):
    k = s.rindex('</div>')
    return s[:k] + taps(cls) + s[k:]

CSS = """
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:var(--paper);color:var(--ink);font-family:var(--body)}
.shot{position:relative;width:1080px;height:1920px;overflow:hidden}
.halft{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.2px,transparent 3px);background-size:22px 22px;opacity:.55}
.kana{position:absolute;left:-60px;top:1180px;font-size:520px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:3px #d9dbd4;white-space:nowrap;letter-spacing:-.04em;animation:drift 14s linear both}
@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-160px)}}
.speed{position:absolute;inset:-20%;opacity:.12;background:repeating-conic-gradient(from 0deg at 50% 55%, var(--ink) 0deg .5deg, transparent .5deg 5deg);
  -webkit-mask:radial-gradient(circle at 50% 55%, transparent 30%, #000 50%, #000 70%, transparent 90%);mask:radial-gradient(circle at 50% 55%, transparent 30%, #000 50%, #000 70%, transparent 90%)}
.wm{position:absolute;left:50%;top:100px;width:280px;margin-left:-140px;z-index:30;animation:drop .45s cubic-bezier(.2,1.3,.4,1) .15s both}
.wm img{width:100%;display:block}
@keyframes drop{from{opacity:0;transform:translateY(-90px)}to{opacity:1;transform:translateY(0)}}
.cap{position:absolute;left:0;right:0;top:250px;text-align:center;font-size:28px;font-weight:900;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-soft);z-index:30;animation:drop .45s cubic-bezier(.2,1.3,.4,1) .4s both}
.cap::before,.cap::after{content:"";display:inline-block;width:60px;height:7px;background:var(--red);vertical-align:middle;margin:0 20px}

.phone,.rv,.hero-stage .phone{animation:none !important;transition:none !important;opacity:1 !important}
.stg{position:absolute;left:0;top:0;transform-origin:top left;z-index:5;transform:translate(188px,330px) scale(2.2)}
.stg .phone{position:relative;transform:none}
.clip{position:absolute;inset:10px;border-radius:41px;overflow:hidden}
.clip .screen{inset:0}
.s1{z-index:1}.s2{z-index:2}.s3{z-index:3}.s4{z-index:4}.s5{z-index:5}
.s2,.s3,.s4,.s5{transform:translateX(102%)}
@keyframes pushIn{from{transform:translateX(102%)}to{transform:translateX(0)}}
@keyframes pushOut{from{transform:translateX(0)}to{transform:translateX(102%)}}
@keyframes under{from{transform:translateX(0)}to{transform:translateX(-28%)}}
@keyframes unUnder{from{transform:translateX(-28%)}to{transform:translateX(0)}}
.s2{animation:pushIn .45s cubic-bezier(.2,.8,.2,1) 2.4s forwards, pushOut .45s cubic-bezier(.4,0,.6,1) 4.7s forwards}
.s1{animation:under .45s cubic-bezier(.2,.8,.2,1) 2.4s forwards, unUnder .45s cubic-bezier(.2,.8,.2,1) 4.7s forwards}
.s3{animation:pushIn .45s cubic-bezier(.2,.8,.2,1) 5.55s forwards}
.s4{animation:pushIn .45s cubic-bezier(.2,.8,.2,1) 6.7s forwards}
.s5{animation:pushIn .45s cubic-bezier(.2,.8,.2,1) 9.8s forwards}

/* home: header stays put, grid scrolls up under it */
.s1 .status,.s1 .hdr,.s1 .fbar{position:relative;z-index:3;background:var(--p)}
.s1 .grid2{animation:scroll .75s cubic-bezier(.3,.7,.2,1) .9s forwards}
@keyframes scroll{from{transform:translateY(0)}to{transform:translateY(-112px)}}
/* card detail: chase toggles on */
.s2 .cd-actions .chase{animation:chaseOn .25s ease-out 3.95s forwards}
@keyframes chaseOn{to{background:var(--b);color:#fff}}
/* binder: the dragged card lands in the pocket, outline releases */
.s4 .slot.drag img{animation:land .8s cubic-bezier(.2,.9,.2,1) 7.7s forwards}
@keyframes land{from{transform:translate(-26px,-30px) rotate(-7deg) scale(1.1)}70%{transform:translate(-88px,4px) rotate(2deg) scale(1.02);box-shadow:0 6px 12px rgba(0,0,0,.35)}to{transform:translate(-88px,0) rotate(0) scale(1);box-shadow:none}}
.s4 .slot.target{animation:release .3s ease-out 8.5s forwards} .s4 .slot.drag::before{animation:release .3s ease-out 8.5s forwards}
@keyframes release{to{outline-color:transparent;border-color:transparent;background:transparent}}
.s4 .slot.target svg{animation:release2 .3s ease-out 8.5s forwards} @keyframes release2{to{opacity:0}}
/* notification banner */
.notif{position:absolute;left:8px;right:8px;top:40px;z-index:20;display:flex;align-items:center;gap:8px;padding:8px 10px;border-radius:14px;background:var(--p2);color:var(--i);box-shadow:0 10px 24px rgba(0,0,0,.3);transform:translateY(-130px);
       animation:notifIn .45s cubic-bezier(.2,1.1,.3,1) 9.0s forwards, notifOut .3s ease-in 9.85s forwards}
.notif .av{width:26px;height:26px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:900;font-size:12px;flex:none}
.notif b{display:block;font-size:10px} .notif small{display:block;font-size:9.5px;font-weight:600;color:var(--is)} .notif .now{margin-left:auto;font-size:8.5px;font-weight:700;color:var(--is);align-self:flex-start}
@keyframes notifIn{from{transform:translateY(-130px)}to{transform:translateY(0)}}
@keyframes notifOut{from{transform:translateY(0)}to{transform:translateY(-130px)}}
/* chat: the message arrives, then the reply */
.s5 .msg.arrive{animation:bubble .4s cubic-bezier(.2,1.3,.4,1) 10.45s both}
.s5 .msg.reply{animation:bubble .4s cubic-bezier(.2,1.3,.4,1) 11.55s both}
@keyframes bubble{from{opacity:0;transform:translateY(14px) scale(.85)}to{opacity:1;transform:translateY(0) scale(1)}}
.s5 .chat{justify-content:flex-end}

/* tap ring, in screen pixels */
.tap{position:absolute;width:40px;height:40px;margin:-20px 0 0 -20px;border-radius:50%;background:rgba(200,50,46,.28);border:3px solid var(--r);z-index:60;opacity:0;pointer-events:none;
     animation:tapk .55s ease-out both}
@keyframes tapk{0%{opacity:0;transform:scale(.3)}25%{opacity:1;transform:scale(.9)}100%{opacity:0;transform:scale(1.7)}}

/* end card */
.end{position:absolute;left:0;right:0;bottom:0;height:520px;background:var(--ink);color:var(--paper);z-index:40;transform:translateY(100%);animation:endIn .55s cubic-bezier(.2,.9,.2,1) 12.5s forwards;text-align:center;padding-top:70px;box-sizing:border-box;border-top:10px solid var(--red)}
@keyframes endIn{from{transform:translateY(100%)}to{transform:translateY(0)}}
.end h1{margin:0;font-family:var(--display);font-weight:400;font-size:150px;line-height:.9;text-transform:uppercase;transform:skewX(-6deg);text-shadow:8px 8px 0 var(--ink),15px 15px 0 var(--red)}
.end h1 .red{color:var(--red);text-shadow:8px 8px 0 var(--ink),15px 15px 0 var(--paper)}
.end .pill{display:inline-block;margin-top:44px;background:var(--paper);color:var(--ink);font-weight:900;font-size:34px;letter-spacing:.08em;padding:22px 48px;border:5px solid var(--ink);box-shadow:12px 12px 0 var(--red);animation:pillpop .5s cubic-bezier(.2,1.4,.4,1) 13.0s both}
@keyframes pillpop{0%{opacity:0;transform:scale(.5)}65%{opacity:1;transform:scale(1.08)}100%{opacity:1;transform:scale(1)}}
"""

HTML = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<title>Dexeon live story</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">
<style>{style}</style>
<style>{CSS}</style>
</head>
<body>
<div class="shot">
  <div class="halft"></div>
  <div class="kana" aria-hidden="true">デクセオン</div>
  <div class="speed"></div>
  <div class="wm"><img src="../assets/logo/dexeon-wordmark-nav.png" alt="Dexeon"></div>
  <div class="cap">Now in beta · iPhone</div>
  <div class="stg"><div class="phone"><div class="island"></div><div class="clip">
    {with_taps(s_home, 's1')}
    {with_taps(s_card, 's2')}
    {with_taps(s_profile, 's3')}
    {s_binder}
    {with_taps(s_chat, 's5')}
  </div></div></div>
  <div class="end"><h1>Track <span class="red">’Em All.</span></h1><div class="pill">dexeontcg.com · free during beta</div></div>
</div>
<script>
  var m = location.search.match(/[?&]t=([\\d.]+)/);
  if (m) {{
    var t = parseFloat(m[1]) * 1000;
    document.body.offsetWidth;
    document.getAnimations().forEach(function (a) {{ a.pause(); a.currentTime = t; }});
  }}
</script>
</body>
</html>
"""
open('marketing/live-story.html', 'w').write(HTML)
print('wrote marketing/live-story.html')
