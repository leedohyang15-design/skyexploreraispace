# -*- coding: utf-8 -*-
"""
uranus_rings_vivid.py — 천왕성 고리 '선명하게' 튜닝 (2026-07-15)
★ 고리 렌더 확정(사용자 스샷). 이제 더 선명하게 = 레버 3개 (고리 밝기 직접 세터는 없음):
  ① 모델 선택: DefaultRing/BasicRing/Asteroids/Asteroids_3_0 중 제일 두껍고 밝은 것
  ② 근접: R 3.5→3.0 (고리가 화면에 더 큼)
  ③ 고리면 개방 각도 B: 너무 눕히면(edge-on) 얇은 선, 너무 세우면(face-on) 옅은 원 → 중간(B~38)이 볼드
★ 4개 모델을 근접·볼드 구도에서 8초씩 큰 라벨과 A/B → 제일 선명한 모델을 사용자가 지목 → 그걸로 고정.
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
uranus = Planet(Planet.PlanetName.Uranus)


def rlog(tag):
    try:
        p = cam.positionLBR
        print("   [%s] posLBR L=%.2f B=%.2f R=%.4g / ringModel=%s"
              % (tag, p.x, p.y, p.z, getattr(uranus, "ringModel", "?")))
    except Exception as e:
        print("   [%s] 실패: %s" % (tag, e))


def feat(obj, fn, *args, label=""):
    try:
        getattr(obj, fn)(*args); print("   ✓ %s%s %s" % (fn, tuple(str(a)[:16] for a in args), label)); return True
    except Exception as e:
        print("   ✗ %s 실패: %s" % (fn, e)); return False


# ── 무대 ────────────────────────────────────────────────────
print("천왕성 고리 선명도 튜닝")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.0, Anim(0.0))   # 배경 완전 검정 = 고리 대비 최대
dm.stop(); sleep(0.3)

t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 58, 0)); t1.setSize(0.045); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.7, 0.95, 1.0))


def label(text):
    t1.setText(text); t1.setIntensity(1.0, Anim(0.6))


# ── 근접 도킹 (R=3.0, B=38 볼드 각도) ──────────────────────
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
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 38.0, 3.0), Anim.cubic(4.5), -1); sleep(4.8)   # 근접 R=3.0 + 고리면 개방 B=38
except Exception as e:
    print("   근접 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.0)); sleep(1.1)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)
rlog("근접 후")

# ── 4개 모델 A/B (근접·볼드 구도에서 8초씩) ────────────────
MODELS = ["DefaultRing", "BasicRing", "Asteroids", "Asteroids_3_0"]
for mname in MODELS:
    if hasattr(Planet.RingModel, mname):
        feat(uranus, "setRingModel", getattr(Planet.RingModel, mname), label="(모델=%s)" % mname)
        label("고리모델: %s" % mname)
        sleep(0.3); rlog("모델 %s" % mname)
        sleep(8.0)
    else:
        print("   ⚠️ RingModel.%s 없음" % mname)

# ── 마지막: Asteroids_3_0 로 두고 살짝 더 근접 + 천천히 회전감(L 드리프트) ─
if hasattr(Planet.RingModel, "Asteroids_3_0"):
    feat(uranus, "setRingModel", Planet.RingModel.Asteroids_3_0, label="(마무리 모델)")
label("가장 선명한 모델은?  (근접 R=2.7)")
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 38.0, 2.7), Anim.cubic(4.0), -1); sleep(4.3)
    cam.setTargetHeight(30.0, Anim(0.0))
except Exception as e:
    print("   추가근접 실패: %s" % e)
sleep(4.0)

t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. 리포트: ①4개 모델 중 '가장 선명/두꺼운' 게 어느 것? (DefaultRing/BasicRing/Asteroids/Asteroids_3_0) "
      "②근접 R=3.0→2.7 로 더 선명해졌나(더 당길까) ③B=38 각도 괜찮나(더 눕히거나 세울까) "
      "④이 이상 밝게는 세터가 없어서 한계 — 이 정도면 쇼로 쓸만한가?")
