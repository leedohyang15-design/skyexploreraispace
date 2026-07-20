# 학습 노트 ⑭ — 예제: 달의 아날렘마 (낮/밤이 지나며 관측)

> 과제: 달의 아날렘마를 낮과 밤이 지나면서 관측하는 시뮬레이션.
> 정답은 **SPC**(RSA COSMOS mini-scene). 요청대로 **Python**으로 이식.
> 스크립트: [`scripts/moon_analemma.py`](../scripts/moon_analemma.py)
> 근거 도움말: [`reference/help/Analemma.md`](../reference/help/Analemma.md)

## ✅ 성공 (ST 실측 확인)

HUD `Earth, Analemma` 상태에서 **노란 물방울(teardrop) 궤적 = 달의 아날렘마**가
돔에 정상적으로 그려짐. 달(회색 점)이 궤적 위를 이동. 관문별로 이름/시그니처를
하나씩 잡아 완성:
1. `Place2DName` = `Place2D001` (ST 에러가 정확한 이름 제공)
2. `Place2DPort` = `dir()` 자동탐색으로 해결
3. `Camera.setPositionXYZ(Vec3, Anim, int)` — 가운데 `Anim` 필수 (누락 시 ArgumentError)
4. `setAnalemmaRotationPeriod`(항성월 27.321661) → Analemma 포트 전환 → 28일 진행

→ 최종 스크립트: [`scripts/moon_analemma.py`](../scripts/moon_analemma.py) (동작 검증됨).

## ⭐⭐ 결정적 발견 — 이 Python SDK엔 'Analemma 포트'가 없다

SPC(Editor)는 **Analemma 포트**(관측자를 Earth Analemma 포트로 전환)로 구현하지만,
**Python SDK 레퍼런스 전수조사 결과 `Planet.PlanetPort`에 `Analemma`가 없음**
(전 70클래스 통틀어 "Analemma"는 `DateManager.MotionType.MotionAnalemma` 하나뿐).
→ 포트 전환 시도는 계속 실패, HUD가 `Equatorial Sync`로 남아 **매일의 궤적 '호'가
겹쳐 쌓인** 그림만 나옴(아날렘마 아님).

✅ **정답 = `DateManager` 아날렘마 시간모드** (도움말도 "시간모드 쓰면 포트 불필요"):
```python
dm = DateManager()
dm.setMotionType(DateManager.MotionType.MotionAnalemma)  # 자전 취소
dm.setDateTime(끝날짜(+30일), ..., Anim(30))              # 한 달 진행 → 고리 완성
```
- 효과: 지구 자전을 취소 → **매일 같은 시각의 달 위치가 한 점** → 30일이 이어지며
  단일 궤적선(아날렘마 고리)으로 그려짐. 여러 호가 하나로 합쳐지면 정상.
- **교훈**: SPC(Editor) 명령이 Python SDK에 1:1로 있으리란 보장 없음. 포트/메서드가
  없으면 **같은 결과를 내는 다른 메커니즘**(여기선 시간모드)을 레퍼런스에서 찾을 것.
- **시점**: 지상뷰라 카메라가 지평선을 보면 아날렘마가 가장자리에 걸림 →
  `setOrientationHPR(Vec(방위, 고도, 0))`로 아날렘마(남쪽 하늘)를 올려다보게(파라미터
  `VIEW_HEADING`/`VIEW_PITCH`).

## (참고) SPC가 쓴 아날렘마 좌표계(Analemma 포트)의 원리

- **적도동기(EquatorialSynchronous)와 같지만 '자전을 따르지 않는' 프레임.**
  관측자를 이 포트에 두고 시간을 흘리면, 천체의 자전을 무시한 채 **설정 주기로
  천체 중심 둘레를 돈다** → 자전/날짜를 조작하지 않고 아날렘마를 그릴 수 있음.
- **기본 회전주기 = 천체 공전주기**(지구=1년). `Analemma Rotation Period` 로 수동 설정 →
  **태양 대신 위성(달)에 동기화** 가능. ★ 이 예제의 핵심: 주기를 **달 항성월
  27.321661일**로 두어 달의 아날렘마를 만듦.
- ⚠️ 주기 변경은 포트에 즉시 반영(붙은 관측자도 이동) → **관측자 붙이기 전에 주기부터** 설정.
- 자전이 실제 속도로 돌아 관측자가 지면과 충돌/지하 진입할 수 있음 → **지형 평탄화
  (Elevation 0)** 필수. 끝나면 복원.

## SPC → Python 대응 (핵심)

| SPC 명령 | Python | 상태 |
|----------|--------|------|
| `SceneGraph Add 2DPlace (Earth, Equatorial Sync)` | `Place2D(...).setParent(Earth.portId(EquatorialSynchronous))` | 확인 |
| `2DPlace Position lon/lat/alt` | `setLongitude/setLatitude/setAltitude` | ✅ |
| `ObsPos Body:2DPlace Port:Place` | `cam.setPositionXYZ(Vec(0,0,0), place.portId(Place))` | 확인 |
| `Date 2017-12-06 12:30` | `DateManager().setDateTime(y,m,d,h,mi,s,tz,Anim())` | ✅ |
| `Satellite Trajectory Intensity Moon 1` | `Satellite(Moon).setTrajectoryIntensity(1, Anim(.5))` | ✅ |
| `Star Size Sun 3` / `Satellite Size Moon 3` | `IndividualStar(Sun).setScale(3)` / `Satellite(Moon).setScale(3)` | ✅ |
| `Planet Analemma Rotation Period Earth 27.321661` | `Earth.setAnalemmaRotationPeriod(27.321661)` | 확인(세터명) |
| `ObsPos [Relative] Earth Port:Analemma (0,0,0)` | `cam.setPositionLBR(Vec(0,0,0), Earth.portId(Analemma))` | 확인(포트명) |
| `Planet Terrain Elevation Factor Earth 0` | `Earth.setElevationScale(0)` | ✅ |
| `Date [Relative] Day:28 Inertial Evolution` | `setDateTime(시작+28일, Anim(28))` (타임랩스) | ✅ |

## ST 실측 결과 & 이름 자동탐색

- ⭐ **ST 런타임 확인: `Place2DName` 은 `Place2D001` 형식**(`Place2D_1` 아님 —
  AttributeError가 "Did you mean: 'Place2D001'?"로 알려줌). InsertText001 과 동일한
  `이름+3자리` 패턴.
- 나머지 불확실 이름(`Place2DPort.Place`, `PlanetPort.Analemma`, 주기 세터,
  `UTC+10:30` TimeZone)은 크래시 방지를 위해 **`dir()` 기반 자동탐색**으로 전환:
  - `_find_enum(cls, *후보, contains=/prefix=)` : 후보 실패 시 dir(cls)에서 부분문자열/접두어로 탐색.
  - `_find_method(obj, *후보, contains_all=[...])` : dir(obj)에서 키워드 모두 포함 메서드 탐색.
  → ST가 실제 갖고 있는 멤버명을 스스로 찾아 쓰고, 찾은 이름을 콘솔 `[auto]`로 출력.
- ✅ **검증**: 목 SDK 드라이런에서 전 시퀀스가 SPC와 일치하고 런타임 에러 0
  (주기 설정 → Analemma 포트 전환 순서, +28일=2018-01-03 계산 확인).

## ⚠️ 시그니처 함정 (ST 실측)

- **`Camera.setPositionXYZ(Vec3 value, Anim anim, int track)`** — `setPositionLBR`
  과 동일하게 **가운데 `Anim` 인자 필수**. 빠뜨리면 `Boost.Python.ArgumentError`.
  (목 드라이런은 인자를 다 받아줘서 이런 C++ 타입 불일치는 **실제 ST에서만** 드러남.)
- 위치/크기/각도 세터 다수는 `Anim` 이 optional 이지만, `setPositionXYZ/LBR/R/L/B`
  같은 **track 인자를 받는 것들은 `(value, Anim, track)`** 로 anim 이 필수 위치.

## 검증된 새 API (이번에 습득)

- `IndividualStar(IndividualStar.IndividualStarName.Sun)` — 태양=별. `setScale`로 크기.
- `Satellite(SatelliteName.Moon)`: `setTrajectoryIntensity`(궤적선), `setScale`(크기).
- `Planet.setElevationScale(0)` — 지형 평탄화.
- `DateManager().setDateTime(...)`에 **Anim 을 주면 날짜 타임랩스**(중간 날짜 보간).
- `DateManager.MotionType.MotionAnalemma` — 포트 없이 아날렘마 시간모드(대안).

## 연출 의미

Analemma 포트(주기=항성월)에서 달은 화면에 머물며 **아날렘마 8자/타원**을 그리고,
그 배경으로 **태양이 뜨고 지며 낮/밤 28회**가 빠르게 지나간다 = "낮과 밤이 지나며
달의 아날렘마 관측".
