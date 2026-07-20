# -*- coding: utf-8 -*-
"""
uranus_rings_final.py — 천왕성 고리 최종 균형 (2026-07-15)
★ 발견: 천왕성 '본체' setIntensity 를 올리면 고리도 밝아짐(고리가 본체 밝기에 묶임). 단 ~2 이상은 원반이 하얘짐(백열전구).
  → 극단값(3.5/5) 빼고 1.0 / 1.5 / 2.0 만 비교해 '원반 색 유지 + 고리 또렷' 균형점 선택.
★ 근접 R=3.0 · 고리면 개방 B=38 · 배경 검정(Stars 0) 고정.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
uranus = Planet(Planet.PlanetName.Uranus)


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


print("천왕성 고리 최종 균형")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
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
if hasattr(Planet.RingModel, "DefaultRing"):
    feat(uranus, "setRingModel", Planet.RingModel.DefaultRing)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 38.0, 3.0), Anim.cubic(4.5), -1); sleep(4.8)
except Exception as e:
    print("   근접 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.0)); sleep(1.1)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

# ── 본체 intensity 1.0 / 1.5 / 2.0 A/B (원반 안 타는 선에서 고리 최적) ─
for pi in (1.0, 1.5, 2.0):
    label("천왕성 본체 밝기 = %.1f" % pi)
    feat(uranus, "setIntensity", pi, Anim(1.2), label="(intensity=%.1f)" % pi)
    sleep(7.0)

# 균형값(잠정 1.5)으로 마무리
feat(uranus, "setIntensity", 1.5, Anim(1.0))
label("천왕성 — 옆으로 누운 얼음 거인과 그 고리")
sleep(5.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. 리포트: ①1.0/1.5/2.0 중 '원반이 안 타면서 고리가 제일 또렷'한 값은? (그 값으로 최종 고정) "
      "②2.0 도 원반이 하얗게 타면 1.3 정도로 낮출까 ③이 정도면 천왕성 고리 마무리 OK?")
