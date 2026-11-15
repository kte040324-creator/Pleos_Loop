"""앱용 index.html 패치(웹 원본 web/loop.html은 건드리지 않음).
1) tts-shim.js 주입  2) CDN → 로컬(vendor/, fonts/) 교체(파일이 있을 때만)"""
import sys, os
p = sys.argv[1]; d = os.path.dirname(p)
s = open(p, encoding="utf-8").read()
if '<meta charset' not in s[:500]:
    s = '<meta charset="utf-8">\n' + s
# 앱에서는 화면 확대(핀치·더블탭) 금지
if '<meta name="viewport"' not in s:
    i = s.find("\n") + 1
    s = s[:i] + '<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">\n' + s[i:]
if "tts-shim.js" not in s:
    i = s.find("<script")
    s = s[:i] + '<script src="tts-shim.js"></script>\n' + s[i:]
LOT = "https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie_light.min.js"
if os.path.exists(os.path.join(d, "vendor/lottie_light.min.js")):
    s = s.replace(LOT, "vendor/lottie_light.min.js")
if os.path.exists(os.path.join(d, "fonts/fonts.css")):
    import re
    s = re.sub(r'<link[^>]+fonts\.googleapis\.com/css2[^>]*>', '<link rel="stylesheet" href="fonts/fonts.css">', s)
    s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">', '').replace('<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>', '')
# 3) Loop 창만 보이기: Pleos가 앱에 주는 영역 = 디자인의 Loop 창(420,48 / 850×592).
#    차량 화면 시뮬레이션(Driving View·상단바·GNB)은 Pleos 실제 화면이 대신하므로 잘라내고,
#    Loop 창 영역만 앱 화면에 비율 유지로 꽉 채운다. (#scr·#ovl·#obl 모두 #unit 안이라 함께 따라감)
#    하루 끝 '다음 날로' 안내는 원래 왼쪽(잘리는 자리)에 뜨므로, 앱에서는 안내·버튼을 숨기고
#    하루 요약을 몇 초 보여준 뒤 자동으로 다음 날로 넘어간다(안내가 뜬 뒤 4초 = 하루 끝 화면 진입 후 약 5.5초).
CROP = """<style id="app-crop">html,body{margin:0!important;padding:0!important;overflow:hidden!important}#stage{position:fixed!important;inset:0!important;width:auto!important;height:auto!important;overflow:hidden!important}#unit{box-shadow:none!important;outline:none!important;border:0!important;border-radius:0!important}#unit.dimon{background:var(--surface)!important}#unit .dimly{display:none!important}</style>
<script id="app-crop-fit">(function(){function cropFit(){var u=document.getElementById('unit');if(!u)return;var W=innerWidth,H=innerHeight,k=Math.min(W/850,H/592),x=(W-850*k)/2-420*k,y=(H-592*k)/2-48*k;u.style.transform='translate('+x+'px,'+y+'px) scale('+k+')'}addEventListener('resize',cropFit);cropFit();var u=document.getElementById('unit'),T=null;if(u)new MutationObserver(function(){var on=u.classList.contains('dimon');if(on&&!T)T=setTimeout(function(){T=null;if(!u.classList.contains('dimon'))return;var b=document.querySelector('#unit [data-a="tonext"]');if(b)b.click()},4000);else if(!on&&T){clearTimeout(T);T=null}}).observe(u,{attributes:true,attributeFilter:['class']})})();</script>
"""
# 4) 시스템 키보드 끄기: Loop는 화면 안에 자체 키보드를 그리므로, 입력창에 inputmode="none"을 붙여
#    안드로이드(Pleos) 키보드가 함께 뜨지 않게 한다. (화면이 다시 그려져도 새 입력창에 계속 적용)
NOIME = """<script id="app-no-ime">(function(){function f(){var l=document.querySelectorAll('input,textarea');for(var i=0;i<l.length;i++)if(l[i].getAttribute('inputmode')!=='none')l[i].setAttribute('inputmode','none')}f();new MutationObserver(f).observe(document.documentElement,{childList:true,subtree:true})})();</script>
"""
if 'id="app-no-ime"' not in s:
    i = s.rfind("</body>")
    s = s[:i] + NOIME + s[i:] if i >= 0 else s + "\n" + NOIME
if 'id="app-crop"' not in s:
    i = s.rfind("</body>")
    s = s[:i] + CROP + s[i:] if i >= 0 else s + "\n" + CROP
open(p, "w", encoding="utf-8").write(s)
