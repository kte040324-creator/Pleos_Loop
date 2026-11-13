# Loop 화면 상세 (v208 기준)

> 원래 claude.ai 대화에서 쓰던 인수인계 문서(v164 기준) + 이후 변경사항.
> 웹 버전(아티팩트): https://claude.ai/artifact/N2o69HUkULEYcXwnEzGB7X (v208)

## 1. 개요
- 제주 렌터카 여행자용 차량 앱 **Loop** 프로토타입. 2026 현대자동차그룹 Pleos Connect 앱 공모전(제안서 마감 11/15).
- 17" 2560×1440 화면을 1280×720 half-scale로 작업. 좌측 Driving View(0~420), 우측 Loop 창(.win L: 420,48 / 850×592), 하단 GNB.
- 시연 시나리오: **1박2일**(반납일 = 2일차). 3일 이상도 동작.

## 2. 파일
- `loop.html` 단일 파일(CSS/JS 인라인, 약 2.2MB).
  - 인라인 데이터: `bg.jpg`(설정 배경, base64 → CSS 변수 `--wbg`), 길 일러스트 4장(`RSRC`), 튜토리얼 미니화면(`TUTIMG`), `mapdata/osm.json`(`<script type=application/json id=osmdata>`).
- 그 외 자산(상대경로): `welcome*.jpg`, `places/*.jpg`(채도 60% 파일에 미리 적용 — CSS filter 금지), `routes/*.jpg`, `chrome.svg`, `dv/*.svg`, `scene/*`, `lottie/*.json`, `tut_mini.jpg`.
- 외부 CDN: lottie-web 5.12.2, Google Fonts(Asta Sans, Noto Sans KR) → 앱에서는 로컬로 교체(CLAUDE.md 2번).
- 장소 사진 없는 곳: 저지오름, 신창 풍차해안. 임시 숙소 이름(협재 OO 펜션 등) 미확정.

## 3. 화면 흐름
welcome(튜토리얼/건너뛰기) → [튜토리얼 3단계] → stay → return → people → taste → 로딩 → profile(취향 다이어그램) → 로딩 → today
→ route → drive(brief/offer) → arrived → … → dayEnd → 다음 날 today
→ (반납일) 마지막 장소 도착 "반납 준비하기" → planner(주유하러 가기 / 한 곳 더 들르기→extra) → drive → refuel → checklist → wrap(QR, 기록 지우고 마치기)

### 다일차
- `S.days[d]` = d일차 장소(1일차는 `S.slots`/`S.plan`). `buildDays()`가 배분.
- 헤더 `‹ N일차 날짜 ›` + 추천대로/자유롭게. 어느 일차를 보든 출발 버튼 유지(항상 1일차부터).
- 장소 박스 최대 4개(높이 64px 고정), 변경→빼기, 다녀온 곳 편집 불가, 0개여도 '+ 추가하기' 유지.
- 3일 이상: 2일차부터 숙소 변경 가능 → 다음 날 출발지.
- 한 곳 더 들르기: 가까운 2 + 먼 2(저지오름, 신창 풍차해안 = 시연용 '빠듯').
- ⚠ 도로 그래프는 제주 **서부만** 커버. 범위 밖 장소(우도·성산)는 넣지 말 것.

## 4. 디자인
- 녹색 #4C5A4F, 베이지 그라데이션 #AFA08C→#A0907C, 키워드 라벨 #99A28D→#88917D, 흰 긴 박스 #FFFFFF→#E7E4DD. **순수 블랙 금지 → #2A2827.**
- 글라스: 흰 24% + blur 17.5, 스트로크/림 없음. 검색창 검정 24% + blur 20.
- Radius: 큰 박스 14, 내부 버튼 10, Driving View 오른쪽 위·아래 14.
- 길 취향 카드: 일러스트 + 투영 3D 박스카, 선택 시 길 따라 루프. 미선택 카드 brightness(.86).
- 취향 다이어그램: HTML 원, CSS(compositor)로 떠다님 — JS transform 금지.
- 모션: 첫 화면·하루 끝·반납 완료 블러→선명 순차 등장. 반납 완료 장소 카드 5장 이상이면 무한 레일.

## 5. 페이지 전환 (v164 이후 추가)
- 콘텐츠를 직접 페이드하지 않는다(backdrop blur 깨짐). 배경 이미지를 깐 커버 `.wcov`를 위에 덮고 페이드아웃(.28s).
  - `.slow`(.85s): 튜토리얼 → 숙소 전환. `.hold`: 튜토리얼 마지막 단계에서 숙소 화면을 미리 그려두는 불투명 커버.
  - 설정 화면에선 커버가 하단 84px(‹ › 화살표 바)를 제외 → 화살표 안 깜빡임.
- 튜토리얼: 앱 창 안의 미니 도식(`.obm`, tut_mini.jpg + 하이라이트 `.mhl`), ‹ › 이동, 하단 진행점. 뒤 창은 시작 0.9초 welcome → obblank → 마지막 단계에 stay(hold 커버).
- 렌더러: `render()` → `morphHTML`로 DOM 제자리 패치. JS가 붙인 클래스는 `KEEP_CLS`로 보존.

## 6. 음성 (speak(t,force) — force=true만 재생, 화면 바뀌면 cancel)
- 화면별 `screenVoice`: 숙소/반납/누구와/어떤 여행/경로 추천/도착/하루 끝/반납 계획. 튜토리얼 중·첫 화면 없음.
- 튜토리얼 단계 `OB[].v`(~요), 끝나면 "숙소를 알려주세요", 경로 제안·수락, 주유소/반납 안내, 체크리스트, 마무리 "반납 완료! …".
- 앱에서는 tts-shim.js → 안드로이드 TTS.

## 7. 사용자 작업 방식
- 요청한 부분만 정확히·최소로. 임의 개선 금지. "원래대로" = 직전 상태로.
- 스크린샷 빨간 표시로 피드백. 수정 후 스크린샷 확인. 확인 못 한 건 못 했다고 말할 것.
- 한국어. 미세 조정 위주("아주 살짝").

## 8. 테스트 팁
- 디버그용: `})();` 앞에 `window.__d={get S(){return S},act,render,tick};` 주입(배포본엔 넣지 말 것).
- 전체 흐름 워커 액션: quick → toroute → pickroute → startleg → skip… → leave → tonext → (반납일) leave → planner → toreturn → refuel → chk → towrap → qr → erase.
- 2026-11-12: 1박2일 / 2박3일 / 한 곳 더(신창) + 튜토리얼·설정·편집·EV·QR 경로 페이지 오류 0건.
