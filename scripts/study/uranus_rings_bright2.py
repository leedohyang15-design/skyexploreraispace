# -*- coding: utf-8 -*-
"""
uranus_rings_bright2.py — 천왕성 고리 밝기: '행성 자체 intensity' 레버 (2026-07-15)
★ 실측 경과: 모델 4개=무효 / GlobalIntensity·Sun intensity 오버드라이브=행성 본체만 하얘지고 고리는 그대로.
  → 마지막 카드: 우리 노트 "고리는 본체(Planet) intensity 에 포함" → **천왕성 자체 setIntensity** 를 올리면
    고리가 같이 밝아지나? (씬 전체 Global 이 아니라 개체 본체 밝기 = 다른 레버.)
  1.0 → 2.0 → 3.5 → 5.0 A/B. 고리가 밝아지면 = 레버 발견(쇼에 적용). 안 밝아지면 = 진짜 한계 확정.
★ 근접(R=2.6)·볼드(B=40)·배경 검정 고정. Global 은 1.0 유지(행성 본체 intensity 만 만짐).
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


print("천왕성 고리: 행성 본체 intensity 레버 실측")
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
    cam.setPositionLBR(Vec(p.x, 40.0, 2.6), Anim.cubic(4.5), -1); sleep(4.8)
except Exception as e:
    print("   근접 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.0)); sleep(1.1)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)

# ── ★ 행성 본체 intensity A/B (Global 은 1.0 고정) ──────────
for pi in (1.0, 2.0, 3.5, 5.0):
    label("천왕성 본체 밝기 = %.1f" % pi)
    feat(uranus, "setIntensity", pi, Anim(1.2), label="(Uranus intensity=%.1f)" % pi)
    sleep(5.5)

feat(uranus, "setIntensity", 1.0, Anim(1.0)); sleep(1.0)
label("고리가 밝아진 구간이 있었나?")
sleep(3.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. 리포트: ①천왕성 본체 intensity 1.0→2.0→3.5→5.0 중 '고리'가 밝아진 구간 있나? "
      "(본체 원반만 밝아지고 고리는 그대로면 = 고리는 본체 intensity 와 별개, 밝기 레버 없음 최종확정) "
      "②밝아지면 몇에서 제일 보기 좋나(과하면 원반이 하얘짐)")
