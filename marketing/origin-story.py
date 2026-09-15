# Writes marketing/origin-story.html: a 22-second Instagram Story (1080x1920)
# telling where Dexeon came from (the app's About page chapters) interleaved with
# its features. Kinetic type, alternating light/dark chapters wiped by panel
# sweeps, and the landing page's phone mockups used as props.
# Run from the repo root, then render with:
#   python3 marketing/origin-story.py && python3 marketing/logo-story.py --page origin-story --dur 22
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
src = open('index.html').read()
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
WM_L, WM_D = '../assets/logo/dexeon-wordmark-nav.png', '../assets/logo/dexeon-wordmark-nav-dark.png'

# chapter start times (sweep starts .2s before each)
T = dict(b0=0.0, b1=2.7, b2=6.1, b3=9.5, b4=12.5, b5=15.7, b6=18.7)

def beat_css(name, t, dark):
    """appear as the sweep covers the screen; lift just before the next sweep."""
    css = ''
    if t > 0:
        css += f'.{name}{{opacity:0;animation:appear .01s linear {t + .07:.2f}s forwards}}\n'
    return css

CSS = f"""
html,body{{margin:0;width:1080px;height:1920px;overflow:hidden;background:#F2F3EF;font-family:var(--body)}}
.shot{{position:relative;width:1080px;height:1920px;overflow:hidden;background:#F2F3EF}}
.beat{{position:absolute;inset:0;background:var(--paper);color:var(--ink)}}
.beat.dk{{--paper:#131316;--paper-2:#1B1B1F;--ink:#F1F0EA;--ink-soft:#B8B6BE;--tone:#2A2A2F;--red:#E0463F;--yellow:#F7C728;--blue:#5B86D6;--green:#43C06A}}
.halft{{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.2px,transparent 3px);background-size:22px 22px;opacity:.55}}
.dk .halft{{opacity:.9;background-image:radial-gradient(#2c2c31 2.2px,transparent 3px)}}
.kana{{position:absolute;left:-60px;top:1180px;font-size:520px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:3px #d9dbd4;white-space:nowrap;letter-spacing:-.04em}}
.dk .kana{{-webkit-text-stroke:3px #2a2a30}}
.kana.top{{top:-40px;left:-80px}}
.wm{{position:absolute;left:50%;top:100px;width:280px;margin-left:-140px;z-index:30}}
.wm img{{width:100%;display:block}}
.b0 .wm{{animation:drop .45s cubic-bezier(.2,1.3,.4,1) .15s both}}
@keyframes drop{{from{{opacity:0;transform:translateY(-90px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes appear{{to{{opacity:1}}}}
@keyframes lift{{from{{opacity:1;transform:translateY(0)}}to{{opacity:0;transform:translateY(-90px)}}}}

.phone,.rv,.hero-stage .phone{{animation:none !important;transition:none !important;opacity:1 !important}}
.stg{{position:absolute;left:0;top:0;transform-origin:top left;z-index:5}}
.stg .phone{{position:relative;transform:none}}

.ch{{position:absolute;left:70px;top:290px;z-index:12;font-size:28px;font-weight:900;letter-spacing:.24em;text-transform:uppercase;color:var(--ink-soft);display:flex;align-items:center;gap:20px}}
.ch::before{{content:"";width:60px;height:7px;background:var(--red)}}
.ch b{{color:var(--red)}}
.ch.c{{left:0;right:0;justify-content:center}}
.words{{position:absolute;left:70px;right:70px;z-index:10}}
.words .l{{display:block;font-family:var(--display);font-size:190px;line-height:.9;text-transform:uppercase;transform:skewX(-6deg);text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);white-space:nowrap}}
.words .l.red{{color:var(--red)}} .words .l.c{{text-align:center}} .words .l.r{{text-align:right}}
.words .q{{font-family:var(--display);font-size:118px;line-height:.95;text-transform:uppercase;transform:skewX(-6deg);text-shadow:7px 7px 0 var(--paper),13px 13px 0 var(--ink);margin:0}}
.copy{{position:absolute;left:80px;right:80px;z-index:10;font-size:32px;line-height:1.3;font-weight:700;color:var(--ink-soft);text-wrap:balance}}
.copy.c{{text-align:center}}
.chip{{position:absolute;z-index:12;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:18px 34px;font-size:32px;font-weight:900;white-space:nowrap;color:var(--ink)}}
.stk{{position:absolute;z-index:12;font-family:'Bangers',var(--display);font-size:92px;letter-spacing:.04em;color:#121114;background:var(--yellow);border:7px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:12px 36px 6px;line-height:1}}
.stk.w{{background:var(--paper-2);color:var(--ink)}}
.tick{{position:absolute;z-index:12;background:var(--paper-2);border:7px dashed var(--ink);box-shadow:12px 12px 0 var(--ink);padding:18px 30px 14px;font-family:var(--display);font-size:56px;text-transform:uppercase;color:var(--ink);line-height:1}}
.tick small{{display:block;font-family:var(--body);font-size:20px;font-weight:900;letter-spacing:.22em;color:var(--red);margin-bottom:4px}}

@keyframes cutL{{from{{opacity:0;transform:skewX(-6deg) translateX(-260px)}}60%{{opacity:1;transform:skewX(-6deg) translateX(24px)}}to{{opacity:1;transform:skewX(-6deg) translateX(0)}}}}
@keyframes cutR{{from{{opacity:0;transform:skewX(-6deg) translateX(260px)}}60%{{opacity:1;transform:skewX(-6deg) translateX(-24px)}}to{{opacity:1;transform:skewX(-6deg) translateX(0)}}}}
@keyframes stamp{{from{{opacity:0;transform:skewX(-6deg) scale(1.7)}}55%{{opacity:1;transform:skewX(-6deg) scale(.94)}}to{{opacity:1;transform:skewX(-6deg) scale(1)}}}}
@keyframes riseW{{from{{opacity:0;transform:skewX(-6deg) translateY(160px)}}65%{{opacity:1;transform:skewX(-6deg) translateY(-18px)}}to{{opacity:1;transform:skewX(-6deg) translateY(0)}}}}
@keyframes fade{{from{{opacity:0;transform:translateY(30px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes pop{{0%{{opacity:0;transform:scale(0) rotate(-30deg)}}65%{{opacity:1;transform:scale(1.18) rotate(-3deg)}}100%{{opacity:1;transform:scale(1) rotate(var(--rot,-6deg))}}}}
@keyframes grow{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}

.sweep{{position:absolute;top:-10%;bottom:-10%;left:-45%;width:190%;transform:translateX(-120%) skewX(-12deg);z-index:20}}
@keyframes sweep{{from{{transform:translateX(-120%) skewX(-12deg)}}to{{transform:translateX(120%) skewX(-12deg)}}}}
.sw1{{background:#C8322E;animation:sweep .55s cubic-bezier(.75,0,.2,1) {T['b1']-.2:.2f}s forwards}}
.sw2{{background:#F7C728;animation:sweep .55s cubic-bezier(.75,0,.2,1) {T['b2']-.2:.2f}s forwards}}
.sw3{{background:#121114;animation:sweep .55s cubic-bezier(.75,0,.2,1) {T['b3']-.2:.2f}s forwards}}
.sw4{{background:#C8322E;animation:sweep .55s cubic-bezier(.75,0,.2,1) {T['b4']-.2:.2f}s forwards}}
.sw5{{background:#F7C728;animation:sweep .55s cubic-bezier(.75,0,.2,1) {T['b5']-.2:.2f}s forwards}}
.sw6{{background:#121114;animation:sweep .55s cubic-bezier(.75,0,.2,1) {T['b6']-.2:.2f}s forwards}}
{''.join(beat_css(n, t, False) for n, t in T.items())}
"""

def A(t, extra=''):  # helper: absolute delay seconds
    return f'{t:.2f}s{extra}'

b0, b1, b2, b3, b4, b5, b6 = (T[k] for k in ('b0', 'b1', 'b2', 'b3', 'b4', 'b5', 'b6'))
CSS += f"""
/* 00 cover (light) 0 -> 2.7 */
.b0 .ch{{animation:fade .4s ease-out .5s both}}
.b0 .words{{top:560px}}
.b0 .l1{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) .7s both}}
.b0 .l2{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) .87s both;font-size:230px}}
.b0 .l3{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) 1.05s both}}
.b0 .chip{{left:50%;top:1330px;--rot:-3deg;transform:translateX(-50%) rotate(-3deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) 1.7s both}}
@keyframes popC{{0%{{opacity:0;transform:translateX(-50%) scale(0) rotate(-30deg)}}65%{{opacity:1;transform:translateX(-50%) scale(1.18) rotate(-3deg)}}100%{{opacity:1;transform:translateX(-50%) scale(1) rotate(-3deg)}}}}
.b0 .chip{{animation-name:popC}}
.b0{{animation:lift .3s ease-in {b1-.15:.2f}s forwards}}

/* 01 why (dark) */
.b1 .ch{{animation:fade .4s ease-out {b1+.1:.2f}s both}}
.b1 .words{{top:390px;right:100px}} .b1 .q{{font-size:104px}} .b1 .q.two{{font-size:92px;margin-top:34px}}
.b1 .q{{animation:cutL .5s cubic-bezier(.2,.9,.2,1) {b1+.25:.2f}s both}}
.b1 .q.two{{color:var(--red);animation-delay:{b1+.45:.2f}s}}
.b1 .copy{{top:960px;right:500px;font-size:29px;animation:fade .4s ease-out {b1+.9:.2f}s both}}
@keyframes p1{{from{{transform:translate(1200px,1000px) rotate(9deg) scale(1.7)}}70%{{transform:translate(560px,1000px) rotate(9deg) scale(1.7)}}to{{transform:translate(590px,1000px) rotate(9deg) scale(1.7)}}}}
.b1 .stg{{animation:p1 .8s cubic-bezier(.2,.9,.2,1) {b1+1.0:.2f}s both}}
.b1 .tick{{--rot:-6deg}}
.b1 .t1{{left:70px;top:1280px;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b1+1.7:.2f}s both}}
.b1 .t2{{left:110px;top:1460px;--rot:4deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b1+1.9:.2f}s both}}
.b1 .t3{{left:60px;top:1640px;--rot:-3deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b1+2.1:.2f}s both}}
.b1{{animation:appear .01s linear {b1+.07:.2f}s forwards, lift .3s ease-in {b2-.15:.2f}s forwards}}

/* 02 craft (light) */
.b2 .ch{{animation:fade .4s ease-out {b2+.1:.2f}s both}}
.b2 .words{{top:380px}}
.b2 .l1{{animation:stamp .4s cubic-bezier(.2,1,.3,1) {b2+.25:.2f}s both;font-size:150px}}
.b2 .l2{{animation:stamp .4s cubic-bezier(.2,1,.3,1) {b2+.42:.2f}s both;font-size:150px}}
.b2 .l3{{animation:stamp .4s cubic-bezier(.2,1,.3,1) {b2+.6:.2f}s both;font-size:116px;line-height:1.1}}
@keyframes p2{{from{{transform:translate(220px,2100px) scale(2.0)}}70%{{transform:translate(220px,870px) scale(2.0)}}to{{transform:translate(220px,900px) scale(2.0)}}}}
.b2 .stg{{animation:p2 .8s cubic-bezier(.2,.9,.2,1) {b2+.9:.2f}s both}}
.b2 .spiral{{position:absolute;left:220px;top:900px;width:640px;height:1036px;z-index:8;overflow:visible}}
.b2 .spiral path{{stroke:#2E5AAC;stroke-width:8;fill:none;stroke-dasharray:100;stroke-dashoffset:100;animation:draw 1.3s cubic-bezier(.4,0,.3,1) {b2+1.6:.2f}s forwards}}
.b2 .spiral rect{{stroke:#2E5AAC;stroke-width:3;fill:none;stroke-dasharray:14 12;opacity:0;animation:appear .3s linear {b2+1.5:.2f}s forwards}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
.b2 .chip{{right:60px;top:1240px;--rot:3deg;transform:rotate(3deg);animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b2+2.5:.2f}s both}}
.b2 .stk{{left:60px;top:1500px;--rot:-7deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b2+2.8:.2f}s both}}
.b2{{animation:appear .01s linear {b2+.07:.2f}s forwards, lift .3s ease-in {b3-.15:.2f}s forwards}}

/* 03 japanese (dark) */
.b3 .ch{{animation:fade .4s ease-out {b3+.1:.2f}s both}}
.b3 .words{{top:400px}}
.b3 .l1{{font-family:var(--body);font-weight:900;font-size:190px;letter-spacing:.02em;transform:none;text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);animation:stamp .45s cubic-bezier(.2,1,.3,1) {b3+.25:.2f}s both}}
.b3 .l2{{font-family:var(--body);font-weight:900;font-size:190px;letter-spacing:.02em;transform:none;text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);animation:stamp .45s cubic-bezier(.2,1,.3,1) {b3+.45:.2f}s both}}
@keyframes stampN{{from{{opacity:0;transform:scale(1.7)}}55%{{opacity:1;transform:scale(.94)}}to{{opacity:1;transform:scale(1)}}}}
.b3 .l1,.b3 .l2{{animation-name:stampN}}
.b3 .card{{position:absolute;top:900px;width:440px;z-index:8}}
.b3 .card img{{width:100%;display:block;border-radius:22px;border:7px solid var(--ink);box-shadow:14px 14px 0 var(--ink)}}
.b3 .card figcaption{{position:absolute;left:-14px;top:-30px;background:var(--red);color:#fff;font-family:var(--display);font-size:44px;padding:8px 26px 4px;border:5px solid var(--ink);box-shadow:8px 8px 0 var(--ink);letter-spacing:.06em}}
.b3 .card.ja figcaption{{background:var(--yellow);color:#121114}}
@keyframes cEN{{from{{transform:translateX(-900px) rotate(-4deg)}}70%{{transform:translateX(20px) rotate(-4deg)}}to{{transform:translateX(0) rotate(-4deg)}}}}
@keyframes cJA{{from{{transform:translateX(900px) rotate(4deg) translateY(60px)}}70%{{transform:translateX(-20px) rotate(4deg) translateY(60px)}}to{{transform:translateX(0) rotate(4deg) translateY(60px)}}}}
.b3 .card.en{{left:90px;animation:cEN .7s cubic-bezier(.2,.9,.2,1) {b3+.9:.2f}s both}}
.b3 .card.ja{{left:560px;animation:cJA .7s cubic-bezier(.2,.9,.2,1) {b3+1.05:.2f}s both}}
.b3 .copy{{top:1660px;animation:fade .4s ease-out {b3+1.8:.2f}s both}}
.b3 .stk{{right:60px;top:760px;--rot:7deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b3+2.1:.2f}s both}}
.b3{{animation:appear .01s linear {b3+.07:.2f}s forwards, lift .3s ease-in {b4-.15:.2f}s forwards}}

/* 04 team (light) */
.b4 .ch{{animation:fade .4s ease-out {b4+.1:.2f}s both}}
.b4 .words{{top:380px}}
.b4 .l1{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b4+.25:.2f}s both;font-size:160px}}
.b4 .l2{{animation:cutR .45s cubic-bezier(.2,.9,.2,1) {b4+.45:.2f}s both;font-size:160px}}
.b4 .l3{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b4+.65:.2f}s both;font-size:160px}}
@keyframes p4a{{from{{transform:translate(-900px,900px) rotate(-8deg) scale(1.6)}}70%{{transform:translate(20px,900px) rotate(-8deg) scale(1.6)}}to{{transform:translate(-10px,900px) rotate(-8deg) scale(1.6)}}}}
@keyframes p4b{{from{{transform:translate(1500px,980px) rotate(7deg) scale(1.6)}}70%{{transform:translate(520px,980px) rotate(7deg) scale(1.6)}}to{{transform:translate(550px,980px) rotate(7deg) scale(1.6)}}}}
.b4 .stg.a{{animation:p4a .8s cubic-bezier(.2,.9,.2,1) {b4+.8:.2f}s both;z-index:5}}
.b4 .stg.b{{animation:p4b .8s cubic-bezier(.2,.9,.2,1) {b4+1.0:.2f}s both;z-index:6}}
.b4 .stk.a{{left:60px;top:1620px;--rot:-8deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b4+1.8:.2f}s both}}
.b4 .stk.b{{right:60px;top:1600px;--rot:6deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b4+2.0:.2f}s both}}
.b4 .chip{{left:50%;top:840px;transform:translateX(-50%) rotate(-2deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b4+2.3:.2f}s both}}
.b4{{animation:appear .01s linear {b4+.07:.2f}s forwards, lift .3s ease-in {b5-.15:.2f}s forwards}}

/* 05 promise (dark) */
.b5 .ch{{animation:fade .4s ease-out {b5+.1:.2f}s both}}
.b5 .rows{{position:absolute;left:80px;right:80px;top:400px;display:grid;gap:26px;z-index:10}}
.b5 .row{{display:flex;align-items:center;gap:30px;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:26px 34px}}
.b5 .row .bx{{width:80px;height:80px;flex:none;border:6px solid var(--ink);background:var(--paper);position:relative}}
.b5 .row .bx::before,.b5 .row .bx::after{{content:"";position:absolute;left:50%;top:50%;width:94px;height:13px;background:var(--red);transform:translate(-50%,-50%) rotate(45deg);transform-origin:center;animation:xin .25s ease-out both}}
.b5 .row .bx::after{{transform:translate(-50%,-50%) rotate(-45deg)}}
@keyframes xin{{from{{opacity:0}}to{{opacity:1}}}}
.b5 .row span{{font-family:var(--display);font-size:80px;text-transform:uppercase;line-height:1;transform:skewX(-6deg);color:var(--ink)}}
.b5 .r1{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b5+.25:.2f}s both}} .b5 .r1 .bx::before,.b5 .r1 .bx::after{{animation-delay:{b5+.75:.2f}s}}
.b5 .r2{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b5+.45:.2f}s both}} .b5 .r2 .bx::before,.b5 .r2 .bx::after{{animation-delay:{b5+.95:.2f}s}}
.b5 .r3{{animation:cutL .45s cubic-bezier(.2,.9,.2,1) {b5+.65:.2f}s both}} .b5 .r3 .bx::before,.b5 .r3 .bx::after{{animation-delay:{b5+1.15:.2f}s}}
@keyframes cutLn{{from{{opacity:0;transform:translateX(-260px)}}60%{{opacity:1;transform:translateX(24px)}}to{{opacity:1;transform:translateX(0)}}}}
.b5 .row{{animation-name:cutLn}}
.b5 .words{{top:1010px}}
.b5 .l1{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b5+1.4:.2f}s both;font-size:170px}}
.b5 .l2{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b5+1.57:.2f}s both;font-size:170px}}
.b5 .ticket{{position:absolute;left:50%;top:1440px;z-index:12;background:var(--yellow);color:#121114;border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:22px 40px;font-size:30px;font-weight:900;white-space:nowrap;transform:translateX(-50%) rotate(-3deg);animation:popC .45s cubic-bezier(.2,1.4,.4,1) {b5+2.2:.2f}s both}}
.b5 .ticket b{{font-family:var(--display);font-weight:400;font-size:48px;display:block;line-height:1;margin-bottom:4px}}
.b5{{animation:appear .01s linear {b5+.07:.2f}s forwards, lift .3s ease-in {b6-.15:.2f}s forwards}}

/* 06 maker + cta (light) */
.b6 .ch{{animation:fade .4s ease-out {b6+.1:.2f}s both}}
.b6 .face{{position:absolute;left:50%;top:400px;width:380px;height:380px;margin-left:-190px;border-radius:50%;border:10px solid var(--ink);box-shadow:16px 16px 0 var(--ink);object-fit:cover;z-index:9;animation:popF .5s cubic-bezier(.2,1.4,.4,1) {b6+.3:.2f}s both}}
@keyframes popF{{0%{{opacity:0;transform:scale(0) rotate(-20deg)}}65%{{opacity:1;transform:scale(1.1) rotate(2deg)}}100%{{opacity:1;transform:scale(1) rotate(0)}}}}
.b6 .stk{{left:640px;top:380px;--rot:8deg;animation:pop .45s cubic-bezier(.2,1.4,.4,1) {b6+.8:.2f}s both}}
.b6 .words{{top:830px}}
.b6 .l1{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b6+.9:.2f}s both;font-size:140px}}
.b6 .role{{position:absolute;left:0;right:0;top:1000px;text-align:center;z-index:10;font-size:28px;font-weight:900;letter-spacing:.24em;text-transform:uppercase;color:var(--red);animation:fade .4s ease-out {b6+1.3:.2f}s both}}
.b6 .copy{{top:1070px;animation:fade .4s ease-out {b6+1.5:.2f}s both}}
.b6 .l2,.b6 .l3{{font-size:150px}}
.b6 .words.two{{top:1290px}}
.b6 .l2{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b6+2.0:.2f}s both}}
.b6 .l3{{animation:riseW .5s cubic-bezier(.2,1.1,.3,1) {b6+2.17:.2f}s both}}
.b6 .pill{{position:absolute;left:50%;top:1600px;z-index:12;background:var(--ink);color:var(--paper);font-weight:900;font-size:34px;letter-spacing:.08em;padding:22px 48px;border:5px solid var(--paper);box-shadow:12px 12px 0 var(--red);white-space:nowrap;transform:translateX(-50%);animation:pillpop .5s cubic-bezier(.2,1.4,.4,1) {b6+2.7:.2f}s both}}
@keyframes pillpop{{0%{{opacity:0;transform:translateX(-50%) scale(.5)}}65%{{opacity:1;transform:translateX(-50%) scale(1.08)}}100%{{opacity:1;transform:translateX(-50%) scale(1)}}}}
@keyframes p6a{{from{{transform:translate(-260px,2100px) rotate(-14deg) scale(1.2)}}to{{transform:translate(-200px,1560px) rotate(-14deg) scale(1.2)}}}}
@keyframes p6b{{from{{transform:translate(900px,2100px) rotate(14deg) scale(1.2)}}to{{transform:translate(880px,1560px) rotate(14deg) scale(1.2)}}}}
.b6 .stg.a{{animation:p6a .7s cubic-bezier(.2,.9,.2,1) {b6+2.4:.2f}s both;z-index:4}}
.b6 .stg.b{{animation:p6b .7s cubic-bezier(.2,.9,.2,1) {b6+2.55:.2f}s both;z-index:4}}
.b6{{animation:appear .01s linear {b6+.07:.2f}s forwards}}
"""

SPIRAL = ('<svg class="spiral" viewBox="0 0 618 1000" width="640" height="1036">'
          '<rect x="0" y="0" width="618" height="618"/><rect x="236" y="618" width="382" height="382"/><rect x="0" y="764" width="236" height="236"/><rect x="0" y="618" width="146" height="146"/>'
          '<path pathLength="100" d="M0 0 A618 618 0 0 1 618 618 A382 382 0 0 1 236 1000 A236 236 0 0 1 0 764 A146 146 0 0 1 146 618 A90 90 0 0 1 236 708 A56 56 0 0 1 180 764"/></svg>')

def beat(name, dark, inner):
    wm = WM_D if dark else WM_L
    return (f'<div class="beat {name}{" dk" if dark else ""}"><div class="halft"></div><div class="kana{" top" if dark else ""}" aria-hidden="true">デクセオン</div>'
            f'<div class="wm"><img src="{wm}" alt="Dexeon"></div>{inner}</div>')

HTML = f"""<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<title>Dexeon origin story</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">
<style>{style}</style>
<style>{CSS}</style>
</head>
<body>
<div class="shot">
{beat('b0', False,
  '<div class="ch c">The story so far</div>'
  '<div class="words"><span class="l l1 c">Where</span><span class="l l2 c red">Dexeon</span><span class="l l3 c">came from.</span></div>'
  '<div class="chip">Built by one collector · 2026</div>')}
{beat('b1', True,
  '<div class="ch"><b>01</b> · なぜ · Why</div>'
  '<div class="words"><p class="q">“I collected as a kid, and picked the hobby back up.”</p><p class="q two">I wanted my binders with me.</p></div>'
  '<p class="copy">Card show, beach, couch: see exactly what’s in the collection. And no wild subscription just to look at my own cards.</p>'
  f'<div class="stg">{binder}</div>'
  '<div class="tick t1"><small>Saturday</small>Card show</div><div class="tick t2"><small>Sunday</small>The beach</div><div class="tick t3"><small>2 a.m.</small>The couch</div>')}
{beat('b2', False,
  '<div class="ch"><b>02</b> · 作り · The craft</div>'
  '<div class="words"><span class="l l1">Drawn like</span><span class="l l2 red">a card.</span><span class="l l3">Not a spreadsheet.</span></div>'
  f'<div class="stg">{home}</div>{SPIRAL}'
  '<div class="chip">Golden-ratio grid · Fibonacci steps</div>'
  '<div class="stk">NOPE!</div>')}
{beat('b3', True,
  '<div class="ch"><b>02</b> · 作り · Japanese sets</div>'
  '<div class="words"><span class="l l1">日本語も。</span><span class="l l2 red">全部。</span></div>'
  '<figure class="card en"><img src="../assets/cards/sv3pt5-199.jpg" alt=""><figcaption>EN</figcaption></figure>'
  '<figure class="card ja"><img src="../assets/cards/ja/SV2a-201.jpg" alt=""><figcaption>JA</figcaption></figure>'
  '<p class="copy c">English and Japanese sets side by side. Every printing, with live prices.</p>'
  '<div class="stk">全部!</div>')}
{beat('b4', False,
  '<div class="ch"><b>03</b> · なかま · The team</div>'
  '<div class="words"><span class="l l1">Collecting is</span><span class="l l2 r red">better with</span><span class="l l3">a team.</span></div>'
  f'<div class="stg a">{chat}</div><div class="stg b">{leaderboard}</div>'
  '<div class="chip">Trade board · DMs · Gym Leaders</div>'
  '<div class="stk a">DEAL!</div><div class="stk b w">やった!</div>')}
{beat('b5', True,
  '<div class="ch"><b>04</b> · やくそく · The promise</div>'
  '<div class="rows"><div class="row r1"><i class="bx"></i><span>No ads.</span></div><div class="row r2"><i class="bx"></i><span>No tracking.</span></div><div class="row r3"><i class="bx"></i><span>No “pro” tier.</span></div></div>'
  '<div class="words"><span class="l l1 c">Buy once.</span><span class="l l2 c red">It’s yours.</span></div>'
  '<div class="ticket"><b>Here early?</b>Free for life. Thanks for betting on a tiny app.</div>')}
{beat('b6', False,
  '<div class="ch c"><b>05</b> · つくったひと · The maker</div>'
  '<img class="face" src="../assets/bree.jpg" alt="">'
  '<div class="stk">HI!</div>'
  '<div class="words"><span class="l l1 c">Bree Pear.</span></div>'
  '<div class="role">Solo developer &amp; collector</div>'
  '<p class="copy c">Every pixel, drawn late at night with a binder open next to me.</p>'
  '<div class="words two"><span class="l l2 c">Track</span><span class="l l3 c red">’Em All.</span></div>'
  '<div class="pill">dexeontcg.com · free during beta</div>'
  f'<div class="stg a">{trades}</div><div class="stg b">{home}</div>')}
  <div class="sweep sw1"></div><div class="sweep sw2"></div><div class="sweep sw3"></div>
  <div class="sweep sw4"></div><div class="sweep sw5"></div><div class="sweep sw6"></div>
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
open('marketing/origin-story.html', 'w').write(HTML)
print('wrote marketing/origin-story.html')
