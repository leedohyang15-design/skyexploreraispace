# 학습 노트 ⑫ — 예제: 말머리 성운 줌인 + 좌우 회전

> ⚠️ **이 노트의 일부 결론은 추측이었고 ST 실측으로 교정됨.**
> 실제 실행 관찰 기반 최종 방식·교정표는 **[노트 ⑬ 실측 로그](./13_sim_log_horsehead.md)** 참조.
> 요약 교정: (1) `setZoomPosition` 줌 락은 방향을 '잠그는 문제'가 아니라 **엔진이
> 자동 재조준**해 공전 중 중앙을 유지하는 **정답**이다. (2) "축으로 돈다"는 롤이
> 아니라 줌 락 위에서 **베이스 위치 L 스윙**. (3) 근접 360°는 뒷면(검은 실루엣)
> 통과 → **정면 스윙 ±75°**. 아래 본문은 그 과정에서의 탐구 기록으로 남겨둠.


> 과제: 말머리 성운(Horsehead / Barnard 33)으로 점차 줌인 → 도달하면 화면이 좌우로 회전.
> 정답은 **SPC(Editor)** 형식이지만 요청대로 **Python**으로 구현.
> 내 작성: [`scripts/zoom_horsehead.py`](../scripts/zoom_horsehead.py) (Python, 주 구현)
> 참고: [`scripts/zoom_horsehead.spc.txt`](../scripts/zoom_horsehead.spc.txt) (SPC 형식 재구성)

## ✅ 정답(SPC) 대조 — SPC 값을 그대로 복제

| 요소 | 정답 SPC | 내 Python(복제) | 일치 |
|------|----------|-----------|------|
| 대상 프레임 | `Port: LOS Local` (Barnard 33) | `Nebula(HORSEHEAD).portId(LineOfSightLocal)` | ✅ |
| 시작 위치/방향 | `ObsPos L:0 B:0 R:1.9e14` + `ObsOri 0,0,0,0` | `setPositionLBR(Vec(0,0,1.9e14))` + `setOrientationXYZR(0,0,0,0)` | ✅ |
| 줌 1단(가속) | `ObsPos R:3e12 Dur12 Exponential` | `setPositionR(3e12, Anim.exp(12))` | ✅ |
| 줌 2단(감속정지) | `ObsPos R:4e10 Dur8 Quintic` | `setPositionR(4e10, Anim.cubic(8))` | ✅ (Quintic→cubic) |
| 좌우 회전 | `ObsPos [Relative] L:360 Dur120` | `setPositionL(360, Anim.cubic(120))` | ✅ |
| 성운 표시 | `SkyEx Nebula Intensity Barnard 33` | `Nebula(HORSEHEAD).setIntensity(1)` | ✅ |
| 배경 | Milky Way, M42(Orion Nebula) | Galaxy MilkyWay, Nebula ORION | ✅ |

## ⭐ 이번에 확정한 두 핵심 (반복 삽질에서 얻음)

1. **줌 = "중앙 고정 후 R만" — 방향을 줌 중에 재조준하면 안 됨.**
   방향(ObsOri)을 **시작에 딱 한 번** 정중앙(`0,0,0,0`)으로 잡고, 줌 단계에선
   `setPositionR`(R만) 호출. 줌 도중 `setOrientation…`을 또 부르면 프레임이
   미세하게 드리프트해서 말머리가 화면 밖으로 밀림. → **처음 중앙 = 끝까지 중앙.**
2. **"작게 보임"의 진짜 원인은 최종 R.** SPC 최종 `R:4e10 km`(≈0.0013 pc)이
   화면을 가득 채우는 근접값. 예전 `R_END=4e13`(≈1.3 pc)은 **1000배 멀어서** 작았음.
   → 크기는 **최종 R 로만** 결정. SPC 는 **2단**(3e12 가속 → 4e10 감속정지)으로
   자연스러운 "빨려들어갔다 스르르 멈춤"을 만듦.

→ 정답도 **"LOS Local 프레임에서 방향 한 번 고정 → R 2단 줌 → L 돌려 팬"** 전략.
오리온에서 배운 '대상 프레임 접근 = 우주 시점' 원리가 그대로 통함.

## ⚠️ 결정적 함정 — `setOrientationXYZR(0,0,0,0)`은 천체를 안 봄

스크린샷 진단: `LOS Local, L:0 B:0, R:~9만 AU` 인데도 말머리가 **화면 아래
구석에 작게** 있었음. 위치(시선축)는 맞지만 **방향**이 틀림.
- `setOrientationXYZR(Vec4(0,0,0,0))` = 프레임 **기본축(접선)** 을 봄 → 천체가
  화면 밖으로 밀림. 줌해도 그 어긋난 화면 위치에서 커지기만 함
  (= "구석에 작게"의 진짜 원인. 거리·R 문제가 아니었음).
- ✅ **해결 = 우리가 저장한 정중앙 스킬 재사용**: `B=90` 위치 +
  `setTarget(Vec2(0, 125))`. 이 recipe 가 천체를 **돔 정중앙**에 놓음.
  방향은 시작에 한 번만 잡고(=target 고정) 줌 중엔 `setPositionR`(R만) 호출.

## ⭐ 최종 방식 — 수동 LBR 조준 포기, `setZoomPosition` 으로 확정 중앙

성운 LOS Local 프레임의 **수동 조준은 불안정**했음(2연속 실패):
- `setOrientationXYZR(0,0,0,0)` → 천체 안 봄, 화면 아래 구석.
- 정중앙 스킬(`B=90` + `target 125`) → 위치가 극점으로 튀어 성운 **속**으로
  (HUD `B:71°, R:88848 km` = 먼지 구름 바로 앞). 행성용 스킬이 성운엔 안 맞음.

✅ **오리온에서 검증된 방식으로 확정**:
```python
horse_track = horse.portId(Nebula.NebulaPort.Ecliptic)
cam.setZoomFormula(Camera.ZoomFormula.GreatCircle)
cam.setZoomFov(120, Anim())
cam.setZoomPosition(Vec(0,0,0), horse_track, Anim(1), Camera.PositionMode.XYZ)  # 중앙 확정
cam.setZoomFov(12, Anim.cubic(12))   # 넓게→좁게 = 점진 줌인
```
→ 엔진이 천체를 **화면 정중앙**에 잡고 확대. 회전은 `AdvancedCamera().roll()`
  (말머리 중앙 고정, 화면만 좌우 회전).

**교훈**: 특정 천체 프레임의 수동 orientation/target 은 프레임마다 규약이 달라
  깨지기 쉬움. "천체를 화면 중앙에 크게" 가 목적이면 **`setZoomPosition`(대상 트랙)
  + `setZoomFov`** 가 프레임 독립적이고 확실함(별=오리온, 성운=말머리 둘 다 성공).

## 참고: R 단위 (LOS Local)
HUD 는 AU/km 를 크기에 따라 자동 전환 표시. 큰 값=AU(예 91919 AU), 작은 값=km
(예 88848 km). 입력 스케일 헷갈리기 쉬움 → 위 zoom 방식은 R 스케일과 무관해 안전.

## ⚠️⚠️ 최중요 순서 함정 — `setOrientationR` 는 '줌인 끝난 뒤'에만

`setZoomPosition` 의 조준은 **베이스 카메라 방향(H/P) 위에 얹힘**. 그래서
`setOrientationR` 을 **줌 전/도중**에 부르면 H/P 가 리셋돼 말머리 '반대쪽'을
보며 줌인하는 참사(2회 발생). ✅ 규칙:
- **줌인 구간(위치·조준·FOV)에서는 롤을 절대 건드리지 않는다** = 예전 성공판 그대로
  정면·중앙·크게.
- **똑바로 세우기(ROLL_FIX)·회전은 줌인이 끝나 조준이 말머리에 락된 '뒤'에만**
  호출 → 이때는 H/P 가 말머리에 고정돼 있어 롤만 적용됨.

## ✅ 최종 해법 — 즉시 LOS Local 진입 + pitch 중앙 + L 공전

FadeTo 는 말머리 LOS Local 프레임 진입엔 성공했지만 (a) 날아가는 모션이
'일렁임', (b) 멀고(38.9pc) 아래로 치우침. → **FadeTo 없이 직접 제어가 더 나음**:
- **즉시 조준(일렁임 0)**: `setPositionLBR(Vec(0,0,R), Anim(), LOSLocal)` +
  `setOrientationP(PITCH, Anim())` 로 실행 즉시 말머리 정면·중앙. (FadeTo 제거.)
- **중앙정렬**: LOS Local 은 L:0 B:0 에서 말머리가 화면 '아래'에 옴 → `setOrientationP`
  (pitch)로 시선 내려 중앙. (줌 락 아니므로 orientation 제어 먹힘.)
- **줌인**: `setPositionR(작게, Anim.exp)` = 접근(중앙 유지).
- ⭐ **"말머리를 축으로 돈다" = 공전(orbit), 롤 아님**:
  `setOrientationR`(롤)은 제자리 핀휠 회전(반시계 빙글)이라 오답.
  정답은 **`setPositionL(+360)`** = 말머리 둘레 공전(SPC `ObsPos [Relative] L:360`).
  배경이 좌우로 흐르고 말머리는 중앙 → "말머리를 축으로" 도는 것.

## (참고) FadeTo 로 프레임 진입 (대안)

`setZoomPosition`(줌) 상태에선 **화면 방향(롤/업)이 완전히 잠김**:
`setOrientationR` 은 락을 깨서 엉뚱한 축, `AdvancedCamera().roll()` 은 무시됨
(speed 키워도 무반응). → **줌 방식으론 "세우기·회전"이 구조적으로 불가.**
장점(크고 선명한 FOV 줌인)은 있으나 방향 제어 불가가 치명적.

✅ **FadeTo(고수준 액션)로 전환** (Data.Type.NebulaType):
```python
d = DataManager.database().data(Data.Type.NebulaType, "Barnard 33 (Horsehead Nebula)")
d.action(Action.Type.FadeTo).trigger()   # 날아가 자동으로 똑바로·중앙 프레이밍
```
- 도착 후엔 **일반 카메라 상태** → `adv.roll()`/`setOrientationR` 회전 정상.
- Action.Type 에 `FadeTo/GoTo/StraightGoTo/LookAt` 존재. 이름 매칭이 변수 →
  HUD 표기('Barnard 33 (Horsehead Nebula)')를 1순위로 후보 순차 시도.
- ⚠️ `data()` 결과·`action()` 결과 None 가드 필수(오리온 때 None.trigger 크래시).

## (참고) 줌 방식의 회전 시도 기록 = `AdvancedCamera().roll()` (setOrientationR 금지)

- ❌ **`setOrientationR` 은 `setZoomPosition` 락과 양립 불가**: 줌 전에 부르면
  말머리 반대쪽을 봄, 줌 후에 부르면 락을 '취소'하고 베이스 카메라를 노출해
  **엉뚱한 축으로 회전**. 실측 2회 확인 → 줌 시나리오에선 아예 사용 금지.
- ✅ **회전은 `adv.roll(speed)`**: 카메라를 굴려 **줌 중심(말머리) 기준**으로 화면
  회전. 줌 락을 안 깨므로 말머리가 축이 됨. `sleep(t)` 후 `adv.stop()`.
  (전에 '안 됨'은 speed 0.15 로 너무 작았던 것 → 6~12 로.)
- **화면 기울기(세우기)도 roll 이 유일 수단**(base orientation 은 락을 깸).
- **크기**: 좋은 프레이밍 = `zoomFov ≈ 1.0`(실측). 더 크게=값↓.

## SPC 형식 이해 (학습)

- **타임라인 기반**: 각 행 = `Timecode | 명령 | 파라미터`. 명령은 지정 시각에 실행.
- **관측자 제어**: `SkyEx ObsPos`(위치 LBR), `SkyEx ObsOri V3`(방향). Python의
  `Camera.setPositionLBR`/`setOrientation*`에 대응.
- **대상 좌표계**: `Port: LOS Local`(=LineOfSightLocal, 성운 시선 프레임) — 깊은하늘 접근용.
  Python의 `Nebula.portId(NebulaPort.LineOfSightLocal)`에 대응.
- **연출**: `Duration` + `Interpolation`(Linear/Exponential/Inertial/Quintic/Inertial Evolution)
  + `Acceleration`/`Deceleration`. Python의 `Anim.cubic/exp/...(duration)`에 대응.
- **매크로**: `SHOW Macro File: X.SPC`(다른 스크립트 병렬 호출), `SHOW End`(실행창 유지).

## 내 풀이 흐름

| 단계 | 명령 | 의도 |
|------|------|------|
| 0 초기화 | `SHOW Macro common_off.SPC` | 기본 요소 끄기 |
| 1 로드 | `Nebula Intensity Barnard 33 = 1`, Milky Way, M42 | 말머리+배경 |
| 2 서베이 | `Sky Survey URL / Intensity(0)` | 근접용 고해상 이미지 준비 |
| 3 시작 | `ObsPos LOS Local R=1.9e14`(멀리) + `ObsOri` | 말머리 원경 정면 |
| 4 밝히기 | `SHOW Macro common_on.SPC` | 페이드 인 |
| 5 **줌인** | `ObsPos R: 크게→작게` Duration 12 **Exponential** → 8 **Quintic** | 가속 접근 후 감속 정지 |
| 6 **좌우 회전** | `ObsPos [Relative] L: 360` Duration 120 **Inertial Evolution** | 도달 후 방위 L 을 천천히 돌려 팬 |

## 핵심 개념 매핑 (Python ↔ SPC)

| 목적 | Python | SPC |
|------|--------|-----|
| 성운으로 줌인 | `setPositionLBR(Vec(0,0,R↓), Anim, nebulaLOStrack)` | `SkyEx ObsPos ... Port: LOS Local R:↓ Duration Interpolation` |
| 좌우 팬 | `setOrientationHPR` / L 회전 | `SkyEx ObsPos/ObsOri [Relative] L: 360 Inertial Evolution` |
| 성운 표시 | `Nebula(...).setIntensity(1, Anim)` | `SkyEx Nebula Intensity Body Intensity` |
| 고해상 | `SkySurvey` | `SkyEx Sky Survey URL/Intensity` |

## 메모 / 불확실성
- SPC 정확한 명령명/파라미터 순서는 정답 스크린샷 어휘 + 도움말(MacroCommands) 기반 재구성.
  실제 Editor에선 명령 팔레트에서 골라 값 입력(수동). 이 파일은 그 논리적 시퀀스.
- R 값 스케일(1.9e14 등)은 LOS Local 프레임 거리 단위 추정 — 실행하며 조정 필요.
- "좌우 회전"은 방위 L 회전(orbit-pan)으로 해석. 순수 시선 회전이면 ObsOri 사용도 가능.
