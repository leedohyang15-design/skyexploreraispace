# 19. 개체별 카메라 무빙 매트릭스 + 예제 학습 정리 (2026-07-09)

> "각 개체마다 할 수 있는 카메라 무빙"을 한곳에 정리. 전부 실측 확정.
> 근거: 복합 여행 데모(docs/16), 가이드 투어, 유성/화구, 혜성, 소행성 예제 + SPC 녹화 해독.

## 0. 카메라 무빙 '수단' 총람 (무엇이 있나)

| 수단 | 화면 | 프레임 | 비고 |
|---|---|---|---|
| **FadeTo** | 페이드아웃→순간이동→인 (접근 **안 보임**) | 대상 프레임(R≈5~10 도킹) | 장면 전환용. 궤도선 지움. |
| **GoTo** | ✅ 연속 비행 (보임) | 대상 도킹 | **비행 중 자세회전 1회 '흔들림' 내장(제거 불가)** |
| **StraightGoTo** | 순간이동 | 대상 | 즉시 배치 |
| **ConnectTo** | 비행 없이 프레임만 전환 (+ 'Look at' 슬루 3~4초) | 대상 (R=실제거리!) | 흔들림 최소. 전환 순간은 암전 권장 |
| **setPositionR(읽은값×배율, -1)** | ✅ 같은 프레임 연속 줌 | 현 프레임 유지 | **줌인/풀백의 정석**. 절대값 금지 |
| **setPositionLBR(Vec, Anim, port)** | 프레임 진입/이동 | 지정 포트 | ⚠️ **지상 Sky View 에선 무효**(관측자 바인딩) |
| **setTargetHeight / setOrientationH** | 트랙볼(틸트/방위) | 현 프레임 | 지상 조준의 기본 레버 |
| **setScale** (개체 메서드) | 개체를 그 자리서 확대 | 불변 | 지상 클로즈업의 정답(카메라 안 움직임) |
| **setZoomFov** | 광학 줌 | 뷰 축 기준 | ⚠️ 지상 무효, 비행/우주 전용 |
| **Land** | 하강+몸 일으키기 10초 | 지표 R=0 | 지구 착륙 (GoTo 지구 후) |

## 1. ★ 개체별 카메라 무빙 매트릭스

| 개체 | FadeTo | GoTo | ConnectTo | setPositionR 줌 | 프레임 특성 | 확정 예제 |
|---|:-:|:-:|:-:|:-:|---|---|
| **Planet(행성)** | ✅ | ✅(20초,흔들림) | ✅ | ✅(도킹 후) | 도킹 R=5 행성반지름. GoTo 는 Target 0 남김→TH30 필수 | zoom_saturn, complex_demo |
| **지구(관측지)** | — | ✅→R=4 호버 | — | — | GoTo 는 북극 호버, 착륙은 **Land** 별도 | complex_demo(Land) |
| **DwarfPlanet(왜소행성)** | ✅→R=4 | (행성과 동일) | — | ✅(도킹 후) | Planet 과 동일. TerrainModel=미션 실측 표면(NewHorizons/Dawn) | pluto_flyby |
| **Satellite(달)** | ✅ | — | — | ✅ | FadeTo 후 R 줌·줌락 다 됨 | moon_phase_show |
| **Comet(혜성)** | ✅→StdEclJ2000 | — | — | ✅(황도 프레임) | **FadeTo 프레임=자전 없음**→줌+시간가속 매끄러움. 궤도선은 지상 전용 | comet_halley_complete |
| **Asteroid(소행성)** | ✅ | ✅(흔들림) | ✅ | ✅ | **ConnectTo 후 R=실제거리(수천만)**→지오메트릭 줌 필요. DB 는 지형모델 有 | asteroid_apophis_v5 |
| **Galaxy(은하)** | ✅ | ✅(3단 안무) | — | ✅(도킹 후) | GoTo=Move away→Look at→프레임점프→비행(제일 비행다움) | complex_demo |
| **Nebula(성운)** | ✅(DB) | — | — | 줌락 | LOS 포트 프레이밍+cmd295 정렬+스텝오빗. 줌락=setZoomPosition(FreeFly) | horsehead_show |
| **IndividualStar/Sun** | — | — | — | (포트 조망) | `portId(Ecliptic)`로 태양계 조망 프레임 | complex_demo |
| **지상(Place2D)** | — | — | — | ❌ | **setTargetHeight+setOrientationH 만**. 위치명령 무효. 클로즈업=setScale | eclipse_2026 |

## 2. 핵심 규칙 (실측 확정)

1. **줌인의 정석 = 대상 프레임 확보 후 `setPositionR(읽은값×배율, track=-1)`**. 절대값 금지(R 단위=대상 반지름).
2. **프레임 확보 3경로**: FadeTo(접근 안 보임)/GoTo(보이나 흔들림)/ConnectTo(흔들림 최소).
   → **흔들림 없는 줌인 = ConnectTo + 지오메트릭 R 줌**(아래 3번).
3. **초대형 범위 줌은 지오메트릭 반복**: ConnectTo 후 R 이 실제 거리(소행성=수천만 반지름)라 한두 번으론
   안 커 보임. **R<목표 될 때까지 ×배율 반복**. ⚠️ `Anim.cubic` 스텝은 경계마다 가감속→'끊김'.
   **`Anim`(선형) + 큰 비율(0.5~0.7, 작은 스텝) + 짧게(1.2초)** = 매끄러운 연속 줌 (Recording9 해독).
4. **지상 Sky View 함정**: setPositionLBR·setZoomFov 무효, setTargetAzimuth 무반응.
   지상 클로즈업은 **setScale**(개체 확대), 조준은 setTargetHeight/setOrientationH.
5. **프레임 간 '보이는 다이브'(행성↔행성 근접)는 미해결** — GoTo(흔들림)/ConnectTo(전환)로 대체.
6. **시간가속은 프레임에 주의**: 지상서 수십 년 가속=지구 자전 광란. 궤도천체 시간가속은
   **FadeTo/ConnectTo 후 황도 프레임**(자전 없음)에서.

## 3. 이번 라운드 예제 학습 정리 (무엇을 배웠나)

| 예제 | 새 클래스/기능 | 핵심 수확 |
|---|---|---|
| **night_guide_tour** | Mark, DomePointer, Stars(반짝임/고유운동), 별자리 아트 | 그리드 본명령=Place2D/Planet 속성 · 포인터 az=180−방위 · 전천구도=Target 0 |
| **pointer_object_test** | 개체 직결 포인터 | 행성은 setPointerType 필수, 별은 기본 타입 有 |
| **geminid_night** | ShootingStar, Bolide | ZHR 내부=분당(÷60) · 화구=ColoredFireball+setElement(색) |
| **comet_halley** | Comet 궤도 6요소 | 모델 먼저+프레임 대기 · 궤도선 지상 전용 · FadeTo 황도프레임서 줌/시간가속 |
| **asteroid_apophis** | Asteroid 궤도요소, ConnectTo 줌 | ConnectTo+지오메트릭 R 줌 = 흔들림 없는 줌인 · DB는 지형모델 有 |

세부는 각 `docs/16~19` 와 `CLAUDE.md` 참조. 스크립트는 `scripts/study/`.
