# -*- coding: utf-8 -*-
# 딥스카이 '여행 가능 목록' 확정 — 카테고리가 능력을 결정한다 (사용자 UI 스샷으로 규칙 도출)
#
# ★ 규칙: 같은 NGC 번호라도 **어느 카테고리에 등록됐냐**가 능력을 정한다.
#   · NEBULA 카테고리(27개, Nebula 클래스/NebulaType) = ✅ Go To / Fade To 여행 가능
#       (Barnard33 말머리, M1 게, M42 오리온, NGC2346, NGC2392 에스키모, NGC6543 고양이눈, NGC7293 나선 …)
#   · NGC 카테고리(NgcType) = ON / ScaleUp / LookAt / Label / Tag 만 (여행 X)
#       (NGC2237 장미 등 — UI 우클릭 메뉴로 사용자 확인)
#
# ① Nebula 클래스 enum 전체를 덤프 + NebulaType DB 로 GoTo/FadeTo 가능 여부 표로
# ② 그중 하나로 실제 여행(GoTo) + 도착 후 줌
from skyExplorer import *
from studio import *
from Initialization import *

NAV = ["GoTo", "FadeTo", "StraightGoTo", "ConnectTo"]

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone
db  = DataManager.database()


def R():
    try: return round(cam.positionLBR.z, 5)
    except Exception: return None


def ground():
    try: SceneGraph().reset(1); sleep(1.6)
    except Exception: pass
    uni.setGlobalIntensity(1.0, Anim(0.0))
    e = Planet(Planet.PlanetName.Earth); e.setIntensity(1.0, Anim(0.0))
    e.setAtmosphereIntensity(0.0, Anim(0.0)); e.setTerrainIntensity(0.0, Anim(0.0))
    Stars(Stars.StarsName.StarrySky).setIntensity(1.0, Anim(0.0))
    Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 200.0))
    dm.stop(); sleep(0.3)
    dm.setDateTime(2026, 1, 15, 12, 0, 0, tz, Anim(0.0)); sleep(0.4)
    cam.setOrientationH(30.0, Anim(0.0)); cam.setTargetHeight(30.0, Anim(0.0))
    sleep(0.6)


# ═══ ① Nebula enum 덤프 + 여행 가능 여부 표 ═══
print("===== ① Nebula 클래스 enum 전체 =====")
enums = [n for n in dir(Nebula.NebulaName) if not n.startswith("_") and n[0].isupper()]
print("멤버 %d개: %s" % (len(enums), enums))

# UI 'NEBULA' 패널에 보인 이름들(DB 조회용 후보). 여러 표기를 시도한다.
UI_NAMES = ["Barnard 33", "M1", "NGC 1952", "M16", "NGC 6611", "HH 47", "M42", "NGC 1976",
            "A39", "M27", "NGC 6853", "M2-9", "M76", "NGC 650", "M97", "NGC 3587", "Mz 3",
            "NGC 2346", "NGC 2392", "NGC 3132", "NGC 3242", "NGC 3918", "NGC 6302",
            "NGC 6537", "NGC 6543", "NGC 6751", "NGC 6826", "NGC 7009", "NGC 7027",
            "NGC 7293", "NGC 2237"]     # 마지막은 대조군(장미=NGC 카테고리, 여행 X 예상)

print("\n===== NebulaType DB 여행 가능 스캔 =====")
print("%-14s %s" % ("이름", "살아있는 이동 액션"))
travelable = []
for nm in UI_NAMES:
    got = []
    h = None
    try: h = db.data(Data.Type.NebulaType, nm)
    except Exception: h = None
    if h is None:
        print("%-14s (NebulaType 핸들 없음)" % nm); continue
    for an in NAV:
        try:
            if h.action(getattr(Action.Type, an)) is not None: got.append(an)
        except Exception: pass
    print("%-14s %s" % (nm, got or "(이동 액션 없음)"))
    if got:
        travelable.append((nm, got[0]))

print("\n>>> 여행 가능: %d개 — %s" % (len(travelable), [t[0] for t in travelable]))
if not travelable:
    print("⚠️ 하나도 없음 — 이름 표기 문제일 수 있음. 위 표를 알려주세요.")
    raise SystemExit

# ═══ ② 실제 여행: 고양이눈(NGC 6543) 우선, 없으면 첫 번째 ═══
pick = None
for want in ["NGC 6543", "NGC 2346", "NGC 7293", "M27"]:
    for (nm, an) in travelable:
        if nm == want: pick = (nm, an); break
    if pick: break
if pick is None: pick = travelable[0]
nm, an = pick

print("\n===== ② '%s' 여행 (%s) =====" % (nm, an))
ground()
h = db.data(Data.Type.NebulaType, nm)
print("여행 시작 (실행전 R=%s)" % R())
h.action(getattr(Action.Type, an)).trigger()
for i in range(9):
    sleep(3.0); print("   +%2ds  R=%s" % ((i + 1) * 3, R()))
cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)
print("도착 R=%s" % R())

# 도착 후 줌 (프레임 잡혔으니 setPositionR 먹음). 배율 클수록 확대 = R/zoom
for zoom in [2.0, 2.0]:
    p = R()
    if p and p > 0:
        cam.setPositionR(p / zoom, Anim.cubic(3.5), -1); sleep(4.0)
        print("   줌인 /%.0f → R=%s" % (zoom, R()))

print("\n===== 보고 =====")
print("① 여행 가능 목록(위 표) — 장미(NGC 2237)는 '없음'으로 나왔나?")
print("② '%s' 로 실제 다가갔나 (커지며 접근)" % nm)
