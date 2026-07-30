# -*- coding: utf-8 -*-
# NGC 여행 v3 — ★정정: NGC 이동 액션은 '개체마다 다르다' (사용자 UI 스샷으로 확정)
#   · NGC2237(장미, 크고 흐린 발광성운) = 이동 액션 없음 → 내가 이놈만 보고 "NGC 死" 로 오판
#   · NGC2346/2392 등 (작고 밀집한 행성상성운) = UI 에 Go To / Fade To / Straight Go To / Connect To 다 있음
#
# ① 여러 NGC 개체를 스캔해 '이동 액션이 살아있는' 놈을 찾아 표로 보여준다
# ② 그중 하나로 실제 여행(GoTo 또는 FadeTo) + 도착 후 줌 을 실행한다
from skyExplorer import *
from studio import *
from Initialization import *

# UI 스샷에 보인 행성상성운 + 우리 enum 에 있는 후보들
CANDIDATES = ["NGC2346", "NGC2392", "NGC6543", "NGC7009", "NGC7293", "NGC6826",
              "NGC2440", "NGC2438", "NGC1535", "NGC3242", "NGC246", "NGC2237"]
NAV = ["GoTo", "FadeTo", "StraightGoTo", "ConnectTo"]

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager(); tz = DateManager.TimeZone.DefaultTimeZone


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


# ═══ ① 스캔: 어느 NGC 가 '여행 가능'한가 ═══
print("===== ① NGC 개체별 이동 액션 스캔 =====")
print("%-12s %-8s %s" % ("개체", "enum", "살아있는 이동 액션"))
travelable = []
db = DataManager.database()
for c in CANDIDATES:
    has_enum = hasattr(NGC.NGCName, c)
    num = c.replace("NGC", "")
    got = []
    h = None
    for nm in ["NGC %s" % num, c]:            # "NGC 2346" 형식이 유효했음(v1)
        try: cand = db.data(Data.Type.NgcType, nm)
        except Exception: cand = None
        if cand is not None:
            h = cand
            for an in NAV:
                try:
                    if h.action(getattr(Action.Type, an)) is not None: got.append(an)
                except Exception: pass
            break
    print("%-12s %-8s %s" % (c, "O" if has_enum else "-", got or "(없음)"))
    if got and has_enum:
        travelable.append((c, num, got[0]))

if not travelable:
    print("\n⚠️ 이동 액션 살아있는 개체를 못 찾음 — 이름 형식 문제일 수 있음. 스캔 표를 알려주세요.")
    raise SystemExit

print("\n>>> 여행 가능 개체: %s" % [t[0] for t in travelable])

# ═══ ② 실제 여행: 첫 번째 여행 가능 개체로 ═══
enum_name, num, action_name = travelable[0]
print("\n===== ② '%s' 여행 (%s) =====" % (enum_name, action_name))
ground()

obj = NGC(getattr(NGC.NGCName, enum_name))
obj.setIntensity(1.0, Anim(1.0))
try: obj.setLabelIntensity(1.0, Anim(1.0))
except Exception: pass
sleep(2.0)
print("지상서 성운 ON — 여행 시작 (실행전 R=%s)" % R())

h = db.data(Data.Type.NgcType, "NGC %s" % num)
h.action(getattr(Action.Type, action_name)).trigger()
for i in range(9):                            # 최대 27초(GoTo 비행 시간 커버)
    sleep(3.0); print("   +%2ds  R=%s" % ((i + 1) * 3, R()))

cam.setTargetHeight(30.0, Anim(1.5)); sleep(2.0)   # 도착 후 관람 정위치(GoTo는 필수)
print("도착 R=%s → 성운이 화면에 크게 보이나?" % R())

# 도착 후 줌인 (프레임 잡혔으니 setPositionR 먹을 것)
for f in [0.5, 0.5]:
    p = R()
    if p and p > 0:
        cam.setPositionR(p * f, Anim.cubic(3.5), -1); sleep(4.0)
        print("   줌인 ×%.1f → R=%s" % (f, R()))
print("\n>>> 성운이 커지며 다가왔나? 어느 R 에서 제일 보기 좋았나?")
print("    (①스캔 표 + ②접근 결과 알려주세요)")
