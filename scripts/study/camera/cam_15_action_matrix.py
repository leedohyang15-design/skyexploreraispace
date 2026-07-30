# -*- coding: utf-8 -*-
# [카메라 15] 액션 매트릭스 — "어느 데이터 타입에 어느 이동 액션이 있나" 한 방에 표로
#   ★ sleep 없음 = 몇 초면 끝남 (실행은 안 하고 '존재 여부'만 스캔)
#
# 배경(실측):
#   · 화성(PlanetType)  = GoTo/FadeTo/ConnectTo/StraightGoTo 있음, LookAt·ScaleUp 없음
#   · 장미(NgcType)     = LookAt·ScaleUp 있음, 이동 계열 전무
#   → 액션 세트는 '데이터 타입마다' 다르다. GoToPlace/FadeToPlace/FadeToObservation/
#     FadeToParent 는 이 둘 다에 없음 → 다른 타입 소속으로 추정. 그걸 이 표로 찾는다.
from skyExplorer import *
from studio import *
from Initialization import *

# 우리가 이름까지 아는 '확실히 핸들 나오는' 조합들
TARGETS = [
    ("PlanetType",          "Mars"),
    ("PlanetType",          "Earth"),
    ("SatelliteType",       "Moon"),
    ("StarType",            "Sun"),
    ("NebulaType",          "M42"),
    ("NebulaType",          "NGC 6543"),
    ("NgcType",             "NGC 2237"),
    ("MessierType",         "M42"),
    ("GlobularClusterType", "Omega Centauri"),
    ("DwarfPlanetType",     "Pluto"),
    ("CometType",           "1P/Halley"),
    ("MountainType",        "Mont blanc"),      # ← '장소' 데이터: GoToPlace 후보
    ("GalaxyType",          "Milky Way"),
    ("SpcType",             ""),                # 이름 없이도 핸들 나오나 확인
]

# 이동/조준/확대 계열 액션 전부
ACTS = ["GoTo", "FadeTo", "StraightGoTo", "ConnectTo",
        "GoToPlace", "FadeToPlace", "FadeToObservation", "FadeToParent", "FadeToDate",
        "LookAt", "ScaleUp", "ScaleDown", "PointerOn", "On"]

db = DataManager.database()
print("=== 액션 매트릭스 (O=살아있음, ·=死) ===\n")
hdr = "%-22s %-16s" % ("데이터타입", "이름")
for a in ACTS:
    hdr += "%-4s" % a[:3]
print(hdr)
print("-" * len(hdr))
print("(약어: GoT=GoTo FaT=FadeTo StG=StraightGoTo Con=ConnectTo GoP=GoToPlace")
print("       FaP=FadeToPlace FaO=FadeToObservation FaPa=FadeToParent FaD=FadeToDate")
print("       Loo=LookAt ScU=ScaleUp ScD=ScaleDown Poi=PointerOn On=On)\n")

found_place = []
for (tn, nm) in TARGETS:
    dt = getattr(Data.Type, tn, None)
    if dt is None:
        print("%-22s %-16s (Data.Type 에 없음)" % (tn, nm)); continue
    try: h = db.data(dt, nm)
    except Exception: h = None
    if h is None:
        print("%-22s %-16s (핸들 없음)" % (tn, nm)); continue
    row = "%-22s %-16s" % (tn, nm)
    for a in ACTS:
        ae = getattr(Action.Type, a, None)
        alive = False
        if ae is not None:
            try: alive = h.action(ae) is not None
            except Exception: alive = False
        row += "%-4s" % ("O" if alive else "·")
        if alive and a in ("GoToPlace", "FadeToPlace", "FadeToObservation", "FadeToParent"):
            found_place.append((tn, nm, a))
    print(row)

print("\n=== 미확인 4종(GoToPlace/FadeToPlace/FadeToObservation/FadeToParent) 발견 ===")
if found_place:
    for (tn, nm, a) in found_place:
        print("  ★ %s / '%s' 에 %s 있음!" % (tn, nm, a))
    print("  → 이 조합으로 실제 실행해볼 가치 있음")
else:
    print("  없음 → 이 4종은 우리가 쓰는 데이터 타입에 아예 없음 = 실사용 불가로 판정")

print("\n=== 참고: Data.Type 전체 목록 (다른 타입에 있을 수 있음) ===")
types = [t for t in dir(Data.Type) if not t.startswith("_") and t[0].isupper()]
print("%d개: %s" % (len(types), types))
