"""앱용 index.html 패치(웹 원본 web/loop.html은 건드리지 않음).
1) tts-shim.js 주입  2) CDN → 로컬(vendor/, fonts/) 교체(파일이 있을 때만)"""
import sys, os
p = sys.argv[1]; d = os.path.dirname(p)
s = open(p, encoding="utf-8").read()
if '<meta charset' not in s[:500]:
    s = '<meta charset="utf-8">\n' + s
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
CROP = """<style id="app-crop">html,body{margin:0!important;padding:0!important;overflow:hidden!important}#stage{position:fixed!important;inset:0!important;width:auto!important;height:auto!important;overflow:hidden!important}#unit{box-shadow:none!important;outline:none!important;border:0!important;border-radius:0!important}</style>
<script id="app-crop-fit">(function(){function cropFit(){var u=document.getElementById('unit');if(!u)return;var W=innerWidth,H=innerHeight,k=Math.min(W/850,H/592),x=(W-850*k)/2-420*k,y=(H-592*k)/2-48*k;u.style.transform='translate('+x+'px,'+y+'px) scale('+k+')'}addEventListener('resize',cropFit);cropFit()})();</script>
"""
if 'id="app-crop"' not in s:
    i = s.rfind("</body>")
    s = s[:i] + CROP + s[i:] if i >= 0 else s + "\n" + CROP
open(p, "w", encoding="utf-8").write(s)
