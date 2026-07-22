# Sky Explorer Python API 레퍼런스 (CLAUDE.md)

> 🚨 **예제(쇼) 만들기 전 무조건 먼저 읽기: [`docs/20_object_playbook.md`](./docs/20_object_playbook.md)**
> — 개체별 확대·이동 방법 매트릭스 + fly-in 가능 판별 + 실패 원인 + 표준 기본값(딥스카이 frac=0.004, Target 30).
> 카메라 무빙/줌이 들어가는 예제는 이 플레이북의 의사결정 트리대로 개체에 맞는 방법만 쓴다(사용자 확정 규칙).
>
> ⭐ **코드 구성 시 참고 우선순위**:
> 1. **정확한 메서드 시그니처** → [`reference/core_api_reference.txt`](./reference/core_api_reference.txt)
>    (사용자 제공 핵심 31클래스 전체 시그니처. 인자 타입·Anim 위치·enum 확인은 여기부터.)
>    ➕ **전 클래스 완본** → [`reference/skyexplorer_api_all_in_one.md`](./reference/skyexplorer_api_all_in_one.md)
>    (2026-07-20 사용자 제공, skyExplorer 앱 전체 파이썬 API 덤프 31k줄. core 에 없는 클래스/메서드는 여기서 grep. 조회 전용 — HF 프롬프트 주입 X.)
> 2. 이 CLAUDE.md — 빠른 요약/사용 패턴/함정.
> 3. 보조: 실측/함정은 [`docs/`](./docs/) 노트, 전체 추출본은 [`reference/`](./reference/).
> ⚠️ 세부 enum 멤버(성운/시간대 이름 등)는 `dir()`/도움말/ST 로그로 확인.
> 실제 SDK 빌드와 미세 차이가 있으면 **ST 실행 로그(에러의 "Did you mean")가 최종 진실.**
>
> ✅ **레퍼런스로 검증된 함정**(우리가 실측으로 도달, core_api_reference.txt 일치):
> - Analemma '포트' 없음 → `DateManager.setMotionType(MotionType.MotionAnalemma)` 존재.
>   ✅✅✅ **태양 아날렘마(8자) 완성 확정 (2026-07-15 사용자 스샷 확인, sun_analemma.py + Recording30)**:
>   파란 낮 하늘 한가운데 **매끈한 8자**가 그려짐(위 크게/아래 작게 = 자전축기울기+타원궤도). 대성공.
>   메커니즘(Recording30 해독): `setMotionType(MotionAnalemma)` 는 **내부적으로 Earth 에
>   `setRotationSpeedScale(≈0.00273=1/366)` 를 걸어 일일 자전을 상쇄** → 매일 같은 시각의 태양이 한 자리에 모임.
>   1년 가속 시 하늘이 365바퀴가 아니라 ~1바퀴(반대방향)만 도는데, 그 1바퀴 = 별 배경의 연주(年周) 회전(정상).
>   → **'낮'(대기 ON)으로 만들면 배경 별이 안 보여 그 1바퀴도 사라지고 정오 태양만 8자**. (밤 버전은 배경 돌아 헷갈림.)
>   레시피: Place2D(0) 관측지(청주) + `setOrientationH(0)`+`setTargetHeight(37)`(남 정오 고도~53 중심) +
>   `Earth.setAtmosphereIntensity(1)`(낮 파란 하늘) + Stars 0 + `sun.setTrajectoryIntensity(1)`(궤적선=8자) +
>   `sun.setScale(3)` + `setMotionType(MotionAnalemma)` + `Earth.setElevationScale(0)` + 1년(365일) setDateTime 가속.
>   ⚠️ 시각 = **청주 현지 정오 = 03:30 UTC** (아래 '청주 시간 규칙' 참조 — 12:00 UTC 넣으면 한밤=검은 화면 버그였음).
>   SPC: setMotionType cmd **4891**(DateManager 전역), setTrajectoryIntensity cmd **772**(IndividualStar).
> - `Planet.setRingIntensity` 없음 → `setRingModel(Planet.RingModel)`.
> - track 받는 카메라 이동은 `(value, Anim, track)` — **Anim 필수**(`setPositionXYZ/LBR/R/L`).
> - `setOrientationR/HPR` 는 track 없는 속성 세터 → `setZoomPosition` 줌 락과 충돌.

## 기본 규칙

> 🟫🟫 **[운영 규칙] 지상 '하늘 쇼'는 지면(terrain)을 반드시 끈다 (2026-07-16 사용자 3회 지적)**:
> 대기만 끄면(`setAtmosphereIntensity(0)`) **지면이 남아 무지갯빛으로 지저분** → **`Planet(Earth).setTerrainIntensity(0.0)` 도 항상 같이**
> (+ `setElevationScale(0)` 평탄). 별·황도·세차 등 '위(하늘)를 보는' 지상 쇼 체크리스트 = 대기 OFF **+ 지면 OFF**. (계속 까먹어 못박음.)

> 🕘🕘 **[운영 규칙] 기본 관측지 = 청주. 시간은 '항상 UTC' 로 넣어야 함 (2026-07-15 사용자 확정 지시)**:
> `DefaultTimeZone = UTC` 이고 기본 Place2D 관측지는 **청주(위도 36.64, 경도 127.49°E)**.
> → **스크립트 짜기 전에 '청주 현지시각 → UTC' 변환부터 확인할 것**: **UTC = KST − 9h**.
> · 청주 현지 정오(태양 남중) = 12:00 KST = **03:30 UTC** (경도 127.5는 135°E 표준자오선서 30분 서쪽 보정).
> · 청주 밤 22:00 KST = **13:00 UTC** / 자정 00:00 KST = **15:00 UTC(전날)**.
> ⚠️ **실수 이력**: 정오를 12:00 UTC 로 넣었다가 = 21:00 KST 한밤 → 태양이 지평선 아래 → 검은 화면(아날렘마 v3).
> **낮/밤·태양고도가 중요한 지상 쇼는 반드시 이 변환을 먼저 계산하고 코드를 쓴다.**

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

- ✅✅✅ **행성 '위상'(초승달↔보름달) = 시간가속으로 실제 렌더됨 (2026-07-15 사용자 확인, venus_phases.py)**:
  금성을 FadeTo 도킹 → **관성 프레임(EquatorialJ2000)** 전환 → 시간가속(금성 1공전 ≈ 243일) 하면
  태양-금성-관측자 각이 돌며 **터미네이터(명암경계)가 쓸려 위상이 한 사이클** 순환(초승달→반달→보름→다시).
  갈릴레이 지동설 증거 재현 성공. ⚠️ **위상이 주제 = 운영 그림자OFF 규칙의 예외** — 오히려 강조:
  `setPlanetShineStrength(0)`(밤면 칠흑) + `setShadowStrength(1)` + `setShadowContrast(1)` = 초승달 선명.
  ⚠️ **적도 옆(B≈6)에서 봐야 터미네이터가 세로 = 초승달 모양**(북극 위 B90 이면 파이조각처럼 보여 부적합).
  ⚠️ 날짜 범위 충분히(1공전 이상) + **reset 이후 시작 날짜 재설정**(reset 이 날짜를 오늘로 되돌림 — DateManager 노트 참조).
- ✅✅ **천왕성 고리 렌더됨! (2026-07-15 사용자 스샷 확정 정정, uranus_rings_probe.py)** — 앞서 '안 됨' 은 오판(성급):
  ⚠️⚠️ **근접(R≈3.5) + 고리면 개방(B≈35) 에서 봐야 보임** — 지난번 안 보인 건 풀백 R=26(천왕성이 작은 점) 때문이었음(에셋 문제 아님).
  Planet 고리 API = `setRingModel(Planet.RingModel)` 하나뿐(enum: DefaultRing/BasicRing/Asteroids/Asteroids_3_0), `ringModel` 읽기.
  **ring intensity 세터는 없음** → 고리 '밝기'는 직접 못 올림. 천왕성 고리 에셋이 원래 어두워(실제도 숯색 반사율 3%) 희미.
  ✅✅ **고리 선명도 레버 실측 완료 (2026-07-15 사용자 스샷 확정, uranus_rings_bright2.py)**:
  · **모델 선택(DefaultRing/BasicRing/Asteroids/Asteroids_3_0) = 화면 변화 없음** (레버 아님, 토성 '미미'와 동일).
  · **GlobalIntensity·Sun intensity 오버드라이브 = 행성 본체만 하얘지고 고리는 그대로** (씬 조명은 고리에 안 먹힘).
  · ✅ **천왕성 '본체' `setIntensity` 를 올리면 고리도 같이 밝아짐** (고리가 본체 intensity 에 묶여있음 = 노트 일치!) —
    단 **~2 이상이면 원반이 새하얗게 타 백열전구처럼 보임**("이게 맞냐 ㅋㅋ"). → **본체 intensity ~1.5 전후가 균형**
    (고리 살짝 또렷 + 원반 색 유지). 그 이상은 과함. + 근접(R≈3)·고리면 개방(B≈38)·배경 검정(Stars 0) 필수.
  → 천왕성 고리 = '은은하게' 가 한계(어두운 에셋+밝기 세터 없음). 본체 intensity 로만 미세 조절.
- ⚠️⚠️ **토성 고리 `setRingModel(Planet.RingModel)` = 전환은 되나 화면 차이 '미미' (2026-07-15 사용자 3회 확인, saturn_rings.py)**:
  RingModel enum = **DefaultRing / BasicRing / Asteroids / Asteroids_3_0** (4종, SPC 값 0/2/13/28). 하드컷·6초홀드·
  고리면 근접(B=80, R 바짝)·DefaultRing↔BasicRing A/B 까지 해도 **구별이 어려움**(카시니 간극 유무가 안 드러남).
  → 쇼용 '고리 룩 변경' 연출로는 부적합. `setRingIntensity` 는 아예 없음(고리는 본체 intensity 에 포함).
  ✅ 같이 확인된 미사용 Planet 렌더: `setScatteringIntensity`(대기 산란)·`setPointSaturation`(색 채도)·
  `setCloudDirection`(가스 띠 방향, Anim 없는 단일 float) — 호출 성공(효과는 미세). SPC cmd(Recording22):
  setRingModel **1186**(enum), setScatteringIntensity **1061**, setPointSaturation **1034**, setCloudDirection **1168**.
  ✅ 가스행성 접근/줌 = 확정 레시피(FadeTo Saturn 옆도킹 R=5 → `setPositionLBR(Vec(L,B,읽은R×배율), Anim, -1)`).
  ⚠️ 줌 과하면(R<3) 고리 바깥지름(4.6 토성반지름)이 화면 밖 → R 3 이상 유지. B 20→45~58 로 고리면 개방.

- ✅✅ **지상 낮 하늘(파란 하늘)의 마스터 스위치 = `Planet(Earth).setIntensity(1)` (2026-07-06 녹화 해독 확정)**:
  reset 후 지구 intensity 가 꺼져 있으면 **대기(atmosphereIntensity)를 켜도 하늘이 검음** —
  행성 본체가 꺼지면 대기 렌더도 통째로 꺼짐. Studio UI '대기효과' 토글의 실체 =
  `setIntensity(1)` + `setAtmosphereIntensity(1)` 두 명령 세트 (사용자 토글 SPC 녹화 역해석).
  지상 씬 체크리스트: 지구 setIntensity(1) + setAtmosphereIntensity(1) + 태양 setIntensity(1) + 시각(UT!).
  ✅✅ **지상 낮밤 타임랩스 확정 예제 (사용자 확인 2026-07-06)**: scripts/study/cheongju_day_night_v3.py —
  아침→정오→석양→밤을 setDateTime+Anim(8초) 가속으로. 별은 상시 1.0 (낮엔 대기가 물리적으로 가림).

- **PlanetName(0~7)**: Mercury=0, Venus=1, Earth=2, Mars=3, Jupiter=4, Saturn=5, Uranus=6, Neptune=7
- ✅✅ **`setTerrainModel(Planet.TerrainModel)` = 표면 지도 데이터셋 교체 (2026-07-15 사용자 확인, mars_terrain.py)**:
  enum **20종(태양계 공용)**: BMNG_Ocean/Seasons/Summer/Winter(지구 블루마블), Magellan/MagellanBW(금성), Messenger(수성),
  Viking/MOC/CTX/CTXColorized/Themis(화성 탐사선), PlanetObserver/PlanetObserverDEM30, Topography/Geoid, BasicTerrain/DefaultTerrain, Sliced/DidSliced.
  화성에 걸면 탐사선별 지도로 표면 텍스처가 실제로 바뀜(동작 확정). 접근/줌 = 암석행성 레시피(FadeTo→읽은R×배율→B틸트 오블리크).
- 🎯🎯 **[운영 표준] 행성/천체를 '자세히·가까이' 보여줄 땐 그림자 OFF (2026-07-15 사용자 확정 규칙)**:
  FadeTo/클로즈업하면 낮/밤 경계(터미네이터)로 **절반이 어두워 지형·표면이 반쯤 안 보임** → **되도록 그림자를 끈다.**
  **기본 세트**: `obj.setShadowStrength(0.0, Anim)` + `obj.setShadowContrast(0.0, Anim)` + `obj.setPlanetShineStrength(1.0, Anim)`
  = 야간면까지 밝혀 표면 전체가 보임. **Planet·Satellite·DwarfPlanet 전부 이 3세터 보유(동일 이름).**
  → 지형/표면/디테일을 보여주는 모든 예제(화성·달·왜소행성 등)에서 접근 직후 기본으로 적용할 것.
  (예외: 위상·일식·월식처럼 '그림자 자체가 주제'인 장면에서만 켜둠.)
  ⚠️⚠️ **가스행성/얼음행성 위성계 쇼(목성·토성·천왕성 등)에도 이 규칙 적용 (2026-07-15 사용자 지적)**:
  본체를 클로즈업하면 터미네이터로 반쪽이 어두워 지저분함 → FadeTo 직후 위 3세터로 그림자 OFF 기본 적용.
  (천왕성서 안 껐다가 "내 말 지키는 거 맞냐" 지적받음 — 위상 장면 아니면 무조건 끈다.)
- ✅ **`setElevationScale`(고도 과장) = 화성에서도 동작, 단 '근접 줌'에서만 보임 (2026-07-15 사용자 확인)**:
  ⚠️ 멀리서(R≈2.6)는 기복이 작아 "티가 안 남" → **바짝 확대(R≈1.5)하면 산·협곡이 솟는 게 보임**(사용자 "확대하니까 티나네").
  조건: ① DEM 모델(Topography/Geoid/PlanetObserverDEM30 등 고도 데이터 有) ② 표면 근접 줌 ③ 비스듬한 뷰(B22)에서 1↔12+ A/B.
  (이미지 전용 모델 Viking/BMNG 엔 고도 데이터가 없어 무효 — DEM 모델 필수.)
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
- ✅✅✅ **태양계 '공전'(revolution) = `setRevolutionSpeedScale(배율)` + 시간흐름 (2026-07-15 사용자 확인, solar_system_revolution.py)**:
  자전(setRotationSpeedScale)과 쌍. 공전량 = 배율 × 날짜Δ(일). `resetRevolutionSpeedScale()` 로 원복.
  ✅ **태양계를 '위에서' 조망 = 태양 Ecliptic 포트 + R(단위=AU!) + B=90** (FreeFlySun 방식):
  `sp = sun.portId(IndividualStar.IndividualStarPort.Ecliptic)` → `cam.setPositionLBR(Vec(0, 90, 18), Anim, sp)` (R=18AU면
  수성~천왕성 궤도, 해왕성 30AU는 밖). 각 행성 `setOrbitIntensity`(궤도 동심원)+`setLabelIntensity`(점 추적).
  배율 걸고 `setDateTime(+수년, Anim)` → 안쪽(수성) 빨리·바깥(목성) 느리게 = 케플러 차등이 눈에 보임(확정).
  ⚠️ 자전과 동일 순서: dm.stop() → 배율 → 날짜 흐름(누적분 ×배율 '확 돎' 방지). 태양 프레임=우주라 지상 '자전 광란' 없음.
- ✅✅ **암석 행성(지구·화성) GoTo/FadeTo 도킹 = 북극 상공 {L, 89.999, R=4}** / **가스 행성(목성·토성) = 옆 {L, 20, R=5}** (Recording19 + 실측 확정).
  → 지형 있는 암석행성은 '착륙 접근' 자세(북극 위)라 **카메라 L 공전이 극축 제자리 스핀 = 불가**. 자전은 위 관성+setRotationSpeedScale 방식으로.
  가스행성은 옆 도킹이라 `setPositionLBR(Vec(L+각, 20, R), Anim, -1)` L 스윕 = 카메라가 옆에서 한 바퀴(정상 공전, 목성/토성 확정).
- ⚠️⚠️ **GoTo 지구(홈 행성) = 지표면 R=0 으로 '집에 가기'** (밖으로 안 나감, 스샷 R:0m 확정). 지구를 **외부에서** 보려면
  `SceneGraph().reset(1)`(관측자 바인딩 해제) → `DataManager...data(PlanetType,"Earth").action(FadeTo).trigger()` (R=4 외부 도킹).
- ✅ **미연습 코드 확정(earth_rotation_sim)**: `setRotationSpeedScale`/`resetRotationSpeedScale`(자전배율) ·
  `setNightLightsIntensity`(밤면 도시광=호박색, 실제 나트륨등 색) · `setTerrainIntensity`/`setCloudsIntensity` ·
  `setEquatorialPoleAxisIntensity`/`setEquatorialPolePointerIntensity`(자전축 시각화, 청록 세로선).
  SPC(Recording19): 자전배율 cmd **1029**, reset **1045**, terrain **1063**, clouds **1064**, nightLights **1057**, 자전축 **1097**(레이어7=축/8=포인터).
- ✅✅✅ **'밤의 지구 — 도시의 불빛' 완성 확정 (2026-07-16 사용자 확인, earth_city_lights.py v3 + Recording39)**:
  안 쓴 Planet 렌더 3종 주역: **`setNightLightsIntensity(1)`=밤면 호박색 도시광**(하이라이트, 사용자 "도시광 잘 보임") +
  `setCloudsIntensity(1)`=구름 + `setTerrainModel(Planet.TerrainModel.BMNG_Ocean)`=블루마블 지표.
  ⚠️⚠️ **이 쇼는 '그림자 ON' 이 맞음(운영 그림자OFF 규칙의 예외 — 위상·일식류)**: 밤면을 만들어야 도시광이 보임 →
  `setShadowStrength(1)`+`setShadowContrast(1)`+`setPlanetShineStrength(0.05)`(밤면 어둡게 → 도시광 도드라짐).
  ✅✅ **'낮면이 안 보임' 함정 + 정답 = 위상 스윕 (2026-07-16 사용자 실측)**: FadeTo Earth 도킹 각도가 하필
  **밤면(태양 반대=신월 위상)**이면 도시광 말고 다 어두움(낮면=구름·바다·블루마블·대기 림이 반대편). ⚠️ 카메라 L 공전은
  암석행성이라 불안정 → **정답: 관성 프레임(EquatorialJ2000) 전환 + `setRotationSpeedScale(0)`(자전 정지) + `setDateTime` 로
  날짜만 흘림** → 태양 각도가 반구를 쓸어 **밤→터미네이터(도시 켜짐)→낮**으로 위상이 바뀜. 자전 정지라 표면이 안 어지럽고
  태양각만 변함. **최고 구도 = ~3개월 지점(터미네이터)에서 홀드** = 한 화면에 낮면(구름·바다) + 밤면(도시광). 끝은 resetRotationSpeedScale.
  SPC(Recording39, family Earth=301989891): setTerrainIntensity **1063**/setCloudsIntensity **1064**/setNightLightsIntensity **1057**/
  setPlanetShineStrength **1140**(=0.05)/setShadowStrength **1040**/setShadowContrast **1041**/setTerrainModel **1184**(BMNG=7)/setRotationSpeedScale **1029**(=0)/reset **1045**/setDateTime **257**.
- ✅✅ **별자리 '경계선' = `Constellation.setLimitsIntensity` (2026-07-16 발견, constellation_boundaries.py v4)**:
  ⚠️⚠️ **RSA Cosmos(프랑스 SDK)는 별자리 경계를 'limits(limites)'라 부름** → bound/border/frontier 키워드 프로브에 안 걸려
  한참 헤맴(v1~v3). **Constellation 전체 메서드 덤프**로 발견: `setLimitsIntensity(강도, Anim)`. 별자리마다 호출 = 그 별자리 경계 다각형.
  · Constellation set* 전체(7개): setLinesIntensity/setArtIntensity/setLabelIntensity/**setLimitsIntensity**/setLinesGap/setArtHybridRatio/setArtUseHybridRatio.
  · ❌ DB `Action.Type.BoundaryOn` 은 트리거돼도 렌더 안 됨(쓰지 말 것). ❌ Planet 엔 경계 세터 없음.
  · ✅ 신화그림 art = 겨울 16개 별자리 대부분 에셋 있어 다 뜸(사용자 확인). **교훈: 세터 못 찾으면 dir(obj) 전체 덤프로 — 이름이 영어 예상과 다를 수 있음(French SDK).**
  · SPC(Recording40, Constellation family 167772xxx): setLinesIntensity **1537** / setArtIntensity **1545** / **setLimitsIntensity 1541**(경계선). Stars setPointSaturation **515**/setContrast **514**.
- ✅✅ **Planet(지구) 미사용 렌더러블 발굴 (2026-07-16 dir 프로브, earth setXxxIntensity 전수)** — 다음 예제 후보 광맥:
  **`setAuroraIntensity`(오로라!)** · `setRainbowIntensity`(무지개) · `setMagnetosphereIntensity`(자기권) · `setWaterSpecularIntensity`(바다 윤슬) ·
  `setAtmosphereHaloIntensity` · `setEclipticBandIntensity`(황도대 띠) · `setPolarCircleIntensity` · `setEquatorialSyncTropicsIntensity`/`setEquatorialSyncPolarCirclesIntensity`(회귀선/극권) ·
  `setRockyCliffIntensity` · `setTreeIntensity` · `setMagnetosphereIntensity` · `setEquatorialSyncMagneticPolesIntensity`. (일식류 setAntumbra/Penumbra/UmbraArea·Line, ShadowCone 계열도 있음.)
- ✅✅✅ **오로라(북극광) 완성 확정 (2026-07-16 사용자 확인, aurora.py + Recording41)**: `Planet(Earth).setAuroraIntensity(강도, Anim)` =
  북쪽 하늘에 **초록 오로라 커튼** 렌더(사용자 "색깔은 초록색"). 세기를 0.4↔1.0 출렁이면 커튼이 밝아졌다 옅어졌다 '춤춤'.
  ⚠️ **오로라 세터는 intensity 하나뿐**(dir 프로브 — 색/고도/속도 세터 없음). 색은 기본 초록 고정(고고도 빨강·질소 보라는 렌더에 따라).
  ⚠️ **청주(위도 36)는 오로라 벨트 밖** → 이 쇼는 관측지를 고위도로: `Place2D.setPosition(Vec(69.65, 18.96, 100))`(트롬쇠, 노르웨이).
  1월 극야라 종일 어둠 = 언제든 밤하늘. 대기 OFF + 지면 OFF + 북쪽(H180)/TH40. SPC(Recording41, family Earth 301989891):
  setAuroraIntensity **1051** / setMagnetosphereIntensity **1048**(보조, 효과 미미). Stars setPointSaturation 515/setContrast 514.
- ⚠️ **무지개 `setRainbowIntensity` = 렌더는 되나 '원래 흐릿'함 (2026-07-16 실측, rainbow.py)**: 대낮(대기 ON) 태양 반대편(대일점)에
  옅은 아치가 뜸(사용자 "잘 모르겠다"). **노브는 setRainbowIntensity 하나뿐**(전체 덤프 — 색/굵기/선명도 세터 없음, 이미 최대).
  ⚠️ 해를 너무 낮추면(황혼) 노을에 오히려 묻힘 → 밝은 낮 하늘(태양 고도 ~20°)이 그나마 나음. 카메라는 '태양 반대 방위'(H=180-태양방위) 조준.
  → 쇼용으로는 임팩트 약함(SDK 한계). 대기광학은 이 정도가 끝. (setAtmosphereHaloIntensity=태양 주변 무리도 있으나 미검증.)
  ✅ **해 낮춘 v2 는 사용자 "좀 잘되네" 인정** — 아치가 더 높이 솟음. SPC(Recording42): setRainbowIntensity **1147**(family Earth 301989891).
- ✅✅✅ **'살아있는 지구 — 구름과 날씨' 완성 (2026-07-16 사용자 확인, clouds_weather.py v3 + Recording43)**: 안 쓴 구름 상세 클러스터.
  ⚠️⚠️ **하이라이트 = `setCloudModel` A/B (사용자 "모델 달라질 때 확 달라진다")**: CloudModel enum 값 = **DefaultCloud=0 / Volumetric=54(입체!) / VolumetricLowRes=55** /
  BasicCloud/SlicedCloud/RawCloud/DidSlicedCloud/CassiniJuno. 기본(평면)↔Volumetric(입체) 전환이 눈에 확 띔.
  ⚠️ **`setCloudCoverage` 는 화면 변화 미미(사용자 "밀려오는 건 잘 모르겠다")** — 토성 고리·pointSaturation 같은 '약한 노브' 부류.
  → **'구름이 밀려온다'는 setCloudCoverage 말고 `setCloudsIntensity` 0→1 페이드인으로** (이게 구름 렌더 마스터라 없음→가득 확실히 보임).
  레시피: FadeTo Earth → 그림자 OFF(전체 밝게=구름 다 보임) → **줌인(R4→2, 지구 크게=변화 보임)** → intensity 0→1 페이드인 →
  모델 A/B(기본→Volumetric) → setCloudSpeed↑ + 시간가속(+14일) 구름 이동. SPC(Recording43, family Earth 301989891):
  setCloudsIntensity **1064** / setCloudCoverage **1141** / setCloudModel **1185**(Volumetric=54) / setCloudThickness **1181** / setCloudAltitude **1180** / setCloudSpeed **1167** / setCloudRaininess(미도달). 줌인 setPositionLBR **273**.
- ✅✅ **지구 '위도선 레이어' 렌더 확정 (2026-07-16 사용자 "그리드 다 보인다", climate_zones.py)**: FadeTo Earth(EquatorialSync 프레임)에서
  지구본 표면에 그려지는 지리 라인 레이어 — `setEquatorialSyncTropicsIntensity`(남·북 회귀선 ±23.4°) · `setEquatorialSyncPolarCirclesIntensity`(남·북 극권 ±66.5°) ·
  `setEquatorialSyncGraticuleIntensity`(위경도 격자) 전부 렌더됨. (`setEquatorialGridIntensity`=적도면도 병행 가능.) 기후대/자전축 교육쇼용.
  ⚠️ FadeTo 도킹 R=4(지구반지름)이면 지구가 작아 링이 흐림 → **줌인 R≈1.8(setPositionLBR로 R×0.45) + 오블리크 B22** 로 링이 또렷.
  SPC(Recording44, family Earth 301989891): **EquatorialSync 라인 = cmd 1187**(graticule=레이어6 / tropics=레이어12 / polarCircles=레이어11) ·
  자전축/적도 = cmd **1097**(equatorialGrid=레이어2 / polePointer=레이어8). 즉 1187/1097 이 각각 '레이어 인덱스'로 여러 선을 관리.
- ✅✅✅ **목성 클로즈업 자전 완성 (2026-07-16 사용자 "배경별 고정, 자전돼", jupiter_grs.py v2)**: 가스행성 FadeTo(옆 도킹 R=5,B20) →
  줌인(R×0.6) → 그림자 OFF → **관성 프레임(EquatorialJ2000) + setRotationSpeedScale + 시간가속** = 줄무늬·대적점이 자전으로 흐름.
  ✅ 줄무늬(벨트/존)·**대적점(GRS) 목성 텍스처에 렌더됨**(사용자 확인). ✅ `setCloudModel(Planet.CloudModel.CassiniJuno)` = 가스행성 구름 룩(✓ 동작).
  ⚠️⚠️ **자전 연출의 핵심 함정 재확인 = 날짜Δ 최소 (안 지키면 '배경별 미친 회전')**: reset 은 날짜를 '오늘'로 맞춤 →
  setDateTime 목표를 과거/미래로 크게 넣으면(예 -29일) 그 날짜치 하늘이 통째로 돌아 별이 미쳐 돎(자전 묻힘). **정답: 시작 날짜를
  '오늘 근처'로 instant 고정 후 배율↑(6) + Δ 최소(+6h)** → 목성 ~3.6바퀴 도는데 별은 6h치라 거의 고정. (배율 6 × 6h / 9.9h주기 ≈ 3.6.)
- ⚠️ **바다 윤슬 `setWaterSpecularIntensity` = 우주 뷰에선 안 보임 (2026-07-16 실측, ocean_glint.py, 사용자 "잘 모르겠다")**:
  세터(setWaterSpecularIntensity/setWaterSpecularShininess)는 존재·호출 성공하나 FadeTo 지구 원반에선 윤슬(sun glint)이 화면에 안 뜸.
  ⚠️ `SeaLevelRenderingMode` enum 이 `Planet.*` 에 없어(위치 불명) 반사 모드 게이팅도 못 함(setSeaLevelRenderingMode 세터만 있음).
  → 무지개류(SDK 은근/미노출). **근접 지표(Terrain View) 전용 효과 추정** — 우주 원반선 미지원. 쇼용 부적합, 붙잡지 말 것.
- ⚠️⚠️ **`setLightPollutionIntensity` 는 별/은하수를 안 지움 (2026-07-09 사용자 실측)**: 이 명령은 지구
  **대기 스카이글로(하늘 배경광)**만 건드림 — `Stars`/`Galaxy` 는 독립 레이어라 광공해값을 올려도 별·은하수가
  그대로 보임. **빛공해 쇼에서 '별이 사라지는' 효과 = Stars/Galaxy intensity 를 단계에 맞춰 직접 감광**
  (setLightPollutionIntensity 는 대기 글로우용으로 병행). ✅ 확정 예제(사용자 밝기 확정, Recording13):
  scripts/study/light_pollution.py — 교외 lp0.3/stars0.80/mw0.35 → 도시외곽 lp0.6/0.60/0.10 →
  대도시 lp1.0/0.40/0.0, 복귀 1.0/0.8. (별을 너무 죽이면 과함 — 대도시도 stars 0.4 유지가 보기 좋음.)

## Satellite — 달·위성 ✅ 실측(2026-07-06, scripts/study/moon_phase_show_v2/v3.py)
- 생성: `Satellite(Satellite.SatelliteName.Moon)` / FadeTo 는 **`Data.Type.SatelliteType` + "Moon" 확정**.
- ✅✅✅ **가스행성 '위성계' 쇼 확정 (2026-07-15 사용자 확인 — jupiter_moons + saturn_system)**:
  갈릴레이 위성(Io/Europa/Ganymede/Callisto)·토성 위성(Mimas/Enceladus/Tethys/Dione/Rhea/Titan/Iapetus) **전부 SatelliteName enum 존재**.
  레시피: 지상 인트로 → reset+**FadeTo 가스행성**(옆 도킹 R=5,B20) → **풀백**(`setPositionLBR(Vec(L,B,R×배율),Anim,-1)`,
  토성은 B 20→38 로 고리면 개방) → **관성 프레임 전환**(EquatorialJ2000, 목성/토성 자전율로 하늘 통째 도는 것 방지) →
  각 위성 `setIntensity`/`setOrbitIntensity`/`setLabelIntensity`/`setScale(6~8)` → **시간가속(+8~14일)** = 위성 공전(케플러 차등:
  안쪽 빠름/바깥 느림). 라벨은 한글로 표출(미마스·타이탄 등). ⚠️ 토성 풀백 R=28 이면 타이탄(궤도 ~20 토성반지름)까지 담김,
  이아페투스(59)는 밖. SPC(Recording31): 위성 setIntensity **1282**/setOrbitIntensity **1286**/setLabelIntensity **1302**/setScale **1283**(family 0x15).
  ✅✅✅ **SatelliteName enum '전체' 확정 (2026-07-16 덤프, satellite_enum_dump.py) — 실제 위성 25개 (추측 금지, 이 목록이 진실)**:
  · 지구=**Moon**(0) · 화성=**Phobos**(1)/**Deimos**(2) (✅ mars_moons.py 확인 — 포보스 7.6h가 데이모스보다 훨씬 빨리 돎, 유일 암석행성 위성계) · 목성=**Io**(3)/**Europa**(4)/**Ganymede**(5)/**Callisto**(6) (갈릴레이 4개만)
  · 토성=**Mimas**(7)/**Enceladus**(8)/**Tethys**(9)/**Dione**(10)/**Rhea**(11)/**Titan**(12)/**Hyperion**(13)/**Iapetus**(14)/**Atlas**(15)/**Pan**(16) (10개!)
  · 천왕성=**Miranda**(17)/**Ariel**(18)/**Umbriel**(19)/**Titania**(20)/**Oberon**(21) (5개)
  · 해왕성=**Triton**(22) (**딱 하나** — Nereid/Proteus 등 전부 없음, 검증 완료)
  · 명왕성=**Charon**(23)/**Nix**(24)/**Hydra**(25) (3개! — 카론은 명왕성 대비 거대 = 쌍행성)
  (index -1=InvalidSatellite, 26=SatelliteCount.) ⚠️ **외행성일수록 위성 빈약(해왕성=1)**, 반면 **명왕성은 3개** 있음.
  ⚠️ 내 saturn_system 은 7개만 썼음 → **Hyperion/Atlas/Pan 3개 더 있음**(원하면 보강). 목성은 4개가 전부(Amalthea 등 없음).
- **위상 수동 제어 (실측 동작)**: `setManualMoonPhase(True)` → `setMoonAge(age, Anim)` (0~29.5)
  → `setMoonAge(0→29.5, Anim(15))` 한 번 호출로 위상 타임랩스(신월→보름→그믐).
- ⚠️ **쇼 끝에 `setManualMoonPhase(False)` 로 자동 복귀시키지 말 것 (실측 리포트)**:
  수동 위상과 실제 날짜 위상이 싸우며 **그림자가 생겼다/없어졌다 깜빡임** → 수동 유지 권장(다음 쇼는 reset).
- **그림자(위상 명암) 강도 = `setPlanetShineStrength(s, Anim)`** — 지구조(지구 반사광이 그늘면을 비춤).
  **0.0 = 그늘 칠흑(그림자 최강)**, 1.0 = 기본. 실측 확인.
- **SatellitePort**: Equatorial/EquatorialJ2000/EquatorialSynchronous/Galactic/NoonEcliptic/NoonEquatorial/OrbitalMeanEquinox.
- ✅✅ **달 표면 = `setTerrainModel(Satellite.TerrainModel)` 탐사선 지도 (2026-07-15 사용자 확인, moon_terrain.py)**:
  enum **13종**: Basic/DefaultTerrain/RAW/Sliced/DidSliced/Topography + 탐사선 **Clementine·LROC·Galileo·Voyager·Cassini·CassiniBW·NewHorizons**.
  FadeTo Moon(북극 R=4 도킹, 행성과 동일) → 그림자 OFF(운영표준) → 중앙 고정 줌 → 지도 교체. `setElevationScale`(1309)로 크레이터 기복(근접).
  ⚠️ **Satellite 엔 `setTerrainIntensity` 없음**(Planet 전용) — setTerrainModel 로 바로 교체. 그림자 세터 cmd: setShadowStrength 1292/setShadowContrast 1291/setPlanetShineStrength 1328.
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
- ✅✅ **별하늘 렌더링 노브 확정 (2026-07-15 사용자 확인, stars_rendering.py)** — 전천이 확 바뀌어 차이 뚜렷:
  · `setExposure(v, Anim)` = 전체 밝기/블룸 (**기본 5.68** 실측, ↑ 밝고 별 부풀음/↓ 밝은 별만). 효과 큼.
  · `setContrast(v, Anim)` = 희미한 별 컷오프 (**기본 1.6**, ↓ 촘촘/↑ 밝은 별만 깨끗). 효과 큼.
  · `setPointSaturation(v, Anim)` = 별 색 채도 (**기본 1.0**, 0=흑백/↑=청백·주황). ⚠️ 별이 대부분 흰색이라
    ×2 로는 은근함 — **0↔4.5 크게 스윕 + 흑백/컬러 A/B** 해야 체감(사용자 "×2.2 는 애매").
  · `setModelset(Stars.Modelset)` = 렌더링 모델셋. **enum = GaiaDR2 / Hipparcos** (2종, Anim 없는 enum).
  · 원본값은 `stars.exposure/contrast/pointSaturation` 로 읽어 복귀(하드코딩 금지 — 기본이 1.0 아님, 노출 5.68!).
- 기타 미연습: setModelset 세부 차이(GaiaDR2 vs Hipparcos 별 목록 차이) 등.

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
- ✅✅ **페르세우스 유성우 완성쇼 확정 (2026-07-16 사용자 확인, meteor_shower.py)**: 지상 밤(청주 8/13 새벽 2시=17 UTC, 대기 OFF+은하수) +
  페르세우스자리(Per) 선 + **`setReferential(RaDec)` + `setRainGradientPoint(Vec2(적경47, 적위58))`** = 복사점을 진짜 페르세우스에 하늘 고정 →
  유성이 그 한 점에서 방사. `setRepresentationType(Model.Gradient)`+`setBrightness`+`setTrailLength`. ZHR 1200→3000(폭풍)→1000 로 연출, `setRainSeed(1/0)` 재생/정지.
  enum 자동탐색: `ShootingStar.Referential.RaDec` / `ShootingStar.Model.Gradient` 존재 확인. 북동 조준(H135/TH22).
  SPC(Recording36, family 117440513): setRepresentationType **2561**/setReferential **2574**/setRainGradientPoint **2569**/setRainChaosGradientPoint **2570**/
  setRainSpeed **2571**/setBrightness **2565**/setTrailLength **2567**/setZenithalHourlyRate **2573**(★값=ZHR/60 확인: 1200→20)/setRainSeed **2566**.

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
- ✅ **`setExposure(v, Anim)` = 은하수 노출/블룸 (2026-07-15 사용자 확인, milky_way.py)**: 기본 1.0, ↑ 밝고 성간구름까지 부풀음.
  cmd **2073**. 어두운 시골 밤(대기 OFF, 고도↑)+`Stars.setExposure`↑/`setPointSaturation`↑ 조합 = 풍성한 은하수. 노출 0.5↔2.2 A/B 대비 뚜렷.

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
- ⚠️⚠️ **enum 은 3,189개지만 '고유이름(proper name)'이 붙은 별은 일부뿐 (2026-07-16 실측)**: 있는 것 = Vega/Deneb/Altair/Sirius/
  Rigel/Betelgeuse/Bellatrix/Aldebaran/Capella/Arcturus/Procyon/Pollux/Castor/Regulus/Spica/Antares/Dubhe/Merak/Polaris/Fomalhaut 등.
  ⚠️ **없는 흔한 이름**(실측): **Mizar / Kochab / Hamal** 등 → 대부분 바이어기호 등 다른 표기로 들어간 듯. **잘 알려진 이름만 써야 안전**(없으면 hasattr 로 걸러짐).
- ✅✅ **'별의 색=온도' 쇼 확정 (2026-07-15 사용자 인정, star_colors.py)**: 지상 밤(청주 21시=12 UTC, 대기 OFF 검은 하늘) +
  오리온 → **개별 별 지목 = `setPointerIntensity(1)`(별은 기본 포인터 있어 바로 뜸) + `setLabelIntensity(1)`(이름표)** +
  `Stars.setPointSaturation(4.2)`(색 채도 확 ↑ = 리겔 청백/베텔게우스 붉음 대비 선명). 이름별 별자리 선도 같이:
  시리우스=`Constellation(CMa)`, 알데바란=`Constellation(Tau)`, 리겔·베텔게우스=`Ori`. IndividualStarName 에 Rigel/Betelgeuse/Bellatrix/Sirius/Aldebaran 존재.
  SPC(Recording33): 별 setPointerIntensity **805**/setLabelIntensity **791**, Constellation setLinesIntensity **1537**, Stars setPointSaturation **515**.
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

- ✅✅ **황도광 `setZodiacalLightIntensity` / `setZodiacalLightScatteringIntensity` = 동작 확정 (2026-07-15 사용자 확인, zodiacal_light.py)**:
  태양(IndividualStar) 세터. 해 진 뒤 **서쪽 지평선에서 황도를 따라 솟는 뿌연 빛 글로우** 표출(가짜 새벽/황혼).
  레시피: 봄 저녁 황혼(황도 서쪽 가파름) + `Earth.setAtmosphereIntensity(0)` 어두운 하늘 + 서쪽 저각(H=-90, TH15)
  + 황도광 ON. `Earth.setEclipticGridIntensity` 로 '빛이 황도를 따라감' 시각화. 세기 0↔1 A/B 로 대비 뚜렷.

## Constellation — `Constellation(Constellation.ConstellationName.Ori)`
- **Name(IAU 3자 약어)**: Ori, UMa, Sco, Crux, Leo, Tau, Cyg, Aql, Vir, Gem …
- `setLinesIntensity`, `setLabelIntensity`, `setArtIntensity` (각 intensity, Anim)
- ✅✅✅ **성군(Asterism) 프리셋 내장 = 별을 잇는 큰 도형을 한 줄로 그림 (2026-07-16 사용자 확인, summer_triangle.py + Recording34)**:
  ConstellationName enum 에 IAU 88개 뒤로 **`ASTERISM_*`** 멤버가 있음(Constellation 객체라 `setLinesIntensity` 로 그려짐):
  **`ASTERISM_STr`=여름 대삼각형(Vega·Deneb·Altair)** · `ASTERISM_WTr`=겨울삼각형 · `ASTERISM_WHx`=겨울육각형 ·
  `ASTERISM_GSP`=페가수스 대사각형 · `ASTERISM_BDr`=북두칠성 · `ASTERISM_NCr`=북십자 · `ASTERISM_SpT`=봄삼각형 ·
  기타 GDi/WAs/KSt/Bfl/Kit/Sal/SSR/CoH 등. → **여름 대삼각형 등 '별 잇는 선'은 직접 계산 말고 이 프리셋을 쓸 것.**
  `Constellation(Constellation.ConstellationName.ASTERISM_STr).setLinesIntensity(1.0, Anim(...))`.
- ✅✅ **임의의 두 천체 잇는 커스텀 선 = `Line` 클래스 (2026-07-16 실측, line_probe.py / bukdu_polaris.py)**:
  `Line(Line.LineName.Line001)` → `setStartPoint(body.id)` + `setEndPoint(body.id)`(별 `.id`/`.osgId` 넘김) + `setIntensity`.
  `setLineColor(Vec3)`/`setLineThickness`/`setLabel`/`setLabelIntensity`. 눈금(칸) = `setGraduationSize` + `setAdvancement`(배수)·`setAdvancementDivisor`(등분).
  ✅✅ **큰곰자리→북극성 지시선 레시피 (사용자 스샷 확인)** — 두 방식:
  · **연장 방식**: 시작=Merak, 끝=Dubhe(국자 1칸), `setAdvancement(7.0)` → 눈금이 국자 간격마다 = 북극성까지 ~6칸. 단 '연장 배수'라 정확히 북극성에 안 닿고 근처(별 정렬 어긋남).
  · **✅✅ 직결 방식(권장, 사용자 제안 + 실측 확정)**: 시작=Dubhe, **끝=Polaris(실제 body)** → 선이 **북극성에 정확히** 끝남.
    ⚠️⚠️ **`setAdvancementDivisor(N)` + `setAdvancement(N)` 를 '같은 값'으로**: divisor=N → 눈금 단위 = (시작-끝 거리)/N,
    advancement=N → N단위(=전체) 그림 → **정확히 N칸으로 끝점까지**. (divisor 만 주면 advancement 기본 1 = 1/N 길이만 = '1칸' 버그.)
    `setGraduationSize(4)` 로 눈금 표시. → 끝점을 목표 별로 지정 = '배수 추정'보다 정확. (예: 5칸 = divisor5+adv5.)
    ✅ **사용자 확인 완료 (Recording35)**. SPC(Line family 536870913): setStartPoint **8985**/setEndPoint **8986**/setAdvancementDivisor **8983**/
    setAdvancement **8965**/setGraduationSize **8971**/setLineColor **8962**/setLineThickness **8963**/setIntensity **8961**.
  ⚠️⚠️⚠️ **`setLineMode` 는 Python 에서 호출 불가 (2026-07-16 실측 확정)**: LineMode enum(Line2D/Line3D)이 어디에도 미노출
  (`Line.LineMode`·global `LineMode` 둘 다 AttributeError), `ln.lineMode` **읽기조차 "No to_python converter for enum LineMode"** →
  값을 만들 수도 읽을 수도 없음. **다행히 기본 모드가 각거리처럼 동작해 북극성 방향에 정렬됨(실측)** → 2D 강제 불필요, advancement 로 거리만 맞추면 됨.
  (2D/3D 명시 전환이 꼭 필요하면 SPC 오퍼레이터 경유. 스크립트에선 기본 모드로 충분.)
- ✅✅ **setArtIntensity(별자리 신화 그림) 대성공 확정 (2026-07-15 사용자 스샷 확인, constellation_art.py)**:
  별을 잇는 선 위에 **신화 형상(백조·거문고·왕관·헤르쿨레스·물병·독수리·뱀주인·페가수스·궁수·전갈…)이 선-드로잉 아트로**,
  **별자리마다 다른 색**으로 표출. 0.85 페이드인 OK. 여러 별자리 동시 ON → '신화로 가득한 밤하늘' 타블로.
  레시피: 검은 하늘(대기 OFF)+`setLinesIntensity`+`setArtIntensity`, 마지막에 선만 끄면 그림만 남음(감상).
  ✅ **Constellation `setLabelIntensity`(이름표) = 동작 확정 (렌더됨) — 단 화려한 art 위에선 '가려짐' (2026-07-15 사용자 확인)**:
  라벨은 정상 표출되나 별자리 그림(art)과 겹치면 묻혀서 안 보임 → **라벨을 보여줄 땐 art 를 낮추거나(0.2)**
  선/라벨만 켜는 장면으로 분리. (렌더 미지원 아님 — v1 은 art 0.85 에 묻혔던 것.) 지평선 아래 별자리는 안 뜸(정상).
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

## Clock — `Clock(Clock.ClockName.Clock001)` ✅✅ 돔 시계 HUD 완성 (2026-07-20 사용자 "잘되네", clock_hud.py + Recording45)
- ✅ **스위스 철도시계 스타일 아날로그 시계(문자판+시/분/초침)가 화면에 렌더됨** — 은하수 밤하늘 위 중앙 하단에 또렷(사용자 스샷 확인).
- **렌더 열쇠 = `setModelset(Clock.Modelset.SystemClock001)`** (Bolide 의 setModel 처럼 모델 없으면 안 그려질 수 있음. Modelset enum = InvalidModelset/**SystemClock001**).
- **붙이기 = `cam.addChild(clk.id, Camera.CameraPort.FixedForeground)`** (InsertText 패턴 그대로 동작). 그 뒤 `setPosition(Vec(az,h,roll))`+`setSize`+`setDistance`+`setIntensity`.
  · 실측 좋은 값: `setPosition(Vec(0,40,0))`(중앙 하단) + `setSize(0.5)` + `setDistance(1.0)`. ClockName = Clock001~011.
- **색 커스터마이즈(전부 Vec3, 동작 확정)**: `setBackgroundColor`(문자판)·`setForegroundColor`(눈금)·`setHoursHandColor`·`setMinutesHandColor`·`setSecondsHandColor` + `setDisplaySecondsHand(bool)` + `setTimezoneName("Asia/Seoul")`.
- ✅ **시뮬레이션 시각 반영** — `DateManager.setDateTime(+24h, Anim)` 시간가속 시 바늘이 하루치 돎(초침 빨강으로 두면 회전 잘 보임). 배경 하늘도 같이 회전.
- 텍스처 세터도 있음(미검증): setBackgroundTexture/setForegroundTexture/setHours·Minutes·SecondsHandTexture (user 폴더 상대경로) — 커스텀 문자판/바늘 이미지.
- SPC(Recording45, family **0x2B**=721420289): addChild **4881** / setModelset **12305** / setPosition **12290** / setSize **12301** / setDistance **12303** /
  setBackgroundColor **12296** / setForegroundColor **12297** / setHoursHandColor **12298** / setMinutesHandColor **12299** / setSecondsHandColor **12300** /
  setDisplaySecondsHand **12304** / setTimezoneName **12302** / setIntensity **12289**.

## OrbitalPlace — `OrbitalPlace(OrbitalPlace.OrbitalPlaceName.OrbitalPlace001)` ✅✅ 인공위성 궤도 완성 (2026-07-20 사용자 스샷 확인, orbital_satellites.py)
- ✅ **지구 둘레 위성 궤도가 렌더됨** — Asteroid 와 같은 궤도 개체지만 '지구 위성용'(TLE 스타일 세터 보유). 슬롯 OrbitalPlace001~007.
- **위성 TLE 세터(단위 명확 → AU/km 모호성 회피)**: `setMeanMotion`(revs/day) + `setEccentricity`/`setInclination`/`setAscendingNodeLongitude`/`setArgumentOfPeriapsis`(또는 setPeriapsisLongitude)/`setMeanAnomaly` + `setEpochYears`/`setEpochDays`/`setBstar`. (setSemiMajorAxis 도 있으나 mean motion 이 스케일 자동 결정 = 안전.)
- **부모 = 지구**: `op.setParent(earth.portId(Planet.PlanetPort.EquatorialJ2000))`. 표시 = `setOrbitColor`(Vec3)/`setOrbitThickness`/`setOrbitIntensity` + `setIntensity`.
- ✅✅ **레시피 (확정)**: reset → **FadeTo 지구(외부)** → 풀백 `cam.setPositionLBR(Vec(L, 35, 12), Anim, -1)`(R=12 지구반지름=HUD 76538km, B35 오블리크) + `setTargetHeight(30)` → 위성들 TLE 요소 + 시간가속(setDateTime +1일) = 고도별 공전속도 차(케플러). 몰니야(e=0.74)는 찌그러진 타원으로 정확히 렌더.
- ⚠️ **LEO(ISS/허블 MM≈15.5 = 고도 1.06 지구반지름)는 지구 표면에 붙어 R=12 줌에선 지구에 묻힘** → 잘 보이는 건 GPS(MM2)/GEO(MM1)/몰니야. LEO 강조하려면 근접 줌(R↓).
- Port: TerrestrialEquatorialJ2000/EclipticJ2000/OribitalMeanEquinox(오타)/Synchronous/Galactic.
- SPC(Recording48, family **0x25**=620756992): setMeanMotion **11022**/setEccentricity **11009**/setInclination **11012**/setAscendingNodeLongitude **11013**/setArgumentOfPeriapsis **11010**/setMeanAnomaly **11011**/setEpochYears **11019**/setBstar **11024** · setOrbitColor **11027**/setOrbitThickness **11029**/setOrbitIntensity **11026**. 부모연결=addChild **4881**. 카메라 setPositionLBR **273**/setTargetHeight **307**.

## Asteroid — `Asteroid(Asteroid.AsteroidName.Asteroid001)` ✅✅ 소행성대(궤도요소로 직접 그림) 완성 (2026-07-20 사용자 확인, asteroid_belt.py + Recording47)
- ✅ **Comet 판박이** — 궤도 6요소로 소행성 궤도(타원)와 본체를 직접 그림. AsteroidName = Asteroid001~ 슬롯(수백 개).
- **궤도요소 세터**(전부 (val, Anim)): `setSemiMajorAxis`(AU) · `setEccentricity` · `setInclination`(°) · `setLongitudeOfAscendingNode`(°) · `setArgumentOfPeriapsis`(°) · `setMeanAnomaly`(°) · `setEpoch`(JD). ⚠️ 요소 넣고 `sleep(0.3)` 프레임 대기(Comet 함정 동일).
- **표시**: `setOrbitIntensity`/`setOrbitColor`(Vec3)/`setOrbitThickness` · `setIntensity`(본체) · `setLabelIntensity` · `setLabelNameOverride`(str) · `setPointerType`/`setPointerIntensity`. 본체 3D 모델 = `setTerrainUserModelFilename`(커스텀, 없으면 기본 점).
- ✅✅ **소행성대 조망 레시피 (확정)**: 태양계 '위에서' — `sp=sun.portId(IndividualStar.IndividualStarPort.Ecliptic)` → `cam.setPositionLBR(Vec(0,90,6), Anim, sp)`(R=6AU=화성~목성 담김) + **`cam.setTargetHeight(30)` 필수**(안 잡으면 띠가 구석/아래로 밀려 "잘 안보임", 사용자 지적). 참조로 Mars/Jupiter `setOrbitIntensity`. 실제 소행성 8개(Ceres/Vesta/Pallas/Juno/Hygiea/Eros/Flora/Eunomia) 궤도요소 + 시간가속(setDateTime +6년) = 케플러 차등 공전.
- **AsteroidPort**: TerrestrialEquatorialJ2000/EclipticJ2000/OribitalMeanEquinox(오타 주의)/Synchronous/Galactic.
- SPC(Recording47, family **0x14**=335544320): setSemiMajorAxis **6410**/setEccentricity **6408**/setInclination **6407**/setLongitudeOfAscendingNode **6406**/setArgumentOfPeriapsis **6409**/setMeanAnomaly **6412**/setLabelNameOverride **6425** ·
  setOrbitColor **6415**/setOrbitThickness **6417**/setOrbitIntensity **6414**/setIntensity **6403**/setLabelIntensity **6426**. 카메라 setPositionLBR **273**/setTargetHeight **307**.

## Chart2D — `Chart2D(Chart2D.Chart2DName.Chart2D001)` ✅✅ 돔 데이터 차트 완성 (2026-07-20 사용자 "8개 다 뜬다 괜찮은듯", chart2d.py + Recording46)
- ✅ **막대(Histogram)/파이(Pie) 데이터 차트가 화면에 렌더됨** — Clock 과 같은 HUD 패턴. ChartType enum = **Histogram / Pie** (2종).
- **붙이기 = `cam.addChild(chart.id, Camera.CameraPort.FixedForeground)`** (Clock/InsertText 패턴) + `setPosition(Vec(az,h,roll))`+`setSize`+`setDistance`+`setIntensity`. 실측 값: pos Vec(0,45,0), size 0.75.
- ⚠️⚠️⚠️ **삽질로 확정한 3대 함정 (chart2d v1~v5)**:
  1. **값은 0~1 범위** — 1 넘으면 clamp(다 1로). v1 에 68/27/5(퍼센트) 넣어 파이가 '똑같은 세 조각' 됨. → **전부 0~1 로 정규화**(파이=분수, 막대=최댓값으로 나눔).
  2. **카테고리 라벨(setCategoryNText)은 영문/숫자만** — **한글은 □□ 두부박스로 깨짐**(Chart2D 폰트에 한글 없음, 폰트 세터도 없음). 숫자(%)는 정상. → 라벨 영문. (자막 InsertText 는 한글 OK — 폰트 다름.)
  3. **`setCategoryCount(N)` 를 카테고리 세팅 전에 먼저 호출** — **기본값 3** 이라 안 하면 4번 이상 카테고리가 무시돼 3개만 뜸(완본: "If category count is lesser than N, it has no effect"). 하드캡 아님.
- 카테고리 API: `setCategoryNText(str)` / `setCategoryNValue(float 0~1, Anim)` / `setCategoryNColor(Vec3, Anim)` (N=1~10). `setChartType(Chart2D.ChartType)`.
- ⚠️ 파이/막대를 한 쇼에서 바꿀 땐 **서로 다른 Chart2D 객체**로(카테고리 수/타입 꼬임 방지). 표시(intensity>0) 전에 카테고리 다 세팅.
- SPC(Recording46, family **0x24**=603979777): addChild **4881** / setChartType **10757**(Histogram=0/Pie=1) / **setCategoryCount 10758** / setPosition **10754** / setDistance **10755** / setSize **10756** / setIntensity **10753** /
  setCategoryText **10759** / setCategoryValue **10760** / setCategoryColor **10761** (셋 다 카테고리 인덱스를 인자로 받음 — Python 의 setCategory1~10 을 SPC 는 인덱스 파라미터로 통합).

## Ephemeris — `Ephemeris(Ephemeris.EphemerisName.Ephemeris001)` ✅✅ 천체 출몰 계산 완성 (2026-07-20 사용자 확인, ephemeris_tonight.py + Recording50)
- ✅ **'데이터/계산' 클래스 (렌더 아님)** — 천체의 rise/set/transit **율리우스일을 계산해 속성으로 반환**. 그 값을 읽어 InsertText 로 시각 표출.
  실측: 태양 → **일출 05:29 / 일몰 19:39 / 남중 12:34 (청주 7/20, KST)** = 실제와 정확히 일치.
- **enum(완본엔 Invalid만 보였으나 런타임 dir() 로 실측)**: `EventType` = **CompatibilityRise / Rise / Set / Transit** · `OffsetType` = **CompatibilityHour / Height / Hour**. EphemerisName 슬롯 = Ephemeris001~006 + 007_Tonight/008_Dynamic/009_Sunrise(프리셋).
- **레시피 (확정)**: `eph = Ephemeris(EphemerisName.Ephemeris001)` → `setUseSimulationTime(True)` → `setStartDate(dm.julianDate)`(현재 JD) →
  `setTargetBody(int id)`(**태양 id = `IndividualStar(Sun).id` = 1200**) → (선택)`setEventType(EventType.Rise)` → `setDayLimit(2)` → **sleep(0.3~0.4) 계산 대기** →
  읽기 `eph.riseDate` / `eph.setDate` / `eph.transitDate` / `eph.isValid`. ⚠️ **rise/set/transit 3개가 한 번에 다 계산됨**(eventType 안 걸어도 세 속성 다 나옴).
- **JD → KST 변환 (실측 정확)**: `jd + 9/24 + 0.5` → 표준 JD→그레고리안 알고리즘(Z=int, F=소수부…)으로 Y/M/D h:m. (UTC 시뮬 → +9h = KST.)
- SPC(Recording50, family **0x2A**=704643072): setUseSimulationTime **12040** / setTargetBody **12035** / setStartDate **12036** / setDayLimit **12039** (setEventType/setOffset 계열은 12034~12039 근방). 자막 InsertText setText **3844**.

## DrawableInsert — `DrawableInsert(DrawableInsert.DrawableInsertName.DrawableInsert2D001)` ✅✅ 돔에 자유 그리기 완성 (2026-07-20 사용자 스샷 확인, drawable_probe.py)
- ✅ **붓으로 돔/화면에 자유 드로잉** — 원/선이 또렷이 렌더됨. 슬롯 DrawableInsert2D001~003.
- ⚠️⚠️ **삽질 3연발로 확정한 함정 (v1~v3)**:
  1. **`BrushType.Pen` 을 명시적으로** — `dir(DrawableInsert.BrushType)` = **['Eraser', 'Pen']** (Invalid 아님!). v1 이 `bts[0]`='Eraser'(지우개) 골라 아무것도 안 그려짐. → **`setBrushType(DrawableInsert.BrushType.Pen)`**.
  2. **부착 = `cam.addChild(d.id, Camera.CameraPort.FixedForeground)`** (InsertText/Clock/Chart2D 패턴). v2 의 `setParent(cam.id)` 는 화면에 안 그려짐.
  3. **좌표 = az/h 돔좌표** (InsertText 와 동일, Vec(az, h, roll)). FixedForeground 로 붙였을 때 이 좌표가 맞음.
- ⚠️⚠️ **곡면(돔) 왜곡 (2026-07-20 사용자 지적)**: 그림은 평면이 아니라 **3D 곡면 돔 위에 얹힘** → 평면 공식으로 계산한 '원'(az/h 반지름 일정)은 **돔 어안 투영 + 경선 수렴(고도↑일수록 az 압축)** 때문에 **계란형으로 찌그러짐**. 버그 아님(선은 정상 렌더).
  · ✅✅ **'정원' 그리는 정석 (drawable_probe v4 확정)**: 돔 = 방위각-등거리 투영(천정 h=90=화면중심, 지평 h=0=가장자리) → **화면반지름 r=90−h, 화면각도 θ=az**.
    화면 직교좌표(X,Y)에서 원을 만들고 **`az=degrees(atan2(Y,X))`, `h=90−hypot(X,Y)`** 로 역변환 → 등거리 투영에서 진짜 둥근 원.
    (원 중심 (az_c,h_c) → 화면중심 Xc=(90−h_c)·cos(az_c), Yc=(90−h_c)·sin(az_c); 원점들 = (Xc+R·cosθ, Yc+R·sinθ).) 별자리 덧그리기 같은 자유형 주석엔 보정 불필요.
- **그리기 절차**: `setBrushType(Pen)` → `setBrushColor(Vec3)`(⚠️ SPC 엔 색 값 전달되나 실측 화면엔 하양 — Pen 색 고정 추정) → `setBrushSize(float)` → `setIntensity(1)` → `beginDraw()` → `setBrushPosition(Vec(az,h,0))` 를 촘촘히 연속 호출(각 점이 획) → `endDraw()`. 지우기 = `clearAll(Anim)`. `undo`/`redo`/`save`/`load` 도 있음.
- 활용 아이디어: 별자리 위에 형상 덧그리기, 화살표/동그라미 주석, 관객 앞 실시간 스케치.
- SPC(Recording49, family **0x26**=637534208): addChild **4881** / setBrushType **11271**(Pen=1) / setBrushColor **11272** / setBrushSize **11275** / setIntensity **11274** / beginDraw **11265** / setBrushPosition **11270** / endDraw **11266** / clearAll **11267**.

## NGC — `NGC(NGC.NGCName.NGC2237)` 🛑 이 빌드서 '쇼 개체로 사용 불가' 확정 (2026-07-20 실측)
- NGCName enum = 실제 카탈로그(NGC253 조각가은하/**NGC2237 장미**/NGC869_884 이중성단/NGC2392 에스키모/NGC4038 안테나 …), NGCPort = **Ecliptic / LineOfSightLocal**. API=setIntensity/setScale/setLabelIntensity/setSize/portId/addChild.
- ⚠️⚠️ **접근 3경로 전부 실패 (ngc_deepsky.py v1~v3)**:
  ① **클래스 LOS 포트로 카메라 이동**(horsehead 방식 그대로) → **프레임이 깨져 배경 별까지 사라지고 자막(HUD)만 남음**. NGC 의 LineOfSightLocal 은 Nebula 의 그것과 다르게 동작(같은 코드가 Nebula 는 OK).
  ② **DB `NgcType` "NGC 2237"** → 핸들은 나오나 **`.action(ConnectTo/FadeTo/GoTo)` 전부 None(死)** = MessierType 함정과 동일(핸들만 나오고 액션 없음).
  ③ **DB `NebulaType`/AsterismType/DeepSkyObjectType "NGC 2237"** → **핸들 자체가 없음**("Failed to get data"). NGC 천체는 NebulaType 에 미등록(M 천체가 NebulaType 에 다 있는 것과 대조).
- → **NGC 천체는 이 빌드서 카메라 접근·센터링 불가 = 쇼 개체로 못 씀.** 딥스카이 쇼는 검증된 **Nebula(HORSEHEAD 등 44개 아트) / Messier(`NebulaType`+"M##")** 로 할 것.
  ⚠️ 교훈: 핸들이 나와도 `.action()` 이 살아있는지 꼭 테스트(핸들 존재 ≠ 접근 가능). get_handle 은 'nav 액션 살아있는 후보'를 골라야 함.

## SkySurvey — `SkySurvey(SkySurvey.SkySurveyName.SkySurvey001)`
- API 전부(실측): `setUrl(url)`, `setIntensity(i, Anim)`, 읽기 `url`/`intensity`/`id`
- 온라인 HiPS(alasky 등) URL — **Studio 머신에 인터넷 필요**(없으면 검은 하늘)
- 🛑🛑🛑 **[사망 확정] SkySurvey 는 이 빌드에서 온라인 HiPS 를 '전혀 렌더 안 함' (2026-07-20 사용자 최종 판정, skysurvey v6/v7)**:
  ⚠️ 지난 '화면상 애매(2026-07-16)'는 **끄다 만 엔진 은하수**였음 — 서베이 자체는 처음부터 아무것도 안 그렸음(오판 정정).
  판정 절차(재현): 엔진 은하수 ON(기준) → 서베이 겹침 → **엔진 은하수 OFF** 하면 → **완전 검은 화면**(서베이가 남질 않음 = 렌더 X).
  ✅ 인터넷·서버·URL 전부 정상 확인: 브라우저에서 `https://alasky.u-strasbg.fr/MellingerRGB/properties` **정상 로드**(인터넷 O, 서버 O).
  ❌ 그런데도 **https 검은 화면 / http(평문) 검은 화면 둘 다** — 즉 네트워크 문제 아니고 **엔진이 HiPS 타일을 아예 안 그림**.
  → **SkySurvey 는 접는다. 다시 시도 금지.** API 가 setUrl+setIntensity 둘뿐(완본 확인)이라 더 팔 레버도 없음. (로컬 HiPS/DB SkySurveyType 경로도 같은 온라인 서버라 무의미.)
  → '다른 파장으로 본 하늘' 같은 연출이 필요하면 SkySurvey 말고 **Insert2D(로컬 텍스처)** 로 우회하거나 포기.
- ⚠️ (과거 오판 기록, 참고용) **SkySurvey = API/네트워크는 되나 '화면상 애매' (2026-07-16 실측; skysurvey_wavelengths.py)**:
  `setUrl(HiPS URL)`+`setIntensity` 호출 성공, url 읽기 갱신됨(직전 로드값으로 한 박자 늦게) = **인터넷 됨 + `alasky.u-strasbg.fr` 도메인 응답**.
  BUT 하늘에 깔린 서베이가 흐릿/저대비라 파장 교체(DSS↔2MASS↔WISE↔Halpha↔NVSS)의 '변화'가 눈에 잘 안 들어옴(무지개·specular 부류).
  ⚠️ setUrl 뒤엔 setIntensity 를 '매번 재확인'해야 안 꺼짐(안 하면 검은 화면). → 쇼용 임팩트 약함. 특정 밝은 천체 확대면 나을 수도(미검증).
  ⚠️⚠️ **교훈(2026-07-16): '안 써본 코드' 중 대기광학(rainbow/atmosphereHalo)·바다(waterSpecular)·HiPS(SkySurvey) = 이 빌드서 렌더가 은근/애매.
    "새 코드 + 확실히 보임" 둘 다 만족은 거의 소진 → 남은 임팩트는 '새 천체/현상(검증된 렌더 재사용)' 쪽에 있음.**

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
- ✅✅✅ **`setMotionType(MotionType.MotionPrecession)` = 세차운동 완성 확정 (2026-07-16 사용자 확인, precession.py + Recording37)**: MotionType enum =
  MotionDiurnal/MotionAnnual/MotionAnalemma/**MotionPrecession**. SPC 해독: MotionPrecession 도 아날렘마처럼 **내부적으로 Earth
  setRotationSpeedScale(cmd 1029)=0 로 자전 정지** + 시간가속 → 세차만 보임. reset = cmd 4891=0 + 1045(자전배율 reset).
  ⏳ **미완성 숙제(사용자 제안)**: '세차 원'(천구 북극이 그리는 원)을 그려주면 더 좋음 → 문서상 Marks 위젯 소관(Mark로 그려야). 다음에 붙일 것.
  ✅✅✅ **황도 12궁 쇼 완성 확정 = MotionAnalemma + 대기 OFF (2026-07-16 사용자 확인, zodiac_sun.py v8 + Recording38)**:
  '태양이 1년간 12별자리를 지나감'을 보여주는 정답. ⚠️⚠️ **긴 삽질 끝(v3~v8) — 방법 선택이 핵심**:
  · ❌ **우주(FadeTo Earth) 프레임 + 태양 줌락 = 전면 실패**(v3~v6): 이 프레임서 `setZoomPosition` 줌락이 근본 불안정 —
    애니슬루면 '공간이 중앙으로 빨려듦', 즉시(Anim0)면 락이 아예 안 걸려 태양이 화면 밖, 지구 블롭이 태양을 가림.
    → **우주 프레임서 '움직이는 천체(태양)에 카메라 줌락 추적'은 하지 말 것**(지상 줌락 무반응과 별개로, 우주도 불안정).
  · ❌ **MotionAnnual = '태양이 움직여' 화면 밖으로 나감**(v7, 사용자 확인). 이름과 달리 조디악 쇼엔 부적합.
  · ✅✅ **정답 = 지상 `setMotionType(MotionAnalemma)` + `setAtmosphereIntensity(0)`**(v8): 아날렘마가 태양을 **남쪽 8자
    자리에 붙잡고**(cmd 4891=1 → 내부적으로 Earth setRotationSpeedScale(1029)=**2.73e-3=1/366** 로 일주 상쇄, Recording38 확인),
    **대기를 끄면** 아날렘마 쇼에선 가려졌던 **배경 별이 보여** → 1년 가속 시 하늘이 ~1바퀴 돌며 **12궁이 태양 뒤를 하나씩 통과**.
    카메라는 남쪽(setOrientationH(0)+setTargetHeight(37)) **한 번만 고정** = 추적·줌락 불필요 = 견고. 궤적선은 꺼라(사용자 요청).
    레시피: 지상 대기OFF+지면OFF + 12궁 setLinesIntensity(0.6)/setLabelIntensity(0.9) + setEclipticGridIntensity + 태양 setScale(3) +
    청주 정오(03:30 UTC) 춘분 시작 → setMotionType(MotionAnalemma) → setDateTime(+1년, Anim(42)). 복귀 = 4891=0 + resetRotationSpeedScale(1045).
    ⚠️ 태양이 8자로 위아래(±23°=계절) 오르내리는 건 정상. SPC(Recording38): setMotionType **4891**, setRotationSpeedScale **1029**, reset **1045**, setDateTime **257**, Stars setPointSaturation **515**, InsertText setText **3844**.
  Planet 에 'PrecessionDate'
  Python 메서드는 **없음**(dir 프로브 확인) → MotionPrecession 로만. 자전축 시각화 = `setEquatorialPoleAxisIntensity`(청록 극축) +
  `setEclipticPolePointerIntensity`(황도극=세차 원 중심). ✅ **극 표시는 '축(Axis)'말고 '포인터(Pointer)'를 쓸 것 (사용자 선호)**:
  `set...PoleAxisIntensity` = 관측자→극 **세로 기둥**(뭔지 헷갈림) / `set...PolePointerIntensity` = 하늘의 극 **지점을 동그라미**로 찍음(직관적).
  세차로 천구 북극이 이동 → **청록 동그라미(천구 북극)가 주황 동그라미(황도극) 둘레로 이동**하는 게 세차의 핵심 시각화.
  ⚠️ **별 포인터(화살표)는 세차 중 위치 재계산으로 '지랄발광'** → 가속 전 꺼라(라벨만). (극 포인터 동그라미는 괜찮음.)
  ⚠️ **지상 세차 쇼도 `setTerrainIntensity(0)` 로 지면 꺼야** 깔끔(대기 OFF 만으론 지면이 남아 지저분).
- ⚠️⚠️ **`stop()` 을 setDateTime "뒤"에 부르면 방금 건 날짜 이동까지 취소됨 (실측 사고)**
  → **순서: `dm.stop()` → `setDateTime(...)` → sleep 으로 적용 대기**. 검증은 `dm.julianDate` 읽기.
- ⚠️⚠️ **`SceneGraph().reset(1)` 은 날짜를 '현재(오늘)'로 되돌림 (2026-07-15 실측, Recording32 금성)**:
  인트로에서 setDateTime 을 걸어도 그 뒤 reset 을 부르면 날짜가 오늘로 초기화됨 → **시간가속 '시작 날짜'는
  반드시 마지막 reset 이후에 다시 명시**할 것. (금성 위상 v1: 인트로 3/1 이 reset 에 지워져 실제론 오늘→9/1 =
  48일만 흘러 위상이 조금만 변함. v2: accel 직전 시작 날짜 재설정 + 범위 금성 1공전으로 확대.)
- ⚠️⚠️⚠️ **`setDateTime(..., Anim(0.0))` = instant 날짜점프 → 위성/궤도천체가 '순간이동' (2026-07-15 사용자 지적, 천왕성)**:
  위성이 화면에 보이는 상태에서 시작 날짜를 instant 로 다시 걸면(예 오늘→8/1 = +17일) 위성이 궤도상 +17일치
  위치로 **뚝 순간이동**(주기 짧은 미란다는 여러 바퀴 점프). **→ 시작 날짜(instant 세팅)는 반드시 위성/천체를
  켜기 전, 암전 중에** 미리 고정하고, 위성이 보일 땐 **매끄러운 가속(Anim(N))만** 돌릴 것.
  (reset 이 날짜를 되돌리는 것과 별개 문제 — reset 이후 '언제' instant 세팅하냐가 핵심: 위성 켜기 전에.)
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
- ✅✅ **지상 자막 '가독성' 표준 (2026-07-15 사용자 확정, star_colors v2)**: 기존 size 0.035 는 **너무 작아 잘 안 보임**.
  → **읽기 좋은 지상 자막 = `setSize(0.052)` + `setPosition(Vec(0, 25, 0))`(높이 25 = 프레임 하단이지만 지평선 위) +
  밝은 색 `setColor(Vec(1.0, 1.0, 0.55))`(검은 하늘에 노랑이 잘 뜸) + distance 1.0**. (행성/은하 프레임은 여전히 distance 20.)
```python
t = InsertText(InsertText.InsertTextName(1))
cam = Camera(Camera.CameraName.MainCamera)
cam.addChild(t.id, Camera.CameraPort.FixedForeground)
t.setText("안녕하세요"); t.setPosition(Vec(0, 25, 0))
t.setSize(0.052); t.setColor(Vec(1, 1, 0.55)); t.setIntensity(1.0, Anim(1.0))
```

## Insert2D — `Insert2D(Insert2D.Insert2DName.Insert2D001)`
- `setTexture(path)`, `setPosition(Vec(az,h,roll), Anim)`, `setSize(size, Anim)`
- `setIntensity(intensity, Anim)`, `setType(Type, Orientation)`
- 특수: `Insert2D.Insert2DName.Insert2D076_LightPollution`(광공해 오버레이)
- ✅✅ **로컬 이미지 표시 완성 (2026-07-20 사용자 스샷 확인, insert2d_image.py)**: `cam.addChild(ins.id, FixedForeground)` +
  `setTexture(경로)` + `setPosition(Vec(0,45,0))`+`setSize(0.6)`+`setIntensity(1)` → 돔에 이미지 렌더(과녁 테스트 이미지 확인).
  ⚠️ 이 뷰에선 FixedForeground 오버레이가 **좌우 반전(미러)**돼 보임(자막 InsertText 도 같이 반전 = 뷰/설정 의존, Insert2D 탓 아님).
  SPC(Recording62, family **0x01**=16777217): addChild **4881** / setPosition **1794** / setDistance **1795** / setSize **1798** / setIntensity **1802** / **setTexture 1796**.
- ✅✅✅ **[중요] 로컬 에셋 폴더 = `Configuration.configuration().localUserFolder` (2026-07-20 확정)**: 이미지/비디오 등 로컬 파일을 넣는 곳.
  실측 예: `'D:/SkyExplorer-Data/user'`. **setTexture/setFilename/VideoPlayer.load 경로는 이 폴더 상대(파일명만) 또는 절대경로 둘 다 OK, 슬래시 `/`·`\\` 둘 다 됨**(3형식 다 로드 확인).
  → 파일 못 찾으면 스크립트에서 `Configuration.configuration().localUserFolder` 를 print 해 정확한 폴더를 확인하고 거기 넣을 것. (igUserFolder(0) 은 빈 문자열이었음 → localUserFolder 사용.)
- ⚠️ **Patch 클래스 ≠ 이미지 표시** (2026-07-20): `Patch(setFilename/setKeyColor/setOpacity…)` 는 **position 세터가 없는 '프로젝션 워핑/블렌딩 패치'** → 창 Sky View 에선 안 뜸. **로컬 이미지 표시는 Insert2D 로 할 것**(Patch 아님).
- 🛑 **VideoPlayer(로컬 영상) = 레거시/미작동 확정 (2026-07-20, videoplayer_show.py)**: `VideoPlayer()` 싱글톤 + `load(파일, Anim, Eye.Both)`+`play`+`setOpacity(1=영상)`.
  ⚠️ **load 해도 `videoFile` 이 계속 빈값 + state 가 `LegacyInvalidState` 에서 안 바뀜 + duration=0** — 파일 등록 자체가 안 됨.
  H.264 default → **Constrained Baseline+yuv420p+L3.1** 로 재인코딩해도 동일(코덱 문제 아님, 경로는 Insert2D 로 검증됨 = 정상). VideoState 에 'Legacy'가 붙은 게 신호.
  ✅✅ **근본 원인 확정 (2026-07-22 v3 포맷판별 + 완본 정독, 사용자 로그)**: **코덱/경로 완전 배제** — 같은 영상을 4개 컨테이너
  (**WMV8 / MPEG-1 / MS-MPEG4(avi) / H.264 mp4**)로 만들어 상대경로(완본: "load 는 유저폴더 상대경로 필수")로 하나씩 load 해도
  **4개 전부 `videoFile='' + state=LegacyInvalidState + duration=0` 로 완전 동일**(생성 직후 첫 읽기부터 Legacy). = 파일을 아예 안 받음.
  → **진짜 이유 = `Source_ViPlayer` 는 `SoftwareManager.Source` enum 멤버** (완본 line 29341). 즉 VideoPlayer.load 가 노리는 'viPlayer'는
  **별도 소프트웨어 소스/호스트**(IG/오퍼레이터 레벨)라, 이 소스가 활성화돼 있지 않으면 Python `VideoPlayer` 객체가 아무 것도 디코드 못 함
  (정상이면 unLoad 후 `UnloadedState` 여야 하는데 처음부터 `LegacyInvalidState`). **스크립트 창(Studio window)에선 ViPlayer 소스가 꺼져 있음.**
  → **[최종] 파이썬 VideoPlayer 로 '파일 떨궈 돔 재생'은 이 빌드/창에서 불가 = 시스템 설정(SoftwareManager ViPlayer 호스트) 소관.** 코덱 바꿔봐야 소용없음(재시도 금지).
  ✅ **영상 대체 = Insert2D 텍스처 시퀀스(프레임 flip)** — Insert2D 는 렌더 확정이라 setTexture 를 빠르게 갈아끼우면 '움직이는 콘텐츠' 흉내 가능(권장 우회).
  또는 `SoftwareManager.softExe/softStart` 로 외부 플레이어 IG 실행 or Studio UI 미디어 임포트. (로컬 이미지 표시는 Insert2D 로 확정.)
- 🛑 **오디오(Audio/AudioLayer/AudioLite/AudioPlayer) = 스크립트 창 미지원 확정 (2026-07-22, audio_show.py, 사용자 "완전 무음")**:
  VideoPlayer 와 동일한 '별도 호스트 필요' 부류. 4형제: `AudioLite()`(단순 load/play), `AudioLayer(Layer001~050)`(load(ch,파일)+play(loop)+상태읽기),
  `Audio()`(모노/스테레오 채널 매핑), `AudioPlayer(MainAudioPlayer)`(마스터 볼륨). 경로는 "audio 폴더 상대 or 절대" — 절대경로(localUserFolder) 사용.
  ⚠️ **AudioLayer 상태읽기로 검증 = 확정 실패**: wav/mp3/ogg 3개 전부 `audioState=InvalidAudioState + audioDuration=0`(로드 안 됨). AudioLite 는 상태읽기 없어 귀로만인데
  **마스터볼륨(MainAudioPlayer.setOutputVolume(1.0))까지 올리고 풀8초 재생해도 완전 무음**(사용자 확인). → 오디오 출력 소스가 스크립트 창(Studio window)엔 비활성.
  → **[최종] 파이썬으로 소리 재생 불가 = VideoPlayer 와 같은 시스템/오퍼레이터(오디오 호스트) 소관. 재시도 금지.** 쇼의 사운드는 Studio UI/오퍼레이터가 입힐 것.
  ⚠️ **교훈: 미디어(영상·오디오)·하드웨어(Light=DMX 코브조명·DMX512) 계열은 '별도 호스트' 부류라 스크립트 창에서 렌더/출력 안 됨.** 남은 미개척은 렌더 오브젝트(Lut/Place3D 등)에서 찾을 것.

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
