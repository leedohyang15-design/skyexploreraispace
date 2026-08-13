# -*- coding: utf-8 -*-
"""
probe_rocket_hpr.py — 로켓을 하늘로 세우는 자세를 **한눈에** 가른다 (2026-08-13)

★ 왜 다시 하나
  `make_ariane5.py` 의 ③ 단계(A~E)는 **로켓 하나를 옆에서** 보여줬다. 그런데 돔은 어안이라
  직선이 휘어 보이고, 화면 각도로 '곧게 섰나'를 재는 게 신뢰가 안 됐다(D 와 E 가 비슷해 보였다).

★ 이번 방법 — **바퀴살(starburst)**
  같은 자세 공식을 **경도 8곳에 동시에** 걸고 **북극 위에서 내려다본다.**
  · 공식이 맞으면 → 로켓 8개가 지구에서 **사방으로 뻗은 바퀴살**이 된다. 한눈에 안다.
  · 틀리면 → 8개가 **전부 같은 쪽으로 비스듬히** 눕는다(바람개비처럼). 이것도 한눈에 안다.
  틀린 정도를 눈금으로 잴 필요가 없다. **모양이 갈린다.**

★ 후보 넷 (전부 pitch=90 — 모델 +Z 는 북극이라 일단 눕혀야 한다)
    ① H = L          ② H = -L         ③ H = L + 90      ④ H = L - 90
  (L = 그 로켓이 놓인 경도)

★ 봐야 할 것: **①~④ 중 어느 번호에서 바퀴살이 되는가.** 그 번호만 알려 주세요.
"""

from skyExplorer import *
from studio import *
from Initialization import *

import os

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone
earth = Planet(Planet.PlanetName.Earth)

LONS = [0.0, 45.0, 90.0, 135.0, 180.0, 225.0, 270.0, 315.0]
R_ROCKET = 2.3            # 지표 위. 지구 원반 밖으로 삐져나와야 방향이 보인다
ROCKET_SCALE = 1.8e5
SLOT0 = 20                # Insert3D 슬롯 20~27

USER = ""
try:
    USER = Configuration.configuration().localUserFolder
except Exception:
    pass


def feat(o, fn, *a):
    try:
        getattr(o, fn)(*a)
        return True
    except Exception as e:
        print("   ✗ %s: %s" % (fn, e))
        return False


def dark(total, step=0.2):
    t = 0.0
    while t < total:
        uni.setGlobalIntensity(0.0, Anim(0.0))
        sleep(step)
        t += step


print("=" * 66)
print("프로브: 로켓 자세 — 바퀴살로 가른다")
print("=" * 66)

uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1)
sleep(1.8)
dark(0.6)

# 앞 실행 잔여 정리 (reset 이 안 해 준다)
for i in range(0, 50):
    try:
        Insert3D(Insert3D.Insert3DName(i)).setIntensity(0.0, Anim(0.0))
    except Exception:
        pass
for i in range(0, 10):
    try:
        OrbitalPlace(OrbitalPlace.OrbitalPlaceName(i)).setOrbitIntensity(0.0, Anim(0.0))
    except Exception:
        pass

for i in range(8):
    try:
        Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
    except Exception:
        pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.35, Anim(0.0))

dm.stop()
sleep(0.2)
dm.setDateTime(2026, 8, 12, 3, 30, 0, tz, Anim(0.0))
sleep(0.4)

h = DataManager.database().data(Data.Type.PlanetType, "Earth")
a = h.action(Action.Type.FadeTo) if h is not None else None
if a is not None:
    a.trigger()
    dark(4.5)

feat(earth, "setIntensity", 1.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 1.0, Anim(0.0))
for fn, v in (("setShadowStrength", 0.0), ("setShadowContrast", 0.0),
              ("setPlanetShineStrength", 1.0)):
    feat(earth, fn, v, Anim(0.0))

ip = earth.portId(Planet.PlanetPort.EquatorialJ2000)
sp = None
for nm in ("EquatorialSynchronous", "EquatorialSync", "Synchronous"):
    try:
        sp = earth.portId(getattr(Planet.PlanetPort, nm))
        break
    except Exception:
        continue

# ── 로켓 8개를 경도에 고루 놓는다 ──────────────────────────────
print("-" * 66)
rockets = []
for k, lon in enumerate(LONS):
    ins = Insert3D(Insert3D.Insert3DName(SLOT0 + k))
    ins.setModelFilename(os.path.join(USER, "ariane5.osg") if USER else "ariane5.osg")
    t = 0.0
    while t < 12.0:
        sleep(0.4)
        t += 0.4
        if "Loaded" in str(ins.loadingStatus):
            break
    feat(ins, "setIntensity", 0.0, Anim(0.0))
    feat(ins, "setShadowStrength", 0.0, Anim(0.0))
    feat(ins, "setScale", ROCKET_SCALE, Anim(0.0))
    feat(ins, "setParent", sp if sp is not None else ip)
    feat(ins, "setPositionLBR", Vec(lon, 0.0, R_ROCKET), Anim(0.0))
    rockets.append((ins, lon))
    print("   로켓 %d  경도 %.0f  로드=%s" % (k + 1, lon, ins.loadingStatus))

# ── 카메라: 북극 위에서 내려다본다 (바퀴살이 한눈에) ────────────
dark(0.5)
cam.setPositionLBR(Vec(0.0, 88.0, 5.2), Anim(0.0), ip)
feat(cam, "setOrientationSmoothXYZR", Vec4(0.0, 0.0, 0.0, 0.0), Anim(0.0), ip)
dark(0.5)
cam.setTargetHeight(30.0, Anim(0.0))
dark(0.4)

txt = InsertText(InsertText.InsertTextName(5))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 58, 0))
txt.setColor(Vec(1.0, 1.0, 0.6))
txt.setDistance(20.0, Anim(0.0))
txt.setIntensity(1.0, Anim(0.0))

uni.setGlobalIntensity(1.0, Anim.cubic(2.0))
sleep(2.5)
for ins, lon in rockets:
    feat(ins, "setIntensity", 1.0, Anim(0.0))

# ── 후보 넷을 차례로 ───────────────────────────────────────────
CASES = [
    (lambda L: L, "1)  H = L"),
    (lambda L: -L, "2)  H = -L"),
    (lambda L: L + 90.0, "3)  H = L + 90"),
    (lambda L: L - 90.0, "4)  H = L - 90"),
]
for fn, label in CASES:
    for ins, lon in rockets:
        feat(ins, "setOrientationHPR", Vec(fn(lon), 90.0, 0.0), Anim(0.0))
    txt.setText(label + "   -   바퀴살인가, 바람개비인가?")
    print("   %s" % label)
    sleep(11.0)

# 참고 — 눕히지 않은 경우(전부 북극을 향해 서 있어야 한다)
for ins, lon in rockets:
    feat(ins, "setOrientationHPR", Vec(0.0, 0.0, 0.0), Anim(0.0))
txt.setText("참고)  HPR(0,0,0)  -  전부 북쪽(화면 밖)을 향한다")
sleep(8.0)

txt.setText("몇 번에서 바퀴살이 됐는지 알려 주세요")
sleep(6.0)
uni.setGlobalIntensity(0.0, Anim.cubic(2.0))
sleep(2.5)
print("=" * 66)
print("바퀴살이 된 번호를 알려 주시면 쇼의 ROCKET_HPR 에 그 공식을 넣습니다.")
print("  1) Vec(ROCKET_LON, 90, 0)      2) Vec(-ROCKET_LON, 90, 0)")
print("  3) Vec(ROCKET_LON + 90, 90, 0) 4) Vec(ROCKET_LON - 90, 90, 0)")
print("=" * 66)
