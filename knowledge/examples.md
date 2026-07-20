# 자연어 → Sky Explorer Python 변환 예제 (검증된 스크립트 기반 few-shot)

아래 예제들은 전부 **Studio 실측으로 검증된 패턴**이다. 새 요청도 이 패턴을 조합해서 생성할 것.

⚠️ 예제의 천체는 견본일 뿐이다. 사용자가 다른 천체를 말하면 반드시 그 천체로 치환한다.
⚠️ 사용자가 "방금/이 코드 수정해줘" 라고 하면 예제가 아니라 **대화의 직전 코드**를 기준으로 고친다.

---

## 예제 1
**요청**: "토성으로 가서 크게 보여줘"

```python
from skyExplorer import *
from studio import *
from Initialization import *

# 관측자 바인딩 해제 (FadeTo 잠김 방지)
try:
    SceneGraph().reset(1)
except Exception:
    pass
sleep(1.0)

uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))         # ★ 암전 — 도착·정렬 슬루를 관객이 못 보게
saturn = Planet(Planet.PlanetName(5))          # 5 = Saturn
saturn.setIntensity(1.0, Anim(0.0))

# ① FadeTo + 돔 중앙 정렬 (전부 암전 속에서)
DataManager.database().data(Data.Type.PlanetType, "Saturn").action(Action.Type.FadeTo).trigger()
sleep(4.0)                                     # FadeTo 도착 대기 (기본 구도는 하단 30°)
cam = Camera(Camera.CameraName.MainCamera)
cam.setTargetHeight(30.0, Anim(1.5))           # 🎯관람 정위치 = Target 30 (운영 표준)
sleep(2.0)                                     # 정렬 슬루 완료 대기

# ② 페이드인 — 처음부터 중앙에 정렬된 채 등장
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))
sleep(3.0)

# ③ 화면 고정 줌 — R "만" 변경 (track=-1 = 현재 프레임 유지)
p = cam.positionLBR                            # R 단위 = 행성반지름 (절대값 금지)
cam.setPositionR(p.z * 0.5, Anim.cubic(4.0), -1)
sleep(4.5)
```

---

## 예제 2 — ✅ 사용자 실측 확인(2026-07-06): 지상 하늘(낮·밤·타임랩스) 표준 골격
**요청**: "청주의 하루(아침→낮→석양→밤)를 보여줘"

```python
from skyExplorer import *
from studio import *
from Initialization import *

def to_ut(y, m, d, hh, mm):        # ★ DefaultTimeZone = UTC! 한국시(KST)는 -9h 변환
    h = hh - 9
    if h < 0: h += 24; d -= 1
    return y, m, d, h, mm

try:
    SceneGraph().reset(1); sleep(1.5)
except Exception:
    pass
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))              # 암전 세팅

place = Place2D(Place2D.Place2DName(0))
place.setPosition(Vec(36.64, 127.50, 100.0))        # (위도, 경도, 고도)

# ★★ 지상 낮 하늘 체크리스트 — 하나라도 빠지면 하늘이 검게 나옴!
earth = Planet(Planet.PlanetName(2))
earth.setIntensity(1.0, Anim(0.0))                  # ① 지구 본체(마스터 스위치)
earth.setAtmosphereIntensity(1.0, Anim(0.0))        # ② 대기(레일리 산란 = 파란 하늘)
earth.setScatteringIntensity(1.0, Anim(0.0))
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))  # ③ 광원
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))   # 별 상시 ON — 낮엔 대기가 가림

dm = DateManager()
tz = getattr(DateManager.TimeZone, "DefaultTimeZone")
y, m, d, h, mi = to_ut(2026, 7, 6, 6, 30)           # 아침 6:30 KST
dm.stop(); sleep(0.3)                                # ★ stop 을 먼저! (뒤에 부르면 취소됨)
dm.setDateTime(y, m, d, h, mi, 0, tz, Anim(0.5)); sleep(1.5)

Camera(Camera.CameraName.MainCamera).setTargetHeight(30.0, Anim(1.5))  # 관람 표준
sleep(2.0)
uni.setGlobalIntensity(1.0, Anim.cubic(2.5)); sleep(5.0)   # 아침 하늘 등장

# 시간 가속: 정오 → 석양 → 밤 (setDateTime+Anim = 부드러운 타임랩스)
for kst in ((12, 0), (19, 40), (21, 30)):
    y, m, d, h, mi = to_ut(2026, 7, 6, kst[0], kst[1])
    dm.setDateTime(y, m, d, h, mi, 0, tz, Anim(8.0))
    sleep(8.5); sleep(4.0)
```

---

## 예제 3 — ✅ 사용자 실측 확인(2026-07-06): 성운 여행 쇼의 표준 골격
**요청**: "말머리성운까지 여행하는 쇼 만들어줘"

```python
from skyExplorer import *
from studio import *
from Initialization import *

PC = 3.086e13                                   # 1 파섹(km)

try:
    SceneGraph().reset(1)
    sleep(1.5)
except Exception:
    pass
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))          # 암전에서 세팅 → 슬루 숨김

Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
horse = Nebula(Nebula.NebulaName.HORSEHEAD)     # 성운은 '이름' enum (숫자 인덱스는 id=-1!)
horse.setIntensity(1.0, Anim(0.0))
Nebula(Nebula.NebulaName.ORION).setIntensity(0.5, Anim(0.0))

cam = Camera(Camera.CameraName.MainCamera)
los = horse.portId(Nebula.NebulaPort.LineOfSightLocal)
cam.setPositionLBR(Vec(0.0, 0.0, 400.0 * PC), Anim(), los)          # 400pc = 지구 시점
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(1.0), los)  # 조준+세우기 (look)
cam.setTargetHeight(30.0, Anim(1.0))            # 🎯관람 정위치(운영 표준 30)
sleep(4.0)

uni.setGlobalIntensity(1.0, Anim.cubic(2.0))    # 페이드인
sleep(5.0)

cam.setPositionR(10.0 * PC, Anim.cubic(18.0), los)   # 10pc 까지 비행 (2pc는 아트 내부라 금지)
sleep(18.5)

# 도착 재정렬 (비행 중 미세 드리프트 정리 — setTargetHeight 같은값 no-op 우회)
cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(2.0), los)
cam.setTargetHeight(29.9, Anim(0.3)); sleep(0.4)
cam.setTargetHeight(30.0, Anim(0.5)); sleep(2.0)
```

---

## 예제 4(구 5)
**요청**: "지구를 돔 한가운데 놓고 두 배 확대해줘"

```python
from skyExplorer import *
from studio import *
from Initialization import *

def goto_planet(name, wait=4.0):
    DataManager.database().data(Data.Type.PlanetType, name).action(Action.Type.FadeTo).trigger()
    sleep(wait)

def center_dome(cam, height=30.0, settle=2.0):   # 🎯운영 표준 30 (90=천정, 관람 부적합)
    cam.setTargetHeight(height, Anim(1.5))
    sleep(settle)                                # 정렬 슬루 완료 대기

def zoom(cam, scale, duration):
    p = cam.positionLBR
    cam.setPositionR(p.z * scale, Anim.cubic(duration), -1)   # R만 변경 = 화면 고정 줌
    sleep(duration + 0.5)

try:
    SceneGraph().reset(1)
except Exception:
    pass
sleep(1.0)
uni = Universe(Universe.UniverseName.MainUniverse)
uni.setGlobalIntensity(0.0, Anim(0.0))           # ★ 암전 — FadeTo·정렬은 관객이 못 보게
earth = Planet(Planet.PlanetName(2))
earth.setIntensity(1.0, Anim(0.0))
earth.setCloudsIntensity(0.6, Anim(0.0))
earth.setAtmosphereIntensity(1.0, Anim(0.0))

cam = Camera(Camera.CameraName.MainCamera)
goto_planet("Earth")
center_dome(cam)                                 # 여기까지 전부 암전 속
uni.setGlobalIntensity(1.0, Anim.cubic(2.5))     # 중앙 정렬된 채 페이드인
sleep(3.0)
zoom(cam, scale=0.5, duration=6.0)
```

---

## 예제 5(구 6) — ✅ 사용자 실측 확인(2026-07-06): 회전/공전(오빗)의 유일한 검증 패턴
**요청**: (직전 턴에서 말머리성운 코드를 받은 뒤) "이 코드에 확대랑 한 바퀴 도는 회전 추가해줘"

→ 직전 코드의 천체(`horse`)와 트랙(`los`)을 **그대로 유지**하고, 끝에 아래 블록만 붙인다.
회전 = **스텝 오빗**: 0.5초 스텝으로 L 을 증가시키며 4스텝마다 재조준(중앙 유지).
(시간가속 자전, orientation 루프, AdvancedCamera.move/roll 은 전부 실측 실패 — 금지)

```python
# ── 확대: 상대 줌 (읽은 R × 배율 — 절대값 금지) ──
R_VIEW = 10.0 * PC                               # 현재 프레이밍 거리
cam.setPositionR(R_VIEW * 0.5, Anim.cubic(6.0), los)   # 절반 거리 = 2배 확대
sleep(6.5)
R_VIEW = R_VIEW * 0.5

# ── 풀 공전: 한 방향 360° — 스텝마다 재조준으로 중앙 유지 ──
ORBIT_DEG = 360.0
ORBIT_SEC = 36.0
step_dt = 0.5
n = int(ORBIT_SEC / step_dt)
for i in range(1, n + 1):
    L = ORBIT_DEG * i / float(n)
    cam.setPositionLBR(Vec(L, 0.0, R_VIEW), Anim(step_dt), los)
    if i % 4 == 0:                               # 2초마다 재조준(중앙 유지)
        cam.setOrientationSmoothXYZR(Vec4(0.0, 0.0, 0.0, 0.0), Anim(step_dt), los)
    sleep(step_dt)
```

※ 행성(FadeTo 상태)에서 같은 요청이면: track 은 `-1`(현재 프레임 유지)을 쓰고
   재조준은 `setTargetHeight(29.9→30)` no-op 우회로 한다. 성운의 `los` 같은
   포트 트랙을 행성에 새로 넘기면 프레임이 바뀌어 카메라가 튄다.
