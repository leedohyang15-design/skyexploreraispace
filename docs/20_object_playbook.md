# 20. 개체별 확대·이동 플레이북 (정본 — 예제 만들기 전 무조건 먼저 읽기)

> 2026-07-13 작성. 이 세션(구상성단·메시에·별의 일생 등)까지의 실측 + SDK 문서(class.rst, HelpCenter.glp)
> 교차 검증으로 확정. **예제를 만들 땐 항상 이 문서를 먼저 읽고, 개체에 맞는 방법만 쓴다.**
> (매트릭스 원본은 docs/19, 세부 함정은 CLAUDE.md. 이 문서가 최상위 요약/의사결정 기준.)

---

## 0. 예제 만들기 전 3초 의사결정 트리

```
"이 개체를 크게/가까이 보여주고 싶다" →
 ├─ 행성/왜소행성/위성/소행성/혜성/은하?  → 각자 전용 레시피(§2 표) — 대부분 FadeTo·GoTo·ConnectTo + setPositionR 줌
 ├─ 성운/딥스카이(Messier)?              → §3 '딥스카이 fly-in' (ConnectTo + setPositionR, frac 기반)
 │     · 단, 그 개체가 ConnectTo 를 지원해야 줌 가능! (M42·M27=O / M8=X / M1=렌더X) — §3-c 판별
 ├─ 구상성단?                            → FadeTo(줌+스핀 내장) 진입 후 setScale (§2)
 ├─ 별(태양/항성)?                       → fly-in 없음. 포인터/포트 조망만 (§2)
 └─ 지상 개체(일식·행성 하늘)?           → 카메라 이동 금지. setScale(확대) + setTargetHeight/OrientationH(조준) (§2)
```

**철칙 3가지 (이번 세션의 피값):**
1. **줌 목표는 절대 R 금지 → 반드시 `R0 × 비율(frac)`.** 개체마다 ConnectTo R0 가 1e16~3.8e18 로 제각각이라
   절대값을 주면 어떤 개체는 대상을 뚫고 지나가 새까맣게 됨(M1 참사). 비율이면 개체 불문 같은 배율로 접근.
2. **Target = 30 (관람 표준).** 기하학적 중앙(90)이 아니라 관람 정위치 30. 특수 요청 시에만 예외.
3. **setScale ≠ 카메라 이동.** "화면이 이동해야" 하는 연출엔 setPositionR(줌)/GoTo(비행). setScale 은 제자리 확대.

---

## 1. 카메라 이동 '수단' 총람

| 수단 | 화면 | R 단위 | 언제 |
|---|---|---|---|
| **FadeTo** | 페이드+순간이동(접근 안 보임) | 딥스카이=R≈0 / 행성=도킹 R≈5 | 장면 전환. 딥스카이는 R=0 라 이후 setScale 로만 확대 |
| **GoTo** | ✅연속 비행(보임) | 도킹 | **행성/은하/소행성만**. 성운·딥스카이 미지원. 비행 중 흔들림 1회 내장 |
| **ConnectTo** | 비행 없이 프레임 전환(+'Look at' 슬루 4~10초) | **실제거리(초대형)** | 딥스카이 줌인의 핵심. 슬루는 **암전 속**에 숨겨라 |
| **StraightGoTo** | 순간이동 | 대상 | 즉시 배치 |
| **setPositionR(tgt, Anim, -1)** | ✅같은 프레임 연속 줌(=날아듦) | 현 프레임 | **줌인 정석**. 절대값 금지, tgt=R0×frac |
| **setScale(개체)** | 개체를 제자리서 확대(카메라 불변) | — | 지상/구상성단 확대. **카메라 이동 아님** |
| **setTargetHeight / setOrientationH** | 트랙볼(틸트/방위) | 현 프레임 | 지상 조준의 유일 레버 |
| **setPositionLBR(Vec,Anim,port)** | 포트 프레임 진입 | 포트 | ⚠️ 지상 Sky View 무효(관측자 바인딩) |

---

## 2. ★ 개체별 확대·이동 매트릭스 (전부 실측 확정)

| 개체 | 프레임 확보 | 확대(가까이) | Target/특이 | 확정 예제 |
|---|---|---|---|---|
| **Planet 행성** | FadeTo / GoTo(흔들림) / ConnectTo | setPositionR(R0×배율,-1) | GoTo 후 TH30 필수. 도킹 R=5반지름 | zoom_saturn |
| **DwarfPlanet 왜소행성** | FadeTo(R=4) | setPositionR | TerrainModel=실측표면(NewHorizons) | pluto_flyby |
| **Satellite 달** | FadeTo | setPositionR / 줌락 | 위상=setMoonAge | moon_phase_show |
| **Asteroid 소행성** | **ConnectTo**(R=실제거리) / GoTo | **setPositionR frac 줌**(초대형 R) | DB=지형모델 有 | asteroid_apophis |
| **Comet 혜성** | FadeTo→StdEclJ2000 | setPositionR(황도프레임) | FadeTo프레임=자전없음→시간가속 굿. 궤도선=지상전용 | comet_halley_complete |
| **Galaxy 은하** | FadeTo / GoTo(3단) | setPositionR | roll 로 세우기(안드로메다 77°) | complex_demo |
| **Nebula/Messier 성운** | **ConnectTo**(지원 시)→LOS Local | **setPositionR frac 줌**(§3) | Target 30 / ⚠️개체별 지원 편차(§3-c) | star_life_cycle, messier_tour |
| **GlobularCluster 구상성단** | **FadeTo**(줌+스핀 내장, R=0) | **setScale(원본×배율)** | 별밭=고정투영(R 무효). 회전=roll | globular_cluster_final |
| **IndividualStar 별** | (fly-in 없음) | ❌(점광원, 안 커짐) | `portId(Ecliptic)` 조망 / setPointerIntensity 지목 | star_life_cycle |
| **지상(Place2D) 일식·행성하늘** | (이동 금지) | **setScale** | setTargetHeight+setOrientationH(H≈180−방위) | eclipse_2026 |

---

## 3. 딥스카이(성운/Messier) fly-in 확정 레시피

**목적**: 성운으로 카메라가 실제로 '날아드는' 연출 (setScale 제자리 확대 아님).

### 3-a. 절차 (star_life_cycle / messier_tour 확정)
```
0) 핸들 선확보: h = DataManager.database().data(Data.Type.NebulaType, "M##")   # 종류불문 NebulaType+M##
   ⚠️ MessierType=FadeTo미지원, DeepSkyObjectType=이름조회실패. 반드시 NebulaType.
1) (매 개체마다) 지상 reset → 일관된 초대형 R0 확보    # 직전이 다른 딥스카이 프레임이면 R0 꼬임
2) 암전(GlobalIntensity 0) 속에서:
     h.action(ConnectTo).trigger(); sleep(8.5)          # LOS Local 프레임 진입 + 내부 슬루 숨김
     bg_off(): Galaxy=0 + 딴 딥스카이 개체 intensity=0   # 배경 잡음(말머리 등) 제거
     setTargetHeight(30)                                 # 🎯 관람 표준 (90 아님!)
     (은하면 setOrientationHPR roll 로 세우기)
3) 페이드인 → setPositionR 지오메트릭 줌 = 날아듦:
     R0 = cam.positionLBR.z
     target = R0 * frac                                  # ★ 절대값 금지! 비율.
     while r>target: r*= (앞 완만 0.86/0.74/0.66/0.62, 이후 0.60); targets.append(r)
     for tgt in targets: setPositionR(tgt, Anim(1.2), -1); sleep(0.8)   # 선형·짧게·겹침=연속·매끄러움
```

### 3-b. 🎯 기본값 (사용자 확정 — 아령성운 M27 기준)
- **기본 frac = 0.004** (M27 아령성운의 비율-대비-크기. **딥스카이 fly-in 의 표준 기본값으로 사용**).
- 큰 발광성운(M42 급)은 덜 당겨도 참 → **frac 0.0094** (안 뚫림, 돔 가득). 작은 개체일수록 frac 작게(더 깊이).
- 줌 스텝: `Anim`(선형) + ratio 0.6 + 짧게(1.2초) + 절대타겟 겹침(sleep<Anim). cubic·절대R·sleep≥Anim 금지.

### 3-c. ⚠️ fly-in 가능 개체 판별 (이번 세션 확정 — 아무 성운이나 되는 게 아님!)
| 개체 | ConnectTo | 결과 | 판정 |
|---|:-:|---|---|
| **M42 오리온**(발광) | ✅ | 초대형 R0 → setPositionR 줌 O | ✅ fly-in 정상 |
| **M27 아령**(행성상) | ✅ | 줌 O (기본값 기준) | ✅ fly-in 정상 |
| **M31 안드로메다**(은하) | ✅ | R0=수백, roll 로 세움 | ✅ (은하) |
| **M8 석호**(발광) | ❌(FadeTo만) | R=0 → setPositionR 무효(줌 안 됨, 보이긴 함) | ⚠️ 제자리 setScale 만 가능 |
| **M1 게**(초신성잔해) | — | 멀면 안 보이고 가까우면 뚫려 새까맘 | ❌ fly-in 렌더 불가 |
| **M45 플레이아데스**(산개성단) | — | 밀집천체 없음 → 성단 안 보이고 배경만 | ❌ fly-in 부적합 |
- **결론**: 딥스카이 fly-in 은 개체별로 **ConnectTo 지원 + 렌더 확인 먼저**. 확정 안전 개체 = **M42, M27**(성운) / M31(은하).
  불확실한 개체는 쇼에 넣기 전 프로브(ConnectTo→R0 로그, 뚫림/안보임 확인). 안 되면 확정 개체로 교체.

---

## 4. 실패 원인 정리 (왜 안 됐나 — 이번 세션 부검)

| 실패 | 증상 | 진짜 원인 | 교훈/정답 |
|---|---|---|---|
| **M1 게성운 새까맘** | 화면 돌더니 껌해 | 목표를 **절대 R** 로 줌 → R0(3.8e18)가 M42 의 300배라 25000배 날아들어 **성운 관통** | 목표=R0×frac(비율). +ConnectTo 슬루 암전에 숨기기 |
| **M1 안 보임** | 멀어도 안 보임 | 게성운 자체가 **fly-in 렌더 안 되는 개체** | 교체(M8/확정개체) |
| **M8 줌 안 됨** | 보이지만 안 날아듦 | M8 은 **ConnectTo 미지원 → FadeTo(R=0)** → setPositionR 무효 | ConnectTo 지원 개체만 fly-in |
| **M45 성단 안 보임** | 배경 성운만 껴 | 산개성단=밀집천체 없어 다가가면 흩어짐. 배경(말머리 등)은 **Nebula enum off 로 지울 수 있음(가능 확인)** | 투어는 밀집 천체로 |
| **setScale 로 키움** | 화면 이동 없이 개체만 커짐 | setScale=제자리 확대(카메라 불변) | 이동 연출엔 setPositionR/GoTo |
| **GoTo 로 성운** | 아무 일 없음 | 성운은 **GoTo 미지원**(행성/은하/소행성 전용) | 성운=ConnectTo+setPositionR |
| **줌 중간 뚝뚝** | 스텝마다 정지 | sleep≥Anim(스텝 완료 대기) → 정지 | sleep<Anim 겹침 + **절대타겟**(겹쳐도 깊이 정확) |
| **줌 뒤 대상 작아짐** | 덜 당겨짐 | `현재R×비율`을 겹쳐 재생 → 덜 완료된 R 을 읽어 곱함 | **목표 R 절대값 미리계산**(비율은 R0 기준 1회) 후 순차 |
| **Target 자꾸 90** | 관람 부적합 | 성운 LOS=90 이 기하중앙이나 **관람 표준은 30** | 항상 30 (사용자 지시) |

> 근본 통찰: **"이동 방법은 클래스가 아니라 개체(DB 카탈로그 항목)별로 다르다."** 같은 NebulaType 이라도
> ConnectTo 있는 개체/없는 개체가 갈림. SDK 문서(class.rst/HelpCenter)는 액션·프레임 '메커니즘'만 정의하고,
> 개체별 지원은 카탈로그 데이터에 달려 있어 **실행 로그(R0 값·렌더 여부)가 최종 진실.**

---

## 5. 지상(이벤트) 쇼 표준 골격 — 참고

일식/특정 날짜·장소 하늘: `reset` → 지구 setIntensity(1)+setAtmosphereIntensity(1) + 태양 setIntensity(1)
+ Place2D 관측지 + setDateTime(UT!) + **setTargetHeight(30)+setOrientationH(180−방위)** 조준.
클로즈업은 **setScale**(카메라 이동 명령 전부 무효). 예제: eclipse_2026_target30.

---
세부·enum·SPC cmd 는 CLAUDE.md, docs/16~19 참조. 스크립트: scripts/study/.
