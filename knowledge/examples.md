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

## 추가 패턴 (핵심 API 순서 — 요청한 천체/현상으로 치환해 조합. 전부 실측 검증)

**"지구·행성을 돔 중앙에 두 배 확대"** — 예제1과 동일: FadeTo → `setTargetHeight(30)` → 페이드인 →
`p = cam.positionLBR; cam.setPositionR(p.z*0.5, Anim.cubic(6), -1)` (0.5=2배). 절대값 금지, 읽은 R×배율.

**"○○ 유성우 보여줘"** (지상 밤): reset → 지상 밤 세팅(지구 `setIntensity(1)`+`setAtmosphereIntensity(0)`+
`setTerrainIntensity(0)`+`Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.6)`+Stars 1) → 청주 좌표·밤 시각(UTC) →
북동 조준(`setOrientationH(135)`/`setTargetHeight(22)`) → 복사점 별자리 선(`Constellation(Constellation.ConstellationName.Per).setLinesIntensity`) →
`ss = ShootingStar(ShootingStar.ShootingStarName.ShootingStar001)`;
`ss.setReferential(ShootingStar.Referential.RaDec)`; `ss.setRainGradientPoint(Vec2(적경,적위))`(페르세우스=Vec2(47,58));
`ss.setRepresentationType(ShootingStar.Model.Gradient)`; `ss.setZenithalHourlyRate(1200)` → 페이드인 → `ss.setRainSeed(1)`(0=정지).
⚠️ 내부저장 ZHR/60이라 800~1500으로 크게 넣어야 돔에서 보임.

**"달 위상 변화"**: reset → FadeTo `data(Data.Type.SatelliteType,"Moon")` → `moon = Satellite(Satellite.SatelliteName.Moon)`;
`setTargetHeight(30)`; `moon.setPlanetShineStrength(0.0, Anim(1))`(그믐면 칠흑) → 페이드인 →
`moon.setManualMoonPhase(True)`; `moon.setMoonAge(0.0, Anim(0))`; sleep(0.3); `moon.setMoonAge(29.5, Anim(15))`.
⚠️ 끝에 setManualMoonPhase(False)로 되돌리지 말 것(그림자 깜빡임).

**"○○ 행성과 위성들"** (가스행성 위성계): reset → FadeTo Jupiter/Saturn → 그림자 OFF(`setShadowStrength(0)`+
`setShadowContrast(0)`+`setPlanetShineStrength(1)`) → 풀백 `p=cam.positionLBR; cam.setPositionLBR(Vec(p.x,p.y,p.z*4),Anim.cubic(4),-1)` →
관성 프레임 `ip = jup.portId(Planet.PlanetPort.EquatorialJ2000); cam.setPositionLBR(Vec(현재L,B,R),Anim,ip)` →
각 위성 `Satellite(Satellite.SatelliteName.Io/Europa/Ganymede/Callisto)` .setIntensity/setOrbitIntensity/setLabelIntensity/setScale(7) →
페이드인 → 시간가속 `dm.setDateTime(+8일, Anim(14))` = 케플러 차등 공전(안쪽 빠름).

**"별자리(그림/선)"**: 검은 하늘(대기0+지면0) → `c = Constellation(Constellation.ConstellationName.Ori)`;
`c.setLinesIntensity(0.6, Anim(1.5))`; `c.setArtIntensity(0.85, Anim(2))`(신화 그림). 여러 별자리 반복 가능.
성군(별 잇는 큰 도형)은 프리셋: `ASTERISM_STr`(여름 대삼각형)/`ASTERISM_WHx`(겨울 육각형)/`ASTERISM_BDr`(북두칠성) →
`Constellation(Constellation.ConstellationName.ASTERISM_STr).setLinesIntensity(1, Anim)`.

**"은하수"**: 지상 밤(대기0+지면0) → `gal = Galaxy(Galaxy.GalaxyName.MilkyWay); gal.setIntensity(1)`;
`gal.setExposure(2)`; `stars.setExposure(7)`; `stars.setPointSaturation(3.5)` = 풍성한 은하수.

**"태양 표면/홍염"**: reset → FadeTo `data(Data.Type.StarType,"Sun")` → ⚠️ 이 프레임 R 단위 = AU!
`cam.setPositionR(0.03, Anim.cubic(5), -1)`(원반이 돔에 꽉 참) → `sun = IndividualStar(IndividualStar.IndividualStarName.Sun)`;
`sun.setModel(IndividualStar.Model.SDO)`(표면 영상 필수); `sun.setMagneticLinesIntensity(1, Anim)`(청록 코로나 루프)+
`sun.setCoronaIntensity(1, Anim)`. 304Å 필터 = 홍염.

**"화성/암석행성 표면 확대"**: FadeTo Mars → 그림자 OFF → `mars.setTerrainModel(Planet.TerrainModel.Topography)`(DEM 모델) →
근접 줌+오블리크 `p=cam.positionLBR; cam.setPositionLBR(Vec(p.x, 22, max(1.5, p.z*0.4)), Anim.cubic(6), -1)` →
`mars.setElevationScale(10)`(DEM+근접에서만 산·협곡이 솟음).

**"인공위성/ISS 궤도"** (지구 둘레): reset → FadeTo `data(Data.Type.PlanetType,"Earth")`(외부) →
풀백 `cam.setPositionLBR(Vec(L,35,12),Anim,-1)`+`setTargetHeight(30)` → `op = OrbitalPlace(OrbitalPlace.OrbitalPlaceName.OrbitalPlace001)`;
`op.setParent(Planet(Planet.PlanetName.Earth).portId(Planet.PlanetPort.EquatorialJ2000))`;
TLE 세터(각 val, Anim): `setMeanMotion`(revs/day)·`setEccentricity`·`setInclination`·`setAscendingNodeLongitude`·`setArgumentOfPeriapsis`·`setMeanAnomaly` + `setEpochYears`/`setEpochDays`;
표시 `setOrbitColor(Vec3)`/`setOrbitThickness`/`setOrbitIntensity`/`setIntensity` → 시간가속 `dm.setDateTime(+1일, Anim)`.
⚠️ ISS/허블은 MeanMotion≈15.5(저궤도)라 지구에 붙어 R=12 줌에선 묻힘 → 근접 줌 필요. GPS(MM 2)/정지궤도(MM 1)/몰니야(e=0.74 찌그러진 타원)가 잘 보임.

**"혜성"**: reset → FadeTo `data(Data.Type.CometType,"1P/Halley")`(황도 J2000 프레임=지구 자전 없음) →
`cam.setPositionR(cam.positionLBR.z*0.45, Anim.cubic(5), -1)`(혜성 확대) → 시간가속(근일점 전후 몇 달)으로 코마·꼬리 변화 관찰.
⚠️ 궤도선은 지상 시점 전용(FadeTo 후엔 안 보임).

**"소행성대"** (태양계 위에서 조망): `sun = IndividualStar(IndividualStar.IndividualStarName.Sun)`;
`sp = sun.portId(IndividualStar.IndividualStarPort.Ecliptic)`; `cam.setPositionLBR(Vec(0,90,6), Anim, sp)`(R=6AU=화성~목성)+`cam.setTargetHeight(30)`(필수, 안 잡으면 띠가 구석) →
`a = Asteroid(Asteroid.AsteroidName.Asteroid001)`; 궤도 6요소 `setSemiMajorAxis`(AU)/`setEccentricity`/`setInclination`/`setLongitudeOfAscendingNode`/`setArgumentOfPeriapsis`/`setMeanAnomaly`(각 val,Anim); sleep(0.3);
`setOrbitIntensity`/`setOrbitColor(Vec3)` → 시간가속 `dm.setDateTime(+6년, Anim)`.

**"빛공해/도시 밤하늘 vs 시골"**: ⚠️ `Earth.setLightPollutionIntensity`는 대기 스카이글로우만 건드림 —
별/은하수는 독립 레이어라 안 지워짐. '별이 사라지는' 효과 = `Stars`/`Galaxy` intensity 를 단계별로 직접 감광:
교외(lp 0.3 / stars 0.8 / mw 0.35) → 도시외곽(0.6/0.6/0.1) → 대도시(1.0/0.4/0.0). setLightPollutionIntensity 는 병행.

**"개기월식/블러드문"**: ⚠️ 달이 붉게 물드는 렌더는 **이 빌드에서 미검증**(SDK 확인 안 됨) — 억지로 만들지 말 것.
검증된 대안을 짧게 제시: **일식**(관측지+시각+`setOrientationH` 자동조준+시간가속+코로나 `setScale`) 또는 **달 위상**(setManualMoonPhase/setMoonAge).

**회전/공전(오빗)** — 검증된 스텝 오빗만: 성운 los 프레임에서 0.5초 스텝으로 L 증가 + 4스텝마다
`setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim, los)` 재조준(중앙 유지). 행성 FadeTo 프레임이면 track=-1 +
`setTargetHeight(29.9→30)` no-op 재조준. (⛔ 시간가속 자전·orientation 루프·AdvancedCamera.move/roll 은 실측 실패 — 금지.)

## ⚠️ 렌더 함정 / 한계 (실측 피드백 반영 — AI는 이걸 반드시 지킬 것)

**프레임 전환(관성 프레임/태양 top-down)엔 반드시 시선 정렬을 붙인다.**
`cam.setPositionLBR(..., Anim, port)` 로 새 포트(EquatorialJ2000, 태양 Ecliptic 등)로 옮긴 직후
**반드시 `cam.setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim, port)` 를 같이 호출**한다.
안 하면 시점이 뒤틀려 "시점이 이상함". 관성 프레임 전환은 **같은 L/B/R 유지**(카메라 위치 안 바뀜)
— B 를 억지로 바꾸면 대상이 화면 밖으로 튄다.

**태양계 top-down 조망**: 태양 Ecliptic 포트 + `Vec(0, 90, R)` + 위 시선 정렬 + **`setTargetHeight(30)`**.
✅ **(2026-07-23 사용자 확정) Target 30 이 정답** — 시선정렬(`setOrientationSmoothXYZR`)만 제대로 붙이면
30 으로 궤도가 화면 중앙에 잘 잡힌다. 예전 '시점 병신'은 Target값 문제가 아니라 시선정렬 누락이 원인이었음.
공전은 `setRevolutionSpeedScale(2.5)` 정도로 감속(60 은 과속) + `setDateTime(+1년, Anim(32))`.

**행성 '자전' 요청은 불안정 = 미해결 영역.** FadeTo 는 극점 상공 도킹이라
관성 프레임에서 시간가속해도 자전이 **'극점 팽이'로 보여 관람 부적합**. 깔끔한 적도-옆 자전은
스크립트로 안정적으로 안 됨(오퍼레이터 수동). → **자연어 '자전' 요청엔** 안정 클로즈업 +
그림자 OFF 로 표면을 보여주거나, 전환 슬루를 암전(GlobalIntensity 0)에 숨기고 한계를 알린다.
"멋진 자전 회전"을 확정처럼 만들지 말 것.

**딥스카이(성운/은하) 접근은 '깊게' 줌인해야 보인다.** ConnectTo 직후 R 은 수백 pc 라 성운이 점.
한 번(×0.5) 줌으론 안 됨 → **초기 R 을 한 번 읽고 절대타겟 여러 단계로 겹쳐 줌**
(`p0=cam.positionLBR.z` → `for f in (0.4,0.16,0.06,0.024,0.01): cam.setPositionR(p0*f, Anim.cubic(3), -1); sleep(2.4)`).
sleep<anim 로 겹쳐야 매끄럽고, 최종 R 이 돔을 채운다.

**유명 성운(말머리·게성운 등)은 DB ConnectTo 말고 `Nebula` 이름 enum + LOS 포트로.** (2026-07-23 확정)
`Data.Type` DB 의 ConnectTo/FadeTo 로는 렌더가 안 뜰 때가 있음(게성운=아무것도 안 보임).
검증된 경로 = `neb = Nebula(Nebula.NebulaName.CRAB)`(또는 HORSEHEAD 등) → `neb.setIntensity(1.0)` →
`los = neb.portId(Nebula.NebulaPort.LineOfSightLocal)` → `cam.setPositionLBR(Vec(0,0,400*PC), Anim, los)` +
시선정렬 → `cam.setPositionR(10*PC, Anim.cubic(16), los)` 비행 접근. **PC=3.086e13 을 스크립트에 직접 정의**
(전역 아님 — 안 하면 pc 가 km 로 새서 카메라가 아트 속에 박힘). NebulaName = HORSEHEAD/CRAB/EAGLE/CATEYE/DUMBBELL 등 44개.

**구름 '이동'(setCloudSpeed+시간가속)은 스크립트 창에서 안 보인다 = 한계.** (2026-07-23 사용자 확인)
`setCloudSpeed(4.0)` 는 **float 단일인자**(Anim 넣으면 C++ 시그니처 에러로 그 줄에서 블록이 끊김). 그러나
시간가속을 걸어도 구름이 눈에 띄게 흐르진 않음. → 구름 연출은 **`setCloudsIntensity(0→1)` 페이드인**(구름이
'생겨나는' 변화)까지가 한계. '구름이 밀려온다/흐른다'를 확정처럼 만들지 말 것. 입체감은 `setCloudModel(Volumetric)`.

## 🎯 카메라 Target 기준 (반드시 지킬 것)

**🎯🎯 [절대 기준] 모든 씬의 기본 카메라 Target = 30 (`cam.setTargetHeight(30.0, Anim)`).**
이게 관람 정위치다. 천체·자막·차트를 **돔 중앙/천정(Target 90, 또는 40/45/50)에 두지 말 것** — 관객이 목을 꺾어야 함.
지상 하늘(별자리·유성·은하수·행성 등)은 예외 없이 **Target 30**. 조준은 `setOrientationH` 로만 하고 높이는 항상 30.
예외는 프레임 의미가 다른 2가지뿐: ① 전천 그리드 구도 = Target 0, ② 성운 LOS 프레임(ConnectTo/Nebula LOS)은 그 프레임상 90이 돔 중앙, ③ 저지평선 현상(황도광·일식 등)은 실제 고도에 맞춰 낮게. **그 외에는 무조건 30.** ⚠️ **태양계 위에서 조망(sun.portId(Ecliptic))도 Target 30이 정답**(90 아님) — 단 프레임 진입 직후 `cam.setOrientationSmoothXYZR(Vec4(0,0,0,0), Anim, sp)`로 시선정렬해야 시점 안 깨짐(정렬 생략이 'AB 시점 병신'의 진짜 원인, Target값 문제 아님).
