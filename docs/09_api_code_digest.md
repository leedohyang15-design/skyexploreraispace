# 학습 노트 ⑨ — Sky Explorer API 코드 다이제스트 (전체 70클래스)

> 코드 중심 정리. 전체 시그니처는 `reference/api/<Class>.md`, 개념 설명은 `reference/help/`.
> 규모: **70 클래스 / 932 메서드**. 여기선 "어떻게 코드로 쓰는가"에 집중.

---

## 0. 공통 코드 패턴 (모든 클래스에 반복됨)

```python
from skyExplorer import *      # 천체/그래픽/수학 클래스
from studio import *          # 카메라 모드/DB/액션 (AdvancedCamera, DataManager, Data, Action)
from Initialization import *  # smoothReset 등

# (1) 객체 생성: Class(Class.<Class>Name.<Value>)
p = Planet(Planet.PlanetName.Saturn)
s = Stars(Stars.StarsName.StarrySky)

# (2) 문자열 이름 → enum : getattr
p = Planet(getattr(Planet.PlanetName, "Saturn"))

# (3) 밝기 등 setter 공통 형태: setXxx(value, Anim(duration))
p.setIntensity(1.0, Anim(2.0))         # 2초 전환
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(1.0))

# (4) Anim: 즉시=Anim(), 시간=Anim(t) 또는 정적 팩토리 Anim.cubic(t)/Anim.exp(t)...

# (5) 기준 좌표계 id(track): <body>.portId(<Class>.<Class>Port.<Value>)
track = p.portId(Planet.PlanetPort.EquatorialSynchronous)

# (6) 카메라
cam = Camera(Camera.CameraName.MainCamera)      # 단 하나의 메인 카메라
cam.setTarget(Vec2(azimuth, height), Anim(d))   # 궤도/트랙볼 조준
cam.setPositionLBR(Vec3(L, B, R), Anim(d), track)
AdvancedCamera().setModeFreeFly()               # 모드 전환(무인자)

# (7) DB 네비게이션(고수준 이동)
obj = DataManager.database().data(Data.Type.PlanetType, "Saturn")
obj.action(Action.Type.FadeTo).trigger()
```

---

## 1. 카메라 / 장면 (studio + skyExplorer)

| 클래스 | 생성 | 핵심 메서드 | 메모 |
|--------|------|-------------|------|
| `Camera` (36m/46p) | `Camera(CameraName.MainCamera)` | `setTarget(Vec2)`, `setTargetAzimuth/Height`, `setPositionLBR/L/B/R(...,track)`, `setPositionXYZ`, `setOrientationHPR(Vec3)`/`HPRD(Vec4,track)`, `setZoomFov`, `setZoomPosition`, `addChild(id,CameraPort)`, `portId` | 조준 2계열: `setTarget`(트랙볼) vs `setOrientationHPR`(고개돌리기). CameraPort={FixedBackground,Background,FixedForeground,Foreground} |
| `AdvancedCamera` (10m) | `AdvancedCamera()` | `setModeFreeFly`, `setModeTerrainView`, `setGuessMode`, `toggleFreeFlyMode`, `takeOffOn`, `move(Vec2)`, `zoom/tilt/roll(speed)`, `stop` | 모드/연속이동. move/zoom 등은 stop 까지 지속 |
| `Universe` (6m) | `Universe(UniverseName.MainUniverse)` | `setGlobalIntensity(f,Anim)`, `setGamma(Vec3)`, `object2objectMatrix` | 전체 씬 밝기/감마 |
| `SceneGraph` (7m) | `SceneGraph()` | `reset(int reinitId)` | 전체 시스템 리셋(smoothReset 보다 강함) |

## 2. 천체 (밝기·궤도·좌표계 port 공통)

공통: 생성 `Class(<Class>Name.X)`, `setIntensity(f,Anim)`, `portId(<Class>Port.X)`.

| 클래스 | 특이 메서드 | port 종류(요약) |
|--------|-------------|-----------------|
| `Planet` (134m) | `setOrbitIntensity`, `setRingModel`, `setEquatorial*Intensity`(격자/자오선/극), `setTilesetIntensity`, 좌표망 다수 | Ecliptic/Equatorial/**EquatorialSynchronous**/Galactic/OrbitalMeanEquinox/EquatorialJ2000/Noon* |
| `DwarfPlanet` (33m) | Planet 축소판 | Planet 과 동일 |
| `Satellite` (70m) | 궤도/트레일 다수 | EquatorialSynchronous/Galactic/EquatorialJ2000/Equatorial/Noon*/OrbitalMeanEquinox |
| `Asteroid`(18) `Comet`(17) | 궤도요소(`setArgumentOfPeriapsis` 등) | TerrestrialEquatorialJ2000/EclipticJ2000/OrbitalMeanEquinox/**Synchronous**/Galactic |
| `IndividualStar` (33m) | `setIntensity`, `heightOnDome`(Sun만) | **Ecliptic** 만 |
| `Stars` (27m) | `setIntensity`(별 카탈로그), `intensity`(조회) | Ecliptic/TerrestrialEquatorialJ2000 |
| `Galaxy` (20m) | `setIntensity` | **Galactic** 만 |
| `Constellation` (7m) | ⚠️ `setIntensity` 없음 → `setLinesIntensity`/`setLabelIntensity`/`setArtIntensity`/`setLimitsIntensity` | - |
| `Nebula`(7) `Messier`(6) `NGC`(6) `GlobularCluster`(7) | `setIntensity` | Ecliptic/LineOfSight*/Galactic |
| `ShootingStar`(13) `Bolide`(8) | 유성/화구 | - |
| `OrbitalPlace`(20) `Place3D`(8) `Body` | 궤도상 위치/천체 베이스 | - |
| `SkySurvey`(2) `Patch`(6) | 하늘 서베이/패치(WMS) | - |

## 3. 시간

| 클래스 | 생성 | 핵심 메서드 |
|--------|------|-------------|
| `DateManager` (12m) | `DateManager()` | `setDateTime(y,mo,d,h,mi,s,tz,Anim)`, `setCurrentDate(h,mi,s,tz,Anim)`, `setCurrentDateTime(Anim)`, `stop()` |
| `Clock` (18m) | `Clock(...)` | 시간 흐름/속도 제어 |
| `Ephemeris` (8m) | - | 천체력 계산 |

⚠️ `DateManager.TimeZone` = `DefaultTimeZone` + `UTC_[MP]_HH_MM_CITY` 형식 436개. `UTC`/`Local` 없음 → UTC+0 = `UTC_P_00_00_MON`, 로컬 = `DefaultTimeZone`.

## 4. 오버레이 / 그래픽 (카메라 자식으로 부착)

| 클래스 | 핵심 메서드 | 메모 |
|--------|-------------|------|
| `InsertText` (11m) | `setText(str)`, `setPosition(Vec3{az,h,roll})`, `setSize`, `setColor(Vec3)`, `setIntensity(f,Anim)` | `Camera.addChild(t.id, CameraPort.FixedForeground)` 로 화면 고정. enum `InsertText001..046` |
| `Insert2D`(19) `Insert3D`(26) `DrawableInsert`(14) | 이미지/3D/공통 인서트 | 좌표/크기/밝기 |
| `Place2D` (23m) | `setLatitude(f)`, `setLongitude(f)`, `setAltitude`, `setPosition(Vec3)`, `set*GridIntensity` | ⭐ 지상 관측지 이동은 여기서 (카메라 잠김 우회) |
| `Mark`(26) `Line`(13) `DomePointer`(8) | 마커/선/돔 포인터 | 연출용 |
| `Chart2D`(38) | 2D 차트/그래프 | - |
| `Lut`(14) `ParameterizationLut`(16) | 색상 LUT | - |
| `Light`(4) | 조명 | - |

## 5. 애니메이션 / 수학

| 클래스 | 요점 |
|--------|------|
| `Anim` (20m) | `Anim()`(즉시), static `Anim.cubic/exp/sin/expEvoIn(...)(duration)`. `Interpo` enum(Linear/Cubic/...) |
| `Animator` (0m/8p) | 예제 스크립트가 `Animator()` 로도 사용(호환) |
| `Vec`=**alias of Vec3** / `Vec2`/`Vec3`/`Vec4` | 벡터. `Vec2{azimuth,height}`, `Vec3{L,B,R}` 등 문맥별 의미 |
| `Mat`/`Mat4x4` | 행렬 |

## 6. 오디오 / 미디어

`Audio`(14), `AudioLayer`(10), `AudioLite`(6), `AudioPlayer`(2), `VideoPlayer`(10) — 재생/레이어/볼륨.

## 7. 시스템 / 관리 / 하드웨어

`SoftwareManager`(27), `ShowEngineManager`(7), `SlideShowHandler`(4), `RemoteShow`(6),
`FreeDomeManager`(3), `DMX512`(1, 조명제어), `Comment`(1).
studio: `DataManager`(5, DB), `Data`(1, Type enum), `Action`(1, Type enum),
`Configuration`(3), `ShowMonitor`(5), `AudienceResponseSystem`(7)/`VotingDevice`(투표), `QObject`(베이스).

---

## 8. ⭐ 실전 함정 & 검증된 패턴 (직접 겪은 것들)

| 주제 | 교훈 | 근거 노트 |
|------|------|-----------|
| **LBR R 단위** | 행성 프레임=**행성 반지름**, 태양/별=**AU**. HUD의 km/AU 값을 입력에 그대로 넣지 말 것 | ⑤ |
| **Vec vs Vec3** | `skyExplorer.Vec`는 `Vec3` 별칭 → `Vec(l,b,r)`=`Vec3(l,b,r)` | ② |
| **setTarget Vec2** | 정식은 `Vec2{az,height}`, `Vec3`는 DEPRECATED | ② |
| **정중앙 공식(행성)** | 우주 시점: `B=90, az=0, height=125, R=1.5` + 대상 port | ⑥ |
| **target height 비선형** | 값↑→천체 화면 위로, 90 부근 포화 → 중앙은 ~125 | ⑤ |
| **FadeTo = Place2D 바인딩** | FadeTo 후 카메라 부분세터(setPositionR 등) 무시됨 | ⑤ |
| **지상 Sky View 카메라 잠금** | `setTarget/setOrientationHPR/takeOffOn` 코드 무시. 지상 하늘 조정은 **Place2D.setLatitude/Longitude + DateManager 시간**(천정=돔중앙)으로만 | ⑧ |
| **stop() 이 setDateTime 취소** | `setDateTime(...,Anim(t))` 직후 `stop()` 하면 시간 전환이 취소됨 → 즉시 `Anim()` 적용 후 stop | ⑧ |
| **Constellation** | `setIntensity` 없음 → lines/label/art 개별 | ⑦ |
| **TimeZone enum** | `UTC`/`Local` 없음(436개 도시별) → `UTC_P_00_00_MON`/`DefaultTimeZone` | ⑦ |
| **InsertText** | 카메라 `FixedForeground` 자식으로 부착, 시선과 무관하게 화면 고정 | ⑦ |
| **PlanetName/InsertTextName 정수캐스팅** | `Name(index)` 는 enum 정수값 가정(0/1-base) 주의 | ③ |
| **표준 시퀀스** | `smoothReset(False)`→암전→설정→페이드인→`AdvancedCamera().setModeFreeFly()` | ①~④ |

---

## 9. 예제 스크립트 매핑 (py)

| 예제 | 사용 API 패턴 |
|------|--------------|
| `FreeFlySun.py` | Universe 암전 → Camera setTarget/setPositionLBR(Sun Ecliptic) → Planet 궤도 루프 → FadeIn → FreeFly |
| `FreeFlySaturn.py` | smoothReset → `DataManager...data(PlanetType,"Saturn").action(FadeTo)` → FreeFly (고수준) |
| `goto_object_agent.py` | 위 API들을 LLM tool 로 래핑 + Claude tool-use 루프 (검증판) |
