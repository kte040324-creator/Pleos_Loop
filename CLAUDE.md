# Loop (Pleos Connect 공모전) — Claude Code 작업 지시서

## 목표
`web/loop.html` 프로토타입(이미 완성된 화면)을 **안드로이드 APK로 감싸서 GitHub에 올리기.**
- **Pleos SDK / 실제 차량 연동은 하지 않음.** 지금 화면에 보이는 부분만 그대로 동작하는 프로토타입.
- 차량 값(좌석 센서, 연료, 주행/정차, 내비)은 전부 loop.html 안의 시뮬레이션 그대로 둔다.
- 마감: 제안서 2026-11-15. 가산점 = 시연 영상 + GitHub 저장소 + APK.

## 구조
```
web/                     화면 원본 (loop.html + 자산). 화면 수정은 여기서만.
app/src/main/assets/     앱에 들어가는 복사본 (index.html = loop.html + tts-shim 주입)
app/src/main/java/...    MainActivity.kt (전체화면 WebView), TtsBridge.kt (안드로이드 음성)
tools/sync-web.sh        web → assets 복사 + 앱용 패치
docs/handoff.md          화면/디자인/음성/사용자 작업방식 상세 (꼭 읽기)
```
- WebView는 `https://appassets.androidplatform.net/assets/index.html` 로 연다 (WebViewAssetLoader). file:// 쓰지 말 것.
- 음성: loop.html은 `speechSynthesis`를 쓴다. `tts-shim.js`가 `window.AndroidTTS`가 있을 때만 `speechSynthesis`를 안드로이드 TTS로 바꿔치기한다. loop.html의 음성 코드는 고치지 않는다.

## 할 일 (순서대로)
1. **Gradle wrapper 생성**: 이 zip에는 wrapper가 없다. `gradle wrapper --gradle-version 8.10.2` 또는 Android Studio로 폴더 열기(자동 생성).
2. **오프라인화 (CDN 제거)** — 차 안에서 인터넷 없어도 되게:
   - lottie: `https://cdnjs.cloudflare.com/ajax/libs/lottie-web/5.12.2/lottie_light.min.js` 를 받아 `app/src/main/assets/vendor/lottie_light.min.js` 로 저장.
   - 폰트: Google Fonts `Asta Sans`(300..700), `Noto Sans KR`(200..700) woff2를 `app/src/main/assets/fonts/`에 받고 `fonts/fonts.css`(@font-face, font-family 이름은 원래와 동일하게 'Asta Sans', 'Noto Sans KR') 작성. Noto Sans KR은 용량이 크니 variable woff2 또는 한글 서브셋 사용.
   - 그다음 `tools/sync-web.sh` 실행 → index.html의 CDN 링크가 로컬로 바뀐다.
   - 이후 Manifest에 INTERNET 권한 없이 동작하는지 확인.
3. **화면 맞춤 확인**: 대상 화면 2560×1440(17"), 디자인은 1280×720 기준.
   - loop.html의 `fit()`이 `(window.innerHeight-48)`을 쓴다(아티팩트 뷰어 여백용). 앱에서 위아래 여백이 생기면 **앱용 패치(tools/patch_app_html.py)에서만** `-48`을 없애고 body/#stage 여백을 0으로. web 원본은 건드리지 말 것.
   - 에뮬레이터: 가로 2560×1440, density 320(xhdpi → CSS 1280×720) AVD 만들어 확인. 태블릿 실기기도 가능.
4. **음성 확인**: 튜토리얼 시작 시 음성이 나오는지. 안 나오면 기기 설정 > TTS 엔진에 한국어(Google TTS 한국어 데이터) 설치 필요 — README에 적기.
   - loop.html은 첫 클릭 전에는 `voiceReady=false`라 음성이 안 나옴(정상).
5. **빌드**: `./gradlew assembleRelease` → `app/build/outputs/apk/release/app-release.apk` (디버그 키 서명, 설치 가능).
6. **전체 흐름 점검**(에뮬레이터): 튜토리얼 → 숙소 → 반납 → 누구와 → 어떤 여행 → 취향 → 오늘 일정 → 경로 → 주행 → 도착 → 하루 끝 → 2일차 → 반납 계획 → 주유 → 체크 → 반납 완료(QR, 기록 지우고 마치기). 콘솔 오류는 `chrome://inspect`.
   - 체크 포인트: 배경 블러(backdrop-filter), 길 취향 카드 3D 차 모션, 취향 다이어그램 떠다니는 모션, 키보드(앱 자체 그린 키보드) 동작, 반납 완료 레일.
7. **GitHub 업로드**: 저장소 https://github.com/kte040324-creator/Pleos_Loop (origin/main). APK는 제출 규정대로 `apk/팀명_앱이름_release.apk` 로 커밋(용량 초과 시에만 Release). 접수 메일에 최종 커밋 hash 기재.
8. **README 마무리**: 스크린샷(docs/screens/), 시연 영상 링크, APK 다운로드 링크 채우기.

## 규칙 (사용자 작업 방식 — 중요)
- 요청한 것만 정확히, 최소로 고친다. **임의로 디자인/코드 "개선" 금지.** "원래대로" = 직전 상태로 복구.
- 화면(디자인·모션·문구)은 이미 확정. 앱 포장 과정에서 화면이 달라지면 안 된다. 달라지면 그건 버그.
- 수정 후엔 스크린샷으로 확인하고, 확인 못 한 건 못 했다고 말한다.
- 한국어로 대화. 순수 블랙 금지(#2A2827).
- 장소 사진 CSS filter 금지(채도는 파일에 미리 적용돼 있음).
- 도로 데이터(osm.json)는 제주 서부만 → 범위 밖 장소 추가 금지.
