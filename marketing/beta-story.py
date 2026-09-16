# Writes marketing/beta-story.html: a 15-second Instagram Story (1080x1920) built
# from REAL simulator screenshots of Dexeon (marketing/shots/*.png, captured with
# `xcrun simctl io booted screenshot`) inside a phone bezel, with the site's
# kinetic type and panel sweeps, ending on a beta call to action.
# Run from the repo root, then render with:
#   python3 marketing/beta-story.py && python3 marketing/logo-story.py --page beta-story --dur 15
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
src = open('index.html').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
WM_L = '../assets/logo/dexeon-wordmark-nav.png'

def ph(name, cls=''):
    return f'<div class="stg {cls}"><div class="ph"><img src="shots/{name}.png" alt=""></div></div>'

# beat starts (sweeps fire .2s earlier)
b1, b2, b3, b4, b5 = 0.5, 3.3, 6.1, 8.9, 11.7

CSS = f"""
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:var(--paper);color:var(--ink);font-family:var(--body)}}
.shot{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.halft{{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.2px,transparent 3px);background-size:22px 22px;opacity:.55}}
.kana{{position:absolute;left:-60px;top:1180px;font-size:520px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:3px #d9dbd4;white-space:nowrap;letter-spacing:-.04em;animation:drift 15s linear both}}
@keyframes drift{{from{{transform:translateX(0)}}to{{transform:translateX(-160px)}}}}
.wm{{position:absolute;left:50%;top:100px;width:280px;margin-left:-140px;z-index:30;animation:drop .45s cubic-bezier(.2,1.3,.4,1) .15s both}}
.wm img{{width:100%;display:block}}
@keyframes drop{{from{{opacity:0;transform:translateY(-90px)}}to{{opacity:1;transform:translateY(0)}}}}
.rule{{position:absolute;left:50%;top:290px;width:120px;height:10px;margin-left:-60px;background:var(--red);z-index:30;animation:grow .35s ease-out .5s both}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}

/* real-screenshot phone */
.stg{{position:absolute;left:0;top:0;transform-origin:top left;z-index:5}}
.ph{{width:402px;height:874px;box-sizing:border-box;padding:12px;background:#0d0d0f;border-radius:66px;box-shadow:0 40px 80px -30px rgba(0,0,0,.55),0 0 0 2px #2b2b30 inset,0 0 0 3px #121114;position:relative}}
.ph::before{{content:"";position:absolute;top:22px;left:50%;transform:translateX(-50%);width:120px;height:34px;background:#0d0d0f;border-radius:20px;z-index:2}}
.ph img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:54px;display:block}}

.beat{{position:absolute;inset:0}}
.words{{position:absolute;left:70px;right:70px;z-index:10}}
.words .l{{display:block;font-family:var(--display);font-size:190px;line-height:.9;text-transform:uppercase;transform:skewX(-6deg);text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);white-space:nowrap}}
.words .l.red{{color:var(--red)}} .words .l.c{{text-align:center}} .words .l.r{{text-align:right}}
.chip{{position:absolute;z-index:12;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:18px 34px;font-size:32px;font-weight:900;white-space:nowrap}}
.stk{{position:absolute;z-index:12;font-family:'Bangers',var(--display);font-size:92px;letter-spacing:.04em;color:var(--ink);background:var(--yellow);border:7px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:12px 36px 6px;line-height:1}}
.stk.w{{background:var(--paper-2)}}

@keyframes cutL{{from{{opacity:0;transform:skewX(-6deg) translateX(-260px)}}60%{{opacity:1;transform:skewX(-6deg) translateX(24px)}}to{{opacity:1;transform:skewX(-6deg) translateX(0)}}}}
@keyframes cutR{{from{{opacity:0;transform:skewX(-6deg) translateX(260px)}}60%{{opacity:1;transform:skewX(-6deg) translateX(-24px)}}to{{opacity:1;transform:skewX(-6deg) translateX(0)}}}}
@keyframes stamp{{from{{opacity:0;transform:skewX(-6deg) scale(1.7)}}55%{{opacity:1;transform:skewX(-6deg) scale(.94)}}to{{opacity:1;transform:skewX(-6deg) scale(1)}}}}
@keyframes riseW{{from{{opacity:0;transform:skewX(-6deg) translateY(160px)}}65%{{opacity:1;transform:skewX(-6deg) translateY(-18px)}}to{{opacity:1;transform:skewX(-6deg) translateY(0)}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(0) rotate(-30deg)}}65%{{opacity:1;transform:scale(1.18) rotate(-3deg)}}100%{{opacity:1;transform:scale(1) rotate(var(--rot,-6deg))}}}}
@keyframes popC{{0%{{opacity:0;transform:translateX(-50%) scale(0) rotate(-30deg)}}65%{{opacity:1;transform:translateX(-50%) scale(1.18) rotate(-3deg)}}100%{{opacity:1;transform:translateX(-50%) scale(1) rotate(-2deg)}}}}
@keyframes lift{{from{{opacity:1;transform:translateY(0)}}to{{opacity:0;transform:translateY(-90px)}}}}
@keyframes fade{{from{{opacity:0;transform:translateY(30px)}}to{{opacity:1;transform:translateY(0)}}}}

.sweep{{position:absolute;top:-10%;bottom:-10%;left:-45%;width:190%;transform:translateX(-120%) skewX(-12deg);z-index:20}}
@keyframes sweep{{from{{transform:translateX(-120%) skewX(-12deg)}}to{{transform:translateX(120%) skewX(-12deg)}}}}
.s1{{background:var(--red);animation:sweep .55s cubic-bezier(.75,0,.2,1) {b2-.2:.2f}s forwards}}
.s2{{background:var(--ink);animation:sweep .55s cubic-bezier(.75,0,.2,1) {b3-.2:.2f}s forwards}}
.s3{{background:var(--yellow);animation:sweep .55s cubic-bezier(.75,0,.2,1) {b4-.2:.2f}s forwards}}
.s4{{background:var(--red);animation:sweep .55s cubic-bezier(.75,0,.2,1) {b5-.2:.2f}s forwards}}

/* 1: all 1025 + home */
.b1{{animation:lift .3s ease-in {b2-.15:.2f}s forwards}}
.b1 .words{{top:380px}}
.b1 .l1{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b1:.2f}s both}}
.b1 .l2{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b1+.16:.2f}s both;font-size:250px}}
.b1 .l3{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b1+.32:.2f}s both}}
@keyframes p1{{from{{transform:translate(300px,2100px) rotate(-5deg) scale(1.55)}}70%{{transform:translate(300px,920px) rotate(-5deg) scale(1.55)}}to{{transform:translate(300px,960px) rotate(-5deg) scale(1.55)}}}}
.b1 .stg{{animation:p1 .8s cubic-bezier(.2,.9,.2,1) {b1+.45:.2f}s both}}
.b1 .stk{{left:60px;top:1160px;--rot:-8deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b1+1.3:.2f}s both}}
.b1 .chip{{left:60px;top:1380px;--rot:-3deg;transform:rotate(-3deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b1+1.6:.2f}s both}}

/* 2: prices + species + card price */
.b2{{animation:lift .3s ease-in {b3-.15:.2f}s forwards}}
.b2 .words{{top:380px}}
.b2 .l1{{animation:stamp .4s cubic-bezier(.2,1,.3,1) {b2+.05:.2f}s both;font-size:148px}}
.b2 .l2{{animation:stamp .4s cubic-bezier(.2,1,.3,1) {b2+.22:.2f}s both;font-size:148px}}
@keyframes p2a{{from{{transform:translate(-800px,860px) rotate(-8deg) scale(1.3)}}70%{{transform:translate(40px,860px) rotate(-8deg) scale(1.3)}}to{{transform:translate(10px,860px) rotate(-8deg) scale(1.3)}}}}
@keyframes p2b{{from{{transform:translate(1500px,900px) rotate(6deg) scale(1.45)}}70%{{transform:translate(440px,900px) rotate(6deg) scale(1.45)}}to{{transform:translate(470px,900px) rotate(6deg) scale(1.45)}}}}
.b2 .stg.a{{animation:p2a .8s cubic-bezier(.2,.9,.2,1) {b2+.5:.2f}s both;z-index:5}}
.b2 .stg.b{{animation:p2b .8s cubic-bezier(.2,.9,.2,1) {b2+.7:.2f}s both;z-index:6}}
.b2 .chip{{left:50%;top:740px;transform:translateX(-50%) rotate(-2deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b2+1.6:.2f}s both}}
.b2 .stk{{left:60px;top:1640px;--rot:-6deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b2+1.9:.2f}s both}}

/* 3: binders */
.b3{{animation:lift .3s ease-in {b4-.15:.2f}s forwards}}
.b3 .words{{top:380px}}
.b3 .l1{{animation:cutR .45s cubic-bezier(.2,.9,.2,1) {b3+.05:.2f}s both;font-size:180px}}
.b3 .l2{{animation:cutR .45s cubic-bezier(.2,.9,.2,1) {b3+.22:.2f}s both;font-size:180px}}
.b3 .l3{{animation:cutR .45s cubic-bezier(.2,.9,.2,1) {b3+.4:.2f}s both;font-size:180px}}
@keyframes p3a{{from{{transform:translate(1500px,900px) rotate(7deg) scale(1.3)}}70%{{transform:translate(520px,900px) rotate(7deg) scale(1.3)}}to{{transform:translate(550px,900px) rotate(7deg) scale(1.3)}}}}
@keyframes p3b{{from{{transform:translate(-900px,940px) rotate(-6deg) scale(1.45)}}70%{{transform:translate(40px,940px) rotate(-6deg) scale(1.45)}}to{{transform:translate(10px,940px) rotate(-6deg) scale(1.45)}}}}
.b3 .stg.a{{animation:p3a .8s cubic-bezier(.2,.9,.2,1) {b3+.6:.2f}s both;z-index:5}}
.b3 .stg.b{{animation:p3b .8s cubic-bezier(.2,.9,.2,1) {b3+.8:.2f}s both;z-index:6}}
.b3 .chip{{left:50px;top:1560px;--rot:-3deg;transform:rotate(-3deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b3+1.7:.2f}s both}}
.b3 .stk{{right:60px;top:1660px;--rot:6deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b3+1.9:.2f}s both}}

/* 4: sets EN + JA */
.b4{{animation:lift .3s ease-in {b5-.15:.2f}s forwards}}
.b4 .words{{top:380px}}
.b4 .l1{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b4+.05:.2f}s both;font-size:180px}}
.b4 .l2{{font-family:var(--body);font-weight:900;font-size:160px;letter-spacing:.02em;transform:none;text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);animation:stampN .45s cubic-bezier(.2,1,.3,1) {b4+.25:.2f}s both}}
@keyframes stampN{{from{{opacity:0;transform:scale(1.7)}}55%{{opacity:1;transform:scale(.94)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes p4a{{from{{transform:translate(-900px,800px) rotate(-7deg) scale(1.3)}}70%{{transform:translate(40px,800px) rotate(-7deg) scale(1.3)}}to{{transform:translate(10px,800px) rotate(-7deg) scale(1.3)}}}}
@keyframes p4b{{from{{transform:translate(1500px,860px) rotate(6deg) scale(1.45)}}70%{{transform:translate(440px,860px) rotate(6deg) scale(1.45)}}to{{transform:translate(470px,860px) rotate(6deg) scale(1.45)}}}}
.b4 .stg.a{{animation:p4a .8s cubic-bezier(.2,.9,.2,1) {b4+.6:.2f}s both;z-index:5}}
.b4 .stg.b{{animation:p4b .8s cubic-bezier(.2,.9,.2,1) {b4+.8:.2f}s both;z-index:6}}
.b4 .stk{{left:60px;top:1640px;--rot:-7deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b4+1.7:.2f}s both}}
.b4 .chip{{left:50%;top:700px;transform:translateX(-50%) rotate(2deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b4+1.5:.2f}s both}}

/* 5: beta CTA */
.b5 .words{{top:400px}}
.b5 .l1{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b5+.05:.2f}s both;font-size:170px}}
.b5 .l2{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b5+.22:.2f}s both;font-size:230px}}
.b5 .sub{{position:absolute;left:80px;right:80px;top:850px;text-align:center;z-index:10;font-size:34px;line-height:1.3;font-weight:700;color:var(--ink-soft);animation:fade .4s ease-out {b5+.7:.2f}s both}}
.b5 .ticket{{position:absolute;left:50%;top:990px;z-index:12;background:var(--yellow);color:#121114;border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:20px 40px;font-size:30px;font-weight:900;white-space:nowrap;transform:translateX(-50%) rotate(-2deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b5+1.0:.2f}s both}}
.b5 .ticket b{{font-family:var(--display);font-weight:400;font-size:46px;display:block;line-height:1;margin-bottom:4px}}
.b5 .pill{{position:absolute;left:50%;top:1170px;z-index:12;background:var(--ink);color:var(--paper);font-weight:900;font-size:36px;letter-spacing:.08em;padding:24px 52px;border:5px solid var(--paper);box-shadow:12px 12px 0 var(--red);white-space:nowrap;transform:translateX(-50%);animation:pillpop .5s cubic-bezier(.2,1.4,.4,1) {b5+1.4:.2f}s both}}
@keyframes pillpop{{0%{{opacity:0;transform:translateX(-50%) scale(.5)}}65%{{opacity:1;transform:translateX(-50%) scale(1.08)}}100%{{opacity:1;transform:translateX(-50%) scale(1)}}}}
@keyframes p5a{{from{{transform:translate(340px,2100px) scale(1.0)}}70%{{transform:translate(340px,1300px) scale(1.0)}}to{{transform:translate(340px,1330px) scale(1.0)}}}}
@keyframes p5b{{from{{transform:translate(-40px,2200px) rotate(-12deg) scale(.95)}}70%{{transform:translate(-40px,1400px) rotate(-12deg) scale(.95)}}to{{transform:translate(-40px,1430px) rotate(-12deg) scale(.95)}}}}
@keyframes p5c{{from{{transform:translate(760px,2200px) rotate(12deg) scale(.95)}}70%{{transform:translate(760px,1400px) rotate(12deg) scale(.95)}}to{{transform:translate(760px,1430px) rotate(12deg) scale(.95)}}}}
.b5 .stg.a{{animation:p5a .8s cubic-bezier(.2,.9,.2,1) {b5+1.9:.2f}s both;z-index:7}}
.b5 .stg.b{{animation:p5b .8s cubic-bezier(.2,.9,.2,1) {b5+1.75:.2f}s both;z-index:5}}
.b5 .stg.c{{animation:p5c .8s cubic-bezier(.2,.9,.2,1) {b5+2.05:.2f}s both;z-index:5}}
.b5 .stk{{right:60px;top:1285px;--rot:7deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b5+2.4:.2f}s both}}
"""

HTML = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<title>Dexeon beta story</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">
<style>{style}</style>
<style>{CSS}</style>
</head>
<body>
<div class="shot">
  <div class="halft"></div>
  <div class="kana" aria-hidden="true">デクセオン</div>
  <div class="wm"><img src="{WM_L}" alt="Dexeon"></div>
  <div class="rule"></div>

  <div class="beat b1">
    <div class="words"><span class="l l1">All</span><span class="l l2 red">1025</span><span class="l l3">Species.</span></div>
    {ph('home')}
    <div class="stk">GOTCHA!</div>
    <div class="chip">Tap to catch · star your favorites</div>
  </div>

  <div class="beat b2">
    <div class="words"><span class="l l1 c">Every printing.</span><span class="l l2 c red">Live prices.</span></div>
    {ph('pokemon-charmander', 'a')}{ph('card-price', 'b')}
    <div class="chip">Low · average · high · 90-day history</div>
    <div class="stk w">ドン!</div>
  </div>

  <div class="beat b3">
    <div class="words"><span class="l l1 r">Binders</span><span class="l l2 r red">that page</span><span class="l l3 r">like binders.</span></div>
    {ph('binders', 'a')}{ph('binder-base', 'b')}
    <div class="chip">Drag. Drop. Share. Print.</div>
    <div class="stk">FLIP!</div>
  </div>

  <div class="beat b4">
    <div class="words"><span class="l l1">Every set.</span><span class="l l2 red">日本語も。</span></div>
    {ph('sets-all', 'a')}{ph('ja-set', 'b')}
    <div class="chip">English and Japanese, side by side</div>
    <div class="stk">全部!</div>
  </div>

  <div class="beat b5">
    <div class="words"><span class="l l1 c">Join the</span><span class="l l2 c red">beta.</span></div>
    <p class="sub">Free while it's in beta. iPhone only, for now.</p>
    <div class="ticket"><b>Early adopters</b>A select group gets Dexeon free for life.</div>
    <div class="pill">dexeontcg.com · link in bio</div>
    {ph('chase', 'b')}{ph('profile', 'c')}{ph('home', 'a')}
    <div class="stk">GO!</div>
  </div>

  <div class="sweep s1"></div><div class="sweep s2"></div><div class="sweep s3"></div><div class="sweep s4"></div>
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
open('marketing/beta-story.html', 'w').write(HTML)
print('wrote marketing/beta-story.html')
