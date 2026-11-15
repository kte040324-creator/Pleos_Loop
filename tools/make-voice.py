"""Pleos용 미리 녹음 음성 생성 (macOS 전용: say + afconvert).
Pleos 에뮬레이터에는 안드로이드 표준 TTS 엔진이 없어서, tools/voice-lines.txt의 문구를
Mac 한국어 음성(Yuna)으로 녹음해 app/src/main/assets/voice/ 에 넣는다.
tts-shim.js가 같은 문구를 말할 때 이 녹음을 재생하고, 없는 문구만 안드로이드 TTS로 넘긴다."""
import hashlib, json, os, subprocess, sys, tempfile
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
out = os.path.join(root, "app/src/main/assets/voice")
os.makedirs(out, exist_ok=True)
lines = [l.strip() for l in open(os.path.join(root, "tools/voice-lines.txt"), encoding="utf-8") if l.strip()]
idx = {}
for t in lines:
    f = hashlib.sha1(t.encode("utf-8")).hexdigest()[:12] + ".m4a"
    idx[t] = f
    dst = os.path.join(out, f)
    if os.path.exists(dst): continue
    with tempfile.TemporaryDirectory() as d:
        a = os.path.join(d, "a.aiff")
        subprocess.run(["say", "-v", "Yuna", "-o", a, t], check=True)
        subprocess.run(["afconvert", "-f", "m4af", "-d", "aac", "-b", "64000", a, dst], check=True)
keep = set(idx.values()) | {"index.json"}
for f in os.listdir(out):
    if f not in keep: os.remove(os.path.join(out, f))
json.dump(idx, open(os.path.join(out, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
print(len(idx), "lines →", out)
