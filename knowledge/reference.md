# Sky Explorer Python API 레퍼런스 (CLAUDE.md)

> 🚨 **예제(쇼) 만들기 전 무조건 먼저 읽기: [`docs/20_object_playbook.md`](./docs/20_object_playbook.md)**
> — 개체별 확대·이동 방법 매트릭스 + fly-in 가능 판별 + 실패 원인 + 표준 기본값(딥스카이 frac=0.004, Target 30).
> 카메라 무빙/줌이 들어가는 예제는 이 플레이북의 의사결정 트리대로 개체에 맞는 방법만 쓴다(사용자 확정 규칙).
>
> ⭐ **코드 구성 시 참고 우선순위**:
> 1. **정확한 메서드 시그니처** → [`reference/core_api_reference.txt`](./reference/core_api_reference.txt)
>    (사용자 제공 핵심 31클래스 전체 시그니처. 인자 타입·Anim 위치·enum 확인은 여기부터.)
> 2. 이 CLAUDE.md — 빠른 요약/사용 패턴/함정.
> 3. 보조: 실측/함정은 [`docs/`](./docs/) 노트, 전체 추출본은 [`reference/`](./reference/).
> ⚠️ 세부 enum 멤버(성운/시간대 이름 등)는 `dir()`/도움말/ST 로그로 확인.
> 실제 SDK 빌드와 미세 차이가 있으면 **ST 실행 로그(에러의 "Did you mean")가 최종 진실.**
>
> ✅ **레퍼런스로 검증된 함정**(우리가 실측으로 도달, core_api_reference.txt 일치):
> - Analemma '포트' 없음 → `DateManager.setMotionType(MotionType.MotionAnalemma)` 사용.
> - `Planet.setRingIntensity` 없음 → `setRingModel(Planet.RingModel)`.
> - track 받는 카메라 이동은 `(value, Anim, track)` — **Anim 필수**(`setPositionXYZ/LBR/R/L`).
> - `setOrientationR/HPR` 는 track 없는 속성 세터 → `setZoomPosition` 줌 락과 충돌.

## 기본 규칙

> 🎯 **돔 연출 표준 Target = 30° (2026-07-06 운영 확정)**: 관객 시야 기준 Target 30 이
> 보기 좋은 위치. **천정 정렬(Target 90)은 관람 부적합** — 관객이 목을 꺾어야 함.
> FadeTo 기본값이 30인 이유가 이것. 천체 배치는 기본 30, '천정/정중앙' 명시 요청 시에만 90.

- `from skyExplorer import *` 로 모든 클래스 import (스크립트 안에서 자동)
- 애니메이션: `Anim(초)` 사용. `Animator(초)` 는 구형이지만 호환됨
- 카메라 타겟: 반드시 `Vec2(azimuth, height)` (`Vec3(x,y,z)`는 DEPRECATED)
- intensity 범위: 0.0 ~ 1.0
- 좌표계: L(경도/azimuth), B(위도/height), R(거리)

## ⚠️ 자주 나는 오류 & 주의사항

1. **intensity는 속성이지 함수가 아님**
   ```python
   Planet(Planet.PlanetName.Earth).intensity()   # ❌ 'float' object is not callable
   Planet(Planet.PlanetName.Earth).intensity      # ✅
   ```
2. **속성 직접 대입 안 됨 — 반드시 setter 사용**
   ```python
   Planet(Planet.PlanetName.Earth).intensity = 1  # ❌
   Planet(Planet.PlanetName.Earth).setIntensity(1)# ✅
   ```
3. **네임스페이스 중복 금지**
   ```python
   skyExplorer.Planet(...)   # ❌ NameError
   Planet(...)               # ✅ (from skyExplorer import * 이후)
   ```
4. **무한 루프 사용 시 sleep 필수**
   ```python
   while True:
       # ... 상태 확인 ...
       sleep(0.016)   # 1/60초 (60fps 1프레임) — CPU 낭비 방지
   ```
5. **import 3종 세트** — 매니저 클래스(`DateManager` 등)는 `skyExplorer import *` 에 **없음**
   (`NameError: name 'DateManager' is not defined`). `Initialization` 에서 노출됨.
   ```python
   from skyExplorer import *
   from studio import *
   from Initialization import *   # ← DateManager 등 매니저는 여기서 (실측 확정)
   ```
6. **TimeZone.UTC 는 없음** — 실제 멤버는 `UTC_P_10_30_MON`/`DefaultTimeZone` 류.
   `dir(DateManager.TimeZone)` 로 확인해 골라 쓸 것(하드코딩 `TimeZone.UTC` → AttributeError).

## 실행 방법

- **Studio**: 추가 버튼/드래그앤드롭으로 `.py` 가져오기 → 데이터베이스 스크립트 →
  Python 스크립트 더블클릭 실행. 재생 패널에서 관리/에러 확인.
- **SPC 안에서 Python 호출**: Editor 주변장치 명령 활성화 → 명령 목록 마지막
  `Studio Python / JS Script Play` → SPC(부모)가 Python(자식) 실행.

## Hello World

```python
from skyExplorer import InsertText, Camera, Vec
myText = InsertText(InsertText.InsertTextName.InsertText001)
myText.setText("Hello world"); myText.setIntensity(1)
myText.setPosition(Vec(0, 90, 0))            # 천정
camera = Camera(Camera.CameraName.MainCamera)
camera.addChild(myText.id, Camera.CameraPort.FixedForeground)
```

---

## Camera — `Camera(Camera.CameraName.MainCamera)`

- `setTarget(Vec2(azimuth, height), Anim)` — 방향 설정 (Vec3 DEPRECATED)
- `setPositionLBR(Vec(l,b,r), Anim, track)` — LBR 위치. track=천체 portId.
  ⚠️ **track 필수**(실측: `(Vec, Anim)` 만 넘기면 ArgumentError — 기본값 없음). 최소 `-1` 이라도 명시.
- `setPositionR(r, Anim, track)` — 거리(R)만 변경
- `setOrientationSmoothXYZR(Vec4, Anim, track)` — 방향 부드럽게
- `takeScreenshot(filename)` — 화면 캡처 저장
- `addChild(id, CameraPort)` — 오버레이 붙이기
- **CameraName**: `MainCamera` / **CameraPort**: `FixedForeground`(화면 고정 오버레이)
- **읽기 속성**: `positionLBR`(현재 Vec3 l,b,r), `positionLBR.z`(현재 R)
- ⚠️⚠️ **실측 확정: `positionLBR` 의 R 은 km 가 아님 — '트랙 대상 반지름' 단위** (착각 시 122 AU 이탈 사고).
  → **절대값 금지. 줌은 '읽은 값 × 배율'**: `p=cam.positionLBR` → `setPositionR(p.z*0.5, Anim, -1)`.
  읽기/쓰기 **프레임 일치** 필수 — track 에 다른 포트를 새로 넘기면 프레임이 바뀌어 튐. track=-1 이 안전.
- ✅✅ **행성 줌인 정석 레시피 (2026-07-02 Studio 실측 검증, scripts/study/zoom_saturn.py)**:
  ```python
  SceneGraph().reset(1)                                   # 관측자 바인딩 해제(FadeTo 잠김 방지)
  DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
  sleep(4.0)                                              # ① 행성에 화면 고정(하단-중앙, R≈5 행성반지름)
  p = cam.positionLBR                                     # ② 읽기 (R 단위 = 트랙 대상 반지름)
  cam.setPositionLBR(Vec(p.x, p.y, p.z*0.5), Anim.cubic(4.0), -1)   # ③ R×배율 = 줌
  ```
  실측: R 5.000→2.500→1.250 동작. **track=-1 = 현재(FadeTo) 프레임 유지**. 절대값 넣지 말고 읽은값×배율.
  ✅ **'줌 중 화면 이동'의 진짜 원인 판명 (2026-07-06 달 실측 확정)**: 줌이 아니라
  **Target 재정렬 슬루가 관객에게 보이는 것**이었음.
  줌 자체는 ①`setPositionR(-1)` ②스텝R+TH재조준 ③줌락+`setZoomFov` **셋 다 화면 고정 확인**(달).
  → **정석: Target 을 바꿔야 할 땐 암전(GlobalIntensity 0)에서 정렬 완료 후 페이드인**.
  `setZoomFov(fov, Anim)` 는 트랙 불필요 단독 동작(광학 줌) — 카메라 이동 없는 줌로도 확인.
  ⚠️⚠️ **setZoomFov 는 지상 Sky View 에선 확대 무효 (2026-07-06 실측)** — 비행/우주 뷰 전용 추정.
  또 동작하는 곳에서도 '뷰 축(돔 중앙 방향)' 기준이라 Target 30 구도와 부적합.
  → **지상 쇼의 클로즈업 = `setScale` ✅실측 확정(2026-07-06, 코로나 확대 동작)**: 태양+달을 같은
  배율로 동시에 키우면 정렬 유지된 채 그 자리에서 확대. 카메라 불변 = 제일 자연스러움.
  **배율 감각: ×5 는 미미, ×20~30 이 체감 확대** (일식 기준 실측).
  ⚠️ **원본 scale 을 먼저 읽어둘 것** — 기본값이 1.0 이 아닐 수 있음(복귀를 1.0 하드코딩했다가
  원래보다 작아진 실측 리포트). 확대 = 원본×배율, 복귀 = 읽어둔 원본값.
  (Planet/Satellite/IndividualStar/Nebula/Messier/NGC 전부 setScale 보유. scripts/study/eclipse_2026_target30.py)
- ✅ **Target 정렬 (실측 + 🎯운영 표준 30)**: FadeTo 직후 `setTargetHeight(값, Anim)` 동작
  (Sky View 에선 잠겼던 트랙볼 계열이 **FadeTo 행성 뷰에선 풀림**).
  **FadeTo 기본 Target 30 = 관람 정위치라 행성 쇼는 보통 재정렬 불필요!**
  90(천정)은 기하학적 정중앙이지만 관람 부적합 — 명시 요청 시에만.
- ✅ **오빗 방향 (실측)**: 행성 FadeTo 프레임에서 L 변화=레코드판 스핀(어지러움), B 변화=자연스러운 굴림.
  성운 LOS 프레임에선 L 스윕이 자연스러움 — 프레임마다 축이 다름.
- ✅✅ **이동 중 조준 유지의 정답 = `setZoomPosition` 줌 락** (말머리 실측 검증, docs/13):
  `cam.setZoomFormula(Camera.ZoomFormula.GreatCircle)` → `cam.setZoomPosition(Vec(0,0,0), track, Anim, Camera.PositionMode.XYZ)`
  → **엔진이 재조준을 내부 처리** — 카메라가 어디로 가든 대상 중앙 유지. 줌인은 `setZoomFov`(110→72).
  타깃 오프셋은 0 유지(주면 GreatCircle 롤 유발). 완전판: `scripts/zoom_horsehead.py`.
  ※ 근접 360° 공전은 성운 뒷면(실루엣) 통과 → 정면 스윙(±75°) 권장.
- ⚠️⚠️ 줌 락 없이 **수동 조준으로 이동 중 유지는 불가 (실측)**: `setTargetHeight` 는 일회성(같은 값
  재호출 no-op), `track=행성 portId` 는 프레임 점프, `track=-1` 만 안전(단 조준 유지 없음).
  행성 '자전 연출'(시간가속+카메라)은 전 시도 실패 — 미해결. 프로덕션도 정지 구도+미세 드리프트만 사용.
  확정 예제: `scripts/study/zoom_earth_orbit.py` (goto_planet/center_dome/zoom).

## Planet — `Planet(Planet.PlanetName.Earth)` / 인덱스 `Planet(Planet.PlanetName(0))`

- ✅✅ **지상 낮 하늘(파란 하늘)의 마스터 스위치 = `Planet(Earth).setIntensity(1)` (2026-07-06 녹화 해독 확정)**:
  reset 후 지구 intensity 가 꺼져 있으면 **대기(atmosphereIntensity)를 켜도 하늘이 검음** —
  행성 본체가 꺼지면 대기 렌더도 통째로 꺼짐. Studio UI '대기효과' 토글의 실체 =
  `setIntensity(1)` + `setAtmosphereIntensity(1)` 두 명령 세트 (사용자 토글 SPC 녹화 역해석).
  지상 씬 체크리스트: 지구 setIntensity(1) + setAtmosphereIntensity(1) + 태양 setIntensity(1) + 시각(UT!).
  ✅✅ **지상 낮밤 타임랩스 확정 예제 (사용자 확인 2026-07-06)**: scripts/study/cheongju_day_night_v3.py —
  아침→정오→석양→밤을 setDateTime+Anim(8초) 가속으로. 별은 상시 1.0 (낮엔 대기가 물리적으로 가림).

- **PlanetName(0~7)**: Mercury=0, Venus=1, Earth=2, Mars=3, Jupiter=4, Saturn=5, Uranus=6, Neptune=7
- `setIntensity(intensity, Anim)`, `setOrbitIntensity(intensity, Anim)`
- `portId(PlanetPort)` — **PlanetPort 실측(9종)**: Ecliptic/Equatorial/EquatorialJ2000/**EquatorialSynchronous**/Galactic/NoonEcliptic/NoonEquatorial/OrbitalMeanEquinox/InvalidPlanetPort

- ✅✅✅ **행성을 '객체로' 자전시키기 = 관성 프레임 + setRotationSpeedScale (2026-07-14 사용자 확인, earth_rotation_sim.py / solar_system_tour.py 화성)**:
  ⚠️⚠️ **GoTo/FadeTo 도킹 프레임은 'EquatorialSync(동기)' = 카메라가 행성 자전을 따라 같이 돎** →
  **행성은 멈춰 보이고 배경 하늘·별이 도는 것처럼** 보임(실측 확정, "지구는 그대로 별만 돈다").
  → **관성 프레임(EquatorialJ2000/Equatorial/Ecliptic)으로 전환**하면 카메라가 별에 고정 → **행성이 그 자리서 자전, 별 고정**.
  전환법(카메라 위치 불변): `ip = Planet(x).portId(Planet.PlanetPort.EquatorialJ2000)` →
  `cam.setPositionLBR(Vec(현재L, 현재B, 현재R), Anim, ip)` (같은 L/B/R 라 안 움직임, R 보존) + `setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim, ip)`.
  · **자전 구동 = `setRotationSpeedScale(배율)`(Anim 없음, 단일 float) + 날짜 흐름(`setDateTime(목표, Anim)`)**.
    회전량 = 배율 × 날짜Δ(일). 관성 프레임에선 배율 낮아도 됨(배율 2 × +12h = 1바퀴). 끝에 `resetRotationSpeedScale()`.
  · **자전 전 시간 완전정지(dm.stop) 후 배율 걸고 시작** — 시간 흐르는 중 배율 걸면 그동안 누적분 ×배율로 '확 돎'(막 회전).
  · **적도 옆(B≈5)에서 봐야 자전축이 세로 = 정상 지구본**. 북극 위(B90)면 자전축 정면 → 팽이처럼 돎(부적합).
  · 배경 별 안 돌게 = 관성 프레임 + 날짜Δ 최소. (Sync 프레임에서 배율만 키우면 하늘이 도니 주의.)
  ⚠️ 카메라 전환(관성+적도이동)이 다소 지저분(사용자 지적) — 미세 개선 여지. 하지만 회전 자체는 확정 동작.
- ✅✅ **암석 행성(지구·화성) GoTo/FadeTo 도킹 = 북극 상공 {L, 89.999, R=4}** / **가스 행성(목성·토성) = 옆 {L, 20, R=5}** (Recording19 + 실측 확정).
  → 지형 있는 암석행성은 '착륙 접근' 자세(북극 위)라 **카메라 L 공전이 극축 제자리 스핀 = 불가**. 자전은 위 관성+setRotationSpeedScale 방식으로.
  가스행성은 옆 도킹이라 `setPositionLBR(Vec(L+각, 20, R), Anim, -1)` L 스윕 = 카메라가 옆에서 한 바퀴(정상 공전, 목성/토성 확정).
- ⚠️⚠️ **GoTo 지구(홈 행성) = 지표면 R=0 으로 '집에 가기'** (밖으로 안 나감, 스샷 R:0m 확정). 지구를 **외부에서** 보려면
  `SceneGraph().reset(1)`(관측자 바인딩 해제) → `DataManager...data(PlanetType,"Earth").action(FadeTo).trigger()` (R=4 외부 도킹).
- ✅ **미연습 코드 확정(earth_rotation_sim)**: `setRotationSpeedScale`/`resetRotationSpeedScale`(자전배율) ·
  `setNightLightsIntensity`(밤면 도시광=호박색, 실제 나트륨등 색) · `setTerrainIntensity`/`setCloudsIntensity` ·
  `setEquatorialPoleAxisIntensity`/`setEquatorialPolePointerIntensity`(자전축 시각화, 청록 세로선).
  SPC(Recording19): 자전배율 cmd **1029**, reset **1045**, terrain **1063**, clouds **1064**, nightLights **1057**, 자전축 **1097**(레이어7=축/8=포인터).
- ⚠️⚠️ **`setLightPollutionIntensity` 는 별/은하수를 안 지움 (2026-07-09 사용자 실측)**: 이 명령은 지구
  **대기 스카이글로(하늘 배경광)**만 건드림 — `Stars`/`Galaxy` 는 독립 레이어라 광공해값을 올려도 별·은하수가
  그대로 보임. **빛공해 쇼에서 '별이 사라지는' 효과 = Stars/Galaxy intensity 를 단계에 맞춰 직접 감광**
  (setLightPollutionIntensity 는 대기 글로우용으로 병행). ✅ 확정 예제(사용자 밝기 확정, Recording13):
  scripts/study/light_pollution.py — 교외 lp0.3/stars0.80/mw0.35 → 도시외곽 lp0.6/0.60/0.10 →
  대도시 lp1.0/0.40/0.0, 복귀 1.0/0.8. (별을 너무 죽이면 과함 — 대도시도 stars 0.4 유지가 보기 좋음.)

## Satellite — 달·위성 ✅ 실측(2026-07-06, scripts/study/moon_phase_show_v2/v3.py)
- 생성: `Satellite(Satellite.SatelliteName.Moon)` / FadeTo 는 **`Data.Type.SatelliteType` + "Moon" 확정**.
- **위상 수동 제어 (실측 동작)**: `setManualMoonPhase(True)` → `setMoonAge(age, Anim)` (0~29.5)
  → `setMoonAge(0→29.5, Anim(15))` 한 번 호출로 위상 타임랩스(신월→보름→그믐).
- ⚠️ **쇼 끝에 `setManualMoonPhase(False)` 로 자동 복귀시키지 말 것 (실측 리포트)**:
  수동 위상과 실제 날짜 위상이 싸우며 **그림자가 생겼다/없어졌다 깜빡임** → 수동 유지 권장(다음 쇼는 reset).
- **그림자(위상 명암) 강도 = `setPlanetShineStrength(s, Anim)`** — 지구조(지구 반사광이 그늘면을 비춤).
  **0.0 = 그늘 칠흑(그림자 최강)**, 1.0 = 기본. 실측 확인.
- **SatellitePort**: Equatorial/EquatorialJ2000/EquatorialSynchronous/Galactic/NoonEcliptic/NoonEquatorial/OrbitalMeanEquinox.
- 줌: `setPositionR(-1)` / 줌락+`setZoomFov` 모두 화면 고정 확인. DomePointer(화면좌표 포인터)도 동작.
- ✅✅ **FadeTo 암전 유지 클램프 (v3 실측 확정)**: reset/FadeTo 직후엔 `setGlobalIntensity(0)` 를 걸어도
  gi 가 1.0 으로 남는 프레임이 있음 → **FadeTo·TH90 진행 중 0.2초 간격으로
  `uni.setGlobalIntensity(0.0, Anim(0.0))` 를 반복(클램프 루프)** → 페이드인 전까지 완전 암전 실측 성공.
  (말머리 쇼처럼 FadeTo 를 안 쓰면 클램프 불필요 — FadeTo 쓸 때만.)

## Stars — `Stars(Stars.StarsName.StarrySky)`
- `setIntensity(intensity, Anim)` / 읽기: `intensity`
- ✅ **반짝임 (2026-07-07 실측)**: `setTwinklingAmplitude(amp, Anim)` — 기본 1.0, 3.0 체감 동작.
  복귀는 읽어둔 원본값으로(`twinklingAmplitude` 읽기, `isTwinklingActive` 존재).
  🎛 **운영 튜닝(Recording6 사용자 SPC판)**: 증폭 1.2 / 기본 0.4 — 3.0 은 과함. 이 값 권장.
- ✅ **고유운동 타임랩스 (2026-07-07 실측)**: `setProperMotion(True)` →
  `setProperMotionOffsetInYears(년수, Anim(초))` — Anim 동안 연속 진행(텔레메트리 선형 확인).
  ⚠️ **전천의 모든 별에 적용**이라 빠르면 멀미(v1: 10만 년/15초 = 어지럽다는 리포트) —
  저속(≈2,500년/초 이하) 권장. `setMotionVectorIntensity`(궤적 벡터)는 멀미 가중 후보라 신중히.
  ✅ **별자리 '선'이 별을 따라 일그러짐 확정 (v2 실측)** — 오리온 변형 연출은 선 ON 으로 극대화.
- 기타 미연습: setContrast/setExposure/setPointSaturation/setModelset 등.

## Mark — 좌표 그리드/눈금 (2026-07-07 v1 프로브 실측)
- 생성: `Mark(Mark.MarkName.Mark001)` — **MarkName = Mark001~050 + Mark051~053_WelcomeGrid** (69멤버).
- ⚠️⚠️ **빈 슬롯 기본값 = 전부 0/Invalid** (posType/repType Invalid, radius/카운트 0) —
  **setIntensity 만으론 아무것도 안 보임(v1 실측)**. posType+repType+카운트 풀구성 필수.
- enum 실측: `PositionType` = FiniteGrid/InfiniteGrid ·
  `RepresentationType` = Grid/GridWithText/Graduation/GraduationWithText/GraduatedGrid/GraduatedGridWithText/TextOnly/None ·
  `TextOrientationMode` = Auto/Pole/Target/Zenith/OrientationNone. Language 에 ko_KR 있음.
- **Mark051_WelcomeGrid = 시스템 프리셋** — 파라미터 덤프해서 '정답 레시피' 채굴 가능.
  ⚠️ v2: 프리셋·수동 풀구성 모두 화면에 안 보임 — 부모 바인딩 필요 추정 (v3 실험 중).
- ✅✅ **좌표 그리드의 '본명령' = Place2D/Planet 그리드 속성 (2026-07-07 v3 실측 확정 — 전부 표시됨!)**:
  지상 = `Place2D.setAzimuthGridIntensity`(방위/고도 그리드)·`setMeridianIntensity`(자오선)·
  `setCardinalPointsIntensity`+`setCardinalPointsRepresentation`(동서남북 표지, Level1=4방위/Level2=8방위)·
  `setHourAngleGridIntensity`(시간각). 하늘 좌표계 = `Planet.setEquatorialGridIntensity`/
  `setEclipticGridIntensity`/`setEquatorialJ2000GridIntensity`/`setSupergalacticGridIntensity`.
  → 커스텀이 필요 없으면 Mark 대신 **무조건 이쪽을 쓸 것**.
  ✅✅ **천구 회전 쇼 확정 (2026-07-13 사용자 확인, scripts/study/celestial_rotation.py)**: 지상 그리드
  (방위/자오선/동서남북 = 지평 프레임 **고정**) + 천구 적도 그리드(별과 함께 **회전**)를 동시에 켜고
  `DateManager.setDateTime(+6h, Anim(32))` 시간가속 → 별·적도그리드가 북극 중심으로 돌고 지상 격자는 고정 =
  '지구 자전'이 그리드로 한눈에. **북극성 지목 = `IndividualStar(...Polaris).setPointerIntensity(1)`** (enum 존재,
  기본 포인터 뜸). ⚠️ `setCardinalPointsRepresentation` enum 경로 불명(Place2D/Body 둘 다 아님) —
  **표지는 setCardinalPointsIntensity 만으로 기본형이 잘 뜸**(Representation 세터 생략 가능).
  SPC(Recording15): 지상그리드 = `Place2D` cmd **5637** + 레이어(**1=자오선/2=방위/10=동서남북**),
  천구 적도 = `Planet` cmd **1097** 레이어2, 별 포인터 = `IndividualStar` cmd **805**.
- ⚠️ **그리드 '아래 잘림' = Target 30 틸트가 원인 (v3 실측)** — 돔 하단에 지평선 아래
  영역이 들어와 하늘 그리드가 비어 보임.
  ✅ **지상 Sky View 의 전천(그리드) 구도 = Target 0 (2026-07-07 사용자 운영 확정!)** —
  90 아님. ⚠️ Target 값의 의미는 프레임마다 다름: 성운 LOS 프레임에선 '90=돔 중앙'
  실측이었지만, 지상 Sky View 전천은 0 이 정답. 그리드 장면만 0, 관람 복귀는 30.
  Target 재정렬 슬루는 암전 속에서 (표준).

## DomePointer — 돔 포인터 (2026-07-07 v1 실측)
- 생성: `DomePointer(DomePointer.DomePointerName.DomePointer001)` (001~010) — 생성/이동/색/크기 동작.
- `setPosition(Vec(az,h,roll))`/`setAzimuth`/`setHeight`(0~90)/`setColor(Vec3)`/`setApparentSize(도)`/
  `setPointerIntensity`/`setPointerType(Body.PointerType.Model1~10[Bold])`.
- ✅✅ **좌표 매핑 확정 (2026-07-07 v2 캘리브레이션)**: **az = 180 − 방위(나침반)** —
  `setOrientationH` 와 동일 공식! (az0=남, az90=동, az180=북, az-90=서 실측).
  **height = 돔 Target 좌표** (하늘 고도 아님 — h85 가 천정 근처, HUD Target 값과 동일 개념).
  → 천체 조준 = `setAzimuth(180-천체방위)` + height 는 Target 환산으로.
- ✅✅ **개체를 '직접' 가리키기 — 2경로 실측 확정 (2026-07-07 v1/v2, docs/17)**: ① 천체 내장 포인터 —
  별/행성/성운/은하 등 Body 계열 `setPointerIntensity`+`setPointerType` (천체 추적, 좌표 불필요).
  ② DB 액션 `Action.Type.PointerOn/Off` — enum 없는 천체도 이름으로.
  ⚠️⚠️ **행성은 `setPointerType` 지정 필수 (기본 Invalid — 목성 A/B 실측)**: 타입 없이 PointerOn
  하면 안 그려짐. **별(IndividualStar)은 기본 타입이 있어 바로 보임** (리겔 대조군 확정).
  ⚠️ Constellation 은 내장 포인터 없음(대표 별 포인팅) / **Messier 도 포인터 API 없음** → 성운은
  Nebula 클래스 경유 (M42 등, 내장 포인터 동작 확정). IndividualStarName enum = 3,189개 (오리온 7별 전부 있음).
- SPC cmd: 8193 intensity / 8194 position(az,h) / 8195 color / 8196 type / 8197 size, family 0x11.

## ShootingStar — 유성/유성우 (2026-07-07 Recording7 실측, docs/18)
- 생성: `ShootingStar(ShootingStar.ShootingStarName.ShootingStar001)` (family 0x07).
- **단발 유성**: `setStartPosition(Vec2(az,h))`+`setArrivalPosition(Vec2(az,h))`(화면좌표=DomePointer 규약)
  → `setAdvancing(0→1, Anim)` 이 비행. `setBrightness`(선 굵기)·`setTrailLength`(꼬리 초)·
  `setRepresentationType(ShootingStar.Model.Gradient)`.
- **유성우**: `setRainGradientPoint(Vec2)`(복사점)+`setRainChaosGradientPoint(반경°)`+`setRainSpeed`+
  `setZenithalHourlyRate(ZHR)` → `setRainSeed(1)`(0=정지). `setReferential(RaDec)` 면 복사점이
  하늘 고정(Vec2=적경°,적위°) — 진짜 별자리에서 방사.
- ⚠️⚠️ **ZHR 내부 저장 = ZHR/60 (분당 개수!)** — 실측 120→분당2→30초에 1개라 **돔에선 거의 안 보임**.
  볼만한 유성우 = **ZHR 800~1500**, 폭풍 = 3000. (실제 유성우가 성긴 건 맞지만 쇼는 크게 써야 함.)

## Bolide — 화구(불덩이 유성) (2026-07-09 실측 확정, docs/18)
- 생성: `Bolide(Bolide.BolideName.Bolide001)` (family 0x2E). `setIntensity(i, Anim)`.
- `set(시작az, 시작h, 시작고도m, 끝az, 끝h, 끝고도m, speed)` = 복합(내부에서 지리좌표로 변환) → `play(speed)`.
- ✅ **enum 실측**: `ModelID` = Chelyabinsk / ColoredFireball / User ·
  `Element` = Sodium(주황·노랑) / Magnesium(청록) / Iron(노랑) / Calcium(보라) / NitrogenOxygen(적색) / Custom.
- ✅✅ **색 6종 전부 검증 완료 (2026-07-09 사용자 확인, bolide_colors.py)**: ColoredFireball 고정 +
  원소만 교체하면 6발 전부 정상 표출. Custom 원소는 `setElement(Custom, Vec3(r,g,b), Anim)` 로 임의 색.
- ⚠️⚠️ **모델 없으면 아예 안 그려짐 (실측)** — `setModel` 필수. **`ColoredFireball` = 확정 정답 모델**
  (Sodium 원소 = 주황 불덩이, 사용자 "진짜 운석 떨어지듯이" 확인). **`Chelyabinsk` 는 이 빌드서 렌더 실패**
  (에셋 파일 필요 추정) — 쓰지 말 것. 불덩이 = `setModel(ModelID.ColoredFireball, "")` + `setElement(...)`.
- ⚠️⚠️ **시그니처 함정 (실측)**: `setModel(model, filename)` — filename **필수**(내장도 `""`). ·
  `setElement(element, customColor, anim)` — **3인자 전부 필수**(문서는 optional 이나 바인딩 강제).
  Custom 원소면 customColor 로 색 지정, 명명 원소면 `Vec3(0,0,0)` 넘겨도 원소 고유색.
- ⚠️⚠️ **속도 규칙 (실측)**: `set(...,speed)` 의 speed 는 **1.0 고정**(바꾸면 화구가 안 보임!).
  재생 속도는 `play(speed)` 로만 — **크로싱 시간 = 148/play_speed 초**. 극적 화구 = play(12~18)(약 8~12초),
  빠른 유성풍 = play(40~60). (speed 단위는 km/s 지만 실사용은 이 규칙으로 고정.)

## Galaxy — `Galaxy(Galaxy.GalaxyName.MilkyWay)`
- `setIntensity(intensity, Anim)`

## DwarfPlanet — 왜소행성 (2026-07-09 실측 확정, pluto_flyby.py)
- 생성: `DwarfPlanet(DwarfPlanet.DwarfPlanetName.Pluto)` — 이름: Pluto/Ceres/Eris/Haumea/Makemake/PlutoBarycenter.
- DB: `Data.Type.DwarfPlanetType`, 이름 = `"Pluto"`(단순형. "134340 Pluto"는 실패). FadeTo → R=4 도킹.
- ✅✅ **TerrainModel 실측 (미션별 실제 표면 텍스처 내장!)**: `Basic`/`DefaultTerrain`(밋밋) ·
  **`NewHorizons`(명왕성 실측 표면=하트!)** · `DawnHamo`/`DawnLamo`(Dawn 탐사선 세레스 표면).
  → 명왕성은 `setTerrainModel(TerrainModel.NewHorizons)` 로 진짜 하트 표면.
- 표시/지형: `setIntensity`/`setOrbitIntensity`/`setLabelIntensity`/`setPointerType` ·
  `setElevationScale`(고도 과장, 8배 실측 동작)·`setShadowStrength`(0=칠흑)·`setShadowContrast`.
- 카메라: **행성과 동일** — FadeTo(R=4 도킹) 후 `setPositionR(읽은값×배율, -1)` 줌. 전부 사용자 확인.
- Port: Ecliptic/Equatorial/EquatorialJ2000/EquatorialSynchronous/Galactic/NoonEcliptic/NoonEquatorial/OrbitalMeanEquinox.
- ✅ **SPC cmd (Recording10 확정, family 0x08)**: 6913 setIntensity / 6926 setShadowStrength /
  6967 setElevationScale / 7008 setTerrainModel(enum, NewHorizons=38). FadeTo Pluto = **지구형 안무**
  (Set place2D→북극 R=4 도킹) + 위성들(Charon 등, cmd 1282) ON.

## Insert3D — 3D 모델 삽입 (2026-07-09 실측, blackhole_show)
- 생성: `Insert3D(Insert3D.Insert3DName(0))` (family 0x1D). **Insert3DName = 269멤버**(대부분 시스템 예약:
  LiveAtlas/HudGrid 등, 사용자용은 001~052 + 059~068 정도).
- 로드: `setModelFilename("..\\data\\scene\\astronomy\\...\\모델.osg")` — **Studio 로컬 .osg 경로**(상대).
  ✅ 블랙홀 강착원반 = `..\data\scene\astronomy\blackhole\schwarzschild\blackholeAccretionSharp.osg`
  (loadingStatus=Loaded, modelRadius=4,850만 실측). `loadingStatus`/`modelRadius` 로 로드 확인.
- 배치: `setParent(홀더.portId(포트))`(좌표계 부착)·`setPositionLBR`/`setOrientationHPR`/`setScale`.
  ⚠️ **포트 이름 클래스마다 다름** — Place2DPort/GalaxyPort 에 EquatorialSynchronous 없음(실패). dir() 확인 필수.
- ✅✅ **introspection = 모델 내부 탐색 (신규)**: `getIntrospection()` → `instrospectionOutput`(철자 주의!)
  가 JSON(uniforms 목록) 반환. 블랙홀은 **애니 노드가 아니라 셰이더 유니폼 `u_simulationTime`(원점=JD)로
  구동** → **시간가속(setDateTime)으로 원반 회전**. `modifyUniform("root/u_emissiveIntensity", Vec4, Anim)`
  로 발광 등 셰이더 파라미터 직접 조절.
- 기타: setVideoState/setVideoSpeed(비디오 텍스처), setAnimationName/Evolution(애니 노드 있을 때), rotateMatrix/translateMatrix.
- ⚠️⚠️ **블랙홀 모델(blackholeAccretionSharp.osg)은 '몰입형' — R≈0 중심에서만 보임 (실측 확정)**:
  홀더 Place2D(CenteredPort)에 부착 후 카메라도 그 포트로 `setPositionLBR(Vec(L,B, 5e-14), Anim, pport)`.
  **R=5e-14(중심)만 보이고, R≥0.05×modelRadius 부터는 안 보임**(v2 6배·v4 0.05배 전부 실패).
  = 바깥 초상화 불가. **강착원반 한가운데서 방향(L/B)만 바꿔 둘러보는 구도**가 정답(원본 SPC 도 그러함).
  포트: Galaxy=`Galactic` / Place2D=`CenteredPort` (EquatorialSynchronous 아님 — 실측).
  중심 고정 후 L 회전=둘러보기 / B 틸트=원반 각도 / 시간가속=원반 회전 (blackhole_show_v5).
  ✅✅ **완성 구도 확정 (사용자 최종, blackhole_final)**: `setPositionLBR(Vec(0, -30, 5e-14), Anim, pport)`
  = 블랙홀 링이 돔 상단 중앙에 완벽(인터스텔라 룩). RC=5e-14→실제 R≈19440km(적당 크기).
  B=0 은 상단 잘림·둘러보기는 시야이탈. **회전=시간가속(u_simulationTime) / 발광=`setIntensity`(0.3↔2.5) /
  틸트=B 이동(중력렌즈)** 전부 확정. ⚠️ **modifyUniform("u_emissiveIntensity")는 밝기에 무효**(emissive 맵
  강도라 화면에 안 이어짐) — 밝기는 setIntensity 로. 완성본: blackhole_final.py (전 파라미터 통합).

## Comet — 혜성 (2026-07-09 실측 확정, comet_halley_final.py)
- 생성: `Comet(Comet.CometName.Comet001)` (Comet001~100 슬롯, family 0x18). 궤도 6요소로 '직접' 그림.
- **궤도 요소**: `setEccentricity`/`setInclination`/`setLongitudeOfAscendingNode`/
  `setArgumentOfPeriapsis`/`setDistanceToPeriapsis`(AU)/`setTimeOfLastPeriapsis`(JD) — 전부 (val, Anim).
- ⚠️⚠️ **확정 순서 (실측)**: `setStandardModelName(모델)` **먼저** → `setModelScale` → 요소들 →
  **sleep(0.3) 한 프레임 대기**. v1 실패 = 요소를 모델보다 먼저 넣고 즉시 읽음 → **전부 0 미반영**.
  모델 먼저 + Anim(0.0) 명시 + 프레임 대기 하면 요소가 정상 반영(읽기값 일치 확인).
- **표시**: `setOrbitIntensity`/`setOrbitThickness`(궤도선)·`setIntensity`(본체)·`setLabelIntensity`·
  `setLabelNameOverride(str)`·`setModelScale`. 포인터는 Body 계열(타입 지정 후 setPointerIntensity).
- **CometModelSet**: Basic(안전) / Generic3D / Halley3D / HaleBopp3D / Hyakutake3D / McNaught3D / Bradfield3D / UserModel.
- ⚠️⚠️ **궤도선만 보이고 본체가 안 보이면 = 날짜가 원일점 시점 (실측)**: 혜성 본체는 궤도상 '현재 날짜 위치'에
  그려짐 — 원일점(먼 지점)이면 까마득한 점. **본체를 보려면 근일점 근처 날짜로** setDateTime 점프
  (예 핼리 2061-06, 2024 는 하필 원일점). modelScale 크게 + 포인터 상시 ON 권장. (comet_halley_show3.py)
- **CometPort**: EclipticJ2000 / Galactic / OribitalMeanEquinox(오타 주의) / Synchronous / TerrestrialEquatorialJ2000.
- ✅ **시간가속(DateManager)으로 궤도 이동 관찰** — 슬롯 방식은 궤도선을 계속 유지한 채 움직임.
- ⚠️⚠️ **궤도선은 '지상(지구 하늘) 시점'에서만 렌더됨 (실측 확정)**: 태양 황도 포트로 카메라를 옮기면
  (`setPositionLBR(... sun.portId(Ecliptic))`) 궤도선 투영이 **사라짐**(우주만 보이고 아무것도 안 나옴).
  → 궤도선을 보려면 reset 기본 지상 시점 유지(카메라 이동 없음).
- ⚠️ **지상 다년(수십 년) 시간가속만 자전 광란** (37년=자전 1.3만 바퀴). 지상 시간가속 자체는 정상
  (day_night/eclipse 로 증명 — 시/일 단위는 부드러움). 혜성 궤도운동은 몇 달~몇 년이 필요해서 지상선 곤란.
- ✅✅ **혜성 클로즈업+시간가속 정답 = FadeTo 후 'Std Ecliptic J2000' 프레임 (2026-07-09 사용자 3확인)**:
  `DataManager.database().data(Data.Type.CometType, "1P/Halley").action(Action.Type.FadeTo).trigger()` →
  혜성 곁(R=AU) 황도 프레임. **이 프레임은 지구 자전 없음** →
  ① `setPositionR(cam.positionLBR.z * 0.45, Anim.cubic(5), -1)` 로 당기면 혜성 확대(6.68→3 AU 실측).
  ② 그 프레임에서 시간가속(근일점 전후 몇 달)이 **안 돌고 부드럽게** — 혜성 이동+코마/꼬리 변화 관찰.
  ※ 궤도선은 지상 전용이라 FadeTo 후엔 없음. 완성쇼 = 지상 궤도조망 → FadeTo 클로즈업 → 시간가속.
  확정 예제: `comet_halley_complete.py`.
- ⚠️⚠️ **DB 경로도 됨** (`DataManager.database().data(Data.Type.CometType, "1P/Halley")` → FadeTo) —
  단 **FadeTo 페이드 전환이 궤도선을 지움**. 궤도선 유지가 필요하면 슬롯 방식(FadeTo 금지)이 정답.

## GlobularCluster — 구상성단 (2026-07-09 실측)
- 생성: `GlobularCluster(GlobularCluster.GlobularClusterName.NGC5139_omegaCen)` — M13(NGC6205_M13)/
  M4/M5/M62 등 다수. `setIntensity`/`setScale`/`setLabelIntensity`/`setPointerType`(내장 포인터 동작).
- DB: `Data.Type.GlobularClusterType` — 이름 "Omega Centauri"/"NGC 5139"/"omega Cen"/"Centauri" 전부 됨.
- Port: Ecliptic/Galactic 만.
- ⚠️⚠️ **FadeTo 후 R=0 (실측)** — 행성(R=5)·소행성과 달리 성단 중앙에 딱 붙음 → `setPositionR` 줌 무효
  (0×배율=0, 절대값으로 뒤로 빼는 건 방향 반대). **확대 = `setScale` 크게가 정답 (사용자 확인, 40~80배 동작)**:
  카메라는 FadeTo 로 이미 중앙 → setScale 을 1→80 으로 올리면 '성단 속으로' 확대. (globular_cluster_final.py)
  ⚠️⚠️ **setScale 은 절대값 금지 — 반드시 '원본 scale × 배율' (2026-07-09 확대 실패 실측)**: 성단 원본
  scale 이 1.0 이 아닐 수 있어 `setScale(30)` 절대값을 주면 오히려 **원본보다 작아져 확대가 안 보임**.
  → `orig=gc.scale` 읽어두고 `gc.setScale(orig*60, Anim)`, 복귀는 `gc.setScale(orig, Anim)`.
- ⚠️⚠️ **AdvancedCamera 비행(setModeFreeFly/zoom/takeOffOn/move)은 스크립트서 여전히 무효 (2026-07-09 재확인)** —
  R 이 0.0 에서 안 변함. 비행 모드는 오퍼레이터 수동.
- ⚠️⚠️⚠️ **성단 별밭은 R 로 확대 안 됨 = 고정 투영 (실측 확정, R 20만~3 스윕 전부 동일 화면)**:
  말머리 성운은 R 로 프레이밍 변화했지만, **구상성단 내부 별밭은 카메라를 감싼 고정 돔**이라
  '멀리서 접근하는 비행'이 구조적으로 불가. → 외부=지상 뿌연 별(setScale 확대) / 내부=FadeTo 로 별밭 진입
  (개별 별로 풀림) / 둘 사이 전환은 FadeTo(페이드)뿐.
  ✅ **FadeTo 자체가 '줌인+한바퀴 스핀' 내장 (사용자 관찰)** — 수동으로 못 만든 접근+회전을 공짜로 해줌(이득).
  ⚠️ **내부 둘러보기/확대는 위치(L·R)가 아니라 `setScale`(확대)·`setOrientationHPR`(회전)** — 별밭이 위치에
  반응 안 하므로 L/R 무효. 확대=scale, 회전=orientation.
- ✅✅ **구상성단 완성쇼 확정 (2026-07-09 사용자 최종, globular_cluster_final.py)**:
  ① 지상: 별자리 선(Cen) + 포인터로 식별, `setScale(orig×30)` (지상 확대는 약하지만 참고용).
  ② **FadeTo → 별밭 진입**(줌+스핀 내장 = 접근 연출). ③ 중앙에서 `setScale(orig×700)` **한방에 확대**
  (Anim.cubic(14) 단일 애니 = 심장부까지 매끄럽게 파고듦, 단계 램프 불필요). ④ **내부 회전 = Roll(Z축/시선축)**:
  `setOrientationHPR(Vec(H, P, R+360), Anim.cubic(16))` **원큐 360° 스핀** — 별밭이 화면 중심축을 돌며 팽이.
  ⚠️ **H(heading) 스윕 = 좌우 팬(시계/반시계 느낌), 진짜 '축 회전'은 세 번째 값 Roll**. 복귀는 orig scale.

## Universe — `Universe(Universe.UniverseName.MainUniverse)`
- `setGlobalIntensity(intensity, Anim)` — 전체 장면 밝기(0=암전,1=정상)

## IndividualStar — `IndividualStar(IndividualStar.IndividualStarName.Sun)`
- **Name(일부)**: Sun, Sirius, Vega … (enum 3,189개) / **Port**: `Ecliptic`
- `setIntensity(intensity, Anim)`, `portId(IndividualStarPort)`
- ✅✅✅ **태양 클로즈업 완성 (2026-07-14 사용자 확인, sun_closeup.py)** — 전부 미연습이었던 태양 표면 기능:
  · **접근 = `reset` → DB `data(Data.Type.StarType, "Sun").action(FadeTo)`** (도킹 posLBR≈{L, 12, R=0.21}).
    ⚠️⚠️ **이 프레임 R 단위 = AU!** (태양 반지름 0.00465 AU). FadeTo R=0.21AU=먼 작은 원반 →
    **`setPositionR(0.03, Anim, -1)`(≈6.4 태양반지름=4.49Gm) 로 당겨야 원반이 돔에 꽉 참**. (4.5 넣으면 4.5AU=별밭만.)
  · **`setModel(Model.SDO)` 필수** — 이걸 켜야 표면 영상(광구/자기장)이 렌더됨. Model enum: DefaultModel/Photosphere/
    HDR/Visible/**SDO**/SDOStatic/Internal/RAW/DidSliced.
  · **필터(태양의 여러 얼굴)**: `Filter_304`=304Å 자외선(붉은 채층·**홍염**) · `Filter_Visible`/`Filter_Intensitygram`=연속광.
    (H-알파 멤버는 없음 — 304 가 홍염용.)
  · ⚠️⚠️ **흑점을 '어두운 점'으로 렌더 안 함 (2026-07-14 사용자 실측 확정)**: Filter_Visible/Intensitygram 은
    **밋밋한 흰 원반**(흑점 안 보임). **흑점 = `setMagnetogramIntensity(1)` 의 색깔 활동영역(노랑/초록/빨강/파랑=자기극성)**
    으로만 표현됨. "자연스러운 어두운 흑점" 장면은 이 빌드에 없음 → 흑점 보여주려면 magnetogram 필수.
  · **`setMagneticLinesIntensity(1)` = 자기력선(청록 코로나 루프, 흑점 사이 아치)** — 제일 볼만함.
  · `setCoronaIntensity`(코로나) · `setPhotosphereIntensity`(광구 밝기) · `setSaturationFactor`(채도) ·
    `setCycle(Cycle.Cycle_2165/2232/2097)` = 태양 활동주기 프리셋 · `setInternalRepresentation(IR_Layers/IR_Zones)`.
  ⚠️ magnetogram + 자기력선 동시엔 화려/복잡 → 원하면 장면 분리(자연스러운 태양 = Filter_Visible 만).
  · 시간가속(setDateTime Anim)으로 태양 자전(~25일) — 흑점이 표면 가로지름.

## Constellation — `Constellation(Constellation.ConstellationName.Ori)`
- **Name(IAU 3자 약어)**: Ori, UMa, Sco, Crux, Leo, Tau, Cyg, Aql, Vir, Gem …
- `setLinesIntensity`, `setLabelIntensity`, `setArtIntensity` (각 intensity, Anim)
- ✅ **setArtIntensity(별자리 그림) 동작 확정 (2026-07-07 실측, night_guide_tour v1)** — 0.9 페이드인 OK.
- ⚠️ **enum 멤버 = 627개 (실측 2026-07-06)** — IAU 88개가 아니라 타 문화권 별자리/성군 전부 포함.
  전체 ON = 난잡(사용자 확인) → **유명 IAU 별자리 큐레이션(15~20개) 권장**, 라벨은 5개 이내.

## Nebula — `Nebula(Nebula.NebulaName.X)`
- `setIntensity(intensity, Anim)`
- ⚠️⚠️ **SPC 의 성운 숫자 인덱스 ≠ Python enum (실측)**: `Nebula(NebulaName(134))` → **id=-1(null)**.
  NebulaName 은 **44개 이름 멤버**: HORSEHEAD, CRAB, EAGLE, CATEYE, DUMBBELL, BUTTERFLY, ESKIMO, HH47 …
  → SPC→Py 변환 시 성운은 이름으로 매핑해야 함.
- ✅ **DB 이름 검색 우회로 (실측)**: enum 에 없는 천체도
  `DataManager.database().data(Data.Type.AsterismType, "Barnard 33")` → `.action(Action.Type.FadeTo).trigger()` 로 이동 가능.
  Data.Type 은 66종(NebulaType, NgcType, DeepSkyObjectType, MessierType, StarType …) — 이름/타입 조합으로 탐색.

- ✅✅ **성운(빌보드 아트) 씬 레시피 (말머리 실측 확정 + 사용자 최종 확인 2026-07-06, scripts/study/horsehead_show.py)**:
  ① 위치: `setPositionLBR(Vec(0,0,R), Anim, neb.portId(NebulaPort.LineOfSightLocal))` — R 10~20pc=프레이밍/400pc=지구시점
  ② **조준+세우기 = cmd295**: `setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim, 포트id)` — 포트 프레임 정렬로 자동으로 섬
  ③ **Target 정렬 = `setTargetHeight(30)`** — 🎯운영 표준 30(관람 정위치).
     돔 투영: Target 0°=가장자리(눕는 원인!), 90°=천정(기하학적 중앙 — 실측 "90이 딱 가운데"지만 관람 부적합)
  ④ 슬루 숨김 = GlobalIntensity 0 에서 전부 세팅 후 페이드인
  ⑤ **공전(오빗) = 스텝 오빗 (사용자 확인 완료)**: 0.5초 스텝으로 L 증가(`setPositionLBR(Vec(L,0,R), Anim(0.5), los)`)
    + **4스텝(2초)마다 ② 재조준** → 360° 한 방향 풀 공전에서도 대상 중앙 유지. 도착 재정렬은 TH 지글(29.9→30) no-op 우회 (🎯표준 Target 30).
    성운 LOS 프레임에선 L 스윕이 자연스러운 공전(행성 FadeTo 프레임의 'L=레코드판' 어지러움과 다름 — 프레임마다 축이 다름).
  ⚠️ 함정: SPC 성운 인덱스≠enum(id=-1) / 줌 락은 FreeFly 전용·TH 와 양립 안 함 / R 2pc는 아트 내부 / NebulaPort 3종(Ecliptic, LOSEcliptic, LOSLocal)

## SkySurvey — `SkySurvey(SkySurvey.SkySurveyName.SkySurvey001)`
- API 전부(실측): `setUrl(url)`, `setIntensity(i, Anim)`, 읽기 `url`/`intensity`/`id`
- 온라인 HiPS(alasky 등) URL — **Studio 머신에 인터넷 필요**(없으면 검은 하늘)

## Messier — `Messier(Messier.MessierName.M42)`
- **형식**: M1~M110. 유명: M1(게), M31(안드로메다), M42(오리온), M45(플레이아데스)
- `setIntensity(intensity, Anim)` · `setScale`(보유)
- ✅✅ **메시에 DB 접근법 확정 (2026-07-13, messier_tour.py)**: ⚠️ `MessierType` 핸들은 **FadeTo/ScaleUp
  미지원**(핸들은 나오지만 `.action()`=None). `DeepSkyObjectType` 은 **이름 조회 자체 실패**.
  → **`DataManager.database().data(Data.Type.NebulaType, "M##")` 가 정답** — 종류 불문(행성상성운·발광성운·은하)
  **전부 NebulaType + "M##" 로 카탈로그됨**(M27/M42/M31 성공). ⚠️ FadeTo 는 **진입/센터링을 안 해줌**(대상은 제자리,
  라벨만 구석). ScaleUp 액션도 무효.
- ✅✅✅ **메시에/딥스카이 접근의 정석 = ConnectTo + 절대타겟 지오메트릭 줌 (2026-07-13 Recording16 검증, 말머리 레시피 확장)**:
  ① **`h.action(Action.Type.ConnectTo).trigger()`** → 대상 **LOS Local 프레임**으로 전환(말머리와 동일 프레임!).
     LookAt 은 미지원 → ConnectTo 가 잡힘. 내부에 ~4초 'Look at' 자세슬루 있음 → **암전 속 전환 권장**.
  ② R = **초대형**(트랙반지름 단위, 성운 ~1e15 / 은하 ~수백). ⚠️ HUD 의 pc 와 다른 단위.
  ③ **센터링 = `setTargetHeight(90)`** (성운 LOS 프레임은 90 이 돔 중앙).
  ④ **접근/확대 = `setPositionR` 지오메트릭 줌** — ⚠️⚠️ **목표 R 을 '절대값'으로 미리 계산**해 순차 재생할 것.
     `p.z×비율`(현재값 읽어 곱)은 겹치면 덜 줄고(대상 작아짐)·엉킴. 절대타겟이면 **겹쳐도(sleep<Anim=연속·매끄러움) 깊이 정확**.
     스텝 stop(sleep≥Anim)=중간 뚝뚝 끊김 / 스텝 겹침(sleep<Anim)+절대타겟=매끄럽고 정확. (아포피스 소행성과 동일 메커니즘)
  ⑤ **은하 세우기 = roll**: `setOrientationHPR(Vec(H,P,R+35))` — 안드로메다는 실제 77° 기울어 '누워'서, roll 로 대각선.
  ⚠️ **개체 종류마다 특성 다름**: 행성상성운(M27,작음)=깊게 / 발광성운(M42)=중간(돔 가득) / 은하(M31)=얕게+roll(통과 방지).
  ⚠️⚠️ **산개성단(M45 플레이아데스)은 접근 부적합 (실측 확정)**: 밀집 천체가 없어(듬성듬성 별) 다가가면
     성단은 안 보이고 배경 성운(말머리 등)만 껴 보임. **배경 끄기(`Galaxy.setIntensity(0)`, `Nebula(...).setIntensity(0)`,
     Nebula enum 전체 off)로 배경은 지울 수 있으나(가능 확인) 성단 자체가 렌더 안 됨** → 투어는 밀집 천체로.
  → 완성 예제 순서: NebulaType 핸들 선확보 → 암전 → ConnectTo(슬루 대기) → 배경 off + 타깃 강조 → TH90 (+roll) →
     페이드인 → 절대타겟 겹침 줌. depth(스텝수)로 개체별 확대량 조절. (messier_tour.py)
  ⚠️ 미해결(나중): ConnectTo 진입의 'Look at' 슬루(cmd 295)가 은하에서 순간이동처럼 보임 → 암전 전환 강화 필요.

## DateManager — `DateManager()` ✅ 실측(2026-07-06, scripts/study/eclipse_2026_v2.py)
- **`DefaultTimeZone` = UTC 로 해석됨 (실측 확정)** — 넘긴 시각이 그대로 UT. KST 아님!
  (멤버: DefaultTimeZone, InvalidTimeZone, UTC_M_01_00_AZO … 지역별 오프셋 이름들)
- `setDateTime(year, month, day, hour, minute, second, TimeZone, Anim)`
- ⚠️⚠️ **`stop()` 을 setDateTime "뒤"에 부르면 방금 건 날짜 이동까지 취소됨 (실측 사고)**
  → **순서: `dm.stop()` → `setDateTime(...)` → sleep 으로 적용 대기**. 검증은 `dm.julianDate` 읽기.
- ✅✅ **시간 가속(타임랩스) = `setDateTime(목표시각, tz, Anim(초))` (실측 확정)**:
  날짜가 Anim 시간 동안 연속으로 흐름 — 일식 49분을 40초에 재생, JD Δ=0.0340 정확.
  가속 중 하늘이 실제로 회전 — 저속(수십 분/수십 초)이면 부드러움.
- `setCurrentDate(hour, minute, second, TimeZone, Anim)` — 오늘 날짜 기준 시각만
- `stop()` — 시간 흐름 정지 (위 순서 함정 주의)
- ✅✅ **일식 쇼 완성 (2026-07-06 사용자 최종 확인, scripts/study/eclipse_2026_target30.py)**:
  관측지+시각+틸트30+setOrientationH 자동조준+시간가속+setScale×25 코로나 클로즈업 전부 동작.
  지상 이벤트 쇼(특정 날짜·장소 하늘)의 표준 골격으로 사용할 것.
  일식 API: `setEclipseShapeIntensity`(Planet·Satellite 존재), `setPenumbraBefore/After*` 존재,
  `setUmbra*` 는 없음(Antumbra 계열이 정답).
- ✅✅ **Sky View(지상) 돔 조준 실측 (2026-07-06 v4 A/B/D)**: `setTargetHeight`/`setTarget` **트랙볼이 Sky View 에서도 동작**
  (HUD Target 값 반영 — 예전 '_Sky View 잠김_' 기록은 그 세션 상태 문제였던 듯, 정정).
  **`setTarget(Vec2(az, t))` 의 t = 돔 틸트각(Target 값)이지 천체 고도가 아님!**
- ✅✅✅ **Sky View 조준 확정 (2026-07-06 사용자 최종 확인 — 일식 쇼 완성)**:
  **스크립트 레버 = `setTargetHeight(틸트)` + `setOrientationH(H, Anim)` 두 줄** (순수 트랙볼/방향 —
  위치 명령 불필요). 일식 쇼에서 자동 조준 성공 실측.
  ① 틸트: 🎯관람 표준 30. (천체를 뷰 축에 정확히 = 90-고도 — 클로즈업 등 특수용)
  ② 좌우 = `setOrientationH(H)`: **H ≈ 180 - (천체 방위)** (+작은 오프셋 ~1.7°는 캘리브레이션 오차 범위).
     예: 태양 az 285.5 → H = -103.85 (사용자 수동 캘리브레이션 역산과 일치, 자동 조준 확인).
  ③ ⚠️ **setPositionLBR 등 위치 명령은 지상 Sky View 에서 금지** — 어떤 track 이든
     관측자 이탈(비행 카메라/Terrain View 전환) 유발 (v9 실측). setTargetAzimuth 는 무반응(v9).
  ④ 지상 클로즈업 = setScale (FOV 줌은 지상 무효).
  **줌 락(setZoomPosition)은 지상 Sky View 에선 무반응 확정** (우주/행성 뷰 전용). FOV 줌(setZoomFov)은 동작.

## InsertText — `InsertText(InsertText.InsertTextName(slot))` (slot 1~46)
- `setText(text)`, `setPosition(Vec(azimuth, height, roll))`, `setDistance(dist, Anim)`
- `setIntensity(intensity, Anim)`(0=숨김,1=표시), `setSize(size)`(예 0.05), `setColor(Vec(r,g,b))`
```python
t = InsertText(InsertText.InsertTextName(1))
cam = Camera(Camera.CameraName.MainCamera)
cam.addChild(t.id, Camera.CameraPort.FixedForeground)
t.setText("안녕하세요"); t.setPosition(Vec(0, 20, 0))
t.setSize(0.05); t.setColor(Vec(1, 1, 1)); t.setIntensity(1.0, Anim(1.0))
```

## Insert2D — `Insert2D(Insert2D.Insert2DName.Insert2D001)`
- `setTexture(path)`, `setPosition(Vec(az,h,roll), Anim)`, `setSize(size, Anim)`
- `setIntensity(intensity, Anim)`, `setType(Type, Orientation)`
- 특수: `Insert2D.Insert2DName.Insert2D076_LightPollution`(광공해 오버레이)

## SceneGraph — `SceneGraph()`
- `reset(reinitId=1)` — 전체 리셋 / `lockManipulator(duration)` — 조작 잠금

## Anim — `Anim(duration)`
- `Anim(2.0)`(선형), `Anim.cubic(2.0)`(부드러움)
- 속성: `duration`, `interpo`(`Anim.Cubic`/`Anim.LinearEvo`…), `offset`

## Animator (구형) — `Animator(duration)`
- 속성: `duration`, `acceleration`, `deceleration`,
  `interpolator`(`Animator.Interpolator.InterpolatorInertial`…),
  `relativity`(`Animator.Relativity.RelativityAdd`),
  `postBehavior`(`Animator.PostBehavior.PostBehaviorContinue`)
- ※ Anim/Animator 둘 다 존재. 최신 코드는 **Anim 선호**.

## DataManager / Action (천체 전환)
```python
obj = DataManager.database().data(Data.Type.PlanetType, "Saturn")
obj.action(Action.Type.FadeTo).trigger()
```
- **Data.Type**: `PlanetType`, `GalaxyType`, `MountainType`, `SpcType`
- ✅✅ **GoTo = 연속 비행 (사용자 실측 확정 2026-07-06!)** — '우주선 여행' 연출의 정답.
  `data.action(Action.Type.GoTo).trigger()` → 현 위치에서 대상까지 실제 비행 (30AU→토성 수십 초).
  비행 시간 가변 → **도착 감지 = '움직임 확인 후 정지 3연속' 폴링** (출발이 느려 초반 정지를 도착으로
  오판 주의 — v7 실측). GoTo 도착 R 단위 = 트랙 대상 반지름 (토성 61273 반지름 = 3.6Gm 일치).
  ⚠️ **비행 중/행성 프레임에선 DataManager.data() 조회가 None (실측)** — 핸들은 쇼 시작 때 선확보.
  ✅ GoTo 도착 = R≈5 트랙반지름 도킹 (토성 5.008/지구 4.0 실측 — FadeTo 와 동일 프레이밍).
  ✅ **행성 프레임 자막 거대화 해결 = `setDistance(20)`** (기본 distance 1.0 = 트랙반지름 1배 거리라 거대).
  ⚠️⚠️ **단 setDistance(20)은 행성/은하 프레임 전용!** 지상 Sky View 에선 **기본 1.0 이 정답** —
  20이면 20배 멀어져 자막이 안 보임(v19 '텍스트 실종' 실측). 프레임 따라 distance 를 갈아탈 것.
  ⚠️ **distance 20 프레임에선 setSize(0.035)도 실종 유발 (v21 실측)** — 행성/은하 자막은
  **size 기본값 + distance 20**, 지상 자막은 **size 0.035 + distance 1.0** 조합으로 고정.
  ✅ **Land 스크립트 재현 성공 (v19 사용자 확인)** — GoTo 도킹 후 273+289 레시피 동작.
  `data.action(타입)` 이 **None 이면 그 데이터가 미지원** — trigger 전 None 체크.
  ⚠️ **GoTo 는 도착 후 Target 을 0(가장자리)으로 남김 (사용자 발견!)** — FadeTo 는 30 자동.
  **GoTo 도착 후 `setTargetHeight(30)` 필수** (안 하면 행성이 돔 바닥에 깔림 + 착륙도 안 보임).
  ⚠️ **정정: GoTo 지구 = R=0 자동 착륙 아님!** 내부 목표 posLBR={0, 89.999, 4} —
  **북극 상공 R=4 지구반지름 '호버'로 끝남** (v9 의 'R=0 자동 착륙' 기록은 그 세션의 Land 조작 혼입).
  ✅✅✅ **GoTo 내부 안무 = 대상 종류별로 다름! (Recording5 완전 해독 → 상세 docs/16_travel_methods.md)**
  공통: Time/Camera stop → Turn ON bodies → **Switch(비행 전에 목적지 트랙 전환)** → 273+295 애니가 비행.
  ① **행성**: 20초 비행 → 도킹 {L60, B20, R=5 행성반지름} + 6.7초 방향정렬(비행 중 회전, 제거 불가).
  ② **지구(관측지)**: **Set place2D 로 관측지 덮어씀(직하점 임의값!)** → 20초 비행 {0, 89.999, R=4} →
     수직하방 응시 → **호버 종료** (착륙은 별도 Land). 미리 건 Place2D/시각은 무효 → 착륙 후 딥에서 재설정.
  ③ **은하**: **Move away(276 후진 13초) → Look at(295 조준 13초) → 프레임 점프 → 은하 프레임 15초 비행**
     — 3단 안무라 제일 비행답게 보임. 도킹 R=16.8 (StdGal).
  ✅✅✅ **Land 버튼 해독·스크립트 재현 성공 (Recording4/5 + v22 사용자 확인)**:
  도킹 후 ① `setPositionLBR(Vec(L유지, B유지, 0), Anim.cubic(10), -1)` (R→0 하강)
  + ② `setOrientationHPR(Vec(cam.orientationHPR.x, 0, 0), Anim.cubic(10))` (pitch -90→0) **동시 발사**.
  착지 = state SkyView/R=0 — reset 없이 지상 복귀 완료. 실측 R: 4.01→3.59→2.60→1.41→0.42→0.
  ⚠️⚠️ **GoTo 지구는 Place2D 를 내부에서 덮어씀** — 몽블랑을 미리 걸어도 위도20/경도-90 에 착륙 실측!
  → **착륙지·시각 세팅은 반드시 '착륙 후' 짧은 딥(암전) 속에서** (지상↔지상 재배치라 reset 불필요).
  ⚠️⚠️ **행성 프레임에서 setDateTime 큰 점프(수개월) = 하늘 통째 회전('한바퀴' 사고, Recording4)** —
  출발 전 시각 변경 금지. 시각 변경은 지상 착륙 후 or 암전 속에서만.
  ✅✅ **ConnectTo = 카메라 프레임을 대상 트랙으로 '이동 없이' 전환 (v13 텔레메트리 실측 확정)**:
  토성 이탈 후 지구 ConnectTo → R 60(토성반지름)→220529(지구반지름)=14.05억km=토성↔지구 거리 정확 일치.
  ⚠️ **ConnectTo 상태에선 GoTo 비행이 동결 (60초 R 불변 실측)** — 둘을 같이 쓰지 말 것.
  ⚠️⚠️ **프레임 간 '보이는 접근 비행(다이브)'은 미해결 확정 (2026-07-06, 행성 자전 연출과 같은 급)**:
  GoTo=접근 안 보임 / ConnectTo+cmd295 조준+수동 R 기하급수 하강(v14)=느린 드리프트 후 멈춤, 실패.
  → **정답은 그냥 착륙: 암전 → reset(1) → 지상 재세팅 → 페이드인** (복합 데모 v15 확정).
  같은 프레임 안 R 애니메이션(도킹 후 줌인/이탈 풀백)만 '보이는 비행'으로 사용할 것.
  지원 액션은 데이터마다 다름(실측): 산 = FadeTo/GoTo 정도, 행성 = +StraightGoTo/ConnectTo/On·Off 계열.
  GoToPlace/FadeToPlace/LookAt/ScaleUp 은 산·행성 데이터에 없음.
  FadeTo=페이드 전환 / StraightGoTo·GoToPlace=순간이동 (실측 판정).
- **Action.Type (전체 실측 목록 2026-07-06)**: FadeTo, GoTo, StraightGoTo,
  GoToPlace/FadeToPlace, FadeToDate/FadeToObservation/FadeToParent, ConnectTo, **LookAt(미검증)**,
  ScaleUp/ScaleDown, On/Off/OnOff, LabelOn/Off, LineOn/Off, OrbitOn/Off, TrajectoryOn/Off, PointerOn/Off,
  PictureOn/Off, BoundaryOn/Off, Play/PlayLoop/PlayInstant/PlayAdvanced/PlayPause/PlayStop, Activate, Add,
  Apply, Clear, Edit, Export, Load, Pause, Properties, Remove, Start, Stop, Tag/Untag, Share/Unshare 등.
- ✅ **DB 명칭 실측(2026-07-06)**: 은하수 = `"Milky Way"`(띄어쓰기! MilkyWay 는 실패), 몽블랑 = `"Mont blanc"`(MountainType — 지상 관측지 FadeTo 동작 확인), 달 = `"Moon"`(SatelliteType).
- ⚠️ **FadeTo 의 실체 = 'Fade out→순간이동→Fade in' (내부 로그+실측 정정)** — 비행 아님, 페이드 전환.
  **연속 비행 연출은 같은 프레임 안 R/L 애니메이션으로 직접**: 접근 = setPositionR(R×0.5, Anim.cubic(5), -1),
  이탈 = R×12 풀백 등 (말머리 비행·토성 줌에서 검증). 프레임 간 이동(행성↔행성)은 페이드가 유일.
- ⚠️ **MountainType FadeTo = 상공(-190km) Terrain View 로 이동 (실측)** — '산에서 본 밤하늘'이 아님!
  지상 밤하늘 = Place2D 좌표 설정(위도,경도,고도m)이 정답.
- ⚠️⚠️ **행성 뷰 → 지상 복귀 (실측)**: Place2D 좌표만 바꿔선 안 됨(카메라가 행성 프레임에 남음).
  **복귀 = 암전 속 `SceneGraph().reset(1)` 후 지상 전체 재세팅**(체크리스트+시각+TH — reset 이 다 끔).
- ✅ 토성 '이탈 풀백'(R×12, Anim.cubic(8), track=-1) = 연속 후진 비행 실측 성공 (0.35→4.21Gm).
- ✅✅ **소행성/궤도천체로 '줌인'(FadeTo 없이) 3경로 실측 (2026-07-09 아포피스)**:
  ⚠️ **지상 Sky View 에서 `setPositionLBR(대상 포트)` 직접 이동은 무효** (관측자 바인딩) — 프레임을 먼저 잡아야 함.
  프레임 잡는 3방법: ① **FadeTo** = 페이드+순간이동(접근 안 보임). ② **GoTo** = 페이드 없는 연속 비행
  (23.5초, 도킹 R=10) — 단 **비행 중 자세 회전 1회 '흔들림' 내장(제거 불가)**. ③ **ConnectTo** =
  비행 없이 프레임만 순간 전환(자세 회전 無). 프레임 확보 후 `setPositionR(읽은값×배율, -1)` 연속 줌.
  → **흔들림 없는 줌인 = ConnectTo(암전 속 전환) + R 애니** / 비행감 원하면 GoTo(흔들림 감수).
  ✅✅ **ConnectTo+setPositionR(읽은값×배율, -1) 매끄러움 확정 (v4/v5, 옛 '드리프트' 우려 정정)**:
  단 **ConnectTo 후 R 이 초대형**(아포피스 지상서 R=4,869만 소행성반지름 = 실제 거리) →
  ×0.4 몇 번으론 안 커 보임. **R<목표 될 때까지 ×배율 반복(적응형 지오메트릭 줌)** = 멀리서 도킹까지 연속 접근.
  ⚠️⚠️ **'끊김' 원인 = 스텝마다 `Anim.cubic`(가감속) (Recording9 해독)** → 경계마다 감속·재가속.
  **매끄러운 줌 = `Anim`(선형) + 큰 비율(0.55, 작은 스텝) + 짧게(1.2초) 다수 반복** (asteroid_apophis_v5.py).
  ✅ **DB 소행성(Apophis)은 지형 3D 모델(asteroid1.osg) 내장** — 슬롯과 달리 진짜 돌덩이로 렌더.
  ✅ **ConnectTo 내부 안무(SPC): Time stop→Camera stop→Turn ON→Switch→'Look at' 자세슬루(3.97초)→Target 30.**
  이 Look at 슬루가 보이므로 ConnectTo 전환 순간은 암전 권장. → **개체별 카메라 무빙 총정리: docs/19**.
- InsertText 위치 조정 = `setPosition(Vec(방위, 높이, 롤))` — 높이 0=지평선, 90=천정. 55 가 제목 위치로 무난.
- ⚠️ 지상 노을 시간대(일몰 직후 ~1h)는 적색 산란으로 지형이 **불탄 듯 벌겋게** 보임 — 밤 연출은 현지 23시 이후 권장.

## AdvancedCamera — ⚠️ 스크립트 제어 대부분 불가 (전부 실측 확정)
- `zoom()/move()/tilt()/roll()` 스크립트에서 **무효**(호출돼도 화면 안 움직임) — 마우스 전용.
- `setModeTerrainView()/takeOffOn()` 도 화면 안 바뀜 — **비행뷰는 UI 'Take off' 버튼을 사람이** 눌러야.
- Place2D 관측자와 비행 카메라는 **위치 비공유** — 스크립트 관측지 세팅이 비행뷰에 반영 안 됨.
- 비행모드에선 `setTargetHeight(-90)` 등 트랙볼이 풀리지만, 특정 지점 수직하강 연출은 구조적으로 불가.
  실전 = 스크립트가 씬 세팅, 오퍼레이터가 비행 조작 (프로덕션도 큐 기반 운용).
