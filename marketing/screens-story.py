# Writes marketing/screens-story.html: a kinetic-type Instagram Story (1080x1920,
# 11 s) that pairs each type beat with the landing page's real phone mockups.
# Run from the repo root, then render with:
#   python3 marketing/screens-story.py && python3 marketing/logo-story.py --page screens-story --dur 11
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
# The live page now shows real simulator captures, so the illustrated phone
# mockups it used to carry were moved to marketing/mockups.html. Appending that
# file keeps `Mockup 1/2/3` (and the grid2 / page blocks inside them) findable,
# while `style` still comes from index.html's first <style> block.
src = open('index.html').read() + open(os.path.join('marketing', 'mockups.html'), encoding='utf-8').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)

def grab_phone(marker):
    i = src.index(marker); i = src.index('<div class="phone', i)
    depth = 0; j = i
    for m in re.finditer(r'<div\b|</div>', src[i:]):
        depth += 1 if m.group(0).startswith('<div') else -1
        if depth == 0:
            j = i + m.end(); break
    return (src[i:j].replace('src="assets/', 'src="../assets/').replace(' id="heroPhone"', '')
            .replace('class="phone back"', 'class="phone"').replace('class="phone front"', 'class="phone"'))

home, binder, leaderboard, chat, trades = (grab_phone(f'Mockup {n}:') for n in (1, 3, 5, 6, 7))

CSS = """
html,body{margin:0;width:1080px;height:1920px;overflow:hidden;background:var(--paper);color:var(--ink);font-family:var(--body)}
.shot{position:relative;width:1080px;height:1920px;overflow:hidden}
.halft{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.2px,transparent 3px);background-size:22px 22px;opacity:.55}
.kana{position:absolute;left:-60px;top:1180px;font-size:520px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:3px #d9dbd4;white-space:nowrap;letter-spacing:-.04em;animation:drift 11s linear both}
@keyframes drift{from{transform:translateX(0)}to{transform:translateX(-160px)}}
.wm{position:absolute;left:50%;top:110px;width:300px;margin-left:-150px;z-index:30;animation:drop .45s cubic-bezier(.2,1.3,.4,1) .15s both}
.wm img{width:100%;display:block}
@keyframes drop{from{opacity:0;transform:translateY(-90px)}to{opacity:1;transform:translateY(0)}}
.rule{position:absolute;left:50%;top:290px;width:120px;height:10px;margin-left:-60px;background:var(--red);z-index:30;animation:grow .35s ease-out .5s both}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}

/* the mockups: kill the landing page's own motion so only the timeline moves them */
.phone,.rv,.hero-stage .phone{animation:none !important;transition:none !important;opacity:1 !important}
.stg{position:absolute;left:0;top:0;transform-origin:top left;z-index:5}
.stg .phone{position:relative;transform:none}

.beat{position:absolute;inset:0}
.words{position:absolute;left:70px;right:70px;z-index:10}
.words .l{display:block;font-family:var(--display);font-size:200px;line-height:.9;text-transform:uppercase;transform:skewX(-6deg);text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);white-space:nowrap}
.words .l.red{color:var(--red)} .words .l.c{text-align:center} .words .l.r{text-align:right}
.chip{position:absolute;z-index:12;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:18px 34px;font-size:34px;font-weight:900;white-space:nowrap}
.stk{position:absolute;z-index:12;font-family:'Bangers',var(--display);font-size:96px;letter-spacing:.04em;color:var(--ink);background:var(--yellow);border:7px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:12px 36px 6px;line-height:1}
.stk.w{background:var(--paper-2)} .stk.r{background:var(--red);color:#fff}

@keyframes cutL{from{opacity:0;transform:skewX(-6deg) translateX(-260px)}60%{opacity:1;transform:skewX(-6deg) translateX(24px)}to{opacity:1;transform:skewX(-6deg) translateX(0)}}
@keyframes cutR{from{opacity:0;transform:skewX(-6deg) translateX(260px)}60%{opacity:1;transform:skewX(-6deg) translateX(-24px)}to{opacity:1;transform:skewX(-6deg) translateX(0)}}
@keyframes stamp{from{opacity:0;transform:skewX(-6deg) scale(1.7)}55%{opacity:1;transform:skewX(-6deg) scale(.94)}to{opacity:1;transform:skewX(-6deg) scale(1)}}
@keyframes riseW{from{opacity:0;transform:skewX(-6deg) translateY(160px)}65%{opacity:1;transform:skewX(-6deg) translateY(-18px)}to{opacity:1;transform:skewX(-6deg) translateY(0)}}
@keyframes pop{0%{opacity:0;transform:scale(0) rotate(-30deg)}65%{opacity:1;transform:scale(1.18) rotate(-3deg)}100%{opacity:1;transform:scale(1) rotate(var(--rot,-6deg))}}
@keyframes lift{from{opacity:1;transform:translateY(0)}to{opacity:0;transform:translateY(-90px)}}

.sweep{position:absolute;top:-10%;bottom:-10%;left:-45%;width:190%;background:var(--red);transform:translateX(-120%) skewX(-12deg);z-index:20}
@keyframes sweep{from{transform:translateX(-120%) skewX(-12deg)}to{transform:translateX(120%) skewX(-12deg)}}
.sweep.s1{animation:sweep .55s cubic-bezier(.75,0,.2,1) 2.85s forwards}
.sweep.s2{background:var(--ink);animation:sweep .55s cubic-bezier(.75,0,.2,1) 5.45s forwards}
.sweep.s3{background:var(--yellow);animation:sweep .55s cubic-bezier(.75,0,.2,1) 8.05s forwards}

/* beat 1 : all 1025 species + home screen  (0.5 -> 3.0) */
.b1{animation:lift .3s ease-in 2.95s forwards}
.b1 .words{top:380px}
.b1 .l1{animation:cutL .45s cubic-bezier(.2,.9,.2,1) .5s both}
.b1 .l2{animation:cutL .45s cubic-bezier(.2,.9,.2,1) .66s both;font-size:260px}
.b1 .l3{animation:cutL .45s cubic-bezier(.2,.9,.2,1) .82s both}
@keyframes p1{from{transform:translate(360px,2100px) rotate(-6deg) scale(1.9)}70%{transform:translate(360px,940px) rotate(-6deg) scale(1.9)}to{transform:translate(360px,980px) rotate(-6deg) scale(1.9)}}
.b1 .stg{animation:p1 .8s cubic-bezier(.2,.9,.2,1) .95s both}
.b1 .stk{left:70px;top:1180px;--rot:-8deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) 1.8s both}
.b1 .chip{left:70px;top:1400px;--rot:-3deg;transform:rotate(-3deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) 2.1s both}

/* beat 2 : binders + binder screen  (3.1 -> 5.6) */
.b2{animation:lift .3s ease-in 5.55s forwards}
.b2 .words{top:380px}
.b2 .l1{animation:stamp .4s cubic-bezier(.2,1,.3,1) 3.15s both}
.b2 .l2{animation:stamp .4s cubic-bezier(.2,1,.3,1) 3.32s both}
.b2 .l3{animation:stamp .4s cubic-bezier(.2,1,.3,1) 3.5s both}
@keyframes p2{from{transform:translate(-1000px,900px) rotate(6deg) scale(1.9)}70%{transform:translate(20px,900px) rotate(6deg) scale(1.9)}to{transform:translate(-20px,900px) rotate(6deg) scale(1.9)}}
.b2 .stg{animation:p2 .8s cubic-bezier(.2,.9,.2,1) 3.6s both}
.b2 .chip{right:60px;top:1240px;--rot:4deg;transform:rotate(4deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) 4.5s both}
.b2 .chip.two{top:1400px;--rot:-2deg;transform:rotate(-2deg);animation-delay:4.7s}
.b2 .stk{right:80px;top:1560px;--rot:6deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) 4.95s both}

/* beat 3 : trade dm climb + chat & leaderboard  (5.7 -> 8.2) */
.b3{animation:lift .3s ease-in 8.15s forwards}
.b3 .words{top:380px}
.b3 .l1{animation:cutL .45s cubic-bezier(.2,.9,.2,1) 5.75s both}
.b3 .l2{animation:cutR .45s cubic-bezier(.2,.9,.2,1) 5.95s both}
@keyframes p3a{from{transform:translate(-900px,820px) rotate(-8deg) scale(1.6)}70%{transform:translate(20px,820px) rotate(-8deg) scale(1.6)}to{transform:translate(-10px,820px) rotate(-8deg) scale(1.6)}}
@keyframes p3b{from{transform:translate(1500px,900px) rotate(7deg) scale(1.6)}70%{transform:translate(520px,900px) rotate(7deg) scale(1.6)}to{transform:translate(550px,900px) rotate(7deg) scale(1.6)}}
.b3 .stg.a{animation:p3a .8s cubic-bezier(.2,.9,.2,1) 6.1s both;z-index:5}
.b3 .stg.b{animation:p3b .8s cubic-bezier(.2,.9,.2,1) 6.3s both;z-index:6}
.b3 .stk.a{left:60px;top:1620px;--rot:-8deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) 7.1s both}
.b3 .stk.b{right:60px;top:1600px;--rot:6deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) 7.3s both}

/* beat 4 : track 'em all + three phones  (8.3 -> end) */
.b4 .words{top:360px}
.b4 .l1{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) 8.35s both}
.b4 .l2{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) 8.52s both}
@keyframes p4a{from{transform:translate(300px,2100px) scale(1.5)}70%{transform:translate(300px,1010px) scale(1.5)}to{transform:translate(300px,1040px) scale(1.5)}}
@keyframes p4b{from{transform:translate(-40px,2200px) rotate(-12deg) scale(1.35)}70%{transform:translate(-40px,1110px) rotate(-12deg) scale(1.35)}to{transform:translate(-40px,1140px) rotate(-12deg) scale(1.35)}}
@keyframes p4c{from{transform:translate(700px,2200px) rotate(12deg) scale(1.35)}70%{transform:translate(700px,1110px) rotate(12deg) scale(1.35)}to{transform:translate(700px,1140px) rotate(12deg) scale(1.35)}}
.b4 .stg.a{animation:p4a .8s cubic-bezier(.2,.9,.2,1) 8.9s both;z-index:7}
.b4 .stg.b{animation:p4b .8s cubic-bezier(.2,.9,.2,1) 8.75s both;z-index:5}
.b4 .stg.c{animation:p4c .8s cubic-bezier(.2,.9,.2,1) 9.05s both;z-index:5}
.eyebrow2{position:absolute;left:0;right:0;top:830px;text-align:center;font-size:30px;font-weight:900;letter-spacing:.26em;text-transform:uppercase;color:var(--ink-soft);z-index:10;animation:fade .4s ease-out 9.6s both}
.eyebrow2::before,.eyebrow2::after{content:"";display:inline-block;width:70px;height:8px;background:var(--red);vertical-align:middle;margin:0 24px}
@keyframes fade{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.pill{position:absolute;left:50%;top:910px;z-index:10;background:var(--ink);color:var(--paper);font-weight:900;font-size:36px;letter-spacing:.08em;padding:24px 52px;border:5px solid var(--paper);box-shadow:12px 12px 0 var(--red);white-space:nowrap;animation:pillpop .5s cubic-bezier(.2,1.4,.4,1) 9.95s both}
@keyframes pillpop{0%{opacity:0;transform:translateX(-50%) scale(.5)}65%{opacity:1;transform:translateX(-50%) scale(1.08)}100%{opacity:1;transform:translateX(-50%) scale(1)}}
.b4 .stk{right:40px;top:1700px;--rot:7deg;z-index:12;animation:pop .45s cubic-bezier(.2,1.4,.4,1) 10.3s both}
"""

HTML = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<title>Dexeon screens story</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">
<style>{style}</style>
<style>{CSS}</style>
</head>
<body>
<div class="shot">
  <div class="halft"></div>
  <div class="kana" aria-hidden="true">デクセオン</div>
  <div class="wm"><img src="../assets/logo/dexeon-wordmark-nav.png" alt="Dexeon"></div>
  <div class="rule"></div>

  <div class="beat b1">
    <div class="words"><span class="l l1">All</span><span class="l l2 red">1025</span><span class="l l3">Species.</span></div>
    <div class="stg">{home}</div>
    <div class="stk">GOTCHA!</div>
    <div class="chip">Tap the ring to catch one</div>
  </div>

  <div class="beat b2">
    <div class="words"><span class="l l1 r">Binders</span><span class="l l2 r red">that page</span><span class="l l3 r">like binders.</span></div>
    <div class="stg">{binder}</div>
    <div class="chip">Drag. Drop. Share.</div>
    <div class="chip two">Print the whole thing.</div>
    <div class="stk w">ドン!</div>
  </div>

  <div class="beat b3">
    <div class="words"><span class="l l1">Trade. <span class="red">DM.</span></span><span class="l l2 r">Climb.</span></div>
    <div class="stg a">{chat}</div>
    <div class="stg b">{leaderboard}</div>
    <div class="stk a">DEAL!</div>
    <div class="stk b w">やった!</div>
  </div>

  <div class="beat b4">
    <div class="words"><span class="l l1 c">Track</span><span class="l l2 c red">’Em All.</span></div>
    <div class="eyebrow2">Free during beta · iPhone</div>
    <div class="pill">dexeontcg.com</div>
    <div class="stg b">{binder}</div>
    <div class="stg c">{trades}</div>
    <div class="stg a">{home}</div>
    <div class="stk">GO!</div>
  </div>

  <div class="sweep s1"></div>
  <div class="sweep s2"></div>
  <div class="sweep s3"></div>
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
open('marketing/screens-story.html', 'w').write(HTML)
print('wrote marketing/screens-story.html')
