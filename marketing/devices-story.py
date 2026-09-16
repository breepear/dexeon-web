# Writes marketing/devices-story.html: a 14-second Instagram Story (1080x1920)
# built from REAL simulator screenshots of Dexeon on BOTH iPhone and iPad
# (marketing/shots/*.png and marketing/shots/ipad/*.png, captured with
# `xcrun simctl io <udid> screenshot`), each inside its device bezel, with the
# site's kinetic type and panel sweeps. Every beat pairs the same screen on the
# two devices, closing on a beta call to action.
# Run from the repo root, then render with:
#   python3 marketing/devices-story.py && python3 marketing/logo-story.py --page devices-story --dur 14
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
src = open('index.html').read()
style = re.search(r'<style>(.*?)</style>', src, re.S).group(1)
WM_L = '../assets/logo/dexeon-wordmark-nav.png'

def phone(name, cls=''):
    return f'<div class="stg {cls}"><div class="ph"><img src="shots/{name}.png" alt=""></div></div>'
def ipad(name, cls=''):
    return f'<div class="stg {cls}"><div class="pad"><img src="shots/ipad/{name}.png" alt=""></div></div>'

# beat starts (sweeps fire .2 s earlier)
b1, b2, b3, b4 = 0.5, 4.2, 7.6, 11.0

CSS = f"""
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:var(--paper);color:var(--ink);font-family:var(--body)}}
.shot{{position:relative;width:1080px;height:1920px;overflow:hidden}}
.halft{{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.2px,transparent 3px);background-size:22px 22px;opacity:.55}}
.kana{{position:absolute;left:-60px;top:1180px;font-size:520px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:3px #d9dbd4;white-space:nowrap;letter-spacing:-.04em;animation:drift 14s linear both}}
@keyframes drift{{from{{transform:translateX(0)}}to{{transform:translateX(-160px)}}}}
.wm{{position:absolute;left:50%;top:100px;width:280px;margin-left:-140px;z-index:30;animation:drop .45s cubic-bezier(.2,1.3,.4,1) .15s both}}
.wm img{{width:100%;display:block}}
@keyframes drop{{from{{opacity:0;transform:translateY(-90px)}}to{{opacity:1;transform:translateY(0)}}}}
.eyebrow2{{position:absolute;left:0;right:0;top:250px;text-align:center;font-size:28px;font-weight:900;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-soft);z-index:30;animation:drop .45s cubic-bezier(.2,1.3,.4,1) .4s both}}
.eyebrow2::before,.eyebrow2::after{{content:"";display:inline-block;width:60px;height:7px;background:var(--red);vertical-align:middle;margin:0 20px}}

/* device bezels, sized in device points (iPhone 17 Pro 402x874, iPad Pro 13" 1032x1376) */
.stg{{position:absolute;left:0;top:0;transform-origin:top left;z-index:5}}
.ph{{width:402px;height:874px;box-sizing:border-box;padding:12px;background:#0d0d0f;border-radius:66px;box-shadow:0 40px 80px -30px rgba(0,0,0,.55),0 0 0 2px #2b2b30 inset,0 0 0 3px #121114;position:relative}}
.ph::before{{content:"";position:absolute;top:22px;left:50%;transform:translateX(-50%);width:120px;height:34px;background:#0d0d0f;border-radius:20px;z-index:2}}
.ph img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:54px;display:block}}
.pad{{width:1032px;height:1376px;box-sizing:border-box;padding:30px;background:#0d0d0f;border-radius:64px;box-shadow:0 50px 100px -30px rgba(0,0,0,.55),0 0 0 3px #2b2b30 inset,0 0 0 4px #121114}}
.pad img{{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:36px;display:block}}

.beat{{position:absolute;inset:0}}
.words{{position:absolute;left:70px;right:70px;z-index:10}}
.words .l{{display:block;font-family:var(--display);font-size:170px;line-height:.9;text-transform:uppercase;transform:skewX(-6deg);text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);white-space:nowrap}}
.words .l.red{{color:var(--red)}} .words .l.c{{text-align:center}} .words .l.r{{text-align:right}}
.chip{{position:absolute;z-index:12;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:18px 34px;font-size:32px;font-weight:900;white-space:nowrap}}
.stk{{position:absolute;z-index:12;font-family:'Bangers',var(--display);font-size:92px;letter-spacing:.04em;color:var(--ink);background:var(--yellow);border:7px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:12px 36px 6px;line-height:1}}
.stk.w{{background:var(--paper-2)}}
.tag{{position:absolute;z-index:12;background:var(--ink);color:var(--paper);font-size:24px;font-weight:900;letter-spacing:.18em;text-transform:uppercase;padding:12px 22px;border:4px solid var(--paper);box-shadow:8px 8px 0 var(--red)}}

@keyframes cutL{{from{{opacity:0;transform:skewX(-6deg) translateX(-260px)}}60%{{opacity:1;transform:skewX(-6deg) translateX(24px)}}to{{opacity:1;transform:skewX(-6deg) translateX(0)}}}}
@keyframes cutR{{from{{opacity:0;transform:skewX(-6deg) translateX(260px)}}60%{{opacity:1;transform:skewX(-6deg) translateX(-24px)}}to{{opacity:1;transform:skewX(-6deg) translateX(0)}}}}
@keyframes stamp{{from{{opacity:0;transform:skewX(-6deg) scale(1.7)}}55%{{opacity:1;transform:skewX(-6deg) scale(.94)}}to{{opacity:1;transform:skewX(-6deg) scale(1)}}}}
@keyframes riseW{{from{{opacity:0;transform:skewX(-6deg) translateY(160px)}}65%{{opacity:1;transform:skewX(-6deg) translateY(-18px)}}to{{opacity:1;transform:skewX(-6deg) translateY(0)}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(0) rotate(-30deg)}}65%{{opacity:1;transform:scale(1.18) rotate(-3deg)}}100%{{opacity:1;transform:scale(1) rotate(var(--rot,-6deg))}}}}
@keyframes popC{{0%{{opacity:0;transform:translateX(-50%) scale(0) rotate(-30deg)}}65%{{opacity:1;transform:translateX(-50%) scale(1.18) rotate(-3deg)}}100%{{opacity:1;transform:translateX(-50%) scale(1) rotate(-2deg)}}}}
@keyframes fade{{from{{opacity:0;transform:translateY(30px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes lift{{from{{opacity:1;transform:translateY(0)}}to{{opacity:0;transform:translateY(-90px)}}}}

.sweep{{position:absolute;top:-10%;bottom:-10%;left:-45%;width:190%;transform:translateX(-120%) skewX(-12deg);z-index:20}}
@keyframes sweep{{from{{transform:translateX(-120%) skewX(-12deg)}}to{{transform:translateX(120%) skewX(-12deg)}}}}
.s1{{background:var(--red);animation:sweep .55s cubic-bezier(.75,0,.2,1) {b2-.2:.2f}s forwards}}
.s2{{background:var(--ink);animation:sweep .55s cubic-bezier(.75,0,.2,1) {b3-.2:.2f}s forwards}}
.s3{{background:var(--yellow);animation:sweep .55s cubic-bezier(.75,0,.2,1) {b4-.2:.2f}s forwards}}

/* 1: one collection, two screens — Full Dex on both */
.b1{{animation:lift .3s ease-in {b2-.15:.2f}s forwards}}
.b1 .words{{top:360px}}
.b1 .l1{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b1:.2f}s both;font-size:140px}}
.b1 .l2{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b1+.17:.2f}s both;font-size:140px}}
@keyframes d1{{from{{transform:translate(1300px,760px) rotate(4deg) scale(.8)}}70%{{transform:translate(300px,760px) rotate(4deg) scale(.8)}}to{{transform:translate(330px,760px) rotate(4deg) scale(.8)}}}}
@keyframes p1{{from{{transform:translate(-40px,2100px) rotate(-7deg) scale(1.15)}}70%{{transform:translate(-40px,1000px) rotate(-7deg) scale(1.15)}}to{{transform:translate(-40px,1040px) rotate(-7deg) scale(1.15)}}}}
.b1 .stg.a{{animation:d1 .8s cubic-bezier(.2,.9,.2,1) {b1+.4:.2f}s both;z-index:5}}
.b1 .stg.b{{animation:p1 .8s cubic-bezier(.2,.9,.2,1) {b1+.7:.2f}s both;z-index:6}}
.b1 .tag.a{{right:40px;top:700px;--rot:0;animation:fade .35s ease-out {b1+1.3:.2f}s both}}
.b1 .tag.b{{left:40px;top:1660px;animation:fade .35s ease-out {b1+1.5:.2f}s both}}
.b1 .chip{{left:50%;top:1760px;transform:translateX(-50%) rotate(-2deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b1+1.9:.2f}s both}}
.b1 .stk{{right:50px;top:1560px;--rot:6deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b1+2.2:.2f}s both}}

/* 2: binders — binder page on iPad, binders grid on iPhone */
.b2{{animation:lift .3s ease-in {b3-.15:.2f}s forwards}}
.b2 .words{{top:360px}}
.b2 .l1{{animation:cutR .45s cubic-bezier(.2,.9,.2,1) {b2+.05:.2f}s both;font-size:150px}}
.b2 .l2{{animation:cutR .45s cubic-bezier(.2,.9,.2,1) {b2+.22:.2f}s both;font-size:150px}}
.b2 .l3{{animation:cutR .45s cubic-bezier(.2,.9,.2,1) {b2+.4:.2f}s both;font-size:150px}}
@keyframes d2{{from{{transform:translate(-1200px,820px) rotate(-4deg) scale(.8)}}70%{{transform:translate(-80px,820px) rotate(-4deg) scale(.8)}}to{{transform:translate(-50px,820px) rotate(-4deg) scale(.8)}}}}
@keyframes p2{{from{{transform:translate(1500px,1000px) rotate(7deg) scale(1.15)}}70%{{transform:translate(620px,1000px) rotate(7deg) scale(1.15)}}to{{transform:translate(650px,1000px) rotate(7deg) scale(1.15)}}}}
.b2 .stg.a{{animation:d2 .8s cubic-bezier(.2,.9,.2,1) {b2+.55:.2f}s both;z-index:5}}
.b2 .stg.b{{animation:p2 .8s cubic-bezier(.2,.9,.2,1) {b2+.8:.2f}s both;z-index:6}}
.b2 .chip{{left:50px;top:1760px;--rot:-3deg;transform:rotate(-3deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b2+1.7:.2f}s both}}
.b2 .stk{{left:60px;top:1500px;--rot:-7deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b2+1.95:.2f}s both}}

/* 3: prices — species on iPad, card price on iPhone */
.b3{{animation:lift .3s ease-in {b4-.15:.2f}s forwards}}
.b3 .words{{top:360px}}
.b3 .l1{{animation:stamp .4s cubic-bezier(.2,1,.3,1) {b3+.05:.2f}s both;font-size:148px}}
.b3 .l2{{animation:stamp .4s cubic-bezier(.2,1,.3,1) {b3+.22:.2f}s both;font-size:148px}}
@keyframes d3{{from{{transform:translate(1300px,700px) rotate(5deg) scale(.8)}}70%{{transform:translate(280px,700px) rotate(5deg) scale(.8)}}to{{transform:translate(310px,700px) rotate(5deg) scale(.8)}}}}
@keyframes p3{{from{{transform:translate(-40px,2100px) rotate(-6deg) scale(1.15)}}70%{{transform:translate(-40px,1090px) rotate(-6deg) scale(1.15)}}to{{transform:translate(-40px,1120px) rotate(-6deg) scale(1.15)}}}}
.b3 .stg.a{{animation:d3 .8s cubic-bezier(.2,.9,.2,1) {b3+.5:.2f}s both;z-index:5}}
.b3 .stg.b{{animation:p3 .8s cubic-bezier(.2,.9,.2,1) {b3+.75:.2f}s both;z-index:6}}
.b3 .chip{{left:50%;top:640px;transform:translateX(-50%) rotate(-2deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b3+1.6:.2f}s both}}
.b3 .stk{{right:50px;top:1560px;--rot:6deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b3+1.9:.2f}s both}}

/* 4: join the beta — sets on iPad, chase on iPhone, small at the bottom */
.b4 .words{{top:380px}}
.b4 .l1{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b4+.05:.2f}s both;font-size:160px}}
.b4 .l2{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b4+.22:.2f}s both;font-size:220px}}
.b4 .sub{{position:absolute;left:80px;right:80px;top:820px;text-align:center;z-index:10;font-size:34px;line-height:1.3;font-weight:700;color:var(--ink-soft);animation:fade .4s ease-out {b4+.7:.2f}s both}}
.b4 .ticket{{position:absolute;left:50%;top:950px;z-index:12;background:var(--yellow);color:#121114;border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:20px 40px;font-size:30px;font-weight:900;white-space:nowrap;transform:translateX(-50%) rotate(-2deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b4+1.0:.2f}s both}}
.b4 .ticket b{{font-family:var(--display);font-weight:400;font-size:46px;display:block;line-height:1;margin-bottom:4px}}
.b4 .pill{{position:absolute;left:50%;top:1130px;z-index:12;background:var(--ink);color:var(--paper);font-weight:900;font-size:36px;letter-spacing:.08em;padding:24px 52px;border:5px solid var(--paper);box-shadow:12px 12px 0 var(--red);white-space:nowrap;transform:translateX(-50%);animation:pillpop .5s cubic-bezier(.2,1.4,.4,1) {b4+1.4:.2f}s both}}
@keyframes pillpop{{0%{{opacity:0;transform:translateX(-50%) scale(.5)}}65%{{opacity:1;transform:translateX(-50%) scale(1.08)}}100%{{opacity:1;transform:translateX(-50%) scale(1)}}}}
@keyframes d4{{from{{transform:translate(120px,2200px) rotate(-3deg) scale(.7)}}70%{{transform:translate(120px,1300px) rotate(-3deg) scale(.7)}}to{{transform:translate(120px,1330px) rotate(-3deg) scale(.7)}}}}
@keyframes p4{{from{{transform:translate(640px,2200px) rotate(8deg) scale(1.0)}}70%{{transform:translate(640px,1400px) rotate(8deg) scale(1.0)}}to{{transform:translate(640px,1430px) rotate(8deg) scale(1.0)}}}}
.b4 .stg.a{{animation:d4 .8s cubic-bezier(.2,.9,.2,1) {b4+1.75:.2f}s both;z-index:5}}
.b4 .stg.b{{animation:p4 .8s cubic-bezier(.2,.9,.2,1) {b4+1.95:.2f}s both;z-index:6}}
.b4 .stk{{right:60px;top:1240px;--rot:7deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b4+2.4:.2f}s both}}
"""

HTML = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<title>Dexeon devices story</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">
<style>{style}</style>
<style>{CSS}</style>
</head>
<body>
<div class="shot">
  <div class="halft"></div>
  <div class="kana" aria-hidden="true">デクセオン</div>
  <div class="wm"><img src="{WM_L}" alt="Dexeon"></div>
  <div class="eyebrow2">iPhone + iPad</div>

  <div class="beat b1">
    <div class="words"><span class="l l1">One collection.</span><span class="l l2 red">Two screens.</span></div>
    {ipad('home', 'a')}{phone('profile', 'b')}
    <div class="tag a">iPad</div><div class="tag b">iPhone</div>
    <div class="chip">One account. Every screen you own.</div>
    <div class="stk">GOTCHA!</div>
  </div>

  <div class="beat b2">
    <div class="words"><span class="l l1 r">Binders</span><span class="l l2 r red">that page</span><span class="l l3 r">like binders.</span></div>
    {ipad('binder-base', 'a')}{phone('binders', 'b')}
    <div class="chip">Nine-pocket pages on either screen</div>
    <div class="stk w">FLIP!</div>
  </div>

  <div class="beat b3">
    <div class="words"><span class="l l1 c">Every printing.</span><span class="l l2 c red">Live prices.</span></div>
    {ipad('pokemon-charmander', 'a')}{phone('card-price', 'b')}
    <div class="chip">Low · average · high · 90-day history</div>
    <div class="stk">ドン!</div>
  </div>

  <div class="beat b4">
    <div class="words"><span class="l l1 c">Join the</span><span class="l l2 c red">beta.</span></div>
    <p class="sub">Free while it's in beta. iPhone and iPad.</p>
    <div class="ticket"><b>Early adopters</b>A select group gets Dexeon free for life.</div>
    <div class="pill">dexeontcg.com · link in bio</div>
    {ipad('chase', 'a')}{phone('sets-all', 'b')}
    <div class="stk">GO!</div>
  </div>

  <div class="sweep s1"></div><div class="sweep s2"></div><div class="sweep s3"></div>
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
open('marketing/devices-story.html', 'w').write(HTML)
print('wrote marketing/devices-story.html')
