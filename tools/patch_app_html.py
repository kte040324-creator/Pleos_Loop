"""앱용 index.html 패치(웹 원본 web/loop.html은 건드리지 않음).
1) tts-shim.js 주입  2) CDN → 로컬(vendor/, fonts/) 교체(파일이 있을 때만)"""
import sys, os
p = sys.argv[1]; d = os.path.dirname(p)
s = open(p, encoding="utf-8").read()
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
open(p, "w", encoding="utf-8").write(s)
