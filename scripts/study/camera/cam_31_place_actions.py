# -*- coding: utf-8 -*-
# [카메라 31] Place 계열 — GoToPlace / FadeToPlace 의 정체 규명 (지구 시점에서)
#
# 배경: `GoToPlace`·`FadeToPlace` 는 행성(PlanetType)·NGC(NgcType) 에선 둘 다 死였다.
#       → 가설: **'장소(Place)' 데이터 타입 소속**일 것. 이제 그걸 확인한다.
#
# 관련 Data.Type (실제 존재 확인됨):
#   PlaceType · CityType · GenericPlaceType · MountainType · VolcanoType · CraterType
#
# ① 각 타입 × 대표 이름으로 핸들을 잡고 '살아있는 액션'을 스캔(표)
# ② 살아있는 게 있으면 **지상(지구 시점)에서 실제로 실행** → 관측지가 그리로 이동하나 관찰
#    (성공하면 "북극에서 본 하늘" 같은 연출을 Place2D 순간이동 대신 부드럽게 할 수 있다)
from skyExplorer import *
from studio import *
from Initialization import *

TYPES = ["PlaceType", "CityType", "GenericPlaceType", "MountainType", "VolcanoType", "CraterType"]
NAMES = ["Seoul", "Paris", "New York", "Cheongju", "London", "Tokyo",
         "Mont blanc", "Everest", "Etna", "Tycho"]
ACTS  = ["GoToPlace", "FadeToPlace", "GoTo", "FadeTo", "StraightGoTo", "ConnectTo",
         "FadeToObservation", "FadeToParent", "LookAt", "On"]

cam = Camera(Camera.CameraName.MainCamera)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone
db  = DataManager.database()


def place_now():
    """현재 관측지(Place2D) 좌표 읽기 — 이동 여부 판별용"""
    try:
        p = Place2D(Place2D.Place2DName(0)).position
        return (round(p.x, 3), round(p.y, 3), round(p.z, 1))
    except Exception as e:
        return "읽기실패(%s)" % e


# ── 지상 밤하늘 (지구 시점) ───────────────────────────────────
SceneGraph().reset(1); sleep(1.5)
Universe(Universe.UniverseName.MainUniverse).setGlobalIntensity(1.0, Anim(0.0))
e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))   # 청주에서 시작
dm.stop(); sleep(0.3)
dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))
sleep(1.5)
print("출발 관측지(청주) =", place_now())

# ═══ ① 스캔: 어느 Place 타입/이름에 어떤 액션이 살아있나 ═══
print("\n===== ① Place 계열 액션 스캔 =====")
found = []
for tn in TYPES:
    dt = getattr(Data.Type, tn, None)
    if dt is None:
        print("  Data.Type.%s 없음" % tn); continue
    hit_any = False
    for nm in NAMES:
        try: h = db.data(dt, nm)
        except Exception: h = None
        if h is None: continue
        alive = []
        for a in ACTS:
            ae = getattr(Action.Type, a, None)
            if ae is None: continue
            try:
                if h.action(ae) is not None: alive.append(a)
            except Exception: pass
        if alive:
            hit_any = True
            print("  ★ %-18s / '%-12s' → %s" % (tn, nm, alive))
            for a in alive:
                if a in ("GoToPlace", "FadeToPlace", "GoTo", "FadeTo", "StraightGoTo"):
                    found.append((tn, nm, a))
        else:
            print("    %-18s / '%-12s' → 핸들O, 액션 없음" % (tn, nm))
    if not hit_any:
        print("  %-18s : 유효한 이름 없음" % tn)

if not found:
    print("\n>>> 이동 액션이 살아있는 Place 데이터를 못 찾음.")
    print("    → 위 표에서 '핸들O' 인 조합이 있었는지, 이름 후보를 더 알려주시면 재시도합니다.")
    raise SystemExit

# ═══ ② 실행: GoToPlace 우선, 없으면 FadeToPlace/GoTo ═══
print("\n===== ② 실제 실행 (지구 시점에서 관측지가 이동하나) =====")
pref = ["GoToPlace", "FadeToPlace", "GoTo", "FadeTo", "StraightGoTo"]
pick = None
for want in pref:
    for (tn, nm, a) in found:
        if a == want:
            pick = (tn, nm, a); break
    if pick: break
tn, nm, a = pick
print("채택: %s / '%s' → %s" % (tn, nm, a))
print("실행 전 관측지 =", place_now())

db.data(getattr(Data.Type, tn), nm).action(getattr(Action.Type, a)).trigger()

# 관측지·카메라 변화 추적 (25초)
for s in range(1, 26):
    sleep(1.0)
    if s % 3 == 0 or s <= 5:
        try:
            r = cam.positionLBR.z
        except Exception:
            r = "?"
        print("  +%2ds  관측지=%s   camR=%s" % (s, place_now(), r))

print("\n===== 보고 =====")
print("① 스캔 표에서 어느 타입/이름에 GoToPlace·FadeToPlace 가 살아있었나")
print("② 실행 후 **관측지 좌표가 실제로 바뀌었나** (청주 36.64/127.49 → 다른 값?)")
print("③ 화면이 그 장소의 하늘로 바뀌었나 (별 배치·지평선이 달라졌나)")
print("   → 되면 '세계 여러 도시에서 본 하늘' 연출을 부드럽게 만들 수 있음")
