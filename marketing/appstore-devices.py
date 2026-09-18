# Ten App Store screens (1242 x 2688, iPhone 6.5") built from REAL simulator
# captures of Dexeon on iPhone 17 Pro and iPad Pro 13", in the site's newsprint
# style. Light and dark alternate, and the screenshots match: light screens use
# the app in light mode, dark screens use it in dark mode.
#
#   python3 marketing/appstore-devices.py            # writes + renders all ten
#   python3 marketing/appstore-devices.py --no-render # HTML only
#
# Captures: marketing/shots/{,dark/}  and  marketing/shots/ipad/{,dark/}
import re, os, subprocess, time, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
style = re.search(r'<style>(.*?)</style>', open('index.html').read(), re.S).group(1)
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
W, H = 1242, 2688
OUT = 'assets/appstore/v2'

WM_L = '../assets/logo/dexeon-wordmark-nav.png'
WM_D = '../assets/logo/dexeon-wordmark-nav-dark.png'

def phone(name, dark, cls=''):
    src = f'shots/dark/{name}.png' if dark else f'shots/{name}.png'
    return f'<div class="stg {cls}"><div class="ph"><img src="{src}" alt=""></div></div>'

def ipad(name, dark, cls=''):
    src = f'shots/ipad/dark/{name}.png' if dark else f'shots/ipad/{name}.png'
    return f'<div class="stg {cls}"><div class="pad"><img src="{src}" alt=""></div></div>'

CSS = """
html,body{margin:0;width:1242px;height:2688px;overflow:hidden;font-family:var(--body)}
.shot{position:relative;width:1242px;height:2688px;overflow:hidden;background:var(--paper);color:var(--ink)}
.shot.dk{--paper:#131316;--paper-2:#1B1B1F;--ink:#F1F0EA;--ink-soft:#B8B6BE;--tone:#2A2A2F;--red:#E0463F;--yellow:#F7C728;--blue:#5B86D6;--green:#43C06A}
.halft{position:absolute;inset:0;background-image:radial-gradient(var(--tone) 2.6px,transparent 3.4px);background-size:24px 24px;opacity:.55}
.dk .halft{opacity:.9;background-image:radial-gradient(#2c2c31 2.6px,transparent 3.4px)}
.kana{position:absolute;left:-70px;bottom:-60px;font-size:560px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:3px #e3e5de;white-space:nowrap;letter-spacing:-.04em}
.dk .kana{-webkit-text-stroke:3px #212126}
.speed{position:absolute;inset:-20%;opacity:.12;background:repeating-conic-gradient(from 0deg at 50% 40%, var(--ink) 0deg .5deg, transparent .5deg 5deg);
  -webkit-mask:radial-gradient(circle at 50% 40%, transparent 26%, #000 44%, #000 68%, transparent 88%);mask:radial-gradient(circle at 50% 40%, transparent 26%, #000 44%, #000 68%, transparent 88%)}

.wm{position:absolute;left:50%;top:96px;width:300px;margin-left:-150px;z-index:30}
.wm img{width:100%;display:block}
.eyebrow2{position:absolute;left:0;right:0;top:292px;text-align:center;font-size:27px;font-weight:900;letter-spacing:.26em;text-transform:uppercase;color:var(--ink-soft);z-index:30}
.eyebrow2::before,.eyebrow2::after{content:"";display:inline-block;width:58px;height:7px;background:var(--red);vertical-align:middle;margin:0 20px}

h1{position:absolute;left:56px;right:56px;top:362px;margin:0;z-index:20;text-align:center;
   font-family:var(--display);font-weight:400;text-transform:uppercase;line-height:.9;
   transform:skewX(-6deg);text-shadow:8px 8px 0 var(--paper),15px 15px 0 var(--ink);font-size:112px}
h1 .red{color:var(--red)}
.sub{position:absolute;left:104px;right:104px;top:606px;z-index:20;text-align:center;
     font-size:35px;line-height:1.3;font-weight:700;color:var(--ink-soft);text-wrap:balance}

/* Device frames, drawn at device-point size then scaled into place. */
.stg{position:absolute;left:0;top:0;transform-origin:top left;z-index:5}
.ph{width:402px;height:874px;box-sizing:border-box;padding:12px;background:#0d0d0f;border-radius:66px;position:relative;
    box-shadow:0 40px 80px -28px rgba(0,0,0,.6),0 0 0 2px #2b2b30 inset,0 0 0 3px #121114}
.ph::before{content:"";position:absolute;top:22px;left:50%;transform:translateX(-50%);width:120px;height:34px;background:#0d0d0f;border-radius:20px;z-index:2}
.ph img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:54px;display:block}
.pad{width:1032px;height:1376px;box-sizing:border-box;padding:28px;background:#0d0d0f;border-radius:58px;
     box-shadow:0 50px 100px -28px rgba(0,0,0,.6),0 0 0 3px #2b2b30 inset,0 0 0 4px #121114}
.pad img{width:100%;height:100%;object-fit:cover;object-position:top;border-radius:32px;display:block}

.chip{position:absolute;z-index:14;background:var(--paper-2);border:7px solid var(--ink);box-shadow:14px 14px 0 var(--ink);
      padding:22px 38px;font-size:34px;font-weight:900;white-space:nowrap;color:var(--ink)}
.stk{position:absolute;z-index:14;font-family:'Bangers',var(--display);font-size:104px;letter-spacing:.04em;color:#121114;
     background:var(--yellow);border:8px solid var(--ink);box-shadow:14px 14px 0 var(--ink);padding:14px 40px 8px;line-height:1}
.stk.w{background:var(--paper-2);color:var(--ink)}
.tag{position:absolute;z-index:16;background:var(--ink);color:var(--paper);font-size:25px;font-weight:900;letter-spacing:.18em;
     text-transform:uppercase;padding:13px 24px;border:4px solid var(--paper);box-shadow:9px 9px 0 var(--red)}
.pill{position:absolute;left:50%;transform:translateX(-50%);z-index:16;background:var(--ink);color:var(--paper);font-weight:900;
      font-size:34px;letter-spacing:.08em;padding:24px 52px;border:5px solid var(--paper);box-shadow:13px 13px 0 var(--red);white-space:nowrap}
"""

# Each screen: (dark?, eyebrow, headline, subline, body)
SCREENS = [
 # Geometry: iPad .80 -> 826x1101, iPhone 1.30 -> 523x1136 on a 1242x2688 canvas.
 # Devices sit between y=830 and y=2380, leaving the bottom chip clear at ~2500.

 # 1 ── Full Dex, both devices
 (False, 'The Full Dex', 'Track all<br><span class="red">1025.</span>',
  'Every species across nine generations, laid out for whichever screen you pick up.',
  ipad('home', False, 'a') + phone('home', False, 'b')
  + '<span class="tag" style="left:104px;top:774px">iPad</span>'
  + '<span class="tag" style="right:64px;top:2336px">iPhone</span>'
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Tap the ring to catch one</div>'
  + '<span class="stk" style="right:36px;top:724px;transform:rotate(7deg)">GOTCHA!</span>',
  'a:96,838,.80 b:660,1176,1.30'),

 # 2 ── prices
 (True, 'Every printing', 'Every printing.<br><span class="red">Live prices.</span>',
  'Low, average and high for every condition, with ninety days of history on the card itself.',
  phone('species', True, 'a') + phone('price', True, 'b')
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">NM · LP · MP · DMG</div>'
  + '<span class="stk w" style="left:40px;top:748px;transform:rotate(-7deg)">ドン!</span>',
  'a:72,884,1.22 b:602,1128,1.42'),

 # 3 ── binders, both devices
 (False, 'Binders', 'Nine pockets.<br><span class="red">Full size.</span>',
  'Lay a page out like the real thing, drag cards between pockets, then share it with a link or print it.',
  ipad('binder-base', False, 'a') + phone('binders', False, 'b')
  + '<span class="tag" style="left:104px;top:774px">iPad</span>'
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Drag. Drop. Share. Print.</div>'
  + '<span class="stk" style="right:36px;top:724px;transform:rotate(6deg)">FLIP!</span>',
  'a:96,838,.80 b:660,1176,1.30'),

 # 4 ── scan
 (True, 'Point and shoot', 'Scan it.<br><span class="red">Match it.</span>',
  'Hold a card up to the camera and Dexeon finds the exact printing, set and number.',
  phone('scan', True, 'a') + phone('species', True, 'b')
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Japanese cards too</div>'
  + '<span class="stk" style="right:36px;top:730px;transform:rotate(8deg)">SNAP!</span>',
  'a:78,900,1.24 b:598,1150,1.40'),

 # 5 ── Japanese sets, both devices
 (False, 'Japanese sets', 'Japanese sets.<br><span class="red">All of them.</span>',
  'The full Japanese catalog sits beside the English one — same pages, same search, same prices.',
  phone('sets-all', False, 'a') + phone('ja-set', False, 'b')
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Browse by language, or search across both</div>'
  + '<span class="stk" style="left:40px;top:730px;transform:rotate(-7deg)">全部!</span>',
  'a:72,884,1.22 b:602,1128,1.42'),

 # 6 ── trade board, both devices
 (True, 'Community trades', 'Trade with<br><span class="red">collectors.</span>',
  'Post the doubles you are done with, browse what everyone else has listed, and sort it your way.',
  ipad('home', True, 'a') + phone('trades', True, 'b')
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Filter by price, condition or your chase list</div>'
  + '<span class="stk" style="left:40px;top:730px;transform:rotate(-8deg)">DEAL!</span>',
  'a:96,838,.80 b:660,1176,1.30'),

 # 7 ── messages
 (False, 'Direct messages', 'Send the card.<br><span class="red">Not a photo.</span>',
  'Cards and whole binders travel inside the message with the price attached — then you shake on the trade.',
  phone('messages', False, 'a') + phone('profile', False, 'b')
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Both confirm · both ship · done</div>'
  + '<span class="stk" style="right:36px;top:730px;transform:rotate(7deg)">やった!</span>',
  'a:72,884,1.34 b:640,1180,1.22'),

 # 8 ── leaderboard, both devices
 (True, 'Gym Leaders', 'Climb the<br><span class="red">board.</span>',
  'Ranked by Full Dex, by sets completed, or by the week — a podium for the top three and a place for everyone else.',
  ipad('binder', True, 'a') + phone('leaderboard', True, 'b')
  + '<span class="tag" style="left:104px;top:762px">iPad</span>'
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Resets every week</div>'
  + '<span class="stk" style="right:36px;top:724px;transform:rotate(6deg)">GO!</span>',
  'a:96,838,.80 b:660,1176,1.30'),

 # 9 ── value, both devices
 (False, 'What it is worth', 'Know the<br><span class="red">number.</span>',
  'A running value for the whole collection, and a chase list that totals itself.',
  ipad('binders', False, 'a') + phone('chase', False, 'b')
  + '<div class="chip" style="left:50%;transform:translateX(-50%);bottom:96px">Estimated from live market data</div>'
  + '<span class="stk" style="left:40px;top:730px;transform:rotate(-6deg)">CHA-CHING!</span>',
  'a:96,838,.80 b:660,1176,1.30'),

 # 10 ── beta CTA, both devices
 (True, 'Now in beta', 'Free while<br><span class="red">it lasts.</span>',
  'A universal app for iPhone and iPad, built by one collector. Early adopters keep it free for life.',
  ipad('profile', True, 'a') + phone('home', True, 'b')
  + '<div class="pill" style="bottom:104px">dexeontcg.com</div>'
  + '<span class="stk" style="right:36px;top:730px;transform:rotate(7deg)">ドン!</span>',
  'a:96,838,.80 b:660,1176,1.30'),
]

def stage_css(spec):
    """`a:x,y,scale b:x,y,scale` → absolute transforms for each device."""
    out = []
    for part in spec.split():
        cls, nums = part.split(':')
        x, y, s = nums.split(',')
        out.append(f'.stg.{cls}{{transform:translate({x}px,{y}px) scale({s})}}')
    return '\n'.join(out)

os.makedirs(OUT, exist_ok=True)
for f in glob.glob('marketing/appstore-v2-*.html'):
    os.remove(f)

HEAD = ('<meta charset="utf-8"><title>Dexeon App Store screen</title>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Anton&family=Bangers&family=M+PLUS+Rounded+1c:wght@400;500;700;800;900&display=swap">')

for i, (dark, eyebrow, head, sub, body, stages) in enumerate(SCREENS, 1):
    wm = WM_D if dark else WM_L
    html = (f'<!doctype html>\n<html lang="en" data-theme="light"><head>{HEAD}'
            f'<style>{style}</style><style>{CSS}\n{stage_css(stages)}</style></head><body>'
            f'<div class="shot{" dk" if dark else ""}">'
            f'<div class="halft"></div><div class="kana" aria-hidden="true">デクセオン</div>'
            f'<div class="speed"></div>'
            f'<img class="wm" src="{wm}" alt="Dexeon">'
            f'<div class="eyebrow2">{eyebrow}</div>'
            f'<h1>{head}</h1><p class="sub">{sub}</p>{body}</div></body></html>')
    open(f'marketing/appstore-v2-{i:02d}.html', 'w').write(html)
print(f'wrote {len(SCREENS)} screens')

if '--no-render' in sys.argv:
    sys.exit(0)

srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    for i in range(1, len(SCREENS) + 1):
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
                        '--force-device-scale-factor=1', f'--window-size={W},{H}',
                        '--virtual-time-budget=9000',
                        f'--screenshot={OUT}/dexeon-{i:02d}.png',
                        f'http://localhost:8765/marketing/appstore-v2-{i:02d}.html'],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('rendered', i)
finally:
    srv.terminate()

for f in glob.glob('marketing/appstore-v2-*.html'):
    os.remove(f)
