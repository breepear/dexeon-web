# "About" Story series: the story of Dexeon, told across ten 1080 x 1920 frames
# that follow the chapters of the app's About Dexeon page (Settings > About).
# Executed from build.py after remix.py, so it shares HEAD, CHROME, the mockups,
# REMIX_CSS, WM_L / WM_D and the mv() / head() helpers.

ABOUT_CSS = """
.ch{position:absolute;right:40px;top:290px;writing-mode:vertical-rl;text-orientation:mixed;font-size:26px;font-weight:900;letter-spacing:.3em;text-transform:uppercase;color:var(--ink-soft);z-index:9;background:var(--paper-2);border:4px solid var(--ink);box-shadow:6px 6px 0 var(--ink);padding:26px 10px 22px}
.ch b{color:var(--red)}
.q{font-family:var(--display);font-weight:400;font-size:420px;line-height:.6;color:var(--red);position:absolute;text-shadow:12px 12px 0 var(--ink);transform:skewX(-6deg)}
.tick{position:absolute;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:22px 34px 18px;font-family:var(--display);font-weight:400;font-size:64px;letter-spacing:.04em;text-transform:uppercase;z-index:8;line-height:1}
.tick small{display:block;font-family:var(--body);font-size:22px;font-weight:900;letter-spacing:.22em;color:var(--red);margin-bottom:6px}
.tick.stamp{border-style:dashed;border-width:7px}
/* 01 cover */
.a1 .toc{position:absolute;left:80px;right:80px;top:900px;background:var(--paper-2);border:7px solid var(--ink);box-shadow:16px 16px 0 var(--ink);padding:44px 52px}
.a1 .toc h2{margin:0 0 26px;font-family:var(--display);font-weight:400;font-size:40px;letter-spacing:.12em;text-transform:uppercase;text-align:center}
.a1 .toc div{display:flex;align-items:baseline;gap:18px;font-size:30px;font-weight:900;padding:14px 0;border-bottom:3px dotted var(--tone)}
.a1 .toc div:last-child{border-bottom:0}
.a1 .toc .n{font-family:var(--display);font-size:38px;color:var(--red);width:64px;flex:none}
.a1 .toc .k{color:var(--ink-soft);font-size:26px;flex:none}
.a1 .toc .t{flex:1;text-align:right}
.a1 .kana-big{position:absolute;left:0;right:0;top:230px;text-align:center;font-size:150px;font-weight:900;letter-spacing:.02em;color:var(--red);-webkit-text-stroke:5px var(--ink);text-shadow:12px 12px 0 var(--ink);z-index:2;white-space:nowrap}
/* 02 pull quote */
.a2 .quote{position:absolute;left:90px;right:150px;top:560px}
.a2 .quote h1{font-size:124px;margin:0}
.a2 .quote p{margin:60px 0 0;max-width:760px}
/* 03 anywhere */
.a3 .stg{left:300px;top:760px;transform:scale(2.35)}
/* 04 not a spreadsheet */
.a4 .sheet{position:absolute;left:70px;right:70px;top:560px;height:520px;background:#fff;border:6px solid var(--ink);overflow:hidden;display:grid;grid-template-columns:70px repeat(5,1fr);grid-auto-rows:52px;font-size:20px;font-weight:700;color:#5a5a60;font-family:ui-monospace,Menlo,monospace}
.a4 .sheet span{border-right:2px solid #d5d7d0;border-bottom:2px solid #d5d7d0;padding:12px 10px;white-space:nowrap;overflow:hidden}
.a4 .sheet span.h{background:#e8e9e3;color:#333;font-weight:900;text-align:center}
.a4 .sheet span.r{background:#e8e9e3;color:#333;text-align:center}
.a4 .x{position:absolute;left:60px;right:60px;top:540px;height:560px;z-index:7;pointer-events:none}
.a4 .stg{left:118px;top:1160px;transform:scale(1.75);z-index:3}
.a4 .spiral{position:absolute;left:118px;top:1160px;width:682px;height:760px;z-index:5;overflow:visible}
/* 05 EN + JA */
.a5 .pair{position:absolute;left:60px;right:60px;top:830px;display:flex;justify-content:center;gap:40px}
.a5 .pair figure{margin:0;position:relative;width:440px}
.a5 .pair img{width:100%;border-radius:22px;border:7px solid var(--ink);box-shadow:14px 14px 0 var(--ink);display:block}
.a5 .pair figcaption{position:absolute;left:-14px;top:-30px;background:var(--red);color:#fff;font-family:var(--display);font-size:44px;padding:8px 26px 4px;border:5px solid var(--ink);box-shadow:8px 8px 0 var(--ink);letter-spacing:.06em}
.a5 .pair figure.ja figcaption{background:var(--yellow);color:var(--ink)}
.a5 .pair figure.en{transform:rotate(-4deg)} .a5 .pair figure.ja{transform:rotate(4deg) translateY(60px)}
/* 06 team */
.a6 .ring{position:absolute;left:0;top:0;width:1080px;height:1920px;z-index:4}
.a6 .av{position:absolute;width:190px;height:190px;border-radius:50%;border:8px solid var(--ink);box-shadow:12px 12px 0 var(--ink);display:grid;place-items:center;font-family:var(--display);font-size:86px;color:#fff;text-shadow:4px 4px 0 var(--ink)}
.a6 .core{position:absolute;left:210px;right:210px;top:930px;text-align:center}
.a6 .core h1{font-size:92px;margin:0}
.a6 .chips{position:absolute;left:80px;right:80px;top:1400px;display:flex;flex-wrap:wrap;justify-content:center;gap:16px}
.a6 .chips span{background:var(--paper-2);border:5px solid var(--ink);box-shadow:7px 7px 0 var(--ink);padding:12px 24px;font-size:26px;font-weight:900}
/* 07 manifesto */
.a7 .rows{position:absolute;left:80px;right:80px;top:560px;display:grid;gap:26px}
.a7 .row{display:flex;align-items:center;gap:30px;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:26px 34px}
.a7 .row .bx{width:88px;height:88px;flex:none;border:6px solid var(--ink);background:var(--paper);position:relative}
.a7 .row .bx::before,.a7 .row .bx::after{content:"";position:absolute;left:50%;top:50%;width:104px;height:14px;background:var(--red);transform:translate(-50%,-50%) rotate(45deg)}
.a7 .row .bx::after{transform:translate(-50%,-50%) rotate(-45deg)}
.a7 .row span{font-family:var(--display);font-size:84px;text-transform:uppercase;line-height:1;transform:skewX(-6deg)}
.a7 .yes{position:absolute;left:80px;right:80px;top:1150px;text-align:center}
.a7 .yes h1{font-size:120px;margin:0}
.a7 .ticket{position:absolute;left:50%;top:1480px;transform:translateX(-50%) rotate(-3deg);background:var(--yellow);color:#121114;border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:22px 40px;font-size:30px;font-weight:900;white-space:nowrap;z-index:8}
.a7 .ticket b{font-family:var(--display);font-weight:400;font-size:48px;display:block;line-height:1;margin-bottom:4px}
/* 08 maker */
.a8 .face{position:absolute;left:50%;top:540px;transform:translateX(-50%);width:520px;height:520px;border-radius:50%;border:10px solid var(--ink);box-shadow:18px 18px 0 var(--ink);object-fit:cover;z-index:4}
.a8 .name{position:absolute;left:80px;right:80px;top:1110px;text-align:center}
.a8 .name h1{font-size:120px;margin:0}
.a8 .name .role{margin:18px 0 0;font-size:28px;font-weight:900;letter-spacing:.2em;text-transform:uppercase;color:var(--red)}
.a8 .name p.copy{margin:40px auto 0;max-width:860px}
.a8 .ig{position:absolute;left:50%;bottom:210px;transform:translateX(-50%);background:var(--red);color:#fff;font-size:30px;font-weight:900;padding:20px 40px;border:5px solid var(--ink);box-shadow:10px 10px 0 var(--ink);white-space:nowrap;z-index:8}
/* 09 name */
.a9 .eq{position:absolute;left:60px;right:60px;top:560px;display:flex;align-items:center;justify-content:center;gap:26px}
.a9 .eq .w{font-family:var(--display);font-size:150px;line-height:1;padding:10px 34px 2px;border:7px solid var(--ink);box-shadow:14px 14px 0 var(--ink);background:var(--paper-2);transform:skewX(-6deg)}
.a9 .eq .w.b{background:var(--blue);color:#fff} .a9 .eq .w.r{background:var(--red);color:#fff}
.a9 .eq .op{font-family:var(--display);font-size:120px;color:var(--ink-soft)}
.a9 .res{position:absolute;left:0;right:0;top:820px;text-align:center}
.a9 .res .w{display:inline-block;font-family:var(--display);font-size:200px;line-height:1;padding:14px 50px 4px;border:8px solid var(--ink);box-shadow:18px 18px 0 var(--ink);background:var(--yellow);color:#121114;transform:skewX(-6deg)}
.a9 .kana{position:absolute;left:0;right:0;top:1120px;text-align:center}
.a9 .kana .k{font-size:110px;font-weight:900;letter-spacing:.06em;color:var(--ink);line-height:1}
.a9 .kana .s{margin-top:16px;font-size:30px;font-weight:900;letter-spacing:.4em;color:var(--red)}
.a9 .fam{position:absolute;left:80px;right:80px;top:1340px;display:flex;justify-content:center;gap:16px;flex-wrap:wrap}
.a9 .fam span{background:var(--paper-2);border:5px solid var(--ink);box-shadow:7px 7px 0 var(--ink);padding:10px 22px;font-size:28px;font-weight:900}
.a9 .fam span b{color:var(--blue)}
/* 10 next */
.a10 .map{position:absolute;left:80px;right:80px;top:620px;display:grid;gap:20px}
.a10 .it{display:flex;align-items:center;gap:26px;background:var(--paper-2);border:6px solid var(--ink);box-shadow:12px 12px 0 var(--ink);padding:16px 32px;font-size:32px;font-weight:900;min-height:56px}
.a10 .it i{width:34px;height:34px;border-radius:50%;background:var(--green);border:5px solid var(--ink);flex:none}
.a10 .it i.q{background:var(--yellow)}
.a10 .it .red{display:inline-block;background:var(--ink);color:var(--ink);height:38px;vertical-align:middle;border-radius:6px}
.a10 .thanks{position:absolute;left:80px;right:80px;top:1300px;text-align:center}
.a10 .thanks h1{font-size:104px;margin:0}
"""

profile = grab_phone('Mockup 2:')

def chapter(n, kana, en):
    return f'<div class="ch"><b>{n:02d}</b> · {kana} · {en}</div>'

def avatar(x, y, bg, letter, rot=0):
    return f'<div class="av" style="left:{x}px;top:{y}px;background:{bg};transform:rotate({rot}deg)">{letter}</div>'

SPIRAL = ('<svg class="spiral" viewBox="0 0 618 1000" width="682" height="1104" fill="none" stroke="#2E5AAC" stroke-width="5" opacity=".95">'
          '<g stroke-dasharray="14 12" stroke-width="3"><rect x="0" y="0" width="618" height="618"/><rect x="236" y="618" width="382" height="382"/>'
          '<rect x="0" y="764" width="236" height="236"/><rect x="0" y="618" width="146" height="146"/><rect x="146" y="618" width="90" height="90"/></g>'
          '<path stroke-width="9" d="M0 0 A618 618 0 0 1 618 618 A382 382 0 0 1 236 1000 A236 236 0 0 1 0 764 A146 146 0 0 1 146 618 A90 90 0 0 1 236 708 A56 56 0 0 1 180 764"/>'
          '</svg>')

BIGX = ('<svg class="x" viewBox="0 0 960 560" preserveAspectRatio="none"><path d="M40 40 L920 520 M920 40 L40 520" stroke="#121114" stroke-width="44" stroke-linecap="round" transform="translate(10 10)"/>'
        '<path d="M40 40 L920 520 M920 40 L40 520" stroke="#C8322E" stroke-width="30" stroke-linecap="round"/></svg>')

sheet_cells = '<span class="h"></span>' + ''.join(f'<span class="h">{c}</span>' for c in 'ABCDE')
rows = [('Charizard', 'sv3pt5', '199', '1', '$178.43'), ('Pikachu', 'sv8', '238', '2', '$41.10'), ('Mew ex', 'sv3pt5', '151', '1', '$14.75'),
        ('Gengar', 'sv4pt5', '232', '1', '$22.00'), ('Bulbasaur', 'base1', '44', '3', '$1.25'), ('Squirtle', 'base1', '63', '2', '$1.10'),
        ('Eevee', 'sv7', '143', '1', '$3.40'), ('Snorlax', 'sv6', '207', '1', '$9.99'), ('Jigglypuff', 'xy12', '11', '4', '$0.60')]
for i, r in enumerate(rows, 1):
    sheet_cells += f'<span class="r">{i}</span>' + ''.join(f'<span>{c}</span>' for c in r)

ABOUT = [
 # 01 cover
 dict(theme='light', cls='a1', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    '<div class="kana-big">デクセオン</div>'
    '<div style="position:absolute;left:80px;right:80px;top:470px;text-align:center"><span class="eyebrow" style="justify-content:center">Origin story · swipe</span>'
    '<h1 class="big" style="font-size:150px;margin:18px 0 0">Where<br><span class="red">it came from.</span></h1></div>'
    '<div class="toc"><h2>Contents</h2>'
    '<div><span class="n">01</span><span class="k">なぜ</span><span class="t">Why</span></div>'
    '<div><span class="n">02</span><span class="k">作り</span><span class="t">The craft</span></div>'
    '<div><span class="n">03</span><span class="k">なかま</span><span class="t">The team</span></div>'
    '<div><span class="n">04</span><span class="k">やくそく</span><span class="t">The promise</span></div>'
    '<div><span class="n">05</span><span class="k">つくったひと</span><span class="t">The maker</span></div>'
    '<div><span class="n">06</span><span class="k">なまえ</span><span class="t">The name</span></div>'
    '<div><span class="n">07</span><span class="k">これから</span><span class="t">What\'s next</span></div></div>'
    '<span class="sfx" style="right:30px;top:850px;transform:rotate(6deg)">ドン!</span>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
 # 02 why: pull quote
 dict(theme='dark', cls='a2', body=(
    f'<img class="brand tl" src="{WM_D}" alt="">'
    + chapter(1, 'なぜ', 'Why') +
    '<div class="q" style="left:70px;top:330px">“</div>'
    '<div class="quote"><h1 class="big">I collected as a kid, and recently picked the hobby<br><span class="red">back up.</span></h1>'
    '<p class="copy">In a digital world, keeping track of it all is somehow both easier and harder than it used to be.</p>'
    '<p class="copy" style="margin-top:30px">Other apps wanted a wild subscription just to look at my own cards. I wanted something accessible, so more people can enjoy this hobby as much as I have.</p></div>'
    '<div class="stat-tag" style="left:80px;top:1560px;transform:rotate(-3deg)"><b>Bree</b>solo developer &amp; collector</div>'
    '<div class="url" style="bottom:110px;left:auto;right:80px;transform:none">dexeontcg.com</div>')),
 # 03 why: binders anywhere
 dict(theme='light', cls='a3', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    + chapter(1, 'なぜ', 'Why') +
    head('The itch', 'Your binders.<br><span class="red">Everywhere.</span>', 128,
         '<p class="copy" style="margin:34px auto 0;max-width:820px">What I really wanted was to carry my physical binders with me. Card show, beach, couch: see exactly what\'s in the collection at any moment.</p>') +
    f'<div class="stg">{binder}</div>'
    '<div class="tick stamp" style="left:60px;top:900px;transform:rotate(-8deg)"><small>Saturday</small>Card show</div>'
    '<div class="tick stamp" style="right:50px;top:1130px;transform:rotate(6deg)"><small>Sunday</small>The beach</div>'
    '<div class="tick stamp" style="left:80px;top:1400px;transform:rotate(-4deg)"><small>2 a.m.</small>The couch</div>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
 # 04 craft: not a spreadsheet
 dict(theme='light', cls='a4', body=(
    f'<img class="brand tl" src="{WM_L}" alt="">'
    + chapter(2, '作り', 'Craft') +
    '<div style="position:absolute;left:80px;width:860px;top:280px"><span class="eyebrow">The craft</span>'
    '<h1 class="big" style="font-size:108px;margin:18px 0 0">Drawn like a card.<br><span class="red">Not a spreadsheet.</span></h1></div>'
    f'<div class="sheet">{sheet_cells}</div>{BIGX}'
    '<span class="sfx" style="right:70px;top:1010px;transform:rotate(6deg)">NOPE!</span>'
    f'<div class="stg">{home}</div>{SPIRAL}'
    '<div class="stat-tag" style="right:60px;top:1240px;transform:rotate(3deg);max-width:300px"><b>φ</b>golden-ratio grid, one Fibonacci step at a time</div>'
    '<div class="url" style="bottom:110px;left:auto;right:80px;transform:none">dexeontcg.com</div>')),
 # 05 craft: EN + JA
 dict(theme='dark', cls='a5', body=(
    f'<img class="brand" src="{WM_D}" alt="">'
    + chapter(2, '作り', 'Craft') +
    head('Same card · two languages', '日本語も。<br><span class="red">全部。</span>', 150,
         '<p class="copy" style="margin:30px auto 0;max-width:820px">English and Japanese sets sit side by side, every printing, with live prices.</p>') +
    '<div class="pair"><figure class="en"><img src="../assets/cards/sv3pt5-199.jpg" alt=""><figcaption>EN</figcaption></figure>'
    '<figure class="ja"><img src="../assets/cards/ja/SV2a-201.jpg" alt=""><figcaption>JA</figcaption></figure></div>'
    '<span class="sfx y" style="left:50px;top:1560px;transform:rotate(-6deg)">全部!</span>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
 # 06 team: avatar ring
 dict(theme='light', cls='a6', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    + chapter(3, 'なかま', 'Team') +
    '<div style="position:absolute;left:80px;right:80px;top:280px;text-align:center"><span class="eyebrow" style="justify-content:center">Collecting is better</span></div>'
    '<div class="ring">'
    + avatar(445, 560, '#2E5AAC', 'H', -6) + avatar(150, 700, '#2FA44F', 'M', 5) + avatar(740, 700, '#C8322E', 'J', -4)
    + avatar(70, 1000, '#F7C728', 'T', 3) + avatar(820, 1000, '#7A4FBF', 'K', -5) + avatar(150, 1300, '#E0463F', 'R', 6)
    + avatar(740, 1300, '#2E5AAC', 'A', -3) + avatar(445, 1420, '#2FA44F', 'B', 4) +
    '</div>'
    '<div class="core"><h1 class="big">With a<br><span class="red">team.</span></h1></div>'
    '<span class="sfx" style="left:250px;top:1180px;transform:rotate(-8deg)">DEAL!</span>'
    '<span class="sfx y" style="right:230px;top:1180px;transform:rotate(7deg)">やった!</span>'
    '<div class="chips" style="top:1660px"><span>Add trainers</span><span>Show off grails</span><span>Trade doubles</span><span>Climb the Gym Leaders board</span><span>DM about the exact card</span></div>'
    '<div class="url" style="bottom:40px">dexeontcg.com · link in bio</div>')),
 # 07 promise: manifesto
 dict(theme='dark', cls='a7', body=(
    f'<img class="brand tl" src="{WM_D}" alt="">'
    + chapter(4, 'やくそく', 'Promise') +
    '<div style="position:absolute;left:80px;width:860px;top:280px"><span class="eyebrow">The promise</span>'
    '<h1 class="big" style="font-size:96px;margin:18px 0 0">One price.<br><span class="red">Never a subscription.</span></h1></div>'
    '<div class="rows"><div class="row"><i class="bx"></i><span>No ads.</span></div><div class="row"><i class="bx"></i><span>No tracking.</span></div>'
    '<div class="row"><i class="bx"></i><span>No “pro” tier.</span></div></div>'
    '<div class="yes"><h1 class="big">Buy once.<br><span class="red">It\'s yours.</span></h1></div>'
    '<div class="ticket"><b>Here early?</b>Free for life. Thanks for betting on a tiny app.</div>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
 # 08 maker
 dict(theme='light', cls='a8', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    + chapter(5, 'つくったひと', 'Maker') +
    '<div style="position:absolute;left:80px;right:80px;top:280px;text-align:center"><span class="eyebrow" style="justify-content:center">Made by one collector</span></div>'
    '<img class="face" src="../assets/bree.jpg" alt="">'
    '<span class="sfx" style="right:130px;top:520px;transform:rotate(8deg)">HI!</span>'
    '<div class="name"><h1 class="big">Bree <span class="red">Pear.</span></h1><p class="role">Solo developer &amp; collector</p>'
    '<p class="copy">I designed, built, and drew every pixel of Dexeon myself, mostly late at night with a binder open next to me. If something feels handmade, that\'s because it is.</p></div>'
    '<div class="ig">@dexeontcg · dexeontcg.com</div>')),
 # 09 name
 dict(theme='dark', cls='a9', body=(
    f'<img class="brand tl" src="{WM_D}" alt="">'
    + chapter(6, 'なまえ', 'Name') +
    '<div style="position:absolute;left:80px;width:860px;top:280px"><span class="eyebrow">Where the name came from</span>'
    '<h1 class="big" style="font-size:108px;margin:18px 0 0">Five minutes.<br><span class="red">One name.</span></h1></div>'
    '<div class="eq"><span class="w b">Dex</span><span class="op">+</span><span class="w r">eon</span></div>'
    '<div class="res"><span class="w">Dexeon</span></div>'
    '<div class="kana"><div class="k">デクセオン</div><div class="s">de · ku · se · on</div></div>'
    '<div class="fam"><span>Jolt<b>eon</b></span><span>Flar<b>eon</b></span><span>Vapor<b>eon</b></span><span>Leaf<b>eon</b></span></div>'
    '<p class="copy" style="position:absolute;left:80px;right:80px;top:1470px;text-align:center;margin:0">“Dex” is a word every collector knows. “-eon” comes from my fiancée\'s favorite family of evolutions. The katakana sits in the logo to honor the culture that birthed this fandom.</p>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
 # 10 next
 dict(theme='light', cls='a10', body=(
    f'<img class="brand" src="{WM_L}" alt="">'
    + chapter(7, 'これから', 'Next') +
    '<div style="position:absolute;left:80px;right:80px;top:280px;text-align:center"><span class="eyebrow" style="justify-content:center">What\'s next</span>'
    '<h1 class="big" style="font-size:128px;margin:18px 0 0">This is just<br><span class="red">the start.</span></h1></div>'
    '<div class="map"><div class="it"><i></i>More sets</div><div class="it"><i></i>Deeper stats</div><div class="it"><i></i>Smarter trades</div>'
    '<div class="it"><i class="q"></i><span class="red" style="width:300px"></span>&nbsp;&nbsp;<small style="font-size:24px;color:var(--ink-soft)">not ready to spoil</small></div>'
    '<div class="it"><i class="q"></i><span class="red" style="width:420px"></span></div></div>'
    '<div class="thanks"><h1 class="big">Thank you for<br><span class="red">being here early.</span></h1>'
    '<p class="copy" style="margin:30px auto 0;max-width:760px">Dexeon grows every week. Now go catch \'em all.</p></div>'
    '<span class="sfx y" style="right:60px;top:1150px;transform:rotate(7deg)">GO!</span>'
    '<div class="url" style="bottom:110px">dexeontcg.com · link in bio</div>')),
]

os.makedirs('assets/social/stories/about', exist_ok=True)
for f in glob.glob('marketing/about-*.html'):
    os.remove(f)
for n, r in enumerate(ABOUT, 1):
    body = f'<div class="shot {r["cls"]}"><div class="halft"></div><div class="kana-bg" aria-hidden="true">デクセオン</div>{r["body"]}</div>'
    open(f'marketing/about-{n:02d}.html', 'w').write(
        f'<!doctype html>\n<html lang="en" data-theme="{r["theme"]}"><head>{HEAD}<style>{REMIX_CSS}{ABOUT_CSS}</style></head><body>{body}</body></html>')

srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
try:
    for n in range(1, len(ABOUT) + 1):
        subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars', '--force-device-scale-factor=1',
                        '--window-size=1080,1920', '--virtual-time-budget=8000',
                        f'--screenshot=assets/social/stories/about/about-{n:02d}.png',
                        f'http://localhost:8765/marketing/about-{n:02d}.html'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print('rendered about', n)
finally:
    srv.terminate()

for f in glob.glob('marketing/about-*.html'):
    os.remove(f)
