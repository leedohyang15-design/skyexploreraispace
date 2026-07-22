# -*- coding: utf-8 -*-
"""
c_misc_sweep.py — C 잔여 명령 스윕: Stars 모델셋 / 황도대 띠 / LookAt / 대기 halo (2026-07-22, C-②③④)
★ ② Stars.setModelset(GaiaDR2↔Hipparcos) = 별 카탈로그 교체 시 별밭 차이 판별.
★ ③ Planet(Earth).setEclipticBandIntensity = 하늘에 황도대 띠.
★ ④ Action.Type.LookAt = 천체 조준 액션(미검증) — 화성으로 조준되나.
★ ⑤ Planet(Earth).setAtmosphereHaloIntensity = 대낮 태양 주변 무리(halo) — 마지막에 낮으로 전환.
★ 지상 청주 밤 기반. 각 단계 narr + 로그.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm = DateManager()
tz = DateManager.TimeZone.DefaultTimeZone


def feat(obj, fn, *args, label=""):
    if not hasattr(obj, fn):
        print("   – %s 없음" % fn); return False
    try:
        getattr(obj, fn)(*args); print("   ✓ %s %s" % (fn, label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, str(e)[:100])); return False


def rd(obj, prop):
    try:
        return getattr(obj, prop)
    except Exception as e:
        return "err:%s" % str(e)[:30]


# ── 무대: 청주 밤 ───────────────────────────────────────────
print("무대: C 잔여 스윕 (모델셋/황도대띠/LookAt/halo)")
uni.setGlobalIntensity(0.0, Anim(0.0))
try:
    SceneGraph().reset(1); sleep(1.5)
except Exception as e:
    print("reset skip:", repr(e)[:50])
uni.setGlobalIntensity(0.0, Anim(0.0))
earth = Planet(Planet.PlanetName.Earth); earth.setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereIntensity", 0.0, Anim(0.0))
feat(earth, "setTerrainIntensity", 0.0, Anim(0.0))
stars = Stars(Stars.StarsName.StarrySky); stars.setIntensity(1.0, Anim(0.0))
Galaxy(Galaxy.GalaxyName.MilkyWay).setIntensity(0.3, Anim(0.0))
Place2D(Place2D.Place2DName(0)).setPosition(Vec(36.64, 127.49, 300.0))
dm.stop(); sleep(0.2)
dm.setDateTime(2026, 7, 22, 13, 0, 0, tz, Anim(0.0)); sleep(0.4)   # 청주 밤 22시
cam.setOrientationH(0.0, Anim(0.0)); cam.setTargetHeight(35.0, Anim(0.0))

txt = InsertText(InsertText.InsertTextName(1))
cam.addChild(txt.id, Camera.CameraPort.FixedForeground)
txt.setPosition(Vec(0, 14, 0)); txt.setSize(0.05); txt.setColor(Vec(1.0, 1.0, 0.55)); txt.setDistance(1.0, Anim(0.0))
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.1)


def narr(text, dur=3.0):
    txt.setText(text); txt.setIntensity(1.0, Anim(1.0)); sleep(dur)


# ── ② Stars.setModelset (GaiaDR2 ↔ Hipparcos) ───────────────
narr("② 별 카탈로그 — setModelset", 2.5)
print("   [Modelset] %s" % [m for m in dir(Stars.Modelset) if not m.startswith("__") and "Invalid" not in m and m[0].isupper()])
print("   현재 modelset=%s" % rd(stars, "modelset"))
if hasattr(Stars.Modelset, "Hipparcos"):
    feat(stars, "setModelset", Stars.Modelset.Hipparcos, label="(Hipparcos)")
    sleep(1.0); narr("★ Hipparcos — 별 수/배치 (홀드)", 4.5)
if hasattr(Stars.Modelset, "GaiaDR2"):
    feat(stars, "setModelset", Stars.Modelset.GaiaDR2, label="(GaiaDR2)")
    sleep(1.0); narr("★ GaiaDR2 로 바뀔 때 별밭 달라졌나?", 4.5)

# ── ③ 황도대 띠 setEclipticBandIntensity ────────────────────
narr("③ 황도대 띠 — setEclipticBandIntensity", 2.5)
feat(earth, "setEclipticBandIntensity", 1.0, Anim(1.5), label="(황도대 띠)")
feat(earth, "setEclipticGridIntensity", 0.6, Anim(1.0), label="(황도선 보조)")
sleep(1.5); narr("★ 하늘 가로지르는 황도대 띠 보이나?", 5.0)
feat(earth, "setEclipticBandIntensity", 0.0, Anim(1.0)); feat(earth, "setEclipticGridIntensity", 0.0, Anim(1.0)); sleep(1.2)

# ── ④ LookAt 액션 (화성 조준) ───────────────────────────────
narr("④ LookAt 액션 — 화성 조준 시도", 2.5)
mars = DataManager.database().data(Data.Type.PlanetType, "Mars")
if mars is not None:
    act = mars.action(Action.Type.LookAt) if hasattr(Action.Type, "LookAt") else None
    print("   Mars LookAt action = %s" % ("있음" if act is not None else "None(미지원)"))
    if act is not None:
        act.trigger(); print("   LookAt trigger")
        sleep(3.0); narr("★ 카메라가 화성 쪽으로 조준됐나?", 5.0)
    else:
        narr("LookAt 액션 None (미지원)", 3.0)
else:
    narr("Mars 데이터 없음", 2.5)

# ── ⑤ 대기 halo (낮으로 전환) ───────────────────────────────
narr("⑤ 대낮으로 전환 — 태양 주변 halo", 3.0)
feat(earth, "setAtmosphereIntensity", 1.0, Anim(1.0), label="(대기 ON=파란 낮)")
dm.setDateTime(2026, 7, 22, 3, 30, 0, tz, Anim(0.0)); sleep(0.5)   # 청주 정오 = 03:30 UTC
cam.setOrientationH(0.0, Anim(1.0)); cam.setTargetHeight(52.0, Anim(1.5)); sleep(1.8)
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
feat(earth, "setAtmosphereHaloIntensity", 1.0, Anim(1.5), label="(태양 주변 무리)")
sleep(1.8); narr("★ 태양 주변에 무리(halo) 링 보이나?", 5.0)

narr("C-②③④⑤ 스윕 끝", 3.0)
txt.setIntensity(0.0, Anim(1.5))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료(C 잔여). ★리포트(각각): "
      "②Hipparcos↔GaiaDR2 별밭이 눈에 띄게 달라졌나 "
      "③황도대 띠(하늘 가로지르는 밝은 띠) 보였나 "
      "④LookAt=화성으로 카메라 조준됐나(로그 'Mars LookAt action=' 값도) "
      "⑤대낮 태양 주변 halo(무리) 보였나. 로그 '[Modelset]' 멤버도 붙여줘.")
