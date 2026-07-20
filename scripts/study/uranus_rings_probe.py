# -*- coding: utf-8 -*-
"""
uranus_rings_probe.py — 천왕성 고리 '진짜 되는지' 전용 프로브 (2026-07-15, 재도전)
★ 지난번 결론(렌더 안 됨)이 성급했을 수 있어 재검증. 두 가설을 각각 테스트:
  ① 모델 문제: DefaultRing 만 비었고 BasicRing/Asteroids/Asteroids_3_0 은 그려질 수 있음 → 4개 전부 A/B
  ② 각도 문제: 고리면이 시야에 옆날(edge-on)이라 안 보였을 수 있음 → 근접(R=4)에서 B 각도 스윕
★ 각 모델을 큰 라벨과 함께 6초씩 홀드 → 어느 모델에서 고리가 뜨는지 눈으로 판정.
  setRingModel 후 ringModel 읽기값도 출력(적용 확인).
"""

from skyExplorer import *
from studio import *
from Initialization import *

cam = Camera(Camera.CameraName.MainCamera)
uni = Universe(Universe.UniverseName.MainUniverse)
dm  = DateManager()
tz  = DateManager.TimeZone.DefaultTimeZone
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
print("천왕성 고리 프로브")
uni.setGlobalIntensity(0.0, Anim(0.0))
SceneGraph().reset(1); sleep(2.0)
uni.setGlobalIntensity(0.0, Anim(0.0))
for i in range(8):
    try: Planet(Planet.PlanetName(i)).setIntensity(1.0, Anim(0.0))
    except Exception: pass
IndividualStar(IndividualStar.IndividualStarName.Sun).setIntensity(1.0, Anim(0.0))
Stars(Stars.StarsName.StarrySky).setIntensity(0.3, Anim(0.0))
dm.stop(); sleep(0.3)

# ── 자막 ────────────────────────────────────────────────────
t1 = InsertText(InsertText.InsertTextName(1))
cam.addChild(t1.id, Camera.CameraPort.FixedForeground)
t1.setPosition(Vec(0, 58, 0)); t1.setSize(0.04); t1.setDistance(1.0, Anim(0.0))
t1.setColor(Vec(0.7, 0.95, 1.0))


def label(text):
    t1.setText(text); t1.setIntensity(1.0, Anim(0.6))


# ── 천왕성 근접 도킹 ────────────────────────────────────────
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
# 근접: R 5→3.5, 고리면 열려고 B 20→35 (고리 반지름 ~2 → R 3.5 면 화면 큼)
try:
    p = cam.positionLBR
    cam.setPositionLBR(Vec(p.x, 35.0, 3.5), Anim.cubic(4.0), -1); sleep(4.3)
except Exception as e:
    print("   근접 실패: %s" % e)
cam.setTargetHeight(30.0, Anim.cubic(1.0)); sleep(1.1)
uni.setGlobalIntensity(1.0, Anim.cubic(2.0)); sleep(2.2)
rlog("근접 후")

# ── ① 4개 모델 A/B (각 6초 홀드, 라벨로 표시) ──────────────
MODELS = ["DefaultRing", "BasicRing", "Asteroids", "Asteroids_3_0"]
for mname in MODELS:
    if hasattr(Planet.RingModel, mname):
        m = getattr(Planet.RingModel, mname)
        ok = feat(uranus, "setRingModel", m, label="(모델=%s)" % mname)
        label("고리모델: %s" % mname)
        sleep(0.3); rlog("모델 %s 적용" % mname)
        sleep(6.0)
    else:
        print("   ⚠️ RingModel.%s 없음" % mname)

# ── ② 각도 스윕: 고리가 옆날이라 안 보였는지 (BasicRing 로 B 10→60) ─
if hasattr(Planet.RingModel, "BasicRing"):
    feat(uranus, "setRingModel", Planet.RingModel.BasicRing, label="(스윕용 BasicRing)")
label("각도 스윕 — 고리면이 열리며 나타나나?")
sleep(1.0)
for B in (10, 20, 30, 40, 50, 60):
    try:
        p = cam.positionLBR
        cam.setPositionLBR(Vec(p.x, float(B), p.z), Anim.cubic(2.0), -1); sleep(2.2)
        cam.setTargetHeight(30.0, Anim(0.0))
        print("   [스윕] B=%d" % B)
    except Exception as e:
        print("   스윕 B=%d 실패: %s" % (B, e))
sleep(1.0)

# ── 정리 ────────────────────────────────────────────────────
label("판정: 어느 모델/각도서 고리가 보였나?")
sleep(3.0)
t1.setIntensity(0.0, Anim(1.0))
uni.setGlobalIntensity(0.0, Anim.cubic(3.0)); sleep(3.5)
print("종료. 리포트(고리 재도전): "
      "①4개 모델(DefaultRing/BasicRing/Asteroids/Asteroids_3_0) 중 '어느 하나라도' 고리가 보인 게 있나? "
      "②각도 스윕(B 10→60) 중 특정 각도에서 고리(선/원반)가 나타났나? (edge-on 가설 검증) "
      "③아무 것도 안 보이면: ringModel 읽기값은 바뀌었나(로그) — 값은 바뀌는데 화면만 안 뜨는지 "
      "④근접 R=3.5 에서 천왕성 원반 크기는 충분한가(더 당길지)")
