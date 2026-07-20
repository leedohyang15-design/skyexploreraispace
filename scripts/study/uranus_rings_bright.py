# -*- coding: utf-8 -*-
"""
uranus_rings_bright.py — 천왕성 고리 '밝기' 레버 실측 (2026-07-15)
★ 실측: 고리 모델 4개(DefaultRing/BasicRing/Asteroids/Asteroids_3_0) = 화면 변화 없음(모델은 레버 아님).
  ring intensity 세터도 없음 → 남은 건 '전체 조명 오버드라이브'뿐. 아직 안 해본 두 가지를 A/B:
  ① GlobalIntensity 를 1 이상(1.0→1.6→2.2)으로 → 어두운 고리가 밝아지나(overexpose)?
  ② Sun intensity 를 1 이상(1.0→2.5→4.0)으로 → 햇빛 받는 고리가 밝아지나?
  둘 다 무효면 = 천왕성 고리는 '희미한 게 한계'(어두운 에셋, 밝기 세터 없음)로 최종 확정.
★ 근접(R=2.6)·볼드(B=40)·배경 검정 고정. 모델은 아무거나(효과 없음) — DefaultRing.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
uranus = Planet(Planet.PlanetName.Uranus)
sun = IndividualStar(IndividualStar.IndividualStarName.Sun)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대 ────────────────────────────────────────────────────
print("천왕성 고리 밝기 레버 실측")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
sun.setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))
dm.stop(); sleep(0.3)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 58, 0)); t1.setSize(0.045); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.7, 0.95, 1.0))


def label(text):
    t1.setText(text); t1.setIntensity(1.0, Anim(0.5))


# ── 근접 도킹 ───────────────────────────────────────────────
SceneGraph().reset(1); sleep(1.5)
h = DataManager.database().data(Data.Type.PlanetType, "Uranus")
act = h.action(Action.Type.FadeTo) if h is not None else None
if act is not None:
    act.trigger(); sleep(4.5); print("   FadeTo Uranus")
cam.setTargetHeight(30.0, Anim.cubic(2.0)); sleep(2.3)
feat(uranus, "setShadowStrength", 0.0, Anim(0.5))
feat(uranus, "setShadowContrast", 0.0, Anim(0.5))
feat(uranus, "setPlanetShineStrength", 1.0, Anim(0.5))
uranus.setIntensity(1.0, Anim(0.0))
if hasattr(Planet.RingModel, "DefaultRing"):
    feat(uranus, "setRingModel", Planet.RingModel.DefaultRing)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 40.0, 2.6), Anim.cubic(4.5), -1); sleep(4.8)
except Exception as e:
    print("   근접 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.0)); sleep(1.1)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

# ── ① GlobalIntensity 오버드라이브 ─────────────────────────
for gi in (1.0, 1.6, 2.2):
    label("전체 밝기(Global) = %.1f" % gi)
    feat(uni, "setGlobalIntensity", gi, Anim(1.2), label="(GI=%.1f)" % gi); sleep(5.5)

# 원복
feat(uni, "setGlobalIntensity", 1.0, Anim(1.0)); sleep(1.2)

# ── ② Sun intensity 오버드라이브 ───────────────────────────
for si in (1.0, 2.5, 4.0):
    label("태양 밝기(Sun) = %.1f" % si)
    feat(sun, "setIntensity", si, Anim(1.2), label="(Sun=%.1f)" % si); sleep(5.5)

# 원복
feat(sun, "setIntensity", 1.0, Anim(1.0)); sleep(1.0)

label("고리가 밝아진 구간이 있었나?")
sleep(3.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. 리포트: ①전체밝기 1.0→1.6→2.2 중 고리가 밝아진 구간 있나(아니면 그냥 다 하얘지나/변화없나) "
      "②태양밝기 1.0→2.5→4.0 중 고리가 밝아진 구간 있나 "
      "③둘 다 무효면 천왕성 고리는 '희미한 게 한계'로 확정 — 이 정도로 쇼에 쓸지 결정")
